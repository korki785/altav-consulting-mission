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

### Incident 1 — doublon d'automatisation : **diagnostiqué le 5 août, fausse alerte**

Diagnostic mené dans le back-office Wix, en lecture seule. **Aucun prospect ne reçoit deux
mails de confirmation.** Le doublon est impossible par construction — et la raison est plus
instructive que l'alerte elle-même.

Les deux automatisations portent le même nom mais **écoutent deux applis de formulaires
différentes** :

| Automatisation | Créée le | Déclencheur | Appli source | Déclenchements | Dernier |
|---|---|---|---|---|---|
| `pré-inscription formation ubuntu` | 22 juin 2026 | `Form submitted` | **Wix Formulaires** *(nouvelle appli)* | 1 | **jamais** |
| `pré-inscription formation ubuntu` | 19 sept. 2023 | `Un formulaire est envoyé` | **Old Wix Forms** *(appli dépréciée)* | 527 | 1er août 2026 |

Un formulaire appartient à une seule des deux applis. **Une même soumission ne peut donc pas
déclencher les deux automatisations.** Le doublon supposé n'a jamais pu se produire.

Ce que le journal d'exécution montre à la place :

- L'automatisation de 2026 **n'a jamais rien envoyé**. Toutes ses exécutions sont `Ignoré`, motif :
  « les données ne correspondent pas aux critères définis dans le déclencheur ».
- Ce qui la déclenche, ce ne sont pas des pré-inscriptions : les 4 exécutions du 4 août
  (12:50, 17:16, 19:47, 19:59) correspondent exactement à 4 envois du formulaire
  **`Préparation Module 8`** — un questionnaire de préparation destiné aux participants en
  cours de formation. `Ignoré` est ici le comportement correct.
- L'automatisation de 2023 tourne encore : 2 exécutions `Terminé` sur les 30 derniers jours
  (7 juillet, 1er août), le reste `Ignoré`.

**Rien à désactiver.** L'accord de Franck n'est plus nécessaire sur ce point.

### Ce que le diagnostic a révélé à la place — plus grave que le doublon

- **Le formulaire de pré-inscription principal est mort.** `Pré-inscription à la formation UBUNTU`
  compte 86 envois, dont **le dernier date du 20 février 2025**. Les trois autres (43, 3, 0)
  ne reçoivent rien non plus. Le canal d'acquisition supposé n'acquiert plus depuis 18 mois.
- **Question ouverte, à poser à Franck :** par où sont donc passés les **136 pré-inscrits de la
  promo 8** ? Ce n'est aucun des quatre formulaires de pré-inscription. Tant qu'on ne sait pas
  par où entre réellement un pré-inscrit aujourd'hui, on ne peut pas rediriger ce canal vers
  HubSpot.
- **Erreur active sur l'automatisation de 2023 :** « Some of the forms are missing ». Sa liste de
  formulaires cibles référence des formulaires supprimés depuis.
- **`Old Wix Forms` est une appli dépréciée** — Wix affiche « L'ancienne version de notre appli
  n'est plus disponible » pour les 17 anciens formulaires. L'automatisation qui tourne encore
  repose dessus.

Le décompte du 3 août est confirmé : **69 formulaires sur 95 autorisés, 52 actifs.**
`Inscription - DRH` (15 envois) et `Inscription - ADG` (8) sont bien là — les 23 futurs
`ENTREPRISE`.

### Incident 2 — messages non lus : **inventaire fait le 5 août**

**60 conversations** dans la boîte de réception Wix, la plus ancienne du 18 mai, la plus récente
du 4 août. **43 relèvent de l'acquisition commerciale**, dont 50 messages non lus au total.

> **Ce que « non lu » veut dire, et ce qu'il ne veut pas dire.** Le constat vérifiable est :
> *non lu dans la boîte Wix*. Il ne prouve pas qu'aucune réponse n'a été apportée — Franck a pu
> répondre depuis sa messagerie, par WhatsApp ou par téléphone, sans que la boîte Wix en garde
> trace. Un fil de 12 messages montre d'ailleurs qu'Altav répond parfois **dans** cette boîte.
> Le sort réel de ces demandes est **inconnu**. Nous n'avons aucun accès à la messagerie de
> Franck ; seul le back-office Wix a été consulté.

| Catégorie | Conv. | Quoi |
|---|---|---|
| **Pré-inscription Formation Ubuntu** | **20** | des gens qui demandent à entrer en formation |
| Formulaire d'inscription personnalisé | 13 | à identifier — quel formulaire, quelle intention |
| Contact général (`Contact 2`) | 4 | demandes entrantes du site |
| Brochure Executive Coaching | 2 | demande de document |
| **Livre blanc** | **2** | demande de document |
| Session d'info / inscription coaching | 2 | inscriptions à un événement |
| — *sous-total leads commerciaux* | **43** | |
| Participants en cours (`supervision ubuntu`) | 9 | hors acquisition |
| Feedback séance de coaching | 3 | hors acquisition |
| Démarchage entrant | 2 | à ignorer |
| Fil en cours / à qualifier / test interne | 3 | |

**Les 20 pré-inscriptions s'étalent du 20 mai au 1er août 2026.** Toutes non lues dans Wix ;
suite donnée inconnue.

Détail nominatif : `donnees/revue/messages_wix_a_traiter.csv` — **non versionné**, il contient
des données personnelles. Une ligne par conversation : date, nom, formulaire d'origine, nombre
de messages, catégorie, action.

> **Méthode :** la liste a été établie sans ouvrir aucune conversation. Ouvrir un fil le marque
> comme lu et détruit la seule information dont on dispose. Les 50 non-lus sont intacts.

### Ce que cet inventaire répond — la question ouverte de l'incident 1

**Voilà par où arrivent les pré-inscriptions.** Elles n'entrent pas par les quatre formulaires
`Pré-inscription à la formation UBUNTU` de l'appli Wix Formulaires — ceux-là sont morts depuis
février 2025. Elles arrivent par un formulaire de l'**ancienne appli**, dont les réponses
tombent directement dans la **boîte de réception**, que personne ne relève.

Ce n'est donc pas un problème d'acquisition. **L'acquisition fonctionne.** Le canal amène des
pré-inscrits toutes les deux semaines environ. Ce qui manque, c'est quelqu'un au bout — et c'est
exactement le diagnostic de la mission : le goulot est la conversion, pas la demande.

Corollaire pour la bascule : c'est **ce formulaire-là** qu'il faut repointer vers HubSpot en
priorité, pas les quatre formulaires morts.

### Les deux formulaires inconnus — identifiés le 5 août

#### 1. Le canal réel de pré-inscription : `Pré-inscription Formation Ubuntu` *(ancienne appli)*

Créé le **28 décembre 2022**, dernière soumission le **1er août 2026**. Il n'apparaît pas dans
les 52 formulaires de l'appli Wix Formulaires : il vit dans les **17 anciens formulaires**, et
ses réponses sont stockées dans une **collection CMS** (`contact11`).

**525 enregistrements**, avec pour chacun : date et heure d'envoi, prénom, nom, **e-mail**,
**téléphone**, « comment connaissez-vous Altav », « qu'est-ce qui vous intéresse »,
« ce qui motive votre engagement ».

> **Conséquence directe : l'Excel des pré-inscrits ne sert plus à rien.** Il était réclamé
> depuis le début de la mission pour migrer « les ~489 pré-inscrits » introuvables dans Wix.
> Ils sont dans Wix — dans le CMS, pas dans l'appli Formulaires. 525 lignes, exportables,
> avec les coordonnées. C'est la source à migrer vers HubSpot.

#### 2. « Formulaire d'inscription personnalisé » : c'est le formulaire du pied de page

13 conversations en boîte de réception portent ce nom. Il n'existe **ni dans les 52 formulaires,
ni dans les 17 anciens, ni parmi les 137 collections CMS** — parce que ce n'est pas un formulaire
d'appli : c'est un **élément natif de l'éditeur Wix**, posé dans le pied de page du site.

Vérifié sur `altavconsulting.com`, ses champs sont :

| Champ | Type |
|---|---|
| Nom · E-mail · Téléphone | texte |
| **Statut** | liste : Entrepreneur (Chef d'entreprise) · En cours de création d'entreprise · En questionnement · Profession libérale · Autre |
| Parlez-nous de votre projet… | texte long |

> **Relevé exact du 6 août, dans le DOM de `www.altavconsulting.com`.** Le relevé du 5 août était
> fait à l'œil ; celui-ci lit la structure. Trois écarts, tous mineurs mais tous à reproduire :
>
> 1. **`Entrepreneur (Chef d'entreprise)`** prend une **majuscule à Chef**. Le relevé du 5 août
>    l'écrivait en minuscule, et la propriété HubSpot avait été créée d'après lui — corrigée le
>    6 août.
> 2. **Le formulaire n'affiche aucun libellé.** `Nom`, `E-mail`, `Téléphone`,
>    `Parlez-nous de votre projet...` sont des **placeholders** à l'intérieur des champs, et
>    `Statut` est l'option vide en tête de la liste déroulante. Reproduire à l'identique impose
>    donc de masquer les libellés côté HubSpot — sinon la version refaite paraît plus lourde que
>    l'actuelle, et la condition n° 1 de Franck tombe.
> 3. Le bouton s'appelle **`Envoyer`**, et le message affiché après envoi est
>    **« Merci pour votre envoi ! »**. C'est le ton actuel du site, à reprendre comme base du
>    message de confirmation plutôt que d'en écrire un.
>
> **Relevé au passage, hors périmètre :** un **widget de chat « Contactez-nous »** est actif en
> bas à droite du site. Il alimente la boîte de réception Wix, pas HubSpot, et ne figure dans
> aucun des 6 formulaires spécifiés. Canal d'entrée non couvert — à signaler à Franck.

Cela confirme le constat du 3 août : ses demandes ne sont comptées nulle part et tombent
uniquement dans la boîte de réception. C'est le formulaire que Franck a accepté de refaire (Q9),
et le champ `Statut` est le futur champ caché du formulaire **Contact général**.

### Ce qu'il faut retenir du scan

- **137 collections de formulaires** existent dans le CMS, contre 69 formulaires comptés dans
  l'appli. Le désordre est plus large que ce que montre l'interface Formulaires.
- Les formulaires qui comptent vraiment ne sont **pas** ceux que l'interface met en avant.
  L'inventaire du 3 août, fait depuis l'appli Formulaires, ratait les deux principaux.
- Les deux canaux vivants sont donc : l'ancien formulaire de pré-inscription (525 réponses) et
  le formulaire du pied de page. Ce sont eux à repointer vers HubSpot **en premier**.

### Plan de traitement

*Aucune dépendance. Peut avancer en parallèle de la création des formulaires.*

| # | Action | Demande Franck ? |
|---|---|---|
| 1 | ~~Extraire et trier les messages de la boîte Wix~~ | **fait le 05/08** — 60 conversations, 43 leads |
| 2 | ~~Relancer les 20 pré-inscriptions~~ | **écarté le 05/08** — hors périmètre pour l'instant |
| 3 | ~~Envoyer le livre blanc et la brochure~~ | **écarté le 05/08** — aucune réponse envoyée à ce stade |
| 4 | Identifier ce qu'est le « Formulaire d'inscription personnalisé » (13 conversations) | non — lecture seule |
| 5 | ~~Préparer et envoyer les réponses aux 43 leads~~ | **écarté le 05/08** |
| 6 | Importer ces 43 contacts dans HubSpot avec le bon tag | non |

**Décision du 5 août : on ne répond à personne pour l'instant.** La priorité va à la mise en
place du formulaire relié à HubSpot. L'inventaire garde sa valeur — il identifie les canaux
vivants et alimente la base — mais aucune relance n'est engagée.

Franck écrit lui-même en Q8 qu'il n'existe « pas de processus clairement défini » pour ces
demandes. Brancher le formulaire sur HubSpot fait arriver la demande au bon endroit — encore
faut-il savoir **qui répond**. C'est tranché ci-dessous.

---

## Qui porte le CRM — tranché le 4 août 2026

C'était la condition bloquante posée depuis le début de la mission
*(voir [`01-mission.md`](01-mission.md))*. Elle est levée.

| Rôle | Titulaire |
|---|---|
| **Propriétaire du CRM** | **Franck** |
| **Réponse aux demandes entrantes** | **Franck**, seul |

Un CRM que personne ne tient redevient un Excel. Il a maintenant un nom.

**Le commercial n'existe pas.** Franck a évoqué l'intention d'en recruter un ; ce n'est pas
fait. Aucune décision ne doit reposer dessus. Concrètement : **un seul utilisateur HubSpot**,
Franck, destinataire par défaut de toutes les tâches créées par les formulaires. Pas de siège
supplémentaire à prévoir, pas de règle de répartition à écrire.

### La réserve, pour mémoire

Franck porte déjà la formation Ubuntu, soit 70 à 80 % du chiffre d'affaires. Y ajouter la
réponse à chaque demande entrante le met en position de goulot unique. Ce n'est pas un
argument contre la mise en place — c'est un paramètre de conception : **les automatisations
doivent réduire le nombre de gestes qu'il a à faire, pas lui créer des tâches supplémentaires
à traiter à la main.**

Si un commercial arrive un jour, le changement se fait en une minute : seul l'utilisateur
assigné change.

### Ce que ça débloque immédiatement

- **La destination des demandes entrantes.** Chaque formulaire notifie un destinataire réel.
  Sans destinataire, une automatisation ne fait que déplacer le silence. *(Notification par
  e-mail : les workflows, donc les tâches assignées, sont verrouillés sur l'abonnement actuel —
  vérifié le 05/08.)*
- **Les tableaux de bord commerciaux** demandés par Franck ont un référentiel.

### Ce qu'il reste à obtenir

- Rien sur ce point. Le sujet est clos : Franck, seul utilisateur, seul destinataire.
