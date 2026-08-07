# 8. Spécification des formulaires HubSpot

Étape 16 de la [checklist](00-checklist.md). **Rien n'est créé avant validation** — ni par moi,
ni sur le compte de Franck.

> **Ordre de construction arbitré le 6 août par Franck.** Cette spec décrit les 6 formulaires ;
> elle ne dit pas dans quel ordre les monter. Franck a tranché : *« Faisons d'abord un test par
> celui du bas de page comme test. »*
>
> 1. **Le formulaire n° 2, contact général (pied de page), sert de pilote.** 5 champs, aucun
>    chiffre d'affaires en jeu — il éprouve toute la plomberie sur l'objet le moins risqué.
> 2. **Le formulaire n° 1, pré-inscription, vient après, et se fait avec Stéphane.** Franck :
>    *« il y a plusieurs choses qui ont été mises en place, il faudra sûrement les améliorer,
>    mais surtout il faudra que Stéphane sache l'administrer »*. Ce que dit cette spec — *« on
>    reproduit à l'identique »* — reste vrai par rapport à **l'existant Wix**, mais l'existant
>    HubSpot n'a pas été inventorié. **Étape 19 ter avant toute création.**
> 3. Les quatre autres suivent.

---

## Le principe qui gouverne cette spec : reproduire, pas refondre

Le formulaire de pré-inscription actuel **fonctionne** : 525 soumissions depuis décembre 2022,
141 sur la seule année 2026, tous les champs renseignés à 99 %. Aucun signal ne dit qu'il pose
problème.

**On le reproduit donc à l'identique dans HubSpot.** Le seul nettoyage appliqué est factuel et
sans risque : les champs à **0 sur 525** disparaissent, les libellés passent en français, et les
valeurs mal enregistrées sont normalisées. **Aucun champ vivant n'est retiré.**

> **Deux erreurs commises sur ce document, corrigées le 5 août.**
>
> 1. Une première version reconduisait les 12 champs en les justifiant par leurs taux de
>    remplissage. L'argument était creux : ces taux ne mesurent que les gens allés au bout.
>    Ce n'était pas une décision, c'était un statu quo présenté comme une analyse.
> 2. Une seconde version réduisait le formulaire à 4 champs, en s'appuyant sur la phrase de
>    Franck *« que le prospect exprime simplement son souhait d'intégrer la formation »*.
>    **Mauvaise lecture** : ce « simplement » s'oppose au fait de **choisir sa promo**, pas au
>    nombre de champs — tout le paragraphe de Franck porte sur la promo. Personne n'a demandé
>    de raccourcir le formulaire.
>
> **Position retenue :** on ne modifie pas un formulaire qui marche sans preuve qu'il pose
> problème. Si un jour on veut tester une version courte, on le fera avec des chiffres, pas
> avec une intuition.

---

## Les trois principes

1. **Le classement se fait à la source.** Chaque formulaire porte des champs cachés qui écrivent
   `Température CRM` et `Type de compte` à la seconde de la soumission. Personne ne requalifie
   après coup — c'est exactement ce qui a produit les 68 pré-inscrits classés `FROID`.
2. **On reproduit l'existant** tant qu'aucune mesure ne justifie de le changer.
3. **Aucune notion de promo** — décision de Franck. La promo est une propriété interne,
   renseignée après encaissement.

---

## Les formulaires

### 1. Pré-inscription à la formation UBUNTU 🟢 *demandé par Franck*

*Le canal vivant. 141 soumissions en 2026. Reproduit à l'identique.*

| Champ | Type | Obligatoire |
|---|---|---|
| Prénom | texte | ✅ |
| Nom | texte | ✅ |
| E-mail | e-mail | ✅ |
| Téléphone | téléphone | ✅ |
| Société | texte | ✅ |
| Poste occupé | texte | ✅ |
| Secteur d'activité | texte | — |
| Niveau d'étude | déroulant — BAC+2 · Master · Doctorat | — |
| Tranche d'âge | déroulant — 30-35 · 35-40 · 40-50 · Plus de 50 | — |
| Années d'expérience | déroulant — 5 ans · 5 à 10 · 10 à 15 · Plus de 15 | — |
| Comment connaissez-vous la formation UBUNTU ? | cases à cocher — Réseaux sociaux · Amis et relations · Site ALTAV · Autre | — |
| Qu'est-ce qui vous intéresse dans la formation ? | cases à cocher — les 7 valeurs actuelles | — |
| Ce qui motive votre engagement | texte long | — |

**Champs cachés :** `Température CRM = CHAUD` · `Type de compte = INDIVIDUEL` ·
`Date de pré-inscription = date du jour`

**Aucun champ promo, pas même caché.**

**Trois corrections de forme, sans effet sur ce qui est demandé :**

- Les libellés mélangent français et anglais — « What is your company name? » à côté de
  « Quel age avez vous ? ». Tout passe en français.
- « Comment connaissez-vous » est stocké en JSON : `["par les réseaux sociaux","Autre"]`.
  **15 combinaisons enregistrées pour 4 valeurs réelles.** Reconstruit en cases à cocher propres.
- Les années d'expérience sont sales : `'+ de 15 ans`, `de 5 à 10 ans`. Valeurs normalisées.

*Suggestion, non appliquée :* ajouter « Moins de 30 ans » aux tranches d'âge. Aujourd'hui un
candidat de 28 ans n'a aucune case à cocher. **À proposer à Franck, pas à décider seul.**

### 2. Contact général *(pied de page du site)* 🟢 *demandé par Franck*

| Champ | Type | Obligatoire |
|---|---|---|
| Nom | texte | ✅ |
| E-mail | e-mail | ✅ |
| Téléphone | téléphone | — |
| Statut du visiteur | déroulant | ✅ |
| Parlez-nous de votre projet | texte long | ✅ |

**Champs cachés :** `Température CRM = INBOUND` · `Type de compte = INDIVIDUEL`

Champs repris **à l'identique** de l'existant.

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
| Poste occupé | texte | ✅ |
| Votre besoin | texte long | — |

**Champs cachés :** `Température CRM = CHAUD` · **`Type de compte = ENTREPRISE`**

C'est le **signal 1** de la grille : déterministe, aucune revue nécessaire. Le critère est celui
de Franck — qui paie la facture.

### 5. Livre blanc 🟢 *demandé par Franck*

| Champ | Type | Obligatoire |
|---|---|---|
| Prénom · Nom · E-mail | | ✅ |
| Société | texte | — |

**Champs cachés :** `Température CRM = INBOUND` · `Type de compte = INDIVIDUEL`

On échange un document contre une adresse, pas contre un questionnaire.

### 6. Session d'information / webinaire 🟠 *proposé, pas demandé*

> **Ce formulaire ne figure pas dans la liste de Franck.** Sa réponse à la Q2 en cite cinq ;
> celui-ci est une proposition de ma part. **À confirmer par lui avant création.**

| Champ | Type | Obligatoire |
|---|---|---|
| Prénom · Nom · E-mail · Téléphone | | ✅ |
| Société · Poste occupé | texte | — |

**Champs cachés :** `Température CRM = CHAUD` · `Type de compte = INDIVIDUEL` ·
`Événement = <nom de la session>` — **le seul champ caché à changer d'un événement à l'autre**

*Justification :* les libellés `Session d'infos Ubuntu en ligne.csv` (103 contacts) et
`parcours-découverte-octobre.csv` (70) montrent que ce canal alimente réellement, et il produit
du `CHAUD` piloté par une date, ce qu'aucun des cinq autres ne fait.

---

## Les 7 champs supprimés

Uniquement ceux à **0 sur 525**. Aucun n'a jamais été rempli par personne.

| Champ | Motif |
|---|---|
| Rédigez un message | jamais rempli |
| E-mail 2 · Téléphone 3 | jamais remplis |
| J'accepte les termes et conditions | jamais coché — remplacé par une mention de consentement explicite |
| Votre niveau d'étude supérieure | doublon du champ « niveau d'étude » |
| Qu'est-ce qui motive votre engagement *(version FR)* | doublon de la version anglaise |
| Choisissez la garniture de votre pizza : 2 | résidu de template |

*« Choix de ma formation » (7/525) disparaît aussi : le choix de la promo relève d'ALTAV, pas du
candidat — décision de Franck.*

---

## Propriétés HubSpot à créer

| Propriété | Type | Valeurs |
|---|---|---|
| `Source déclarée` | cases à cocher | Réseaux sociaux · Amis et relations · Site ALTAV · Autre |
| `Attente vis-à-vis de la formation` | cases à cocher | les 7 valeurs actuelles, reprises telles quelles |
| `Motivation` | texte long | libre |
| `Niveau d'étude` | menu déroulant | BAC+2 · Master · Doctorat |
| `Tranche d'âge` | menu déroulant | 30-35 · 35-40 · 40-50 · Plus de 50 |
| `Années d'expérience` | menu déroulant | 5 ans · 5 à 10 ans · 10 à 15 ans · Plus de 15 ans |
| `Statut du visiteur` | menu déroulant | Chef d'entreprise · En création · En questionnement · Profession libérale · Autre |
| `Événement` | texte | nom de la session ou du webinaire |

Société, poste et secteur se branchent sur les propriétés **standard** de HubSpot
*(`Nom de l'entreprise`, `Poste`, `Secteur d'activité`)* — rien à créer.

*Déjà créées :* `Température CRM`, `Type de compte`, `Email actif`, `Date de pré-inscription`.

---

## Ce qui se passe après l'envoi

| Formulaire | Message affiché | Mail automatique | Alerte Franck |
|---|---|---|---|
| Pré-inscription | confirmation + prochaines étapes | mail de confirmation | ✅ |
| Contact général | accusé de réception | — | ✅ |
| Demande d'information | accusé de réception | — | ✅ |
| Je souhaite former mes équipes | accusé + délai de rappel annoncé | — | ✅ **priorité** |
| Livre blanc | lien de téléchargement immédiat | envoi du PDF | — |
| Session d'information | confirmation + date et lien | rappel la veille | ✅ |

> ⚠️ **Vérifié le 5 août : la création de tâche n'est pas disponible.** Les workflows sont
> verrouillés — HubSpot renvoie vers **Sales Hub Pro**. L'alerte prend donc la forme d'une
> **notification par e-mail** à Franck, native aux formulaires. Voir
> [solution provisoire](09-solution-provisoire.md).

**Le ton des messages** vient de Franck : on lui demande un exemple de mail qu'il envoie
habituellement à ses prospects, et on s'en sert comme modèle. Écrire de zéro puis lui faire
corriger serait plus de travail pour lui, et moins juste.

---

## Ce qui attend Franck

| # | Point | Bloque quoi |
|---|---|---|
| 1 | **La mise en relation avec Stéphane** — et son périmètre d'administration | la pré-inscription *(étape 20)* et toute la phase 6 |
| 1 bis | **Valider les textes de consentement RGPD** du pilote — posés, mais ce sont ceux de HubSpot | la mise en ligne du formulaire : ils engagent ALTAV |
| 2 | **Un exemple de mail** qu'il envoie à ses prospects | les messages de confirmation |
| 3 | **Le formulaire « Session d'information »**, qu'il n'a pas demandé | ce formulaire seul |
| 4 | **Les destinataires des notifications** — Franck, Stéphane, ou les deux | l'étape 22 bis, pas la création |
| 5 | **Le champ `Nom`** du pied de page : unique comme aujourd'hui, ou scindé en `Prénom` + `Nom` | rien — mais salit la base tant que ce n'est pas tranché |
| 6 | *(mineur)* L'ajout de « Moins de 30 ans » aux tranches d'âge | rien |

**Seul le point 1 est bloquant**, et il bloque la pré-inscription, pas le pilote.

> **Retiré de cette liste le 6 août : « les supports en circulation ».** On demandait à Franck
> quel QR code était imprimé sur quelle brochure. **Question inutile :** un QR code encode une
> URL, il ne redirige pas. Tant qu'aucune adresse n'est supprimée — c'est la stratégie retenue
> depuis Q3 — le support physique n'a aucune importance. La liste des URL vivantes se relève
> seul dans le back-office *(étape 17 quater)*, et elle est plus fiable qu'un inventaire de
> mémoire.

## Ce qui attend Stéphane

| # | Point | Bloque quoi |
|---|---|---|
| 1 | **L'inventaire de ce qu'il a déjà mis en place** sur la pré-inscription | l'étape 20 — rien ne s'écrase avant |
| 2 | **Ce qu'il veut pouvoir administrer seul** | le mode d'emploi *(étape 48)* |
