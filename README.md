# Altav — Mission Consulting

Automatisation du tunnel de conversion (CRM + séquences). Objectif : lever le goulot de
**conversion**, pas la demande. CRM cible : **HubSpot**.

**État au 4 août 2026** — base nettoyée (7 483 contacts) et importée dans HubSpot. Le chantier
en cours est l'**acquisition** : tant qu'aucun formulaire n'alimente HubSpot, aucune séquence de
nurturing n'a de déclencheur.

---

## Documentation

Lire dans cet ordre. Chaque document est autonome.

| # | Document | Contenu |
|---|---|---|
| 1 | [Mission](docs/01-mission.md) | Constat, principe, plan de déploiement en 4 volets |
| 2 | [Classification](docs/02-classification.md) | Les 4 axes : `Tag_CRM`, `type_compte`, `Email_actif`, `Origine_nom` |
| 3 | [Mise en œuvre HubSpot](docs/03-hubspot.md) | Ce que permet chaque palier d'abonnement, ce qui a été écarté |
| 4 | [Acquisition](docs/04-acquisition.md) | État des lieux Wix, décision « les formulaires vivent dans HubSpot » |
| 5 | [Journal de traitement](docs/05-journal.md) | Chaque décision de nettoyage et sa justification |
| — | [Référence `type_compte`](docs/reference-type-compte.md) | Paramétrage détaillé de la propriété custom |

Livrables client (envoyés ou à envoyer à Franck) : [`livrables/`](livrables/) —
guide CRM, questions formulaires, mail d'accompagnement.

---

## Structure du dépôt

```
docs/         documentation de la mission, numérotée dans l'ordre de lecture
livrables/    documents destinés au client
scripts/      pipeline de nettoyage, numéroté dans l'ordre d'exécution
donnees/      CSV — JAMAIS versionné (données personnelles)
  source/       entrées brutes, jamais modifiées
  travail/      fichiers du pipeline, réécrits en place
  exports/      fichiers prêts à importer dans HubSpot
  revue/        sorties destinées à une relecture humaine
  sauvegardes/  copies .bak écrites avant chaque modification
journaux/     logs d'exécution — non versionné
```

`scripts/chemins.py` est le seul endroit qui sait où vivent les fichiers. Un script se lance
depuis n'importe quel répertoire.

---

## Pipeline

Deux étages : segmentation de l'export Wix (1–5), puis préparation de l'import HubSpot (6–10).
Chaque script sauvegarde avant d'écrire et accepte `--dry-run` (sauf le premier).

```bash
# étage Wix : donnees/source/CRM Contact.csv → donnees/travail/contacts_wix_tagges.csv
python3 scripts/01_tag_contacts.py            # segmentation + dédoublonnage
python3 scripts/02_appliquer_suppressions.py  # emails morts
python3 scripts/03_purger_internes.py         # collaborateurs Altav
python3 scripts/04_deduire_noms.py            # noms déduits par règle
python3 scripts/05_deduire_noms_claude.py     # noms déduits par modèle (payant)

# étage HubSpot : → donnees/travail/contacts_hubspot.csv
python3 scripts/06_ajouter_type_compte.py     # colonne type_compte
python3 scripts/07_preparer_import_hubspot.py # normalisation pré-import
python3 scripts/08_nettoyer_noms.py           # casse, tokens répétés, déchets
python3 scripts/09_verifier_noms_claude.py    # inversions prénom/nom (payant)
python3 scripts/10_retirer_colonnes_vides.py  # retrait des colonnes mortes
```

Les scripts 05 et 09 appellent l'API Anthropic : clé lue dans `ANTHROPIC_API_KEY`, sinon dans
un `.env` (voir `scripts/chemins.py`).

**Résultat : 7 483 contacts, 22 colonnes.** FROID 6 241 · CLIENT 753 · CHAUD 318 · INBOUND 171.
Contacts nommés : 3 605 (48 %), contre 33 % au départ.

---

## Méthode de travail

Sur toute transformation de masse : **tester sur ~10 lignes, lister les changements, valider,
puis appliquer.** Cette règle a évité de propager 3 défauts sur 232 contacts, et a détecté un
faux fichier de suppression avant qu'il ne détruise 8 354 lignes.

Le fichier source `donnees/source/CRM Contact.csv` n'est jamais modifié.

---

## Prochaine étape

Pas les séquences de nurturing : l'**acquisition** d'abord.

1. Envoi de `livrables/QUESTIONS_FORMULAIRES_FRANCK.html` à Franck — 9 questions, dont une seule
   bloquante : l'engagement à ne plus créer de formulaire dans Wix.
2. Vérification du doublon d'automatisation et traitement des 63 messages non lus.
3. Création des 5 formulaires HubSpot, puis bascule des anciens liens.
4. **Alors seulement** : les séquences de nurturing, qui auront enfin de quoi se déclencher.

## Ce qu'il me faut

- ~~Accès **back-office Wix**~~ — obtenu le 03/08/2026.
- Accès **Excel pré-inscrits** *(les ~489 ne se retrouvent pas dans les formulaires Wix — 132
  pré-inscriptions cumulées seulement)*.
- Décision : **qui porte le CRM en interne**. Condition de tout le reste.
- Fichier des certifiés de Stéphane → basculer les « Certification Promo 4 & 5 » payants de
  `CHAUD` vers `CLIENT`. *Peut-être déjà disponible : 19 réponses au formulaire Wix du même nom.*
- Réponses aux **9 questions** de `livrables/QUESTIONS_FORMULAIRES_FRANCK.html`.

## Limite connue

**La géographie n'est pas exploitable en l'état.** `Pays` n'est renseigné que sur **587 / 7 483
contacts (8 %)**. Les indicatifs téléphoniques comblent partiellement : 386 numéros en +257
(Burundi), 56 en +225 (Côte d'Ivoire), 53 en +243 (RDC), 44 en +229 (Bénin), 42 en +221
(Sénégal) — soit ~24 % de la base au total.

Or l'objectif 80/20 se pilote **par zone** : quasi atteint au Burundi, très loin du compte hors
Burundi. Sans pays fiable, ce rapport n'est pas mesurable. Chantier à arbitrer.

---

## Données personnelles

Aucun CSV n'est versionné (`.gitignore`). Le dépôt ne contient que les scripts et la
documentation. La base fait ~7 500 personnes physiques : noms, emails, téléphones. Un
`git add` forcé publierait des données que l'historique git conserverait ensuite
définitivement.
