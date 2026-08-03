# Altav — Mission Consulting

Automatisation du tunnel de conversion (CRM + séquences). Objectif : lever le goulot de conversion, pas la demande.

---

## Constat

- **Produit phare** (formation Ubuntu) = **70–80 % du CA**. Demande présente, objectif 2027 clair : **2 → 4 promos/an**.
- Le problème n'est pas la demande, c'est **la conversion**. Trois fuites :
  - **Leads chauds perdus** : promo 8 = 136 pré-inscrits → 26 confirmés (~20 %). Aucune relance.
  - **~6 000 contacts dormants** depuis 2017, jamais réactivés.
  - **Facturation** : 1 employé à 80 % de son temps sur les relances.
- **Aujourd'hui** : Excel + Wix (utilisé < 10 %). Aucune séquence automatisée.

## Principe

- Poser le **CRM d'abord**. Les 3 automatismes reposent tous dessus.
- Puis brancher le **premier gain rentable** immédiatement.
- **Point critique** : ce n'est pas l'outil, c'est l'**adoption**. Définir qui pilote le CRM dès le départ.

## Déploiement

### 1. Socle CRM
- Migrer la base pré-inscrits (~489).
- Pipeline : **pré-inscrit → contacté → payé → converti**.
- Désigner le **responsable CRM interne**. Condition de tout le reste.

### 2. Nurturing inbound *(premier gain)*
- Mail de confirmation réécrit (l'actuel trop brut).
- Séquence auto : livre blanc **J+5**, relance **J+30**, bascule promo suivante si non converti.
- Rappel **< 5 min** après inscription.

### 3. Réactivation dormants
- Segmenter les ~6 000 contacts.
- Séquences newsletter / contenu. CA déjà acquis, jamais exploité.

### 4. Facturation
- Automatiser les relances de paiement (échéances 11×).
- Libère l'employé pour le suivi commercial.

---

# Règles de classification CRM

Le CRM cible est **HubSpot**. Un contact est décrit par **deux axes indépendants**, plus deux
champs de qualité de donnée. Les confondre est l'erreur classique : un même contact peut être
`CLIENT` **et** `INDIVIDUEL`, ou `FROID` **et** `ENTREPRISE`.

| Axe | Question posée | Valeurs |
|---|---|---|
| `Tag_CRM` | Où en est la **relation commerciale** ? | CLIENT · CHAUD · INBOUND · FROID |
| `type_compte` | **Qui paie** ? | INDIVIDUEL (B2C) · ENTREPRISE (B2B) |
| `Email_actif` | L'adresse est-elle joignable ? | OUI · NON |
| `Origine_nom` | D'où vient le nom du contact ? | WIX · DEDUIT_EMAIL · DEDUIT_CLAUDE · vide |

---

## Axe 1 — `Tag_CRM` : la température

**Ce qu'il mesure :** l'avancement dans le cycle commercial. Une seule dimension, quatre
valeurs mutuellement exclusives.

**D'où vient l'information :** de la colonne `Libellés` de l'export Wix — 167 libellés
distincts accumulés depuis 2017 par plusieurs personnes, sans convention. Chaque contact ne
porte **qu'un seul** libellé ; la classification est donc un mapping libellé → tag.

### Les quatre valeurs

| Tag | Définition | Contacts |
|---|---|---|
| `CLIENT` | A déjà payé une prestation Altav | 753 |
| `CHAUD` | A manifesté une intention explicite — pré-inscription, session d'info, demande de brochure | 318 |
| `INBOUND` | Est venu à nous sans intention d'achat affirmée — livre blanc, formulaire, webinaire | 171 |
| `FROID` | Ne nous connaît pas, ou import scrapé | 6 241 |

### Règles d'attribution, dans l'ordre d'évaluation

L'ordre compte : la première règle qui s'applique gagne.

| # | Règle | Résultat | Pourquoi cet ordre |
|---|---|---|---|
| 1 | Libellé vide | `FROID` | Aucune trace de relation = aucune relation |
| 2 | Libellé dans le mapping manuel | valeur forcée | Les arbitrages humains priment sur toute heuristique |
| 3 | Libellé contenant `csv`, **sauf exceptions** | `FROID` | Un nom de fichier `.csv` trahit un import de masse |
| 4 | Mots-clés `ARCHIVE` (concours, église, obsolète) | `ARCHIVE` | Hors périmètre commercial, isolé avant tout le reste |
| 5 | Mots-clés `CLIENT` (coaching, team building, certifié, institut, formation ubuntu, KCB, Brarudi…) | `CLIENT` | Une relation payante est le signal le plus fort |
| 6 | Mots-clés `CHAUD` (pré-inscription, parcours découverte, session d'info, brochure, certification promo 4 & 5) | `CHAUD` | Intention explicite |
| 7 | Mots-clés `INBOUND` (livre blanc, formulaire, webinaire, séminaire) | `INBOUND` | Venu à nous, sans intention affirmée |
| 8 | Aucune correspondance | `A_CLASSER` | **On ne devine pas, on signale** |

### L'exception à la règle CSV — la décision la plus importante

La règle initiale disait : tout libellé contenant `csv` est un import scrapé, donc `FROID`.

Problème : presque **tous** les libellés sont des noms de fichiers finissant en `.csv`, y
compris ceux d'inscrits volontaires. `Session d'infos Ubuntu en ligne.csv` (103 contacts) et
`parcours-découverte-octobre.csv` (70 contacts) désignent des gens **venus à nous**. Les
classer en outbound froid était un contresens.

**Règle retenue :** la règle CSV s'applique **sauf** si le libellé contient un signal
d'inscription (`session d'info`, `parcours découverte`). **195 leads récupérés.**

### Ordre de priorité en cas de conflit

`ARCHIVE > CLIENT > FROID > CHAUD > INBOUND`

Non déclenché aujourd'hui — aucun contact ne porte plus d'un libellé. Conservé pour les
imports futurs, où un contact pourra cumuler plusieurs origines.

---

## Axe 2 — `type_compte` : qui paie

**Ce qu'il mesure :** l'entité qui achète et règle la formation. **Pas** l'employeur du contact.

C'est l'axe qui pilote l'objectif du fondateur : **80 % B2B / 20 % B2C**.

| Valeur | Définition |
|---|---|
| `INDIVIDUEL` (B2C) | La personne s'inscrit et paie pour elle-même |
| `ENTREPRISE` (B2B) | La société achète et paie la formation pour ses salariés |

### Le contresens à ne jamais commettre

Dans la base actuelle :

- **789 contacts** ont une `Société` renseignée
- **685 contacts** ont un email à domaine professionnel (undp.org, heineken.com, bancobu.com, ecobank.com…)
- **6 761 contacts** ont un email gratuit (gmail, yahoo, hotmail…)

Et pourtant **ces ~800 contacts sont tous des leads individuels.** Une économiste du PNUD qui
s'inscrit à la formation Ubuntu pour elle-même reste du B2C, quel que soit son email.

> **Avoir un employeur ≠ être un lead entreprise.** Classer sur `Société` renseignée ou sur le
> domaine email basculerait ~800 individuels en `ENTREPRISE` à tort, et fausserait
> immédiatement le pilotage du 80/20.

### État actuel

**Les 7 483 contacts partent en `INDIVIDUEL`.** Décision assumée : la base ne contient à ce
jour aucun lead entreprise identifiable de façon fiable, et deviner coûterait plus cher que de
ne rien dire.

### Règles de promotion vers `ENTREPRISE`

Principe : **défaut `INDIVIDUEL`, promotion sur signal fort uniquement.** Un faux `ENTREPRISE`
fausse le pilotage ; une case restée `INDIVIDUEL` se corrige à la main en dix secondes.

| # | Signal | Fiabilité | Décision |
|---|---|---|---|
| 0 | Défaut | — | `INDIVIDUEL` |
| 1 | Formulaire B2B soumis (« je forme mes équipes ») | Déterministe | `ENTREPRISE` |
| 2 | Import outbound / enrichissement LinkedIn | Déterministe | `ENTREPRISE` |
| 3 | Champs B2B remplis (SIREN, TVA, effectif) | Forte | `ENTREPRISE` |
| 4 | Transaction liée à une Entreprise ayant plus d'un contact | Forte | `ENTREPRISE` |
| 5 | Domaine pro **+** poste décideur (DRH, resp. formation, DG, DAF) | Faible | **Candidat** — revue manuelle, jamais d'auto-classement |
| 6 | `Société` renseignée seule | Nulle | **Jamais suffisant** |

**Le principe qui structure tout :** capter le type **à la source** plutôt que l'inférer après
coup. Les signaux 1 et 2 sont gratuits, déterministes et disponibles immédiatement. Les
signaux 3 à 5 ne servent qu'au rattrapage.

---

## Axe 3 — `Email_actif` : joignabilité

Issu du croisement avec la liste Wix des bounces et désabonnés (976 adresses).

La règle métier n'est pas « supprimer la personne » mais « ne plus lui écrire » :

| Situation | Traitement | Contacts |
|---|---|---|
| Email mort **et** `FROID` / `INBOUND` | Ligne **supprimée** | 889 |
| Email mort **et** `CLIENT` / `CHAUD` | Ligne **conservée**, `Email_actif = NON` | 84 |

**Pourquoi :** un client dont l'adresse a changé reste un client. 44 d'entre eux ont un
téléphone et restent joignables. Email mort + aucune relation = aucune valeur, en revanche.

Mappe sur un champ d'opt-out marketing dans HubSpot.

---

## Axe 4 — `Origine_nom` : traçabilité de l'enrichissement

70 % des contacts n'avaient qu'un email. Cette colonne dit d'où vient chaque nom, pour qu'on
sache toujours ce qui est déclaré et ce qui est déduit.

| Valeur | Sens | Contacts |
|---|---|---|
| `WIX` | Nom présent dans l'export d'origine | 2 211 |
| `DEDUIT_CLAUDE` | Déduit par modèle, relu et validé par Nael le 2026-07-20 | 1 162 |
| `DEDUIT_EMAIL` | Déduit par règle déterministe sur `prenom.nom@` | 232 |
| *(vide)* | Aucun nom — sociétés, sigles, pseudos | 3 878 |

**Contacts nommés : 3 605 / 7 483 (48 %)**, contre 33 % au départ.

---

## Mise en œuvre dans HubSpot

Abonnement actuel : **Starter** *(~15 €/mois — formule exacte à confirmer)*. Le tableau ci-dessous
décrit ce qui était déjà acquis en Free :

| Brique | Free | Rôle |
|---|---|---|
| Propriété custom `type_compte` (liste déroulante) | ✅ | Porter l'axe 2 |
| Formulaires à **champ caché** (Hidden + Default value) | ✅ | **Classer à la source** — le levier principal |
| Segments actifs sur propriété de contact | ✅ 10 actifs | Isoler B2B / B2C |
| Objet Entreprise + association auto par domaine email | ✅ | Documenter l'employeur, **sans piloter `type_compte`** |
| Pipelines de transaction | ⚠️ 1 seul | Starter en donne 2 = split B2B / B2C |
| Workflows | ❌ Professional | Classement automatique sur signaux 3 à 5 |

### Écarté, et pourquoi

| Piste | Raison du rejet |
|---|---|
| Propriété calculée | Une équation n'accepte qu'**une seule** propriété non-numérique, et seulement du même objet. Ne peut pas évaluer « domaine hors freemail ET poste décideur ». |
| Classement par domaine email | HubSpot ne sait pas tester un domaine contre une liste de freemails sans action codée (Ops Hub Pro) ou énumération manuelle. |
| Inférence sur `Société` / intitulé de poste | Basculerait ~800 individuels à tort (voir plus haut). |

### Trajectoire de palier

- **Free** — tout ce qui précède. Suffisant pour classer proprement.
- **Starter** *(souscrit)* — 2 pipelines de transaction, soit exactement le split B2B / B2C.
- **Professional** — workflows : classement automatique et bascule rétroactive.

> ⚠️ **Le compteur à surveiller n'est pas le prix mensuel, c'est le nombre de contacts
> *marketing*.** HubSpot facture les contacts démarchés, pas les contacts stockés. Le chantier
> de réactivation des **6 241 dormants** peut donc coûter bien plus que l'abonnement de base.
> À chiffrer avant de le lancer, pas après.

---

## Acquisition — d'où viennent les nouveaux leads

*Relevé du 3 août 2026, dans le back-office Wix d'Altav.*

### Le trou dans le raisonnement précédent

Le plan initial enchaînait sur les séquences de nurturing. Il manquait une marche : **une
séquence se déclenche sur une soumission de formulaire, or aucun formulaire n'alimente
HubSpot.** La base importée est un instantané figé au 20/07/2026. Tant que l'acquisition n'est
pas branchée, il n'y a rien à déclencher — et chaque nouveau lead réintègre le désordre qu'on
vient de nettoyer.

### État des lieux

| Constat | Détail |
|---|---|
| Formulaires | **52 actifs** + 17 anciens = 69 *(plafond du forfait : 95)* |
| Réponses cumulées | ~**1 116**, soit ~**25 par mois** |
| Formulaires posés sur le site | 5, totalisant **0 réponse** — ce sont des restes (`My Form`, `Questionnaire DRH copy`…) |
| Où vivent les formulaires vivants | pages autonomes sur `franckpecastaing.wixforms.com` |
| Diffusion | lien direct, **QR code**, WhatsApp, Facebook, LinkedIn, X |
| Automatisations Wix | 34 personnalisées, 11 actives |

Trois faits structurants :

- **Aucun formulaire vivant n'est sur le site.** Poser un formulaire HubSpot dans une page Wix
  n'intercepterait rien. Tout le trafic passe par des liens autonomes déjà diffusés.
- **Les liens ne portent pas la marque.** Ils sont sur l'espace personnel de Franck, pas sur un
  domaine Altav.
- **Le formulaire du pied de page du site n'est compté nulle part** — ni dans les 52, ni dans les
  1 116 réponses. Ses demandes tombent dans la boîte de réception Wix. Son menu `Statut`
  (*Chef d'entreprise · En création · En questionnement · Profession libérale · Autre*) reste un
  signal 5, candidat à revue manuelle — jamais un `ENTREPRISE` automatique.

### Il n'existe pas d'intégration Wix ↔ HubSpot

Vérifié dans l'App Market le 3 août. Trois applications tierces, aucune validée par Wix :

| Application | Note | Coût pour 8 925 contacts |
|---|---|---|
| Hubspot *(éditeur PURPLE)* | 5/5 **sur un seul avis** — dont l'auteur écrit ne pas l'avoir encore installée | 15,76 €/mois |
| HubSpot by EYEMAGINE | 2,4/5 | — |
| HubSpot Sync | **1,9/5** | dès 22,70 €/mois |

**Et aucune ne résout le problème réel.** Elles recopient des *contacts*. Un contact Wix ne porte
pas « vient du formulaire Livre blanc, donc `INBOUND` » — il porte un **libellé en texte libre**,
c'est-à-dire exactement les 167 valeurs qu'il a fallu mapper à la main en juillet. L'appli
transporterait le désordre fidèlement, et `tag_contacts.py` serait à refaire côté HubSpot, en
continu.

### Décision : les formulaires vivent dans HubSpot

Le lead naît dans le CRM, déjà classé par le champ caché du formulaire. Pas de synchronisation,
pas d'abonnement tiers, pas de pièce intermédiaire. C'est aussi ce qui rend les séquences
possibles : sans étiquette à l'arrivée, rien ne peut se déclencher.

Cible — **5 formulaires au lieu de 52** :

| Formulaire | `Tag_CRM` | `type_compte` | Champ caché |
|---|---|---|---|
| Pré-inscription formation UBUNTU | `CHAUD` | INDIVIDUEL | `promo` |
| Livre blanc | `INBOUND` | INDIVIDUEL | — |
| Session d'information / webinaire | `CHAUD` | INDIVIDUEL | `evenement` |
| « Je forme mes équipes » | `CHAUD` | **ENTREPRISE** | — |
| Contact général *(pied de page)* | `INBOUND` | INDIVIDUEL | `statut` |

Le formulaire entreprise remplace `Inscription - DRH` et `Inscription - ADG`.

**Un seul formulaire de pré-inscription, versionné par `promo`** — il en existe quatre
aujourd'hui (86, 43, 3, 0 réponses). Le formulaire neuf à chaque événement est la cause racine
des 167 libellés ; le corriger est plus important que le nettoyage lui-même.

### Bascule des anciens liens : vider, pas supprimer

Les QR codes imprimés et les liens partagés dans WhatsApp ne se remplacent pas. Chaque ancien
formulaire d'acquisition est donc **vidé et repointé** vers son équivalent HubSpot : le support
en circulation continue de fonctionner et amène au bon endroit.

Les ~30 formulaires de feedback et d'événements passés **restent dans Wix**. Ils s'adressent à
des contacts déjà `CLIENT` ; aucune valeur d'acquisition, rien à synchroniser.

Volume à l'appui : **~25 réponses par mois**. Ce débit ne justifie ni pipeline permanent, ni
abonnement de synchronisation. Le rattrapage du delta depuis le 20/07 se fait en un export/import
ponctuel.

### Deux incidents ouverts

- **Doublon d'automatisation.** Deux automatisations actives portent le même nom,
  `pré-inscription formation ubuntu`, sur deux déclencheurs distincts (`Form submitted`, 2026 —
  et `Un formulaire est envoyé`, 2023). Si elles visent le même formulaire, chaque pré-inscrit
  reçoit **deux** mails de confirmation. À vérifier avant tout rebranchement.
- **63 messages non traités.** 13 réponses de formulaire non lues *(dont une demande de Livre
  blanc)* et 50 non lus en boîte de réception Wix. Des leads vivants, certains antérieurs au
  20/07.

Quatre automatisations portent par ailleurs « Modifications non publiées », dont deux actives :
la version qui tourne n'est pas celle que l'équipe croit avoir mise en ligne.

### Deux blocages du présent document peut-être déjà levés

- `Inscription - DRH` **(15 réponses)** et `Inscription - ADG` **(8)** : formulaires réservés à
  des fonctions décisionnaires. Si ces personnes venaient faire former leurs équipes aux frais de
  leur société, ce sont les **23 premiers `ENTREPRISE`** de la base — signal 1, déterministe.
  À confirmer par Franck.
- `Certification Promo 4 & 5 — Présence` **(19 réponses)** : possiblement la liste des certifiés
  attendue de Stéphane, déjà présente dans Wix.

### Validation client

Rien ne sera créé ni modifié avant accord écrit de Franck — les changements touchent son compte,
sa marque et des supports en circulation. Les 9 questions qui débloquent le chantier sont dans
[`QUESTIONS_FORMULAIRES_FRANCK.html`](QUESTIONS_FORMULAIRES_FRANCK.html).

---

## Méthode de travail

Sur toute transformation de masse : **tester sur ~10 lignes, lister les changements, valider,
puis appliquer.** Cette règle a évité de propager 3 défauts sur 232 contacts, et a détecté un
faux fichier de suppression avant qu'il ne détruise 8 354 lignes.

Chaque script du pipeline a un `--dry-run`. Le fichier source `CRM Contact.csv` n'est jamais
modifié.

Détail des décisions de nettoyage et de leurs justifications : voir [`JOURNAL.md`](JOURNAL.md).

---

## Ce qu'il me faut

- ~~Accès **back-office Wix**~~ — obtenu le 03/08/2026.
- Accès **Excel pré-inscrits** *(les ~489 ne se retrouvent pas dans les formulaires Wix — 132
  pré-inscriptions cumulées seulement)*.
- Décision : **qui porte le CRM en interne**.
- Fichier des certifiés de Stéphane → basculer les « Certification Promo 4 & 5 » payants de
  `CHAUD` vers `CLIENT`. *Peut-être déjà disponible : 19 réponses au formulaire Wix du même nom.*
- Réponses aux **9 questions** de `QUESTIONS_FORMULAIRES_FRANCK.html`.

## Limite connue

**La géographie n'est pas exploitable en l'état.** `Pays` n'est renseigné que sur **587 / 7 483
contacts (8 %)**. Les indicatifs téléphoniques comblent partiellement : 386 numéros en +257
(Burundi), 56 en +225 (Côte d'Ivoire), 53 en +243 (RDC), 44 en +229 (Bénin), 42 en +221
(Sénégal) — soit ~24 % de la base au total.

Or l'objectif 80/20 se pilote **par zone** : quasi atteint au Burundi, très loin du compte
hors Burundi. Sans pays fiable, ce rapport n'est pas mesurable. Chantier à arbitrer.

## Prochaine étape

CRM choisi et base importée. Le point de travail suivant n'est **pas** les séquences de nurturing
mais **l'acquisition** : sans formulaire branché sur HubSpot, aucune séquence n'a de déclencheur.

1. Envoi de `QUESTIONS_FORMULAIRES_FRANCK.html` à Franck — 9 questions, dont une seule bloquante :
   l'engagement à ne plus créer de formulaire dans Wix.
2. Vérification du doublon d'automatisation et traitement des 63 messages non lus.
3. Création des 5 formulaires HubSpot, puis bascule des anciens liens.
4. **Alors seulement** : les séquences de nurturing, qui auront enfin de quoi se déclencher.
