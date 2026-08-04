#!/usr/bin/env python3
"""
Chemins du depot — un seul endroit qui sait ou vivent les fichiers.

Les scripts du pipeline etaient ecrits pour tourner a la racine, avec des noms
de fichiers nus ("contacts_hubspot.csv"). Ils tournent desormais depuis
scripts/ et les donnees vivent dans donnees/. Ce module resout les chemins
depuis l'emplacement du fichier, pas depuis le repertoire courant : un script
se lance de n'importe ou.

    import chemins
    CIBLE = chemins.TRAVAIL / "contacts_hubspot.csv"

Roles des repertoires :

    donnees/source/       entrees brutes, JAMAIS modifiees
    donnees/travail/      fichiers du pipeline, reecrits en place
    donnees/exports/      fichiers prets a importer dans HubSpot
    donnees/revue/        sorties destinees a une relecture humaine
    donnees/sauvegardes/  copies .bak ecrites avant chaque modification
"""

from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent

DONNEES = RACINE / "donnees"
SOURCE = DONNEES / "source"
TRAVAIL = DONNEES / "travail"
EXPORTS = DONNEES / "exports"
REVUE = DONNEES / "revue"
SAUVEGARDES = DONNEES / "sauvegardes"

JOURNAUX = RACINE / "journaux"

# Cle API : le .env du depot d'abord, les autres depots ensuite (historique).
FICHIERS_ENV = [
    str(RACINE / ".env"),
    str(Path.home() / "gk-advancing/.env"),
    str(Path.home() / "automation-orfeo/.env"),
    str(Path.home() / "living-memory/.env"),
]
