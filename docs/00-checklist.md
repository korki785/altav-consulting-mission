# 0. Checklist — l'ordre des choses

État au **6 août 2026**. Une seule liste, dans l'ordre logique : chaque étape suppose la
précédente. On lit de haut en bas, on s'arrête à la première pastille rouge.

🟢 fait · 🟠 en cours · 🔴 à faire

> **Les numéros ne changent jamais.** Ils servent de référence aux autres documents. Quand
> l'ordre change, ce sont les lignes qui bougent, pas les numéros — d'où les sauts.

---

## Phase 0 — Le socle 🟢

| | Étape | Quand |
|---|---|---|
| 🟢 | **1.** Nettoyer l'export Wix — 8 915 → **7 483 contacts**, 531 fusions, 889 e-mails morts | 07/2026 |
| 🟢 | **2.** Enrichir les noms — 33 % → **48 % de contacts nommés** | 07/2026 |
| 🟢 | **3.** Classer la base en 4 axes — `Tag_CRM`, `type_compte`, `Email_actif`, `Origine_nom` | 07/2026 |
| 🟢 | **4.** Importer dans HubSpot — 7 478 contacts | 20/07/2026 |
| 🟢 | **5.** Obtenir l'accès au back-office Wix | 03/08/2026 |
| 🟢 | **6.** Faire l'état des lieux des formulaires — 69 dont 52 actifs | 03/08/2026 |
| 🟢 | **7.** Faire trancher les 9 questions par Franck — dont la seule bloquante | 04/08/2026 |
| 🟢 | **8.** Désigner le propriétaire du CRM — **Franck** *(amendé le 06/08, voir ci-dessous)* | 04/08/2026 |

> **Amendement du 6 août — qui tient le CRM au quotidien.** Franck : *« il faudra que Stéphane
> sache l'administrer, ce n'est pas moi qui vais gérer une fois en exploitation »*.
> **Franck reste propriétaire et décideur ; Stéphane devient l'administrateur en exploitation.**
> Ce n'est pas un détail d'organisation : tout ce qui est construit doit désormais être
> administrable par quelqu'un qui n'était pas dans la construction. D'où la [phase 6](#phase-6--la-passation--que-stéphane-tienne-loutil-sans-nous).

## Phase 0 bis — Remettre la base d'aplomb 🟢

| | Étape | Quand |
|---|---|---|
| 🟢 | **9.** Diagnostiquer le doublon d'automatisation — **fausse alerte** | 05/08/2026 |
| 🟢 | **10.** Inventorier la boîte de réception — 60 conversations, 43 d'acquisition | 05/08/2026 |
| 🟢 | **11.** Identifier les deux canaux réellement vivants | 05/08/2026 |
| 🟢 | **12.** Exporter les 525 pré-inscriptions du CMS Wix | 05/08/2026 |
| 🟢 | **13.** Requalifier les 68 pré-inscrits mal classés — **CHAUD 318 → 386** | 05/08/2026 |
| 🟢 | **14.** Créer la propriété `Date de pré-inscription` dans HubSpot | 05/08/2026 |
| 🟢 | **15.** Répercuter dans HubSpot — **417 fiches, 0 doublon créé** | 05/08/2026 |

---

## Phase 1 — Acquisition : que le lead naisse déjà classé

*Rien de ce qui suit ne fonctionne sans cette phase.*

| | Étape | Dépend de |
|---|---|---|
| 🟢 | **16.** Spécifier les 6 formulaires — [spec complète](08-formulaires-hubspot.md) | 05/08/2026 |
| 🟢 | **16 bis.** Vérifier si la création de tâche demande un workflow — **oui, workflows verrouillés, alerte par e-mail à la place** | 05/08/2026 |
| 🟠 | **17.** Informer Franck du changement et obtenir **les supports en circulation** — quel QR code sur quelle brochure, quel lien dans quel groupe | **Franck** |
| 🔴 | **17 bis.** Faire relire par Franck les messages de confirmation et le mail réécrit | **Franck** |
| 🔴 | **17 ter.** Faire confirmer le formulaire « Session d'information », qu'il n'a pas demandé | **Franck** |
| 🔴 | **18 ante.** Créer les **8 propriétés** manquantes dans HubSpot — [liste](08-formulaires-hubspot.md#propriétés-hubspot-à-créer). *Le pilote n'en demande qu'une : `Statut du visiteur`* | — *(rien ne se mappe sans elles)* |
| 🔴 | **19.** **Pilote —** refaire le formulaire du **pied de page**, champ `Statut` conservé | étape 18 ante · *(déjà validé en Q9)* |
| 🔴 | **19 bis.** Recetter le pilote sur les **3 critères de Franck** — intégré au design, transparent pour le visiteur, alimente HubSpot | étape 19 · **Franck** |
| 🔴 | **18 bis.** Inventorier **ce que Stéphane a déjà mis en place** sur la pré-inscription | **Stéphane** |
| 🔴 | **18.** Créer le formulaire de **pré-inscription** — sans champ promo, **avec Stéphane** | étape 19 bis · étape 18 bis · **Stéphane** |
| 🔴 | **20.** Créer les 4 formulaires restants | étape 18 · *session d'info : étape 17 ter* |
| 🔴 | **21.** Vider et repointer les anciens liens — QR codes et WhatsApp préservés | étape 20 · **étape 17** |
| 🔴 | **22.** Tester : une soumission arrive dans HubSpot **déjà étiquetée** | étape 21 |
| 🔴 | **22 bis.** Activer les notifications par e-mail sur les 6 formulaires — **destinataires à trancher : Franck, Stéphane, ou les deux** | étape 20 · **Franck** |
| 🔴 | **22 ter.** Créer les 3 vues manuelles de relance — [provisoire](09-solution-provisoire.md) | étape 22 |

> **Décision du 6 août — on commence par le pied de page, pas par la pré-inscription.**
> Franck : *« Faisons d'abord un test par celui du bas de page comme test. »*
>
> L'ordre s'inverse pour deux raisons, et la seconde est la vraie :
>
> 1. Le formulaire de pied de page est le **plus petit** — 5 champs, 2 champs cachés. Il éprouve
>    toute la plomberie (mapping, classement à la source, notification, intégration au design du
>    site) sur l'objet le moins risqué.
> 2. Le formulaire de pré-inscription **n'est plus un terrain vierge.** Franck : *« il y a
>    plusieurs choses qui ont été mises en place, il faudra sûrement les améliorer »*. On ne sait
>    pas encore quoi. Le reconstruire avant d'avoir inventorié ce qui existe, c'est écraser du
>    travail de Stéphane — sur le seul formulaire qui produit du chiffre *(141 soumissions en
>    2026)*.
>
> **Le pilote sert à ça :** prouver la méthode sur un formulaire sans enjeu, pour arriver devant
> Stéphane avec une démonstration plutôt qu'une proposition.

**Fin de phase :** une soumission de test crée un contact classé et envoie une notification,
sans intervention humaine. *(Pas de tâche : les workflows sont verrouillés.)*

---

## Phase 2 — Le cycle de vie : savoir où en est chacun

| | Étape | Dépend de |
|---|---|---|
| 🔴 | **23.** Créer les 7 étapes du cycle de vie défini par Franck | phase 1 |
| 🔴 | **24.** Créer la propriété interne `promo` — renseignée après encaissement | étape 23 |
| 🔴 | **25.** Dédoubler le pipeline de transaction B2B / B2C | étape 23 |
| 🔴 | **26.** Obtenir l'export Wix `Inscription - DRH`, `- ADG`, `Certification 4 & 5` | **Franck** |
| 🔴 | **27.** Basculer les 23 contacts en `ENTREPRISE` et les 19 en `CLIENT` | étape 26 |
| 🔴 | **28.** Créer les 5 pré-inscrits absents de la base | — |
| 🔴 | **29.** Exploiter le signal B2B des 437 — société, poste, secteur | étape 27 |
| 🔴 | **30.** Remplir `Wix — Libellés d'origine`, propriété créée mais vide | — |

**Fin de phase :** on répond sans ouvrir un fichier à « combien de pré-inscrits n'ont pas encore
payé, et depuis combien de temps ».

---

## Phase 3 — Les séquences : le premier gain rentable

| | Étape | Dépend de |
|---|---|---|
| 🔴 | **31.** **Lancer l'essai de 14 jours** — une fois le mapping vérifié, pas avant | étape 22 |
| 🔴 | **31 bis.** Configurer et éprouver les séquences pendant l'essai | étape 31 |
| 🔴 | **32.** **Arbitrer le palier HubSpot** — sur les chiffres de l'essai | étape 31 bis · **Franck** |
| 🔴 | **33.** Réécrire le mail de confirmation *(l'actuel est trop brut)* | phase 1 |
| 🔴 | **34.** Rappel téléphonique sous 5 min après pré-inscription | étape 32 |
| 🔴 | **35.** Livre blanc à J+5 | étape 32 |
| 🔴 | **36.** Relance des non-confirmés à J+30 | étape 32 |
| 🔴 | **37.** Bascule automatique sur la promo suivante en fin de promo | étape 32 |

> ⚠️ **Les étapes 34 à 37 demandent les workflows — vérifié le 05/08 : ils sont verrouillés.**
> HubSpot renvoie vers **Sales Hub Pro**. Un **essai de 14 jours** est proposé, sans frais ni
> renouvellement automatique : de quoi mesurer avant d'acheter. C'est l'étape 32 qui tranche, et
> elle se décide sur les chiffres de l'étape 31, pas avant.

**Fin de phase :** un pré-inscrit qui ne paie pas reçoit trois relances sans que personne n'y
pense.

---

## Phase 4 — Le chiffre déjà acquis

| | Étape | Dépend de |
|---|---|---|
| 🔴 | **38.** Automatiser les relances de facturation — échéances en 11 fois | phase 2 |
| 🔴 | **39.** Chiffrer le coût de la réactivation des 6 196 dormants | — |
| 🔴 | **40.** Décider de lancer ou non la réactivation | étape 39 · **Franck** |
| 🔴 | **41.** Segmenter et séquencer les dormants | étape 40 |

> ⚠️ **L'étape 39 vient avant l'étape 41, pas après.** HubSpot facture les contacts *marketing*,
> pas les contacts stockés : basculer 6 196 dormants peut coûter plus que l'abonnement.

**Fin de phase :** les relances de paiement partent seules, et le salarié qui y passe 80 % de
son temps fait autre chose.

---

## Phase 5 — La mesure

| | Étape | Dépend de |
|---|---|---|
| 🔴 | **42.** Tableau de bord — entrées par canal, conversion par étape, délai moyen | phase 2 |
| 🔴 | **43.** Recalcul automatique du ratio de la promo 8 à chaque promo | étape 42 |
| 🔴 | **44.** Capter le pays à la source dans les nouveaux formulaires | phase 1 |
| 🔴 | **45.** Arbitrer l'enrichissement géographique de l'existant *(payant)* | étape 44 · **Franck** |

> `Pays` n'est renseigné que sur **8 %** de la base. L'objectif 80/20 se pilote **par zone** :
> sans pays fiable, il n'est pas mesurable.

**Fin de phase :** Franck ouvre un écran et voit son taux de conversion sans demander à personne.

---

## Phase 6 — La passation : que Stéphane tienne l'outil sans nous

*Ouverte le 6 août par la phrase de Franck : « ce n'est pas moi qui vais gérer une fois en
exploitation ». Un CRM que l'administrateur n'ose pas modifier redevient un Excel en six mois.*

| | Étape | Dépend de |
|---|---|---|
| 🔴 | **46.** Cadrer avec Stéphane **ce qu'il administre** — formulaires, propriétés, vues, ou tout | **Stéphane** · **Franck** |
| 🔴 | **47.** Lui ouvrir un accès HubSpot avec les droits correspondants | étape 46 |
| 🔴 | **48.** Écrire le **mode d'emploi d'administration** — créer un formulaire, poser un champ caché, modifier une vue | phase 1 · étape 46 |
| 🔴 | **49.** **Passation à blanc** — Stéphane crée seul un formulaire de bout en bout, je regarde sans toucher | étape 48 |
| 🔴 | **50.** Reprendre le mode d'emploi sur ce qui l'a bloqué à l'étape 49 | étape 49 |

**Fin de phase — et fin de mission :** Stéphane crée et modifie un formulaire sans nous appeler,
et un lead entré par ce formulaire arrive classé.

> **Le critère est celui de l'étape 49, pas celui de l'étape 48.** Un mode d'emploi que personne
> n'a exécuté ne prouve rien. La mission n'est pas finie quand la documentation est écrite, elle
> est finie quand Stéphane s'en est servi.

---

## Écarté en route

| Étape abandonnée | Pourquoi |
|---|---|
| Répondre aux 43 leads de la boîte Wix | hors périmètre — décision du 05/08 |
| Désactiver l'automatisation Wix de 2023 | sans objet — le doublon était une fausse alerte |
| Attendre l'Excel des pré-inscrits | sans objet — les 525 étaient dans le CMS Wix |
| Attendre le fichier des certifiés de Stéphane | sans objet — Franck confirme les 19 réponses Wix |
| Assigner les tâches à un commercial | sans objet — pas de commercial |
| Construire la pré-inscription en premier | inversé le 06/08 — le pied de page sert de pilote |
| Synchroniser Wix ↔ HubSpot par appli tierce | aucune ne transporte la qualification |

---

## Points de vigilance permanents

- **« Non lu » n'est pas « sans réponse ».** Aucun accès à la messagerie de Franck.
- **HubSpot remappe mal à chaque import** : `E-mail 1` → `E-mail 3` sans identifiant unique.
  Tel quel, 419 lignes créent 419 doublons. À recorriger systématiquement.
- **L'écran « Problèmes de formatage » est global** — 635 fiches. *Tout accepter* les modifie
  toutes.
- **Franck décide, Stéphane administrera.** Chaque automatisation doit retirer un geste à
  Franck ; chaque réglage doit rester compréhensible par quelqu'un qui n'était pas là quand on
  l'a posé. Les deux contraintes ne tirent pas dans le même sens — l'astuce qui fait gagner un
  clic à Franck est souvent celle que Stéphane n'osera pas toucher.
- **La pré-inscription n'est pas un terrain vierge.** Des choses y ont déjà été mises en place,
  contenu inconnu au 6 août. Rien ne s'y écrase avant l'inventaire *(étape 18 bis)*.
- **Le désordre se reconstitue tout seul** si créer un formulaire dans HubSpot devient plus
  pénible que dans Wix.
