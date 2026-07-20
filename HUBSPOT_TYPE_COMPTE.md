# Mise en place HubSpot — `type_compte`

Guide de paramétrage. **Les règles de classification et leur justification sont dans
[`README.md`](README.md), section « Règles de classification CRM ».** Ce document ne les
répète pas : il dit quoi cliquer, dans quel ordre, et ce qui casse si on s'en écarte.

Abonnement de référence : **HubSpot gratuit**.

---

## 1. Les 9 propriétés custom à créer

Settings → Properties → Contact properties → **Create property**, pour chacune.

HubSpot n'en reconnaît aucune. **Sans création préalable, la colonne est ignorée
silencieusement à l'import** — pas d'erreur, pas d'alerte, la donnée disparaît.

Elles se rangent en deux familles, et **il ne faut pas les mélanger** :

- **Pilotage** — champs vivants, qui servent à segmenter et à décider. On les met à jour.
- **Héritage Wix** (`wix_`) — archive figée au 20/07/2026. **Personne n'écrit dedans après
  l'import.** Elles existent pour ne pas perdre l'historique, pas pour piloter.

### Famille 1 — Pilotage

| Label HubSpot | Internal name | Type | Options | Description à coller |
|---|---|---|---|---|
| Type de compte | `type_compte` | Dropdown | `INDIVIDUEL` · `ENTREPRISE` | Qui paie la formation. INDIVIDUEL = la personne pour elle-même (B2C). ENTREPRISE = la société pour ses salariés (B2B). Ne dépend PAS de l'employeur du contact. |
| Température CRM | `tag_crm` | Dropdown | `CLIENT` · `CHAUD` · `INBOUND` · `FROID` | Où en est la relation commerciale. CLIENT = a déjà payé. CHAUD = intention explicite. INBOUND = venu à nous sans intention affirmée. FROID = ne nous connaît pas. |
| Email actif | `email_actif` | Dropdown | `OUI` · `NON` | NON = adresse morte (bounce ou désabonnement) sur un contact qu'on garde pour la valeur de la relation. Ne pas écrire à ces contacts par email. |
| Origine du nom | `origine_nom` | Dropdown | `WIX` · `DEDUIT_EMAIL` · `DEDUIT_CLAUDE` | D'où vient le nom. WIX = déclaré par le contact. DEDUIT_* = reconstruit depuis l'email, donc faillible. Vide = aucun nom connu. |
| Domaine d'activité | `domaine_activite` | **Texte** *(1 ligne)* | — | Secteur d'activité déclaré par le lead. Texte libre : 162 valeurs distinctes pour 180 contacts, aucune nomenclature à figer. |

### Famille 2 — Héritage Wix *(lecture seule)*

Les deux premières sont la paire qui prête à confusion. Elles décrivent **le même événement**,
sous deux angles : *quoi* et *quand*. Nommées avec le même préfixe et un suffixe distinct,
elles se rangent côte à côte dans HubSpot.

| Label HubSpot | Internal name | Type | Contenu | Exemple |
|---|---|---|---|---|
| Wix — Dernière action : **nature** | `wix_derniere_action_type` | Texte | *Quelle* action | `Une campagne e-mail a été envoyée à ce contact` |
| Wix — Dernière action : **date** | `wix_derniere_action_date` | Date | *Quand* | `27/05/2026 07:41` |
| Wix — Source d'acquisition | `wix_source` | Texte | Comment le contact est entré chez Wix | `Prospection`, `Envoi d'un formulaire` |
| Wix — Libellés d'origine | `wix_libelles` | Texte | Libellé Wix brut, remplacé fonctionnellement par `tag_crm` | `Session d'infos Ubuntu en ligne.csv` |

**Description à coller sur les 4 :**

> Archive Wix figée au 20/07/2026. Ne reflète aucune activité HubSpot. Lecture seule — ne
> jamais mettre à jour ni utiliser pour segmenter l'engagement actuel.

### Pourquoi ces choix

**Liste déroulante plutôt que texte, sur les 4 propriétés de pilotage.** Un champ texte laisse
entrer `Entreprise`, `entreprise`, `B2B`, `Ese`. Au bout de trois mois la segmentation est
inexploitable. La liste fermée est la seule garantie que les segments restent justes.

**Valeur par défaut `INDIVIDUEL` sur `type_compte`.** Tout contact créé hors formulaire et hors
import — saisie manuelle, synchro — tombe dans le cas majoritaire au lieu de rester vide. Une
propriété vide n'est ni B2B ni B2C : elle disparaît des deux segments et fausse le comptage.

**Préfixe `wix_` sur l'héritage.** Il regroupe ces propriétés au même endroit dans la liste
HubSpot et signale au premier coup d'œil qu'on regarde une archive, pas une donnée vivante.
Sans ce marqueur, quelqu'un finira par bâtir un rapport d'engagement sur des dates Wix.

---

## 2. Plan de mapping, colonne par colonne

Le fichier compte 22 colonnes. Toutes n'ont pas vocation à entrer dans HubSpot, et certaines
ne doivent surtout pas atterrir dans une propriété native.

### Le principe : historique Wix ≠ activité HubSpot

`Dernière activité` (la nature — « Une campagne e-mail a été envoyée ») et `Date de la
dernière activité` (le moment) sont l'**historique Wix**. HubSpot possède ses propres
propriétés équivalentes, qu'il **alimente lui-même en continu**.

Les mapper sur les natives casse deux choses : HubSpot écrasera les valeurs à la première
activité réelle, et entre-temps les rapports d'engagement seront faux — un contact « actif au
27/05/2026 » qui n'a jamais rien fait dans HubSpot.

> **Tout l'historique Wix va dans des propriétés custom préfixées `wix_`, jamais dans les
> natives.** C'est de l'archive, pas de l'activité vivante.

### A — Vers les propriétés natives

| Colonne | Propriété HubSpot | Rempli |
|---|---|---|
| Prénom / Nom de famille | `firstname` / `lastname` | 47 % / 41 % |
| E-mail 1 | `email` | 99,5 % |
| E-mails secondaires *(fusion de E-mail 2 + E-mail 3)* | `hs_additional_emails` | 1,4 % |
| Téléphone 1 | `phone` | 19 % *(après nettoyage)* |
| Société | `company` — texte. **L'employeur, pas l'acheteur** | 10,5 % |
| Occupation | `jobtitle` | 8,6 % |
| Adresse 1 - Rue / Ville / Pays | `address` / `city` / `country` | 2 % / 1,7 % / 7,8 % |
| Langue | `hs_language` | 6,6 % |
| Créé le (UTC+0) | `createdate` | 62,7 % |

### B — Vers des propriétés custom, en lecture seule

| Colonne | Propriété à créer | Pourquoi pas la native |
|---|---|---|
| Dernière activité *(nature)* | `wix_derniere_action_type` | HubSpot gère la sienne |
| Date de la dernière activité | `wix_derniere_action_date` | idem — sinon rapports faussés |
| Source | `wix_source` | *Original source* est piloté par HubSpot |
| Libellés | `wix_libelles` | Trace d'origine ; `Tag_CRM` la remplace fonctionnellement |
| Domaine d'activité | `domaine_activite` | Aucun équivalent natif |
| Tag_CRM · Email_actif · Origine_nom · type_compte | voir section 1 | — |

**`Domaine d'activité` en texte libre, pas en liste déroulante :** 162 valeurs distinctes pour
180 contacts renseignés — quasiment aucune ne se répète. Il n'y a pas de nomenclature à figer
aujourd'hui. *(La colonne s'appelait « Sujet de coaching » dans Wix ; le libellé était
trompeur, le contenu est le secteur d'activité du lead.)*

### C — Traitement particulier

**`Statut d'abonné aux e-mails` — enjeu légal, à traiter à part.** **1 051 désabonnés.** Ne se
mappe pas comme une propriété ordinaire : il faut passer par l'opt-out marketing HubSpot,
sinon on réexpédie à des gens qui se sont désabonnés. À croiser avec les 84 `Email_actif = NON`
→ l'ensemble « ne plus écrire » fait environ 1 100 contacts. **Import séparé, après le
principal.**

### D — Retirées du fichier, pas seulement « à ne pas importer »

Ces 26 colonnes ne figurent plus dans `contacts_hubspot.csv` : elles ont été supprimées par
`retirer_colonnes_vides.py`, pas seulement écartées du mapping. Bruit structurel Wix,
0,0 % à 1,0 % de remplissage, jamais utilisé nulle part.

| Colonne | Remplissage |
|---|---|
| Adresses 2 à 5 et tous leurs sous-champs *(19 colonnes)* | 0,0 % à 0,9 % |
| Adresse 1 - Type, Rue ligne 2, État/Région, Code postal | 0,0 % à 1,0 % |
| Téléphone 2, 3, 4 | 0,1 % à 2,9 % |

**Conservées malgré un taux tout aussi bas**, parce qu'elles portent une vraie donnée pour un
sous-ensemble réel de contacts, pas du bruit structurel :

| Colonne | Remplissage | Pourquoi on la garde |
|---|---|---|
| `E-mails secondaires` | 1,4 % | Réel pour les 106 contacts concernés |
| `Domaine d'activité` | 2,4 % | Réel pour les 180 contacts concernés |
| `Langue` | 6,6 % | Réel pour les 493 contacts concernés |
| `Adresse 1 - Pays` | 7,8 % | Seul signal géo disponible pour l'objectif 80/20 Burundi (voir README.md) |

### Nettoyages déjà appliqués

Par `preparer_import_hubspot.py`, avant import :

| Opération | Effet |
|---|---|
| Téléphones parasites vidés | 134 valeurs (`1`, `600`, `60000`, `'+257`) → 1 444 numéros exploitables |
| Langues normalisées | `fr-fr`, `fr-FR` → `fr` ; `en-US`, `en-GB` → `en`. Reste : fr 389 · en 101 · pt 2 · ar 1 |
| `Statut d'abonné aux SMS` retiré | 325 lignes, **toutes** à « Jamais abonné » — aucune information |
| `Sujet de coaching` renommé | → `Domaine d'activité` |

### Points de vigilance à l'import

- **37 lignes sans email** — HubSpot les créera sans clé de dédoublonnage
- **6 emails en double** — HubSpot fusionnera automatiquement

---

## 3. Importer le fichier

Fichier : **`contacts_hubspot.csv`** — 7 483 lignes, 22 colonnes, UTF-8 avec BOM,
séparateur `;`.

**Piège d'import : ne mapper qu'UNE colonne sur la propriété Email.** HubSpot exige que
`E-mail` reste unique — c'est la clé d'identification du contact. `E-mail 2` et `E-mail 3` ne
peuvent pas s'y mapper aussi. Ils ont donc été fusionnés dans une colonne unique
`E-mails secondaires`, valeurs séparées par `;` (le format exact qu'attend HubSpot pour sa
propriété *Adresses e-mail supplémentaires*), à mapper sur `hs_additional_emails`.

Le `;` étant aussi le séparateur de colonnes du fichier, ce champ apparaît entre guillemets
dans le CSV (`"email1;email2"`) — c'est standard, ne pas s'en inquiéter à l'ouverture dans un
éditeur de texte.

Produit par `ajouter_type_compte.py` à partir de `contacts_wix_tagges.csv`, qui n'est jamais
modifié.

**Procédure :**

1. **Importer 10 lignes d'abord.** Extraire un échantillon, l'importer, ouvrir un contact,
   vérifier que les 4 propriétés custom sont bien remplies.
2. À l'écran de mapping, contrôler les 4 colonnes custom une par une. C'est là que ça casse :
   HubSpot mappe les colonnes standard tout seul et laisse les custom en « Don't import »
   sans le signaler franchement.
3. Vérifier que le séparateur détecté est bien `;` et l'encodage UTF-8.
4. Puis importer le reste.

**`Libellés` va dans `wix_libelles`, en lecture seule** — jamais dans une propriété active.
La colonne reste comme trace d'origine, mais `Tag_CRM` la remplace fonctionnellement. Deux
champs actifs qui disent la même chose divergent toujours.

---

## 4. Les deux formulaires — le cœur du dispositif

C'est le mécanisme qui classe les futurs leads. Il fonctionne en Free, sans workflow.

| Formulaire | Intitulé public | Champ caché |
|---|---|---|
| **B2C** | « Je m'inscris à la formation » | `type_compte` = `INDIVIDUEL` |
| **B2B** | « Je forme mes équipes » / « Demander un devis entreprise » | `type_compte` = `ENTREPRISE` |

**Configurer le champ caché :** ajouter `type_compte` au formulaire → dans l'éditeur latéral,
activer **Hidden**, puis renseigner **Default value**. La valeur part dans la propriété à la
soumission, invisible pour le visiteur.

**Deux pièges documentés :**

- Un champ ne peut pas être **Required** et **Hidden** en même temps. Laisser Required off.
- Si **« pré-remplir les champs pour les visiteurs connus »** est actif sur le formulaire, la
  valeur cachée peut être écrasée par l'ancienne valeur du contact. **Désactiver cette option
  sur les deux formulaires.**

**Champs à mettre sur le formulaire B2B uniquement :** nombre de salariés à former, budget
envisagé, fonction du demandeur. Ils n'ont aucun sens en B2C, et deviennent eux-mêmes des
signaux B2B fiables pour la suite.

> Le lead arrive **déjà classé**. C'est tout l'intérêt : pas d'inférence, pas de workflow, pas
> de reprise manuelle.

---

## 5. Les segments

CRM → Segments → Create segment. *(HubSpot a renommé « Listes » en « Segments » en 2026.)*

| Segment | Critère | Type |
|---|---|---|
| Leads B2B | `Type de compte` = `ENTREPRISE` | Actif |
| Leads B2C | `Type de compte` = `INDIVIDUEL` | Actif |

Le plan gratuit donne **10 segments actifs** et 1 000 statiques. Le critère « propriété de
contact » y est supporté — ces deux segments sont donc réalisables immédiatement et se
tiennent à jour seuls.

Garder de la marge : ces deux-là plus les segments de température consomment déjà la moitié
du quota.

---

## 6. Association automatique aux entreprises

Settings → Data Management → Objects → **Companies** → cocher « Create and associate contacts
and companies ».

HubSpot matche le domaine de `email` contre le `Company domain name` d'une entreprise. Les
domaines gratuits (gmail, yahoo, hotmail…) ne déclenchent rien.

Effet attendu sur la base actuelle : **aucune entreprise créée depuis les 6 761 emails
gratuits**, environ **685 domaines pro** en généreront (undp.org, heineken.com, bancobu.com,
ecobank.com…).

> **Cette association ne pilote pas `type_compte`, et ne doit jamais le piloter.** Elle
> documente *l'employeur*. `type_compte` dit *qui paie*. Les 685 contacts qui se verront
> associer une entreprise restent `INDIVIDUEL` — ils se sont inscrits pour eux-mêmes.
> Confondre les deux est l'erreur qui ferait basculer ~800 contacts à tort.

---

## 7. Spec du workflow — à activer au passage Professional

Les workflows sont indisponibles en Free et Starter. Cette spec est écrite maintenant pour
qu'il n'y ait rien à reconcevoir le jour du passage.

**Workflow : « Classement type_compte à la création »**

- **Type :** Contact-based
- **Déclencheur :** Contact created
- **Ré-inscription :** désactivée — le classement se fait une fois, les corrections manuelles
  ne doivent pas être écrasées

**Branches, dans cet ordre :**

| Ordre | Condition | Action |
|---|---|---|
| 1 | `type_compte` est connu | **Sortir du workflow** — ne jamais écraser un classement à la source |
| 2 | SIREN **ou** TVA **ou** effectif est connu | `type_compte` = `ENTREPRISE` |
| 3 | Associé à une entreprise ayant plus d'un contact | `type_compte` = `ENTREPRISE` |
| 4 | Poste décideur (DRH, resp. formation, DG, DAF) **et** email hors domaine gratuit | Créer une tâche de revue manuelle — **pas** de classement auto |
| 5 | Sinon | `type_compte` = `INDIVIDUEL` |

**La branche 1 est la plus importante.** Sans elle, le workflow réécrase ce que les
formulaires ont correctement posé.

**Limite technique de la branche 4 :** HubSpot ne sait pas tester un domaine contre une liste
de freemails. Deux options seulement — une action codée (Ops Hub Professional), ou une
condition OR énumérant à la main les domaines gratuits courants. La seconde est fragile et
demande un entretien régulier. C'est aussi pourquoi la branche 4 crée une tâche au lieu de
classer.

---

## 8. Ce qui a été écarté

À ne pas reproposer sans élément nouveau.

| Piste | Raison du rejet |
|---|---|
| Propriété calculée | Une équation n'accepte qu'**une seule** propriété non-numérique, et uniquement du même objet. Ne peut pas évaluer « domaine hors freemail ET poste décideur ». |
| Classement par domaine email | Pas de test contre une liste de freemails sans action codée. Maillon faible de toute approche par domaine. |
| Inférence sur `Société` ou intitulé de poste | Basculerait ~800 individuels en `ENTREPRISE` à tort — ils ont un employeur, pas un achat d'entreprise. |
| Deviner le type sur la base existante | Aucun signal fiable disponible. Une case fausse coûte plus cher qu'une case par défaut. |

---

## 9. Trajectoire de palier

| Palier | Ce que ça débloque pour ce sujet |
|---|---|
| **Free** *(actuel)* | Sections 1 à 5. Suffisant pour classer proprement les nouveaux leads. |
| **Starter** | 2 pipelines de transaction au lieu d'1, soit exactement le split B2B / B2C. Meilleur rapport coût / bénéfice. |
| **Professional** | Workflows : section 6, plus le classement rétroactif de l'existant. |

---

## Vérification de bout en bout

1. `python3 ajouter_type_compte.py --dry-run` → échantillon de 10 lignes, aucune écriture
2. Les 4 propriétés existent dans HubSpot **avant** l'import
3. Import de 10 lignes → ouvrir un contact, les 4 propriétés sont remplies
4. Import complet → 7 483 contacts, segment « Leads B2C » = 7 483, segment « Leads B2B » = 0
5. Soumettre le formulaire B2B en test → le contact créé porte `type_compte = ENTREPRISE` et
   entre dans le segment « Leads B2B »
6. Soumettre le formulaire B2C en test → `type_compte = INDIVIDUEL`
