# Journal de traitement — base contacts Altav

Ce document trace le nettoyage de l'export Wix, les décisions prises et leurs
raisons. Objectif : qu'on puisse reprendre ce travail dans six mois, ou qu'un
tiers comprenne pourquoi le fichier a cette forme.

Les adresses email citées en exemple sont anonymisées.

---

## Point de départ

Export Wix `CRM Contact.csv` : **8 915 lignes, 51 colonnes**, séparateur `;`,
UTF-8 avec BOM. **167 libellés distincts** dans la colonne `Libellés`, créés au
fil des années par plusieurs personnes sans convention commune — un mélange de
noms de fichiers d'import (`senegalDRH.csv`, `fromlinkedin4.csv`), d'intitulés
de sessions (`Session d'information — 11 septembre 2024`) et de formulaires.

Constat structurant : **aucun contact ne porte plus d'un libellé**. Les règles
de priorité entre libellés ne se déclenchent donc jamais — un libellé = un tag.

---

## Le pipeline

Quatre scripts, exécutés dans cet ordre, repartant toujours de la source :

```bash
python3 tag_contacts.py          # segmentation + dédoublonnage
python3 appliquer_suppressions.py # emails morts
python3 purger_internes.py        # collaborateurs Altav
python3 deduire_noms.py           # noms déduits par règle
python3 deduire_noms_claude.py    # noms déduits par modèle (payant)
```

`CRM Contact.csv` n'est jamais modifié. Chaque script écrit une sauvegarde
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

La liste `contacts a supprimer.csv` (976 adresses) est un export Wix de bounces
et désabonnés. La règle métier n'est pas « supprimer la personne » mais
« ne plus lui écrire ».

- `FROID` / `INBOUND` → **ligne supprimée** (889). Email mort + aucune relation
  = aucune valeur.
- `CLIENT` / `CHAUD` → **ligne conservée**, `Email_actif = NON` (85). La relation
  vaut plus que l'adresse ; 44 d'entre eux ont un téléphone.

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
Transformée en `purger_internes.py`.

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
« améliorer » `deduire_noms.py` en ajoutant ce découpage.*

---

## Résultat

**7 483 contacts**, 54 colonnes.

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
- ~~Relire `deductions_claude_a_verifier.csv` (1 162 lignes) par échantillon.~~
  Relu et validé par Nael le 2026-07-20. Les 1 162 noms déduits sont confirmés
  dans `contacts_wix_tagges.csv` (`Origine_nom = DEDUIT_CLAUDE`).
- 28 groupes de fusion à clé courte : risque d'homonymes non vérifié.

**Prochain gain, sans dépendance :** séquence de nurturing sur les 489 contacts
`INBOUND` + `CHAUD` — mail de confirmation réécrit, livre blanc J+5, relance
J+30, rappel sous 5 min après inscription.

---

## Données

Aucun CSV n'est versionné (`.gitignore`). Le dépôt ne contient que les scripts
et la documentation. La base fait ~7 500 personnes physiques : noms, emails,
téléphones. Un `git add` forcé publierait des données personnelles que
l'historique git conserverait ensuite définitivement.
