#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Retire les colonnes structurellement mortes, pour un import HubSpot plus leger.

Ne coupe pas sur un seuil de pourcentage aveugle. Deux familles bien
differentes se cachent derriere "peu de donnees" :

  - MORT : Adresse 2 a 5 et leurs sous-champs, Telephone 2/3/4,
    Adresse 1 - Type / Rue ligne 2 / Etat-Region / Code postal.
    0,0% a 1,0% de remplissage, et surtout : jamais mappees sur une
    propriete HubSpot, jamais utilisees dans une segmentation. Du bruit
    Wix structurel, pas de la donnee rare.

  - RARE MAIS REEL : Domaine d'activite (2,4%), E-mails secondaires (1,4%),
    Langue (6,6%). Le taux est bas parce que peu de contacts Wix ont
    rempli le champ a l'origine -- pour ceux qui l'ont fait, c'est une
    vraie donnee. Adresse 1 - Pays (7,8%) est conservee a part : c'est
    le seul signal geographique disponible pour piloter l'objectif
    80/20 Burundi vs hors-Burundi du fondateur (voir README.md).

Ne pas "ameliorer" ce script en coupant sur un seuil unique : ca supprimerait
Domaine d'activite et E-mails secondaires, qui portent une vraie information
pour un sous-ensemble de contacts.

Entree  : contacts_hubspot.csv
Sortie  : contacts_hubspot.csv (+ contacts_hubspot.colonnes.bak.csv)

Idempotent : une seconde execution ne trouve plus rien a retirer.

Usage :
    python3 retirer_colonnes_vides.py [--dry-run]
"""

import csv
import shutil
import sys

CIBLE = "contacts_hubspot.csv"
SAUVEGARDE = "contacts_hubspot.colonnes.bak.csv"
DELIMITEUR = ";"

# Colonnes retirees : jamais mappees, bruit structurel Wix.
A_RETIRER = [
    "Adresse 1 - Type", "Adresse 1 - Rue ligne 2", "Adresse 1 - État/Région",
    "Adresse 1 - Code postal",
    "Adresse 2 - Type", "Adresse 2 - Rue", "Adresse 2 - Ville",
    "Adresse 2 - État/Région", "Adresse 2 - Code postal", "Adresse 2 - Pays",
    "Adresse 3 - Type", "Adresse 3 - Rue", "Adresse 3 - Ville",
    "Adresse 3 - État/Région", "Adresse 3 - Code postal", "Adresse 3 - Pays",
    "Adresse 4 - Type", "Adresse 4 - État/Région", "Adresse 4 - Code postal",
    "Adresse 4 - Pays",
    "Adresse 5 - Type", "Adresse 5 - État/Région", "Adresse 5 - Pays",
    "Téléphone 2", "Téléphone 3", "Téléphone 4",
]


def main():
    dry_run = "--dry-run" in sys.argv

    with open(CIBLE, encoding="utf-8-sig", newline="") as f:
        lecteur = csv.DictReader(f, delimiter=DELIMITEUR)
        entetes = lecteur.fieldnames
        lignes = list(lecteur)

    n = len(lignes)
    presentes = [c for c in A_RETIRER if c in entetes]
    entetes_sortie = [c for c in entetes if c not in A_RETIRER]

    print("=== COLONNES RETIREES (%d) ===" % len(presentes))
    print("%-32s %8s %6s" % ("COLONNE", "remplie", "%"))
    print("-" * 48)
    for c in presentes:
        nz = sum(1 for l in lignes if (l.get(c) or "").strip())
        print("%-32s %8d %5.1f%%" % (c, nz, 100 * nz / n))

    print()
    print("=== CONSERVEES MALGRE UN TAUX BAS ===")
    for c in ("E-mails secondaires", "Domaine d'activité", "Langue", "Adresse 1 - Pays"):
        if c in entetes_sortie:
            nz = sum(1 for l in lignes if (l.get(c) or "").strip())
            print("%-32s %8d %5.1f%%" % (c, nz, 100 * nz / n))

    print()
    print("=== RESULTAT ===")
    print("Lignes   : %d (inchange)" % n)
    print("Colonnes : %d -> %d" % (len(entetes), len(entetes_sortie)))

    if dry_run:
        print()
        print("--dry-run : AUCUNE ecriture. Fichier inchange.")
        return

    if not presentes:
        print()
        print("Rien a retirer, fichier inchange.")
        return

    shutil.copy2(CIBLE, SAUVEGARDE)
    with open(CIBLE, "w", encoding="utf-8-sig", newline="") as f:
        ecrivain = csv.DictWriter(
            f, fieldnames=entetes_sortie, delimiter=DELIMITEUR, extrasaction="ignore"
        )
        ecrivain.writeheader()
        ecrivain.writerows(lignes)

    print()
    print("Ecrit      : %s" % CIBLE)
    print("Sauvegarde : %s" % SAUVEGARDE)


if __name__ == "__main__":
    main()
