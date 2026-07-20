# Mise en place HubSpot — `type_compte`

Guide de paramétrage. **Les règles de classification et leur justification sont dans
[`README.md`](README.md), section « Règles de classification CRM ».** Ce document ne les
répète pas : il dit quoi cliquer, dans quel ordre, et ce qui casse si on s'en écarte.

Abonnement de référence : **HubSpot gratuit**.

---

## 1. Créer la propriété

Settings → Properties → Contact properties → **Create property**

| Champ | Valeur |
|---|---|
| Label | Type de compte |
| Internal name | `type_compte` |
| Group | Informations de contact |
| Field type | **Dropdown select** |
| Options | `INDIVIDUEL` · `ENTREPRISE` |
| Valeur par défaut | `INDIVIDUEL` |

**Pourquoi une liste déroulante et pas un texte libre :** un champ texte laisse entrer
`Entreprise`, `entreprise`, `B2B`, `Ese`. La segmentation devient inexploitable au bout de
trois mois. La liste fermée est la seule garantie que les segments restent justes.

**Pourquoi une valeur par défaut :** tout contact créé hors formulaire et hors import (saisie
manuelle, synchro) tombe dans le cas majoritaire au lieu de rester vide. Une propriété vide
n'est ni B2B ni B2C — elle disparaît des deux segments et fausse le comptage.

### Les trois autres propriétés à créer

Le CSV en porte quatre au total. HubSpot ne reconnaît aucune : sans création préalable, la
colonne est **ignorée silencieusement à l'import**.

| Colonne CSV | Propriété HubSpot | Type |
|---|---|---|
| `type_compte` | Type de compte | Dropdown — `INDIVIDUEL` / `ENTREPRISE` |
| `Tag_CRM` | Température CRM | Dropdown — `CLIENT` / `CHAUD` / `INBOUND` / `FROID` |
| `Email_actif` | Email actif | Dropdown — `OUI` / `NON` |
| `Origine_nom` | Origine du nom | Dropdown — `WIX` / `DEDUIT_EMAIL` / `DEDUIT_CLAUDE` |

---

## 2. Importer le fichier

Fichier : **`contacts_hubspot.csv`** — 7 483 lignes, 50 colonnes, UTF-8 avec BOM,
séparateur `;`.

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

**Ne pas importer `Libellés`** dans une propriété active. La colonne est conservée dans le CSV
comme trace d'origine, mais `Tag_CRM` la remplace fonctionnellement. Deux champs qui disent la
même chose divergent toujours.

---

## 3. Les deux formulaires — le cœur du dispositif

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

## 4. Les segments

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

## 5. Association automatique aux entreprises

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

## 6. Spec du workflow — à activer au passage Professional

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

## 7. Ce qui a été écarté

À ne pas reproposer sans élément nouveau.

| Piste | Raison du rejet |
|---|---|
| Propriété calculée | Une équation n'accepte qu'**une seule** propriété non-numérique, et uniquement du même objet. Ne peut pas évaluer « domaine hors freemail ET poste décideur ». |
| Classement par domaine email | Pas de test contre une liste de freemails sans action codée. Maillon faible de toute approche par domaine. |
| Inférence sur `Société` ou intitulé de poste | Basculerait ~800 individuels en `ENTREPRISE` à tort — ils ont un employeur, pas un achat d'entreprise. |
| Deviner le type sur la base existante | Aucun signal fiable disponible. Une case fausse coûte plus cher qu'une case par défaut. |

---

## 8. Trajectoire de palier

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
