# 5. Journal de traitement — base contacts Altav

Ce document trace le nettoyage de l'export Wix, les décisions prises et leurs
raisons. Objectif : qu'on puisse reprendre ce travail dans six mois, ou qu'un
tiers comprenne pourquoi le fichier a cette forme.

Les adresses email citées en exemple sont anonymisées.

---

## Point de départ

Export Wix `donnees/source/CRM Contact.csv` : **8 915 lignes, 51 colonnes**, séparateur `;`,
UTF-8 avec BOM. **167 libellés distincts** dans la colonne `Libellés`, créés au
fil des années par plusieurs personnes sans convention commune — un mélange de
noms de fichiers d'import (`senegalDRH.csv`, `fromlinkedin4.csv`), d'intitulés
de sessions (`Session d'information — 11 septembre 2024`) et de formulaires.

Constat structurant : **aucun contact ne porte plus d'un libellé**. Les règles
de priorité entre libellés ne se déclenchent donc jamais — un libellé = un tag.

**Colonnes retirées à la main.** `E-mail 4`, `E-mail 5`, `E-mail 6`,
`Adresse 4 - Rue`, `Adresse 4 - Ville` ont été supprimées avant de lancer le
pipeline, hors script — chacune n'était remplie que pour 1 contact sur 8 915.
Aucun script ne fait ce nettoyage : relancer le pipeline depuis
`donnees/source/CRM Contact.csv` les fait réapparaître. Suppression correcte sur le fond,
juste non automatisée.

---

## Le pipeline

Quatre scripts, exécutés dans cet ordre, repartant toujours de la source :

```bash
python3 scripts/01_tag_contacts.py           # segmentation + dédoublonnage
python3 scripts/02_appliquer_suppressions.py # emails morts
python3 scripts/03_purger_internes.py        # collaborateurs Altav
python3 scripts/04_deduire_noms.py           # noms déduits par règle
python3 scripts/05_deduire_noms_claude.py    # noms déduits par modèle (payant)
```

`donnees/source/CRM Contact.csv` n'est jamais modifié. Chaque script écrit une sauvegarde
`.bak` avant modification et accepte `--dry-run` (sauf le premier).

---

## Décisions et justifications

### 1. Segmentation sur une seule dimension

`Tag_CRM` répond à une question unique : **où en est la relation commerciale ?**
Quatre valeurs, mutuellement exclusives : `CLIENT`, `CHAUD`, `INBOUND`, `FROID`.

Ordre de priorité en cas de conflit : `ARCHIVE > CLIENT > FROID > CHAUD > INBOUND`.
Non utilisé en pratique (aucun contact multi-libellé), conservé pour les imports
futurs.

### 2. Exception à la règle « CSV → FROID »

La règle initiale disait : tout libellé contenant « CSV » est un import scrapé,
donc `FROID`. Problème : presque tous les libellés sont des **noms de fichiers**
finissant en `.csv`, y compris ceux d'inscrits volontaires.

`Session d'infos Ubuntu en ligne.csv` (103 contacts) et
`parcours-découverte-octobre.csv` (70 contacts) sont des gens venus à nous —
les classer en outbound froid était un contresens.

**Décision :** la règle CSV s'applique sauf si le libellé contient un signal
d'inscription (session d'info, parcours découverte). **195 leads récupérés.**

### 3. Dédoublonnage : nom si présent, sinon email

64 % des lignes n'avaient aucun nom. Une clé strictement nominale n'aurait
dédoublonné que 36 % du fichier. Clé retenue : nom complet normalisé si
disponible, sinon email principal.

**531 fusions.** Aucune donnée perdue : cellule vide d'un côté remplie de
l'autre, emails secondaires rangés dans les colonnes `E-mail 2..6` existantes
plutôt que dans une nouvelle colonne — pour rester importable dans Wix.

*Limite connue :* 28 groupes de fusion ont une clé nom très courte
(`eric`, `johndoe`), donc un risque d'homonymes fusionnés à tort. Non traité.

### 4. Emails morts : supprimer ou marquer, selon la valeur du contact

La liste `donnees/source/contacts a supprimer.csv` (976 adresses) est un export Wix de bounces
et désabonnés. La règle métier n'est pas « supprimer la personne » mais
« ne plus lui écrire ».

- `FROID` / `INBOUND` → **ligne supprimée** (889). Email mort + aucune relation
  = aucune valeur.
- `CLIENT` / `CHAUD` → **ligne conservée**, `Email_actif = NON` (85). La relation
  vaut plus que l'adresse ; 44 d'entre eux ont un téléphone.

Le fichier final n'en compte que **84** : l'un des 85 était un collaborateur Altav, retiré à
l'étape suivante. Les deux chiffres sont justes, à deux moments différents du pipeline.

> **Incident notable.** Un premier fichier nommé `contacts à supprimer.csv`
> (1,5 Mo, 8 924 lignes) s'est révélé être un export complet de la base, pas une
> sélection. L'appliquer aurait supprimé 8 354 contacts sur 8 384, dont 733
> CLIENT. Détecté avant toute écriture en comparant la taille et la distribution
> des libellés à celles du fichier source. **Toujours vérifier qu'une liste de
> suppression ressemble à une sélection, pas à une copie de la base.**

### 5. Contacts internes retirés

12 adresses Altav sorties de la base prospects. Le filtre balaie **toutes** les
colonnes email : plusieurs collaborateurs ont un email personnel en `E-mail 1`
et leur adresse professionnelle en `E-mail 2`, récupérée lors du dédoublonnage.

Cette étape a d'abord été faite en commande directe, hors script — ce qui
cassait la reproductibilité du pipeline (relancer aurait fait revenir les 12).
Transformée en `scripts/03_purger_internes.py`.

### 6. Déduction des noms — règle déterministe

70 % des contacts n'ont qu'un email. Pour les adresses de forme `prenom.nom@`,
le nom est extractible. Le dictionnaire de prénoms est **construit depuis le
fichier lui-même** (les lignes déjà nommées, ~1 600 prénoms), donc calibré sur
la base réelle : prénoms burundais, ivoiriens, sénégalais inclus, sans
dépendance externe.

Règle : exactement 2 tokens séparés, dont **exactement un** est un prénom connu.
Ce token devient le prénom, l'autre le nom — ce qui résout l'ordre inversé
(`nom.prenom@`) sans heuristique de position. Ambigu ou inconnu → ignoré.

**232 déductions**, dont 43 en ordre inversé.

Trois défauts corrigés après revue d'un échantillon de 10 :

| Symptôme | Cause | Correctif |
|---|---|---|
| Sigle pris pour un patronyme | `bgrh`, `dft` passent le filtre | Nom exigé ≥ 4 lettres avec voyelle, sinon prénom seul |
| Inversion erronée | Un prénom vu 1 seule fois suffisait | Inversion exige ≥ 2 occurrences |
| Raison sociale en nom | `haroinvest`, `assistanceetservices` | Liste de fragments commerciaux |

> Un seuil global de 2 occurrences avait été testé : il faisait perdre
> **67 déductions correctes** et en cassait de nouvelles. Le seuil ne doit
> s'appliquer qu'à l'inversion, pas à l'ordre direct. Documenté dans le script.

### 7. Déduction des noms — modèle

Les cas que la règle refuse par construction : blocs collés sans séparateur, et
adresses à séparateur dont aucun token n'est au dictionnaire.

Traités par Claude (Opus 4.8), consigne stricte : remplir uniquement si certain,
chaîne vide au moindre doute. **1 162 enrichis sur 5 009 candidats (23 %)**,
3 847 laissés vides — sociétés, sigles, pseudos, coupures ambiguës.
Coût réel : **4,76 USD**.

Le modèle réussit précisément là où la regex échouait :

| Local-part | Découpage naïf | Résultat correct |
|---|---|---|
| `paulemilekeita` | Paule Milekeita ❌ | **Paul Émile Keita** |
| `issakaabdoulaye` | Issa Kaabdoulaye ❌ | **Issaka Abdoulaye** |

**Hors périmètre assumé :** le découpage algorithmique des blocs collés. Sans
séparateur, plusieurs coupures sont valides et rien ne permet de trancher. Un
faux prénom dans une séquence coûte plus cher qu'une case vide. *Ne pas
« améliorer » `scripts/04_deduire_noms.py` en ajoutant ce découpage.*

---

## Résultat

**7 483 contacts**, 49 colonnes.

Le pipeline en produit 54 (51 d'origine + `Tag_CRM` + `Email_actif` + `Origine_nom`). Les 5
colonnes quasi vides listées plus haut ont été retirées à la main **après** son exécution :
54 − 5 = 49.

| Tag_CRM | Contacts |
|---|---|
| FROID | 6 241 |
| CLIENT | 753 |
| CHAUD | 318 |
| INBOUND | 171 |

| Colonne ajoutée | Rôle |
|---|---|
| `Tag_CRM` | Stade dans le cycle commercial |
| `Email_actif` | `OUI` / `NON` — mappable sur un champ opt-out CRM |
| `Origine_nom` | `WIX` (2 211) · `DEDUIT_CLAUDE` (1 162) · `DEDUIT_EMAIL` (232) · vide (3 878) |

**Contacts nommés : 3 605 / 7 483 (48 %)**, contre 33 % au départ.

La colonne `Libellés` d'origine est intacte.

---

## Méthode de travail

Sur toute transformation de masse : **tester sur ~10 lignes, lister les
changements, valider, puis appliquer**. Cette règle a directement évité de
propager 3 défauts sur 232 contacts, et a détecté le faux fichier de
suppression avant qu'il ne détruise la base.

Chaque script a un `--dry-run` pour ça.

---

## Reste à faire

**Bloquant, côté Altav :**
1. **Qui porte le CRM en interne ?** Condition de tout le reste — un CRM que
   personne ne tient redevient un Excel.
2. Accès back-office Wix + fichier Excel des pré-inscrits.
3. Fichier des certifiés de Stéphane → basculer les « Certification Promo 4 & 5 »
   payants de `CHAUD` vers `CLIENT`.

**Technique, optionnel :**
- 3 878 contacts toujours sans nom. Enrichissement externe payant possible
  (Dropcontact, Societeinfo) — coût par contact, décision à part.
- ~~Relire `donnees/revue/deductions_claude_a_verifier.csv` (1 162 lignes) par échantillon.~~
  Relu et validé par Nael le 2026-07-20. Les 1 162 noms déduits sont confirmés
  dans `donnees/travail/contacts_wix_tagges.csv` (`Origine_nom = DEDUIT_CLAUDE`).
- 28 groupes de fusion à clé courte : risque d'homonymes non vérifié.

**Prochain gain, sans dépendance :** séquence de nurturing sur les 489 contacts
`INBOUND` + `CHAUD` — mail de confirmation réécrit, livre blanc J+5, relance
J+30, rappel sous 5 min après inscription.

---

## 8. Requalification des pré-inscrits — 5 août 2026

Le pipeline de juillet déduit `Tag_CRM` du champ `Libellés` de l'export Wix. Or le
formulaire de pré-inscription réel — un ancien formulaire Wix, dont les réponses vivent
dans une collection CMS et non dans l'appli Formulaires — **n'écrit aucun libellé**. Ses
répondants tombaient donc dans la règle 1 : *libellé vide → FROID*.

Conséquence : des gens ayant explicitement demandé à entrer en formation étaient rangés
avec les imports scrapés.

### Source

Collection CMS `Pré-inscription Formation Ubuntu`, exportée le 5 août :
**525 soumissions, 437 adresses distinctes** (71 personnes se sont pré-inscrites
plusieurs fois, jusqu'à 6 fois). Champs : date et heure, prénom, nom, e-mail, téléphone,
comment ils ont connu Altav, ce qui les intéresse, motivation, **société, poste occupé,
secteur d'activité, niveau d'étude, âge, années d'expérience**.

Ce fichier remplace l'« Excel des pré-inscrits » réclamé depuis le début de la mission :
la donnée était dans Wix, dans le CMS.

### Rapprochement

| | |
|---|---|
| Adresses distinctes | 437 |
| Déjà dans la base | 430 |
| Absentes | 7 *(dont 2 internes Altav, retirés par le pipeline)* |
| Contacts de la base reconnus | 424 |
| dont déjà `CLIENT` | 339 — **intacts** |
| **Requalifiés `FROID`/`INBOUND` → `CHAUD`** | **68** |

Par année de dernière pré-inscription : 14 en 2023, 17 en 2024, 28 en 2025, 9 en 2026.

### Décision : aucun seuil d'ancienneté

Un pré-inscrit de 2023 jamais converti passe `CHAUD` comme les autres. Dans le cycle de vie
défini par Franck, on quitte l'étape *Pré-inscrit* par le **règlement des frais**, pas par le
temps écoulé — et la séquence prévue fait basculer les non-convertis sur la promo suivante.
Les exclure aurait reproduit la fuite que la mission répare : les 110 non-relancés de la
promo 8.

La colonne `date_preinscription` est écrite pour les 424, y compris les clients : la relance
trie par ancienneté, l'ancienneté justifie un message différent, pas une exclusion.

`scripts/11_requalifier_preinscrits.py` — `--dry-run`, `--echantillon N`, idempotent, ne
touche jamais aux `CLIENT`.

**Résultat : CHAUD 318 → 386 (+21 %)**, FROID 6 241 → 6 196, INBOUND 171 → 148.
7 483 contacts avant et après.

### Répercussion dans HubSpot

Propriété **`Date de pré-inscription`** (type Calendrier) créée. Import en deux fois :
10 lignes en test, puis 409.

| | Test | Reste | Total |
|---|---|---|---|
| Lignes | 10 | 409 | 419 |
| **Contacts créés** | 0 | 0 | **0** |
| Mises à jour | 10 | 407 | **417** |
| Erreurs | 0 | 2 | 2 |

> **Ce que l'échantillon a évité.** HubSpot mappait `E-mail 1` sur la propriété `E-mail 3`
> et n'avait sélectionné **aucun identifiant unique**. Tel quel, les 419 lignes auraient créé
> **419 doublons**. Le piège se represente à chaque import : il a fallu recorriger le mapping
> pour le second fichier.

Les 2 lignes en erreur (`evodie_p@yahoo.com`, `magzum@yahoo.fr`) portent le motif *ID
alternatif en double* : l'adresse vit sur deux fiches HubSpot. Doublon préexistant, tag déjà
correct (`CLIENT`), seule la date manque.

**Noms des propriétés HubSpot**, qui ne sont pas ceux du CSV :

| Colonne CSV | Propriété HubSpot | Remplissage |
|---|---|---|
| `Tag_CRM` | Température CRM | 99,97 % |
| `type_compte` | Type de compte | 99,97 % |
| `Email_actif` | Email actif | 99,97 % |
| `date_preinscription` | Date de pré-inscription | 5,58 % |
| `Libellés` | Wix — Libellés d'origine | **0 %** — créée, jamais remplie |
| `Origine_nom` | *n'existe pas* | — |

`Wix — Libellés d'origine` vide est un manque réel : c'est le champ qui justifie chaque
`Température CRM`. Sans lui, impossible de vérifier dans HubSpot pourquoi un contact est
`FROID`.

### Reste ouvert

- **Le signal B2B.** Société renseignée sur 524/525, poste sur 525/525, secteur sur 518/525.
  En juillet, le 80/20 B2B/B2C était déclaré non pilotable faute de données. Pour ces 437
  personnes, elles existent. À exploiter **sans** casser la règle : société renseignée ≠ lead
  entreprise, c'est le poste et qui paie qui tranchent.
- 5 pré-inscrits absents de la base, dont une du 1er août, à créer.
- `lionelngoyagoye@gmai.com` — faute de frappe du contact (`gmai.com`). HubSpot propose de
  supprimer l'adresse ; refusé, ce serait effacer le seul point de contact d'un client.

---

## Données

Aucun CSV n'est versionné (`.gitignore`). Le dépôt ne contient que les scripts
et la documentation. La base fait ~7 500 personnes physiques : noms, emails,
téléphones. Un `git add` forcé publierait des données personnelles que
l'historique git conserverait ensuite définitivement.
