# Base contacts Altav → HubSpot — bilan et guide d'utilisation

*Préparé par Nael pour Franck, 20/07/2026.*

---

## En une phrase

**8 915 contacts Wix bruts et inexploitables → 7 483 contacts propres, segmentés, importés
dans HubSpot.**

---

## Chiffres clés

| Indicateur | Valeur |
|---|---|
| Contacts finaux | **7 483** |
| Contacts nommés | **3 598 (48 %)**, contre 33 % au départ |
| Colonnes finales | **22**, contre 51 à l'origine |
| Emails actifs | **7 399 (99 %)** |
| Coût total (traitement par IA) | **7,10 $** |

**Répartition commerciale (`Tag_CRM`) :**

- 🔴 **CLIENT** — 753 — a déjà payé
- 🟠 **CHAUD** — 318 — intention d'achat explicite
- 🟡 **INBOUND** — 171 — venu à nous, sans intention forte
- ⚪ **FROID** — 6 241 — ne nous connaît pas / prospection

---

## Ce qui a été fait

### 1. Segmentation commerciale
- Ajout d'une colonne unique `Tag_CRM` → répond à *« où en est la relation ? »*
- 195 leads récupérés grâce à une exception de règle *(des inscriptions volontaires
  auraient été classées à tort comme prospection froide)*
- Libellés d'origine conservés intacts, rien n'a été effacé

### 2. Dédoublonnage
- **531 fusions**, aucune perte de donnée
- Emails secondaires conservés plutôt qu'écrasés

### 3. Emails morts
- 976 adresses mortes croisées avec la base
- **889 lignes supprimées** *(FROID/INBOUND sans email → aucune valeur)*
- **84 lignes conservées** *(CLIENT/CHAUD → la relation vaut plus que l'adresse)*
- ⚠️ Incident évité : un fichier de suppression fourni était en réalité une quasi-copie de
  toute la base — appliqué tel quel, il aurait supprimé 733 clients

### 4. Nettoyage interne
- **12 adresses Altav** retirées de la base prospects
- Sans ça, l'équipe aurait reçu les séquences de prospection

### 5. Enrichissement des noms
- **232 noms** déduits par règle (adresses `prenom.nom@…`)
- **1 162 noms** déduits par IA *(relus et validés le 20/07/2026)*
- **939 corrections** sur des noms mal saisis dans Wix *(casse, doublons, valeurs bouchon)*
- **122 inversions prénom/nom** corrigées par IA

### 6. Distinction B2B / B2C
- Nouvel axe créé : `type_compte` → répond à *« qui paie ? »*
- Tous les contacts actuels classés **INDIVIDUEL** *(aucun lead entreprise fiable identifié
  à ce jour)*
- ⚠️ Point de vigilance traité : 789 contacts ont une société renseignée mais restent des
  particuliers — les classer en ENTREPRISE aurait été une erreur

### 7. Import HubSpot
- Base réduite à **22 colonnes utiles** *(colonnes mortes retirées)*
- **9 propriétés personnalisées** créées pour porter la segmentation

---

## Guide d'utilisation

### Règle n°1 : deux axes, jamais à confondre

| Axe | Question | Valeurs |
|---|---|---|
| **Température** | Où en est la relation ? | CLIENT · CHAUD · INBOUND · FROID |
| **Type de compte** | Qui paie ? | INDIVIDUEL · ENTREPRISE |

> ❌ **Piège à éviter :** un email professionnel ne veut PAS dire ENTREPRISE.
> ENTREPRISE = la société paie. Un salarié qui paie pour lui-même reste INDIVIDUEL.

### Règle n°2 : archive vs donnée vivante

- Les propriétés « **Wix — ...** » sont figées au 20/07/2026 → **ne jamais les modifier**
- HubSpot tient ses propres indicateurs d'activité, à jour en continu, à côté

### Règle n°3 : classer les nouveaux leads entreprise à la source

- Formulaire dédié (« Je forme mes équipes ») → classe automatiquement en ENTREPRISE
- Import outbound / LinkedIn → se déclare ENTREPRISE dès le fichier d'import
- **Jamais** en devinant après coup sur une fiche existante

---

## Décisions à prendre

- [ ] **Qui porte le CRM au quotidien ?** *(condition de tout le reste)*
- [ ] **Fichier des certifiés de Stéphane** *(bascule CHAUD → CLIENT pour les payants)*
- [ ] **Accès back-office Wix + Excel des pré-inscrits**

---

## Prochaine étape recommandée

**Séquence de nurturing sur les 489 contacts INBOUND + CHAUD** — ne dépend d'aucune des
décisions ci-dessus :

- Mail de confirmation réécrit
- Livre blanc à J+5
- Relance à J+30
- Rappel sous 5 minutes après inscription

---

## Limite connue

**Géographie non exploitable** — pays renseigné sur seulement 8 % des contacts. Or l'objectif
80/20 B2B/B2C se pilote par zone *(quasi atteint au Burundi, très loin ailleurs)* → non
mesurable en l'état.
