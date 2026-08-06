# 10. Guide d'exécution — le pilote du pied de page

Étapes **18** et **19** de la [checklist](00-checklist.md). Procédure à exécuter dans
HubSpot, écran par écran.

> **Ce document a une seconde vie.** C'est le brouillon du mode d'emploi d'administration remis à
> Stéphane *(étape 48)*. Il est donc écrit pour quelqu'un qui n'a jamais créé de formulaire
> HubSpot — pas pour quelqu'un qui connaît déjà le dossier. Chaque écart constaté à l'exécution
> se corrige **ici**, pas dans un fil de discussion.

**Pourquoi ce formulaire et pas un autre :** 5 champs, aucun chiffre d'affaires en jeu, et il
n'existe nulle part ailleurs qu'en pied de page du site. C'est le terrain d'essai le moins cher
de toute la mission. Décision de Franck du 6 août.

---

## Avant de commencer

| | Vérification |
|---|---|
| ☐ | Compte HubSpot ouvert, droits **Super administrateur** *(sinon la création de propriété est grisée)* |
| ☐ | Accès à l'éditeur Wix de `altavconsulting.com` — nécessaire en partie C uniquement |
| ☐ | Les 4 propriétés `Température CRM`, `Type de compte`, `Email actif`, `Date de pré-inscription` existent déjà — créées en juillet |

**On ne touche pas au formulaire Wix existant pendant tout ce guide.** Il continue de tourner. La
bascule est l'étape 21, elle vient après la recette.

---

## Partie A — Créer la propriété `Statut du visiteur`

*Étape 18, réduite à ce dont le pilote a besoin. Les 7 autres propriétés de la
[spec](08-formulaires-hubspot.md#propriétés-hubspot-à-créer) se créent au même endroit, plus
tard, quand leur formulaire arrive.*

**Chemin :** roue crantée ⚙️ *(en haut à droite)* → **Gestion des données** → **Propriétés** →
bouton **Créer une propriété** *(en haut à droite)*.

**Écran 1 — Informations de base**

| Champ | Valeur à saisir |
|---|---|
| Type d'objet | **Contact** |
| Groupe | le **même groupe que `Température CRM`** — à vérifier d'abord *(voir encadré)* |
| Libellé | `Statut du visiteur` |
| Description | `Déclaré par le visiteur dans le formulaire de contact du pied de page. Signal 5 de la grille : candidat à revue manuelle, jamais un ENTREPRISE automatique.` |

> **Vérifier le groupe avant de créer.** Dans la liste des propriétés, filtrer sur
> `Température CRM` et lire sa colonne **Groupe**. Reprendre exactement le même. Une propriété
> ALTAV rangée ailleurs devient invisible pour quelqu'un qui cherche au bon endroit — c'est
> exactement le genre de détail qui fait qu'un administrateur n'ose plus toucher à l'outil.

**Écran 2 — Type de champ**

- Type de champ : **Sélection déroulante** *(menu déroulant, un seul choix)*
- Options, dans cet ordre, **libellés repris mot pour mot du formulaire Wix** :

| # | Libellé de l'option |
|---|---|
| 1 | `Entrepreneur (chef d'entreprise)` |
| 2 | `En cours de création d'entreprise` |
| 3 | `En questionnement` |
| 4 | `Profession libérale` |
| 5 | `Autre` |

> ⚠️ **Écart entre deux documents, tranché ici.** La [spec des formulaires](08-formulaires-hubspot.md)
> abrège ces libellés en « Chef d'entreprise · En création · … ». Le [relevé du 5 août sur le
> site](06-decisions-franck.md) donne la version longue ci-dessus. **C'est la version longue qui
> fait foi** — principe de la spec : on reproduit, on ne refond pas. Un visiteur qui a lu
> « En cours de création d'entreprise » ne doit pas trouver « En création ».

**Écran 3 — Règles**

- Laisser les valeurs internes **générées automatiquement**. Ne pas les saisir à la main.
- Ne pas cocher « Afficher dans les formulaires » — le formulaire choisit ses champs lui-même.

**Vérification de sortie :** noter le **nom interne** de la propriété *(visible en survolant son
nom dans la liste, ou dans l'onglet Règles)*. Il ressemblera à `statut_du_visiteur`. **On en aura
besoin le jour d'un import CSV** — c'est lui que HubSpot remappe de travers.

---

## Partie B — Créer le formulaire

*Étape 19.*

**Chemin :** menu **Marketing** → **Capture de leads** → **Formulaires** → **Créer un
formulaire** → type **Formulaire intégré** → modèle **Vierge**.

> Choisir **Formulaire intégré**, pas « page de destination » ni « pop-up ». C'est le seul type
> qui s'incruste dans une page existante, condition n° 2 de Franck : *le visiteur ne doit pas
> voir qu'il change d'outil*.

**Nom du formulaire** *(interne, jamais vu par le visiteur)* : `ALTAV — Contact général (pied de page)`

### Les 5 champs visibles, dans cet ordre

| Ordre | Champ à glisser | Propriété HubSpot | Libellé affiché | Obligatoire |
|---|---|---|---|---|
| 1 | Nom | `Nom` *(lastname)* | `Nom` | ✅ |
| 2 | E-mail | `E-mail` *(email)* | `E-mail` | ✅ |
| 3 | Téléphone | `Numéro de téléphone` *(phone)* | `Téléphone` | — |
| 4 | Statut du visiteur | `Statut du visiteur` *(créée en partie A)* | `Statut` | ✅ |
| 5 | Message | `Message` *(propriété standard HubSpot)* | `Parlez-nous de votre projet` | ✅ |

**Deux points de mapping qui ne se devinent pas :**

- **Le champ 5 ne se crée pas.** HubSpot a déjà une propriété standard `Message`, prévue pour ça.
  On la réutilise et on **change son libellé affiché** dans l'éditeur de formulaire — le libellé
  du formulaire et le nom de la propriété sont deux choses différentes. Créer une propriété
  « Parlez-nous de votre projet » serait un doublon de plus.
- **Le champ 4 affiche `Statut`, pas `Statut du visiteur`.** C'est le libellé du formulaire Wix
  actuel. La propriété, elle, garde son nom complet côté CRM.

> **Un point à remonter à Franck, sans le décider seul.** Le formulaire Wix a **un seul champ
> `Nom`**. Reproduit à l'identique, il verse « Jean Dupont » dans le champ **Nom de famille** de
> HubSpot, prénom compris. C'est exactement le désordre qui a coûté le chantier de juillet — 33 %
> à 48 % de contacts correctement nommés, deux scripts de déduction, une passe de vérification.
> Le formulaire de pré-inscription, lui, a bien deux champs séparés.
>
> **Ce guide applique la consigne validée en Q9 : à l'identique, un seul champ.** La correction —
> scinder en `Prénom` + `Nom` — coûte un champ de plus au visiteur et se décide avec Franck, pas
> ici. **À poser en même temps que les autres points en attente.**

### Les 2 champs cachés

Dans l'éditeur, onglet des champs, section **Champs masqués** — les glisser comme les autres,
puis fixer leur valeur :

| Propriété | Valeur fixe |
|---|---|
| `Température CRM` | `INBOUND` |
| `Type de compte` | `INDIVIDUEL` |

> **C'est tout le cœur de la mission, dans deux champs.** Le contact naît classé, à la seconde de
> la soumission. Personne ne requalifie après coup — c'est le défaut de requalification qui avait
> produit 68 pré-inscrits classés `FROID`.
>
> `INBOUND` et non `CHAUD` : le visiteur est venu à nous **sans intention d'achat affirmée**.
> `INDIVIDUEL` même si le visiteur répond « Entrepreneur » : le statut déclaré est le **signal 5**
> de la grille, jamais suffisant pour basculer un compte en `ENTREPRISE`. Ce qui tranche, c'est
> qui paie la facture.

**Vérifier l'orthographe et la casse des deux valeurs** contre la liste d'options de chaque
propriété. `Inbound` ≠ `INBOUND` : HubSpot crée alors une valeur parasite, et le contact
n'apparaît dans aucune vue filtrée.

### Options du formulaire

**Onglet Options :**

| Réglage | Valeur |
|---|---|
| Message après envoi | **Afficher un message** *(pas de redirection — le visiteur reste sur le site)* |
| Texte du message | `Merci, votre message est bien arrivé. Nous revenons vers vous rapidement.` |
| Envoyer une notification par e-mail | ✅ **activé** |
| Destinataire | **Franck**, en attendant l'arbitrage de l'étape 22 bis |
| Type de notification | E-mail. *La création de tâche est grisée — workflows verrouillés, vérifié le 5 août.* |

> **Le texte de confirmation est provisoire.** Le ton définitif vient de Franck : on lui demande
> un exemple de mail qu'il envoie habituellement, et on s'en sert de modèle *(étape 17 bis)*.
> Écrire de zéro puis lui faire corriger serait plus de travail pour lui, et moins juste.

**Onglet Style :** ne rien régler pour l'instant. Le calage visuel se fait en partie C, sur le
site, où l'on voit le résultat.

---

## Partie C — Poser le formulaire dans le pied de page Wix

*Toujours l'étape 19. C'est ici que se jouent les conditions n° 1 et n° 2 de Franck.*

1. Dans HubSpot, formulaire ouvert → bouton **Publier** → **Intégrer** → copier le **code
   d'intégration**.
2. Dans l'éditeur Wix : ouvrir le **pied de page**, sélectionner le formulaire natif existant.
   **Ne pas le supprimer** — le déplacer temporairement hors écran ou le masquer.
3. **Ajouter** → **Intégrer** → **Intégrer un code / HTML iframe** → coller le code HubSpot.
4. Redimensionner le bloc : le formulaire HubSpot doit occuper la même place que l'ancien.
5. Publier le site, puis **regarder la page en navigation privée** — pas dans l'éditeur.

**Trois pièges connus sur cette partie :**

- **L'intégration de code Wix demande un forfait payant.** Si le bouton est grisé, c'est un
  point de blocage à remonter à Franck, pas un problème HubSpot.
- **Le bloc d'intégration Wix est une iframe** : le formulaire n'hérite **pas** des polices ni
  des couleurs du site. Le calage se fait dans l'onglet **Style** du formulaire HubSpot —
  police, taille, couleur du bouton — relevées sur le site. C'est la condition n° 1 de Franck,
  et c'est du travail à l'œil, pas un réglage.
- **Vérifier sur mobile.** Le pied de page est l'endroit du site le plus souvent cassé en petite
  largeur, et une iframe ne se redimensionne pas toujours seule.

---

## Partie D — Recette

*Étape 19 bis. Les trois critères sont ceux que Franck a posés en Q9. Aucun ne se coche à sa
place : cette liste se parcourt **avec lui**.*

**Le test technique, à faire seul avant de le solliciter :**

| | Contrôle | Comment on vérifie |
|---|---|---|
| ☐ | Une soumission de test crée bien un contact | HubSpot → Contacts, trier par date de création |
| ☐ | `Température CRM` = `INBOUND` | sur la fiche du contact de test |
| ☐ | `Type de compte` = `INDIVIDUEL` | idem |
| ☐ | `Statut du visiteur` contient la valeur choisie, **libellé exact** | idem |
| ☐ | Le message du champ 5 est bien dans `Message` | idem |
| ☐ | La notification par e-mail arrive | boîte de Franck |
| ☐ | Une **seconde** soumission avec le même e-mail **met à jour** la fiche, sans créer de doublon | comportement natif — mais il se vérifie |
| ☐ | Le contact de test est supprimé après recette | sinon il pollue les vues |

**Les trois critères de Franck :**

| | Critère *(Q9)* | Ce qui le prouve |
|---|---|---|
| ☐ | **Parfaitement intégré au design du site** | le formulaire, vu en navigation privée sur mobile et sur ordinateur, ne détonne pas |
| ☐ | **Transparent pour le visiteur** | pas de redirection, pas de logo HubSpot, pas de changement de page à l'envoi |
| ☐ | **Alimente directement HubSpot** | démontré par le test technique ci-dessus, sur sa fiche à lui |

**Ce que la recette débloque, et c'est le vrai enjeu :** une fois ces cases cochées, la méthode
est prouvée. On arrive devant Stéphane avec un formulaire qui tourne, pas avec une proposition —
et l'étape 20 devient une conversation sur ce qu'on améliore, pas sur ce qu'on tente.

---

## Ce qui reste ouvert à la fin de ce guide

| Point | Pour qui | Bloque |
|---|---|---|
| Champ `Nom` unique ou scindé en `Prénom` + `Nom` | **Franck** | rien aujourd'hui — se rattrape, mais salit la base en attendant |
| Destinataire des notifications : Franck, Stéphane, ou les deux | **Franck** | étape 22 bis |
| Texte de confirmation définitif | **Franck** | étape 17 bis |
| Forfait Wix autorisant l'intégration de code | **Franck** | partie C, s'il est absent |
