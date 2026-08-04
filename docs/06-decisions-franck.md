# 6. Décisions validées par Franck — 4 août 2026

Réponses écrites aux 9 questions de
[`livrables/QUESTIONS_FORMULAIRES_FRANCK.html`](../livrables/QUESTIONS_FORMULAIRES_FRANCK.html),
envoyées le 3 août. **Les 9 sont tranchées, dont la seule bloquante (Q1).** Le chantier
acquisition est débloqué.

Ce document fait foi sur ce qui est validé. Là où la réponse de Franck diverge de ce qui était
proposé, c'est **sa version qui s'applique** — les autres documents ont été alignés dessus.

---

## Ce qui est acté

| # | Question | Décision |
|---|---|---|
| 1 | Plus aucun formulaire créé dans Wix ? | **Oui, sur le principe** — avec un partage explicite : HubSpot = acquisition commerciale, Wix = opérationnel et interne |
| 2 | Quels formulaires servent encore ? | 5 : pré-inscription Ubuntu, livre blanc, demande d'information, contact général, « je forme mes équipes ». Le reste est archivable |
| 3 | QR codes à ne pas casser ? | **Oui, plusieurs en circulation.** Brochures Ubuntu, supports de conférence, présentations commerciales, LinkedIn, WhatsApp, PDF. Redirection retenue, pas de suppression |
| 4 | Où sont diffusés les liens ? | LinkedIn, WhatsApp, QR codes, site, emailings, PowerPoint, brochures PDF, conférences |
| 5 | Un seul formulaire de pré-inscription ? | **Oui — et sans notion de promo dans le formulaire** (voir ci-dessous) |
| 6 | DRH / ADG = entreprise ? | **Oui.** Ces 23 contacts passent en `ENTREPRISE`. Critère retenu : **qui paie la facture** |
| 7 | Les 19 certifiés Promo 4 & 5 ? | **Oui, ce sont des clients.** Bascule en `CLIENT`, après vérification des cas particuliers |
| 8 | Qui traite le formulaire du pied de page ? | **Personne — aucun processus défini.** D'où les non-lus. Il doit arriver dans HubSpot et déclencher le workflow commercial |
| 9 | Refaire ce formulaire ? | **Oui**, à trois conditions : intégré au design du site, transparent pour le visiteur, alimente directement HubSpot |

**Règle de partage des outils, telle que formulée par Franck :**

> HubSpot = acquisition commerciale. Wix = formulaires opérationnels ou internes
> (feedbacks, évaluations, questionnaires d'événements, formulaires réservés aux clients
> déjà engagés).

---

## Q5 — correction de fond : la promo sort du formulaire

C'est le seul point où la réponse **corrige** la proposition, et la correction est juste.

| | Proposé le 3 août | Validé par Franck |
|---|---|---|
| Nombre de formulaires de pré-inscription | 1 | 1 |
| Notion de promo | champ caché `promo` sur le formulaire | **aucune** — le formulaire ne mentionne ni « Promo 8 » ni « Promo 9 » |
| Où vit la promo | dans le formulaire | **propriété interne du contact dans HubSpot** |
| Qui décide de la promo | implicitement le prospect | **ALTAV**, après règlement des frais |

> Le prospect exprime son souhait d'intégrer la formation. L'affectation à une promotion relève
> de l'organisation d'ALTAV, pas du choix du candidat.

**Conséquence concrète :** le formulaire de pré-inscription n'a **aucun champ caché**. La
propriété `promo` est renseignée dans HubSpot à l'étape 4 du cycle de vie ci-dessous, une fois
les frais encaissés. Un formulaire de moins à toucher à chaque promo, et la cohorte reste
pilotable côté CRM.

---

## Le cycle de vie, tel que défini par Franck

Sept étapes, dans l'ordre :

| # | Étape | Déclencheur du passage à l'étape suivante |
|---|---|---|
| 1 | Prospect | soumission d'un formulaire d'acquisition |
| 2 | Pré-inscrit | règlement des frais d'inscription |
| 3 | Frais d'inscription réglés | décision d'ALTAV |
| 4 | Affecté à une promotion | démarrage de la promo |
| 5 | Participant | obtention de la certification |
| 6 | Certifié | fin de la formation |
| 7 | Alumni Ubuntu | — |

### Articulation avec `Tag_CRM` — à valider

Deux axes coexistent désormais et il faut dire lequel fait foi, sinon la base aura deux vérités.

**Proposition :**

- `Tag_CRM` (`CLIENT` · `CHAUD` · `INBOUND` · `FROID`) reste l'axe **d'origine** : d'où vient le
  contact, ce qu'il valait au moment de l'import de juillet. Il ne bouge plus, sauf correction.
- Le **cycle de vie en 7 étapes** devient l'axe **opérationnel** : où en est la personne
  aujourd'hui. C'est lui qui pilote les séquences et les tableaux de bord.

Correspondance à l'entrée dans le cycle :

| `Tag_CRM` | Étape de départ dans le cycle |
|---|---|
| `FROID` · `INBOUND` | 1 — Prospect |
| `CHAUD` | 2 — Pré-inscrit |
| `CLIENT` | 3 minimum — Frais réglés *(l'étape exacte se tranche contact par contact)* |

Voir [`02-classification.md`](02-classification.md) pour la définition des quatre tags.

---

## Ce que ces réponses débloquent

### Immédiat, sans dépendance

- **Les 23 premiers `ENTREPRISE`.** `Inscription - DRH` (15) + `Inscription - ADG` (8) →
  `type_compte = ENTREPRISE`. C'est le **signal 1** de la grille de promotion : déterministe,
  donc automatisable sans revue. Jusqu'ici la base entière était en `INDIVIDUEL` faute de
  signal fiable.
- **Les 19 certifiés Promo 4 & 5** passent de `CHAUD` à `CLIENT`. Le dossier « fichier de
  Stéphane » se referme sans attendre de fichier supplémentaire.
- **Le formulaire du pied de page** est refait dans HubSpot et embarqué dans le site. C'est le
  seul formulaire vivant réellement posé sur le site — les 52 autres vivent sur des pages
  autonomes.

**Prérequis à ces deux premières actions :** exporter depuis Wix les réponses des trois
formulaires concernés, pour disposer des identités. Les 23 et les 19 ne sont pas identifiables
dans la base actuelle : le libellé ne porte pas cette information.

### Ce que Franck attend de chaque formulaire

> Mon objectif n'est pas d'avoir davantage de technologie mais davantage de ventes.

Quatre exigences, à traiter comme critères de recette :

1. qualifier le prospect automatiquement ;
2. déclencher les bonnes relances ;
3. alimenter les tableaux de bord commerciaux ;
4. mesurer les taux de conversion.

Corollaire à tenir : **approche simple et évolutive.** Un formulaire de plus, une propriété de
plus, une automatisation de plus se justifient par une vente, pas par une élégance de modèle.

---

## « Demande d'information » et « contact général » : deux formulaires, pas un

Tranché le 4 août : **ce sont deux formulaires distincts.** La cible passe donc à **6
formulaires**, pas 5.

| | Demande d'information | Contact général *(pied de page)* |
|---|---|---|
| Sujet | la formation | inconnu à l'arrivée |
| Intention | identifiable | à qualifier |
| `Tag_CRM` | `CHAUD` | `INBOUND` |
| Champ caché | — | `statut` |

La distinction ne coûte rien tant qu'elle est posée **à la source**. Fusionner les deux
obligerait à requalifier à la main, plus tard, avec moins d'information qu'au moment de la
soumission. « Session d'information / webinaire » est conservé : seul formulaire piloté par
date d'événement, il alimente réellement — `Session d'infos Ubuntu en ligne.csv` (103 contacts)
et `parcours-découverte-octobre.csv` (70).

---

## Les deux incidents : ce qu'on fait sans attendre Franck

Ni le doublon d'automatisation ni les 63 messages n'ont été adressés dans la réponse. Ils
étaient pourtant en tête de document, section « à regarder tout de suite ». Ce sont des leads
vivants, certains antérieurs au 20 juillet.

**Constat qui débloque : la réponse de Franck n'est nécessaire ni pour l'un ni pour l'autre.**
L'accès au back-office Wix est obtenu depuis le 3 août. Le diagnostic est faisable seul ; seule
l'action qui touche à de vrais envois demande son accord.

### Incident 1 — doublon d'automatisation

*Bloque le rebranchement du formulaire de pré-inscription. À traiter en premier.*

| # | Action | Demande Franck ? |
|---|---|---|
| 1 | Ouvrir les deux automatisations `pré-inscription formation ubuntu`, comparer le formulaire ciblé et l'action déclenchée | non — lecture seule |
| 2 | Confirmer sur un pré-inscrit récent qu'il a bien reçu deux mails | non — lecture seule |
| 3 | Lister ce que contiennent les « Modifications non publiées » des 4 automatisations concernées, dont 2 actives | non — lecture seule |
| 4 | **Désactiver** la plus ancienne (2023, déclencheur `Un formulaire est envoyé`) | **oui** — ça touche des envois réels |

Désactiver, jamais supprimer : réversible d'un clic si le diagnostic était faux.

À noter : toutes les automatisations Wix d'acquisition s'éteignent de toute façon à la bascule
vers HubSpot. Mais si le double mail part aujourd'hui, il n'y a aucune raison d'attendre — c'est
un prospect qui reçoit deux fois le même message d'Altav.

### Incident 2 — 63 messages non traités

*Aucune dépendance. Peut avancer en parallèle de la création des formulaires.*

| # | Action | Demande Franck ? |
|---|---|---|
| 1 | Extraire les 13 réponses de formulaire non lues et les 50 messages de la boîte Wix : date, nom, email, demande | non |
| 2 | Trier : demande commerciale vivante · spam · déjà traité ailleurs | non |
| 3 | **Envoyer le livre blanc** à la personne qui l'a demandé | non — c'est un PDF, pas une décision |
| 4 | Préparer les réponses aux demandes commerciales, en lot | non |
| 5 | Valider et envoyer ces réponses | **oui** |
| 6 | Importer ces contacts dans HubSpot avec le bon tag | non |

**La question de fond reste entière.** Franck écrit lui-même en Q8 qu'il n'existe « pas de
processus clairement défini » pour ces demandes. Brancher le formulaire sur HubSpot fait
arriver la demande au bon endroit — ça ne dit toujours pas **qui répond**. C'est la même
question que « qui porte le CRM en interne », restée sans réponse depuis le début de la mission.
Un workflow qui crée une tâche sans destinataire ne fait que déplacer le silence.
