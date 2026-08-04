# 2. Règles de classification CRM

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
