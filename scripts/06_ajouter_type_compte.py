#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ajoute la colonne type_compte en vue de l'import HubSpot.

type_compte repond a UNE question : qui paie la formation ?
    INDIVIDUEL (B2C) : la personne s'inscrit et paie pour elle-meme
    ENTREPRISE (B2B) : la societe achete et paie pour ses salaries

Toutes les lignes partent en INDIVIDUEL. C'est une decision assumee, pas un
defaut technique : la base ne contient aujourd'hui aucun lead entreprise
identifiable de facon fiable.

Ne PAS classer sur "Societe renseignee" ni sur le domaine email. 789 contacts
ont un employeur et 685 un email a domaine pro (undp.org, heineken.com...),
et ce sont malgre tout des leads individuels : avoir un employeur ne fait pas
un lead entreprise. Classer dessus basculerait ~800 contacts a tort.

Le classement des futurs leads se fait A LA SOURCE (formulaire B2B a champ
cache, colonne renseignee dans les imports outbound), pas par inference.
Voir README.md, section "Regles de classification CRM".

Entree  : contacts_wix_tagges.csv  (JAMAIS modifie, ouvert en lecture seule)
Sortie  : contacts_hubspot.csv     (nouveau fichier)

Idempotent : relancer reecrit la sortie a l'identique.

Usage :
    python3 ajouter_type_compte.py [--dry-run]
"""

import csv
import os
import sys

import chemins

SOURCE = chemins.TRAVAIL / "contacts_wix_tagges.csv"
SORTIE = chemins.TRAVAIL / "contacts_hubspot.csv"
DELIMITEUR = ";"

COLONNE = "type_compte"
VALEUR_DEFAUT = "INDIVIDUEL"

# Colonnes custom a mapper explicitement dans l'import HubSpot : l'outil ne
# les reconnait pas seul, il les ignorerait silencieusement.
COLONNES_CUSTOM = ["Tag_CRM", "Email_actif", "Origine_nom", COLONNE]

ECHANTILLON = 10


def main():
    dry_run = "--dry-run" in sys.argv

    if not os.path.exists(SOURCE):
        raise SystemExit("Introuvable : %s" % SOURCE)

    with open(SOURCE, encoding="utf-8-sig", newline="") as f:
        lecteur = csv.DictReader(f, delimiter=DELIMITEUR)
        entetes = lecteur.fieldnames
        lignes = list(lecteur)

    if COLONNE in entetes:
        raise SystemExit(
            "%s contient deja une colonne %r. Rien a faire." % (SOURCE, COLONNE)
        )

    for ligne in lignes:
        ligne[COLONNE] = VALEUR_DEFAUT

    entetes_sortie = list(entetes) + [COLONNE]

    # --- Echantillon avant masse ------------------------------------------
    # Regle de travail du projet : montrer ~10 lignes et les changements
    # avant tout traitement en masse. Voir JOURNAL.md.
    print("=== ECHANTILLON (%d premieres lignes) ===" % ECHANTILLON)
    print("%-38s | %-9s | %s" % ("E-mail 1", "Tag_CRM", COLONNE))
    print("-" * 72)
    for ligne in lignes[:ECHANTILLON]:
        print("%-38s | %-9s | %s" % (
            (ligne.get("E-mail 1") or "(sans email)")[:38],
            ligne.get("Tag_CRM", ""),
            ligne[COLONNE],
        ))

    print()
    print("=== CHANGEMENTS ===")
    print("Colonnes  : %d -> %d  (ajout de %r en derniere position)"
          % (len(entetes), len(entetes_sortie), COLONNE))
    print("Lignes    : %d  (inchange)" % len(lignes))
    print("Valeur    : %r sur 100%% des lignes" % VALEUR_DEFAUT)
    print("Intactes  : Tag_CRM, Email_actif, Origine_nom, et toutes colonnes Wix")
    print("Source    : %s NON modifie" % SOURCE)

    print()
    print("=== A MAPPER MANUELLEMENT A L'IMPORT HUBSPOT ===")
    for c in COLONNES_CUSTOM:
        print("  %s" % c)

    if dry_run:
        print()
        print("--dry-run : AUCUNE ecriture.")
        return

    with open(SORTIE, "w", encoding="utf-8-sig", newline="") as f:
        ecrivain = csv.DictWriter(
            f, fieldnames=entetes_sortie, delimiter=DELIMITEUR, extrasaction="ignore"
        )
        ecrivain.writeheader()
        ecrivain.writerows(lignes)

    print()
    print("Ecrit : %s (%d lignes, %d colonnes)"
          % (SORTIE, len(lignes), len(entetes_sortie)))


if __name__ == "__main__":
    main()
