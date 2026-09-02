# 11. Architecture des outils — qui fait autorité sur quoi

**Cadre posé par Franck le 6 août 2026.** *« Je déconseille fortement de laisser plusieurs outils
gérer les mêmes informations. »*

Ce document n'est pas une proposition : c'est le cadre dans lequel tout le reste de la mission
doit tenir. Les documents antérieurs décrivent **comment** brancher les formulaires ; celui-ci
dit **pourquoi** ils quittent Wix.

---

## Les trois rôles

| Outil | Rôle |
|---|---|
| **Wix** | Site web, catalogue, paiement, espace client, réservation |
| **HubSpot** | **Base de données unique des contacts** — CRM, marketing, ventes, historique de toutes les interactions |
| **Evalangdo** | Moteur de production des évaluations *(Drivers, IE, etc.)* |

**Autrement dit :** Wix vend · HubSpot connaît le client · Evalangdo réalise les tests.

---

## La règle qui compte : HubSpot est la source unique de vérité

**Chaque personne a une seule fiche, et elle est dans HubSpot.**

C'est la décision structurante du 6 août. Elle ne dit pas que le nom d'un client n'existera que
dans HubSpot — c'est impossible, Wix a besoin du nom pour émettre une facture. Elle dit
qu'**un seul outil fait autorité par donnée** :

| Donnée | Qui fait autorité | Les autres |
|---|---|---|
| La **personne** — coordonnées, historique, qualification | **HubSpot** | lisent, ne décident pas |
| La **commande** — panier, paiement, facture | **Wix** | HubSpot reçoit le résultat |
| Le **résultat d'évaluation** | **Evalangdo** | HubSpot reçoit le résultat |

Quand deux outils prétendent tous les deux dire la vérité sur la même personne, ce n'est pas un
outil qui gagne : c'est la donnée qui se dédouble, puis diverge, puis n'est plus crue par
personne. C'est déjà arrivé ici — 167 libellés Wix pour 4 catégories réelles.

---

## Ce que ce cadre change dans la mission

### 1. Il confirme la phase 1, et lui donne sa vraie raison

Faire quitter Wix aux formulaires n'était jusqu'ici justifié que par la qualification à la source.
Le cadre de Franck ajoute l'argument de fond : **Wix ne doit plus être un endroit où des contacts
s'accumulent.** Les 137 collections CMS deviennent des archives, pas des bases vivantes.

**Conséquence sur l'étape 21 :** vider et repointer les anciens formulaires n'est plus une
tâche de ménage, c'est l'application de la règle. Un formulaire Wix qui continue d'écrire dans
une collection CMS crée une seconde source de vérité.

### 2. « Une personne, une fiche » devient une étape, pas une intention

L'état au 6 août n'est pas conforme :

- **Deux doublons connus et documentés** — `evodie_p@yahoo.com` et `magzum@yahoo.fr` vivent
  chacun sur deux fiches. Repérés le 5 août, jamais fusionnés.
- **Le mécanisme qui les produit est toujours actif.** HubSpot remappe `E-mail 1` → `E-mail 3` à
  chaque import sans identifiant unique. Tel quel, 419 lignes créent 419 doublons — vérifié deux
  fois en juillet et en août.

**Règle opposable, à partir d'aujourd'hui :** aucun import CSV dans HubSpot sans avoir vérifié le
mapping des colonnes d'e-mail, écran par écran. C'est la première cause de doublons du dossier,
loin devant la saisie humaine.

### 3. Le paiement reste dans Wix — mais le cycle de vie est dans HubSpot

Le cycle de vie validé par Franck comporte l'étape **« Frais réglés »** *(3ᵉ des 7)*. Le paiement,
lui, se fait dans Wix.

**Rien ne fait aujourd'hui remonter l'un vers l'autre.** Tant que ce chaînon manque, l'étape
« Frais réglés » se renseigne à la main — et une étape de cycle de vie tenue à la main est une
étape qui se désynchronise en quelques semaines. Toute la mesure de la phase 5 repose dessus :
sans elle, « combien de pré-inscrits n'ont pas payé » redevient une question à laquelle on répond
en ouvrant un fichier.

**C'est une question ouverte, pas une décision.** Elle se traite en phase 2, une fois le cycle de
vie créé.

### 4. Evalangdo est un angle mort complet

**Cet outil n'apparaît dans aucun document antérieur de la mission.** Aucun accès, aucun export,
aucune idée du volume. On ne sait pas :

- qui l'administre aujourd'hui ;
- quelles données il produit, et sous quelle forme ;
- s'il expose une API, un export, ou rien ;
- **sur quel identifiant commun** on rapprocherait un résultat d'évaluation d'une fiche HubSpot —
  l'e-mail, probablement, mais ce n'est pas vérifié.

Tant que ces quatre points sont inconnus, « HubSpot contient l'historique de toutes les
interactions » reste une intention. **L'inventaire d'abord ; l'intégration ne se conçoit pas
avant.**

---

## Ce que ce cadre ne tranche pas

- **Comment** les trois outils se parlent. La décision antérieure tient : *aucune application
  tierce de synchronisation Wix ↔ HubSpot ne transporte la qualification* — c'est pour ça que les
  formulaires sont refaits plutôt que synchronisés.
- **Le sens des flux.** « HubSpot reçoit le résultat » ne dit pas si Wix pousse ou si HubSpot
  tire. À instruire avec les capacités réelles de chaque outil, pas sur le papier.
- **Le périmètre d'Evalangdo dans la mission.** Il peut très bien rester hors périmètre et
  n'être qu'un point de vigilance. C'est un arbitrage de Franck, une fois l'inventaire fait.

---

## Le risque que ce cadre crée

Une architecture propre sur le papier **ajoute du travail à celui qui la tient**. Trois outils qui
se renvoient des données, ce sont trois endroits où quelque chose peut se désynchroniser — et
c'est **Stéphane** qui les tiendra, pas Franck *(voir [checklist](00-checklist.md), amendement de
l'étape 8)*.

La règle « un rôle par outil » est juste. Elle ne devient vraie que si chaque passage d'un outil à
l'autre est automatique. **Chaque chaînon laissé manuel est une promesse d'incohérence à trois
mois**, et personne ne verra le moment où elle s'installe.

---

## L'automatisation ne passera pas par HubSpot — décision du 2 septembre

**Constat : les workflows HubSpot sont hors budget.** Vérifié dans le portail le 2 septembre.

| | |
|---|---|
| Abonnement réel | **Starter Customer Platform**, `20 €/mois` remisé 50 % → **10 €/mois payés** |
| Comprend | Marketing Hub · Sales Hub · Service Hub · Content Hub · Data Hub, tous en **Starter** — 1 000 contacts marketing inclus, 3 utilisés |
| **Workflows** | **verrouillés** — `/workflows/` redirige vers la page de vente. C'est une fonction **Pro** |
| Coût de Pro | **1 283 €/mois** *(remisé, sinon 1 430 €)*, plus onboarding obligatoire |

**Deux ordres de grandeur d'écart avec ce que paie ALTAV aujourd'hui.** Franck n'a pas ce budget,
et le proposer serait disproportionné pour une mission dont le premier formulaire vient d'entrer
en service.

### La décision

**Make.com devient la couche d'automatisation.** Offre gratuite : 1 000 opérations par mois.

Pour situer le volume : le formulaire de pré-inscription, le plus actif du site, fait
**141 soumissions par an**. L'enveloppe gratuite n'est pas une contrainte, elle est
surdimensionnée.

**Ce que ça ne change pas :** HubSpot reste la **source unique de vérité** sur la personne. Make
ne stocke rien, ne qualifie rien, ne décide rien. Il déclenche des actions à partir de ce que
HubSpot contient déjà. La règle du 6 août tient — Make est un exécutant, pas un troisième outil
qui prétendrait connaître le client.

### La conséquence technique à connaître

**HubSpot ne peut pas prévenir Make.** Les webhooks sortants sont eux-mêmes une action de
workflow, donc verrouillés. Make devra donc **interroger** HubSpot à intervalle régulier plutôt
qu'être notifié.

Conséquence pratique : une réponse « automatique » arrivera avec le délai du cycle
d'interrogation — quelques minutes, pas l'instant. Sans importance pour un accusé de réception ;
à savoir avant de promettre un délai à qui que ce soit.

### Ce que ça débloque, et dans quel ordre

| Besoin | État |
|---|---|
| Réponse automatique au visiteur qui soumet | premier chantier Make |
| Création de tâche à chaque soumission *(étape 16 bis, abandonnée faute de workflows)* | redevient possible |
| Séquences de nurturing *(phase 3)* | à réévaluer — Make peut orchestrer, HubSpot Starter sait envoyer |

> **Le garde-fou.** Chaque scénario Make est une pièce de plus à transmettre à Stéphane
> *(phase 6)*. Un scénario qu'on ne sait pas expliquer en trois phrases est un scénario qui ne
> survivra pas à la passation. Documenter au fur et à mesure, ici.
