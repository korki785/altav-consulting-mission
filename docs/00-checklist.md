# 0. Checklist — où on en est

État au **5 août 2026**. Ce document porte l'avancement ; les autres portent le pourquoi.
Une ligne par action, datée, avec sa dépendance réelle.

**Dépendance** : `Nael` = faisable seul · `Franck` = attend le client · `Palier` = attend une
décision d'abonnement HubSpot.

---

## Fait

| Quand | Action | Détail |
|---|---|---|
| 07/2026 | Nettoyage de la base Wix | 8 915 → **7 483 contacts**, 531 fusions, 889 e-mails morts retirés — [journal](05-journal.md) |
| 07/2026 | Enrichissement des noms | 33 % → **48 % de contacts nommés** (règle + modèle, 4,76 $) |
| 07/2026 | Classification en 4 axes | `Tag_CRM`, `type_compte`, `Email_actif`, `Origine_nom` — [règles](02-classification.md) |
| 20/07/2026 | Import initial dans HubSpot | 7 478 contacts, propriétés custom créées par Franck |
| 03/08/2026 | Accès back-office Wix | obtenu |
| 03/08/2026 | État des lieux des formulaires | 69 formulaires, 52 actifs — [acquisition](04-acquisition.md) |
| 04/08/2026 | **Les 9 questions tranchées par Franck** | dont la seule bloquante — [décisions](06-decisions-franck.md) |
| 04/08/2026 | Propriétaire du CRM désigné | **Franck, seul.** Pas de commercial recruté |
| 04/08/2026 | Restructuration du dépôt | racine 36 fichiers → 5 entrées |
| 05/08/2026 | Diagnostic du doublon d'automatisation | **fausse alerte** — deux applis de formulaires distinctes, aucun double mail possible |
| 05/08/2026 | Inventaire de la boîte de réception Wix | 60 conversations, 43 relevant de l'acquisition |
| 05/08/2026 | Identification des deux canaux vivants | l'ancien formulaire de pré-inscription et le formulaire du pied de page |
| 05/08/2026 | Export des 525 pré-inscriptions | remplace l'Excel jamais fourni — la donnée était dans le CMS Wix |
| 05/08/2026 | Requalification des pré-inscrits | 68 passés en `CHAUD` — **vivier chaud 318 → 386** |
| 05/08/2026 | Propriété `Date de pré-inscription` | créée dans HubSpot |
| 05/08/2026 | Répercussion dans HubSpot | **417 fiches mises à jour, 0 doublon créé**, 2 erreurs de doublon préexistant |

---

## À faire

### Sans dépendance — je peux avancer

| Priorité | Action | Détail |
|---|---|---|
| **1** | **Spécifier les 6 formulaires HubSpot** | champ par champ, valeurs écrites, tâche déclenchée — à valider avant création |
| **1** | **Créer le formulaire de pré-inscription** | sans champ promo *(décision de Franck)*. C'est le canal vivant |
| 2 | Refaire le formulaire du pied de page | champ `Statut` conservé comme champ caché |
| 2 | Mettre en place le cycle de vie en 7 étapes | + propriété interne `promo` |
| 3 | Créer les 5 pré-inscrits absents de la base | dont Floriane ROBERTO, 01/08 |
| 3 | Exploiter le signal B2B des 437 pré-inscrits | société, poste, secteur — sans casser la règle « société ≠ lead entreprise » |
| 4 | Remplir `Wix — Libellés d'origine` | propriété créée mais vide ; c'est elle qui justifie chaque `Température CRM` |

### En attente de Franck

| Action | Pourquoi lui |
|---|---|
| Export Wix des réponses `Inscription - DRH`, `Inscription - ADG`, `Certification Promo 4 & 5` | → **23 contacts en `ENTREPRISE`**, 19 en `CLIENT`. Les identités ne sont pas dans la base |
| Accord avant création des formulaires sur son compte | ça touche sa marque et des supports en circulation |
| Bascule des anciens liens et QR codes | supports imprimés déjà diffusés |

### En attente d'une décision de palier

| Action | Blocage |
|---|---|
| Séquences de nurturing automatiques | les **workflows** demandent le palier Professional |
| Réactivation des 6 196 dormants | **à chiffrer avant de lancer** : HubSpot facture les contacts *marketing*, pas les contacts stockés |

---

## Écarté, et pourquoi

| Action | Décision |
|---|---|
| Répondre aux 43 leads de la boîte Wix | **écarté le 05/08** — hors périmètre pour l'instant, priorité au formulaire |
| Désactiver l'automatisation Wix de 2023 | **sans objet** — le doublon était une fausse alerte |
| Attendre l'Excel des pré-inscrits | **sans objet** — les 525 pré-inscriptions sont dans le CMS Wix |
| Attendre le fichier des certifiés de Stéphane | **sans objet** — Franck confirme que les 19 réponses Wix sont des clients |
| Recruter/assigner un commercial | **sans objet** — pas de commercial. Franck seul |
| Synchronisation Wix ↔ HubSpot par appli tierce | **écarté** — aucune appli ne transporte la qualification, seulement les contacts |

---

## Points de vigilance

- **« Non lu » n'est pas « sans réponse ».** Les 50 non-lus de la boîte Wix ne prouvent pas
  qu'aucune réponse n'a été apportée : aucun accès à la messagerie de Franck.
- **HubSpot remappe mal à chaque import.** Il propose `E-mail 1` → `E-mail 3` sans identifiant
  unique. Tel quel, un import de 419 lignes crée 419 doublons. À recorriger systématiquement.
- **L'écran « Problèmes de formatage » est global** — 635 fiches. Le bouton *Tout accepter* les
  modifierait toutes.
- **Franck est seul.** Chaque automatisation doit lui retirer un geste, pas lui créer une tâche.
- **La géographie n'est pas exploitable** : `Pays` renseigné sur 8 % de la base. Le 80/20 se
  pilote par zone — non mesurable en l'état.
