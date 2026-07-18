#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Retire les contacts internes Altav de la base prospects.

Collaborateurs et boites generiques (contact@, info@) n'ont rien a faire dans
une sequence de prospection. Le filtre balaie TOUTES les colonnes email, pas
seulement la principale : plusieurs collaborateurs ont un gmail personnel en
E-mail 1 et leur adresse Altav en E-mail 2, recuperee lors du dedoublonnage.

Entree  : contacts_wix_tagges.csv
Sortie  : contacts_wix_tagges.csv (+ contacts_wix_tagges.bak.csv)

Idempotent : une seconde execution ne retire plus rien.

Usage :
    python3 purger_internes.py [--dry-run]
"""

import csv
import re
import shutil
import sys
import unicodedata

CIBLE = "contacts_wix_tagges.csv"
SAUVEGARDE = "contacts_wix_tagges.bak.csv"
DELIMITEUR = ";"

# Fragment cherche dans les adresses. Couvre altav-consulting.com,
# altavconsulting.com et altavconsulting7@gmail.com.
FRAGMENT_INTERNE = "altav"

COLONNE_EMAIL = re.compile(r"^e-?mail\s*\d*$")


def normaliser(texte):
    texte = unicodedata.normalize("NFD", (texte or "").lower())
    return "".join(c for c in texte if unicodedata.category(c) != "Mn").strip()


def main():
    dry_run = "--dry-run" in sys.argv

    with open(CIBLE, encoding="utf-8-sig", newline="") as f:
        lecteur = csv.DictReader(f, delimiter=DELIMITEUR)
        entetes = lecteur.fieldnames
        lignes = list(lecteur)

    cols_email = [c for c in entetes if COLONNE_EMAIL.match(normaliser(c))]

    def est_interne(ligne):
        return any(FRAGMENT_INTERNE in normaliser(ligne.get(c)) for c in cols_email)

    internes = [l for l in lignes if est_interne(l)]
    conserves = [l for l in lignes if not est_interne(l)]

    print("=== CONTACTS INTERNES RETIRES (%d) ===" % len(internes))
    for l in internes:
        nom = ("%s %s" % (l.get("Prénom", ""), l.get("Nom de famille", ""))).strip()
        print("  %-44s | %-26s | %s"
              % (l.get("E-mail 1"), nom or "(sans nom)", l.get("Tag_CRM", "")))

    print()
    print("Lignes : %d -> %d" % (len(lignes), len(conserves)))

    if dry_run:
        print("--dry-run : AUCUNE ecriture. Fichier inchange.")
        return

    if not internes:
        print("Rien a retirer, fichier inchange.")
        return

    shutil.copy2(CIBLE, SAUVEGARDE)
    with open(CIBLE, "w", encoding="utf-8-sig", newline="") as f:
        ecrivain = csv.DictWriter(
            f, fieldnames=entetes, delimiter=DELIMITEUR, extrasaction="ignore"
        )
        ecrivain.writeheader()
        ecrivain.writerows(conserves)

    print("Ecrit : %s" % CIBLE)
    print("Sauvegarde : %s" % SAUVEGARDE)


if __name__ == "__main__":
    main()
