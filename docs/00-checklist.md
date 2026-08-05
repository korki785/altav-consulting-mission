# 0. Checklist — l'ordre des choses

État au **5 août 2026**. Une seule liste, dans l'ordre logique : chaque étape suppose la
précédente. On lit de haut en bas, on s'arrête à la première pastille rouge.

🟢 fait · 🟠 en cours · 🔴 à faire

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
| 🟢 | **8.** Désigner le propriétaire du CRM — **Franck, seul** | 04/08/2026 |

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
| 🟠 | **16.** Spécifier les 6 formulaires — champ par champ, valeurs écrites, tâche déclenchée | — |
| 🔴 | **17.** Faire valider la spec par Franck | **Franck** |
| 🔴 | **18.** Créer le formulaire de **pré-inscription** — sans champ promo | étape 17 |
| 🔴 | **19.** Refaire le formulaire du **pied de page** — champ `Statut` conservé | étape 17 |
| 🔴 | **20.** Créer les 4 formulaires restants | étape 18 |
| 🔴 | **21.** Vider et repointer les anciens liens — QR codes et WhatsApp préservés | étape 20 |
| 🔴 | **22.** Tester : une soumission arrive dans HubSpot **déjà étiquetée** | étape 21 |

**Fin de phase :** une soumission de test crée un contact classé et une tâche pour Franck, sans
intervention humaine.

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
| 🔴 | **31.** Mesurer un mois de volume réel de leads entrants | phase 1 |
| 🔴 | **32.** **Arbitrer le palier HubSpot** — Starter ou Professional | étape 31 · **Franck** |
| 🔴 | **33.** Réécrire le mail de confirmation *(l'actuel est trop brut)* | phase 1 |
| 🔴 | **34.** Rappel téléphonique sous 5 min après pré-inscription | étape 32 |
| 🔴 | **35.** Livre blanc à J+5 | étape 32 |
| 🔴 | **36.** Relance des non-confirmés à J+30 | étape 32 |
| 🔴 | **37.** Bascule automatique sur la promo suivante en fin de promo | étape 32 |

> ⚠️ **Les étapes 34 à 37 demandent les workflows, donc le palier Professional.** L'abonnement
> actuel est Starter. C'est l'étape 32 qui débloque — et elle se décide sur les chiffres de
> l'étape 31, pas avant.

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

**Fin de phase — et fin de mission :** Franck ouvre un écran et voit son taux de conversion sans
demander à personne.

---

## Écarté en route

| Étape abandonnée | Pourquoi |
|---|---|
| Répondre aux 43 leads de la boîte Wix | hors périmètre — décision du 05/08 |
| Désactiver l'automatisation Wix de 2023 | sans objet — le doublon était une fausse alerte |
| Attendre l'Excel des pré-inscrits | sans objet — les 525 étaient dans le CMS Wix |
| Attendre le fichier des certifiés de Stéphane | sans objet — Franck confirme les 19 réponses Wix |
| Assigner les tâches à un commercial | sans objet — pas de commercial, Franck seul |
| Synchroniser Wix ↔ HubSpot par appli tierce | aucune ne transporte la qualification |

---

## Points de vigilance permanents

- **« Non lu » n'est pas « sans réponse ».** Aucun accès à la messagerie de Franck.
- **HubSpot remappe mal à chaque import** : `E-mail 1` → `E-mail 3` sans identifiant unique.
  Tel quel, 419 lignes créent 419 doublons. À recorriger systématiquement.
- **L'écran « Problèmes de formatage » est global** — 635 fiches. *Tout accepter* les modifie
  toutes.
- **Franck est seul.** Chaque automatisation doit lui retirer un geste, pas lui en créer un.
- **Le désordre se reconstitue tout seul** si créer un formulaire dans HubSpot devient plus
  pénible que dans Wix.
