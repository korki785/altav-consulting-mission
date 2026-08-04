# 4. Acquisition — d'où viennent les nouveaux leads

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
transporterait le désordre fidèlement, et `scripts/01_tag_contacts.py` serait à refaire côté HubSpot, en
continu.

### Décision : les formulaires vivent dans HubSpot

Le lead naît dans le CRM, déjà classé par le champ caché du formulaire. Pas de synchronisation,
pas d'abonnement tiers, pas de pièce intermédiaire. C'est aussi ce qui rend les séquences
possibles : sans étiquette à l'arrivée, rien ne peut se déclencher.

Cible — **6 formulaires au lieu de 52** *(validée par Franck le 4 août, voir
[`06-decisions-franck.md`](06-decisions-franck.md))* :

| Formulaire | `Tag_CRM` | `type_compte` | Champ caché | Ce qui le distingue |
|---|---|---|---|---|
| Pré-inscription formation UBUNTU | `CHAUD` | INDIVIDUEL | **aucun** | « je veux entrer en formation » — l'intention la plus forte |
| Session d'information / webinaire | `CHAUD` | INDIVIDUEL | `evenement` | inscription à une date précise |
| Demande d'information | `CHAUD` | INDIVIDUEL | — | question sur la formation, sans engagement de date |
| « Je forme mes équipes » | `CHAUD` | **ENTREPRISE** | — | c'est la société qui paie |
| Livre blanc | `INBOUND` | INDIVIDUEL | — | vient chercher du contenu, pas la formation |
| Contact général *(pied de page)* | `INBOUND` | INDIVIDUEL | `statut` | tout-venant du site, sujet non qualifié |

Le formulaire entreprise remplace `Inscription - DRH` et `Inscription - ADG`.

**Un seul formulaire de pré-inscription, sans aucune notion de promo** — il en existe quatre
aujourd'hui (86, 43, 3, 0 réponses). Le formulaire neuf à chaque événement est la cause racine
des 167 libellés ; le corriger est plus important que le nettoyage lui-même.

> **Correction de Franck sur ce point.** La cible portait d'abord un champ caché `promo`. Le
> formulaire ne doit mentionner aucune promotion : le prospect exprime un souhait d'intégrer la
> formation, l'affectation à une cohorte est une décision d'ALTAV prise **après** règlement des
> frais. `promo` devient une propriété interne du contact dans HubSpot.

**Demande d'information et contact général restent deux formulaires distincts** *(tranché le
4 août)*. Le premier porte sur la formation — l'intention est identifiable, donc `CHAUD`. Le
second est le tout-venant du site, sujet inconnu à l'arrivée, donc `INBOUND` : c'est le champ
`statut` qui le qualifie ensuite. Les fusionner ferait perdre la distinction à la source, seul
endroit où elle est gratuite.

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

### Deux blocages du présent document — levés le 4 août

- `Inscription - DRH` **(15 réponses)** et `Inscription - ADG` **(8)** : Franck confirme que ces
  personnes venaient faire former leurs équipes aux frais de leur société. Ce sont les
  **23 premiers `ENTREPRISE`** de la base — signal 1, déterministe.
- `Certification Promo 4 & 5 — Présence` **(19 réponses)** : confirmé, ce sont des clients ayant
  payé. Bascule `CHAUD` → `CLIENT`, après vérification des cas particuliers.

Les deux actions demandent d'abord un **export Wix des réponses** de ces trois formulaires :
les identités ne sont pas déductibles de la base actuelle.

### Validation client

Rien ne sera créé ni modifié avant accord écrit de Franck — les changements touchent son compte,
sa marque et des supports en circulation. Les 9 questions sont dans
[`livrables/QUESTIONS_FORMULAIRES_FRANCK.html`](../livrables/QUESTIONS_FORMULAIRES_FRANCK.html),
**toutes répondues le 4 août 2026** — décisions consolidées dans
[`06-decisions-franck.md`](06-decisions-franck.md).
