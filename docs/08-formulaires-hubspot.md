# 8. Spécification des formulaires HubSpot

Étape 16 de la [checklist](00-checklist.md). **Rien n'est créé avant validation** — ni par moi,
ni sur le compte de Franck.

---

## La règle qui prime sur tout le reste

> *« L'objectif est que le prospect exprime **simplement** son souhait d'intégrer la
> formation. »* — Franck, réponse à la Q5

Un formulaire d'acquisition demande **le minimum pour qu'un contact existe et soit rappelé**.
Tout le reste — société, poste, secteur, motivation — se collecte **après** l'engagement : au
rappel téléphonique, qui doit partir sous 5 minutes, ou par un second message.

Le contexte impose cette sobriété : **136 pré-inscrits, 26 confirmés** sur la promo 8. Le déchet
est déjà massif en aval ; il n'y a aucune raison d'en ajouter en amont.

> **Note d'honnêteté.** Une première version de cette spec reconduisait les 12 champs du
> formulaire Wix actuel, en s'appuyant sur leurs taux de remplissage (518 à 525 sur 525). Cet
> argument ne vaut rien : ces taux ne mesurent que les gens **allés au bout**, pas ceux qui ont
> renoncé devant douze champs. Reconduire l'existant n'était pas une décision, c'était un statu
> quo. Corrigé le 5 août.

---

## Les trois principes

1. **Le classement se fait à la source.** Chaque formulaire porte des champs cachés qui écrivent
   `Température CRM` et `Type de compte` à la seconde de la soumission. Personne ne requalifie
   après coup — c'est exactement ce qui a produit les 68 pré-inscrits classés `FROID`.
2. **Le moins de champs possible.** Un champ de plus doit se payer par une vente, pas par une
   élégance de modèle.
3. **Aucune notion de promo** — décision de Franck. La promo est une propriété interne,
   renseignée après encaissement.

---

## Les formulaires

### 1. Pré-inscription à la formation UBUNTU 🟢 *demandé par Franck*

*Le canal vivant. 141 soumissions en 2026.*

| Champ | Type | Obligatoire |
|---|---|---|
| Prénom | texte | ✅ |
| Nom | texte | ✅ |
| E-mail | e-mail | ✅ |
| Téléphone | téléphone | ✅ |

**Quatre champs. Rien d'autre.**

**Champs cachés :** `Température CRM = CHAUD` · `Type de compte = INDIVIDUEL` ·
`Date de pré-inscription = date du jour`

**Aucun champ promo, pas même caché.**

Le téléphone est obligatoire : c'est lui qui rend possible le rappel sous 5 minutes, et
44 clients à e-mail mort ne sont joignables que par là.

### 2. Contact général *(pied de page du site)* 🟢 *demandé par Franck*

| Champ | Type | Obligatoire |
|---|---|---|
| Nom | texte | ✅ |
| E-mail | e-mail | ✅ |
| Téléphone | téléphone | — |
| Statut du visiteur | déroulant | ✅ |
| Parlez-nous de votre projet | texte long | ✅ |

**Champs cachés :** `Température CRM = INBOUND` · `Type de compte = INDIVIDUEL`

Champs repris **à l'identique** de l'existant : c'est un formulaire que Franck accepte de
refaire, pas de repenser.

**Ses trois conditions d'acceptation** *(Q9)*, à traiter comme critères de recette :

1. **parfaitement intégré au design du site** ;
2. **transparent pour le visiteur** — il ne doit pas voir qu'il change d'outil ;
3. **alimente directement HubSpot**.

Le champ `Statut` reste un **signal 5** : candidat à revue manuelle, jamais un `ENTREPRISE`
automatique.

### 3. Demande d'information 🟢 *demandé par Franck*

| Champ | Type | Obligatoire |
|---|---|---|
| Prénom · Nom · E-mail · Téléphone | | ✅ |
| Votre question | texte long | ✅ |

**Champs cachés :** `Température CRM = CHAUD` · `Type de compte = INDIVIDUEL`

### 4. « Je souhaite former mes équipes » 🟢 *demandé par Franck*

*Remplace `Inscription - DRH` et `Inscription - ADG`. Le seul formulaire B2B.*

| Champ | Type | Obligatoire |
|---|---|---|
| Prénom · Nom · E-mail · Téléphone | | ✅ |
| Société | texte | ✅ |
| Votre besoin | texte long | — |

**Champs cachés :** `Température CRM = CHAUD` · **`Type de compte = ENTREPRISE`**

C'est le **signal 1** de la grille : déterministe, aucune revue nécessaire. Le critère est celui
de Franck — qui paie la facture.

### 5. Livre blanc 🟢 *demandé par Franck*

| Champ | Type | Obligatoire |
|---|---|---|
| Prénom · Nom · E-mail | | ✅ |

**Champs cachés :** `Température CRM = INBOUND` · `Type de compte = INDIVIDUEL`

On échange un document contre une adresse, pas contre un questionnaire.

### 6. Session d'information / webinaire 🟠 *proposé, pas demandé*

> **Ce formulaire ne figure pas dans la liste de Franck.** Sa réponse à la Q2 en cite cinq ;
> celui-ci est une proposition de ma part, retenue en interne le 5 août.
> **À confirmer par lui avant création.**

| Champ | Type | Obligatoire |
|---|---|---|
| Prénom · Nom · E-mail · Téléphone | | ✅ |

**Champs cachés :** `Température CRM = CHAUD` · `Type de compte = INDIVIDUEL` ·
`Événement = <nom de la session>` — **le seul champ caché à changer d'un événement à l'autre**

*Justification :* les libellés `Session d'infos Ubuntu en ligne.csv` (103 contacts) et
`parcours-découverte-octobre.csv` (70) montrent que ce canal alimente réellement, et il produit
du `CHAUD` piloté par une date, ce qu'aucun des cinq autres ne fait.

---

## Ce qu'on ne demande plus, et où ça se collecte

Le formulaire Wix actuel pose douze questions. Neuf disparaissent des formulaires d'acquisition.

| Champ retiré | Où il se collecte désormais |
|---|---|
| Société · Poste occupé · Secteur d'activité | au rappel téléphonique, ou par mail de qualification |
| Niveau d'étude · Tranche d'âge · Années d'expérience | dossier d'inscription, après règlement des frais |
| Source déclarée | remplacée par la source HubSpot, automatique |
| Attente vis-à-vis de la formation · Motivation | entretien commercial — c'est de la matière de conversation, pas de formulaire |

**Le signal B2B n'est pas perdu**, il arrive simplement après l'engagement au lieu de le
freiner. Et pour les 437 pré-inscrits déjà en base, il existe déjà : société, poste et secteur
sont dans le fichier des 525.

**Sept champs sont supprimés sans reprise**, parce qu'ils sont à **0 sur 525** : « Rédigez un
message », « E-mail 2 », « Téléphone 3 », « J'accepte les termes et conditions », « Votre niveau
d'étude supérieure » *(doublon)*, « Qu'est-ce qui motive votre engagement » *(doublon français
d'un champ anglais)*, et « Choisissez la garniture de votre pizza : 2 » — résidu d'un template.

---

## Propriétés HubSpot à créer

Deux seulement, contre huit dans la version précédente.

| Propriété | Type | Valeurs |
|---|---|---|
| `Statut du visiteur` | menu déroulant | Chef d'entreprise · En création · En questionnement · Profession libérale · Autre |
| `Événement` | texte | nom de la session ou du webinaire |

*Déjà créées :* `Température CRM`, `Type de compte`, `Email actif`, `Date de pré-inscription`.

---

## Ce qui se passe après l'envoi

| Formulaire | Message affiché | Mail automatique | Alerte Franck |
|---|---|---|---|
| Pré-inscription | confirmation + prochaines étapes | mail de confirmation réécrit | ✅ |
| Contact général | accusé de réception | — | ✅ |
| Demande d'information | accusé de réception | — | ✅ |
| Je souhaite former mes équipes | accusé + délai de rappel annoncé | — | ✅ **priorité** |
| Livre blanc | lien de téléchargement immédiat | envoi du PDF | — |
| Session d'information | confirmation + date et lien | rappel la veille | ✅ |

> ⚠️ **À vérifier avant création : la création de tâche demande peut-être un workflow**, donc le
> palier Professional. En Starter, l'alerte prend la forme d'une **notification par e-mail** à
> Franck plutôt que d'une tâche assignée. Suffisant tant qu'il est seul utilisateur — mais à
> confirmer dans son abonnement avant de promettre l'un ou l'autre. C'est l'étape 16 bis.

---

## Ce que Franck doit valider

1. **Le formulaire de pré-inscription à quatre champs** — c'est un changement net par rapport à
   l'existant, qui en pose douze.
2. **Le formulaire « Session d'information »**, qu'il n'a pas demandé.
3. **Les messages de confirmation et le mail réécrit** — ils portent sa voix, pas la mienne.
4. **Où et quand se collectent société, poste et secteur**, puisqu'ils sortent du formulaire.

Rien ne part avant son accord écrit : les formulaires touchent son compte, sa marque et des
supports déjà en circulation.
