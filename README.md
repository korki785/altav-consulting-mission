# Altav — Mission Consulting

Automatisation du tunnel de conversion (CRM + séquences). Objectif : lever le goulot de
**conversion**, pas la demande. CRM cible : **HubSpot**.

**État au 2 septembre 2026** — base nettoyée (7 483 contacts) et importée dans HubSpot, et
**le premier formulaire HubSpot est en ligne** : le pilote du pied de page tourne sur
`altavconsulting.com`, chaque soumission crée un contact déjà classé `INBOUND` / `INDIVIDUEL`.
L'acquisition a son premier canal ; restent les 5 autres formulaires, et la validation des
3 critères par Franck.

**Franck a répondu aux 9 questions le 4 août.** Les 9 sont tranchées, dont la seule bloquante :
plus aucun formulaire d'acquisition dans Wix. La construction des formulaires HubSpot est
ouverte — voir [décisions](docs/06-decisions-franck.md).

---

## Documentation

Lire dans cet ordre. Chaque document est autonome. **Pour l'avancement, une seule adresse :
la [checklist](docs/00-checklist.md).**

| # | Document | Contenu |
|---|---|---|
| **0** | **[Checklist](docs/00-checklist.md)** | **Où on en est : fait · à faire · écarté, daté, avec les dépendances** |
| 1 | [Mission](docs/01-mission.md) | Constat, principe, plan de déploiement en 4 volets |
| 2 | [Classification](docs/02-classification.md) | Les 4 axes : `Tag_CRM`, `type_compte`, `Email_actif`, `Origine_nom` |
| 3 | [Mise en œuvre HubSpot](docs/03-hubspot.md) | Ce que permet chaque palier d'abonnement, ce qui a été écarté |
| 4 | [Acquisition](docs/04-acquisition.md) | État des lieux Wix, décision « les formulaires vivent dans HubSpot » |
| 5 | [Journal de traitement](docs/05-journal.md) | Chaque décision de nettoyage et sa justification |
| 6 | [Décisions de Franck](docs/06-decisions-franck.md) | Réponses aux 9 questions, cycle de vie en 7 étapes — **fait foi** |
| 7 | [Roadmap](docs/07-roadmap.md) | Les 5 phases jusqu'à la fin de mission, et ce qui peut la faire échouer |
| 8 | [Formulaires HubSpot](docs/08-formulaires-hubspot.md) | Spec des 6 formulaires, champ par champ — **à valider par Franck** |
| 9 | [Solution provisoire](docs/09-solution-provisoire.md) | Ce qui tourne sans workflows, et le déclencheur exact de sortie du provisoire |
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

Trois étages : segmentation de l'export Wix (1–5), préparation de l'import HubSpot (6–10),
puis enrichissement depuis le CMS Wix (11).
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

# enrichissement depuis le CMS Wix
python3 scripts/11_requalifier_preinscrits.py  # pré-inscrits FROID/INBOUND -> CHAUD
```

Les scripts 05 et 09 appellent l'API Anthropic : clé lue dans `ANTHROPIC_API_KEY`, sinon dans
un `.env` (voir `scripts/chemins.py`).

**Résultat : 7 483 contacts, 23 colonnes.** FROID 6 196 · CLIENT 753 · **CHAUD 386** · INBOUND 148.
Contacts nommés : 3 605 (48 %), contre 33 % au départ.

*Le vivier chaud est passé de 318 à 386 le 05/08 : 68 pré-inscrits étaient classés froids ou
tièdes. Voir [journal, §8](docs/05-journal.md).*

---

## Méthode de travail

Sur toute transformation de masse : **tester sur ~10 lignes, lister les changements, valider,
puis appliquer.** Cette règle a évité de propager 3 défauts sur 232 contacts, et a détecté un
faux fichier de suppression avant qu'il ne détruise 8 354 lignes.

Le fichier source `donnees/source/CRM Contact.csv` n'est jamais modifié.

---

## Prochaine étape

Pas les séquences de nurturing : l'**acquisition** d'abord — spécifier puis créer les
6 formulaires HubSpot, en commençant par la pré-inscription et le formulaire du pied de page,
les deux seuls canaux réellement vivants.

L'état détaillé de chaque action vit dans la **[checklist](docs/00-checklist.md)**.
Le chemin complet jusqu'à la fin de mission est dans la **[roadmap](docs/07-roadmap.md)**.

## Ce qu'il me faut

- ~~Accès **back-office Wix**~~ — obtenu le 03/08/2026.
- ~~Accès **Excel pré-inscrits**~~ — inutile, trouvé le 05/08 : les pré-inscriptions sont dans le
  **CMS Wix**, collection `Pré-inscription Formation Ubuntu` — **525 lignes** avec e-mail et
  téléphone, la dernière du 01/08/2026. C'est la source à migrer vers HubSpot.
- ~~Décision : **qui porte le CRM en interne**~~ — tranché : **Franck, seul**. Le commercial
  qu'il évoquait n'est pas recruté ; aucune décision ne repose dessus. Un seul utilisateur
  HubSpot, pas de siège supplémentaire.
- ~~Fichier des certifiés de Stéphane~~ — inutile : Franck confirme le 04/08 que les 19 réponses
  du formulaire Wix `Certification Promo 4 & 5` sont bien des clients ayant payé.
- **Export Wix des réponses** de `Inscription - DRH`, `Inscription - ADG` et
  `Certification Promo 4 & 5` — seule façon d'identifier les 23 `ENTREPRISE` et les 19 `CLIENT`.
- ~~Réponses aux **9 questions**~~ — obtenues le 04/08/2026.
- ~~Par où passent réellement les pré-inscriptions ?~~ — répondu le 05/08 : par un formulaire de
  l'**ancienne appli Wix**, dont les réponses tombent dans la boîte de réception que personne ne
  relève. C'est ce formulaire-là qu'il faut repointer vers HubSpot, pas les 4 formulaires morts.
- Rien en attente de Franck sur ces points : pas de relance des leads pour l'instant, et il est
  le destinataire par défaut de toutes les tâches.

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
