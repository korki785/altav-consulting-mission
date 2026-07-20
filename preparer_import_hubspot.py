#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Derniere passe avant l'import HubSpot : nettoyages decides avec Nael.

Quatre operations, toutes tracees a l'ecran :

1. Telephone 1 : vide les numeros de moins de 8 chiffres. La colonne contient
   "1", "600", "60000", "243" -- des saisies parasites, pas des numeros.
   Importer un numero injoignable coute plus cher qu'une case vide.

2. Langue : normalise en code a 2 lettres minuscules. Wix melange "fr",
   "fr-fr", "fr-FR", "en-US", "en-GB". HubSpot attend une valeur unique par
   langue, sinon la segmentation par langue se fragmente.

3. Statut d'abonne aux SMS : colonne retiree. 325 lignes remplies, TOUTES a
   "Jamais abonne" -- une colonne a valeur unique ne porte aucune information.

4. "Sujet de coaching" renomme en "Domaine d'activite". Le libelle Wix etait
   trompeur : le contenu est le secteur d'activite du lead (Agroalimentaire,
   Microfinance, Energie renouvelable...), pas un sujet de coaching.
   162 valeurs distinctes pour 180 contacts -> texte libre a l'import, pas
   une liste deroulante : il n'y a pas de nomenclature a figer.

5. "E-mail 2" et "E-mail 3" fusionnes en une seule colonne "E-mails
   secondaires", valeurs separees par ";". HubSpot n'accepte qu'UNE colonne
   mappee sur la propriete "Adresses e-mail supplementaires"
   (hs_additional_emails) -- deux colonnes source ne peuvent pas s'y mapper
   toutes les deux. Le point-virgule est le separateur exige par HubSpot ;
   comme c'est aussi le separateur de colonnes de ce fichier, le champ est
   automatiquement mis entre guillemets par le module csv (CSV standard).

Entree  : contacts_hubspot.csv
Sortie  : contacts_hubspot.csv (+ contacts_hubspot.bak.csv)

Idempotent : une seconde execution ne change plus rien.

Usage :
    python3 preparer_import_hubspot.py [--dry-run]
"""

import csv
import re
import shutil
import sys

CIBLE = "contacts_hubspot.csv"
SAUVEGARDE = "contacts_hubspot.bak.csv"
DELIMITEUR = ";"

COL_TEL = "Téléphone 1"
COL_LANGUE = "Langue"
COL_SMS = "Statut d'abonné aux SMS"
COL_COACHING = "Sujet de coaching"
COL_DOMAINE = "Domaine d'activité"
COL_EMAIL2 = "E-mail 2"
COL_EMAIL3 = "E-mail 3"
COL_EMAILS_SECONDAIRES = "E-mails secondaires"

MIN_CHIFFRES_TEL = 8


def normaliser_langue(valeur):
    """"fr-FR" -> "fr". Garde les 2 premieres lettres, en minuscules."""
    v = (valeur or "").strip().lower()
    if not v:
        return ""
    code = re.split(r"[-_]", v)[0]
    return code if len(code) == 2 and code.isalpha() else v


def main():
    dry_run = "--dry-run" in sys.argv

    with open(CIBLE, encoding="utf-8-sig", newline="") as f:
        lecteur = csv.DictReader(f, delimiter=DELIMITEUR)
        entetes = lecteur.fieldnames
        lignes = list(lecteur)

    # --- 1. Telephones parasites -------------------------------------------
    vides = []
    for ligne in lignes:
        brut = (ligne.get(COL_TEL) or "").strip()
        if brut and len(re.sub(r"\D", "", brut)) < MIN_CHIFFRES_TEL:
            vides.append(brut)
            ligne[COL_TEL] = ""

    print("=== 1. TELEPHONES PARASITES VIDES (%d) ===" % len(vides))
    apercu = sorted(set(vides), key=lambda v: (len(v), v))[:12]
    print("   valeurs retirees : %s" % ", ".join(repr(v) for v in apercu))

    # --- 2. Langues ---------------------------------------------------------
    changees = {}
    for ligne in lignes:
        avant = (ligne.get(COL_LANGUE) or "").strip()
        apres = normaliser_langue(avant)
        if avant != apres:
            changees[avant] = apres
        ligne[COL_LANGUE] = apres

    print()
    print("=== 2. LANGUES NORMALISEES (%d formes) ===" % len(changees))
    for avant, apres in sorted(changees.items()):
        print("   %-8s -> %s" % (repr(avant), apres))
    if not changees:
        print("   deja normalisees")

    # --- 3. Colonne SMS retiree --------------------------------------------
    entetes_sortie = [c for c in entetes if c != COL_SMS]
    print()
    print("=== 3. COLONNE RETIREE ===")
    print("   %s %s" % (COL_SMS, "" if COL_SMS in entetes else "(deja absente)"))

    # --- 4. Renommage -------------------------------------------------------
    print()
    print("=== 4. COLONNE RENOMMEE ===")
    if COL_COACHING in entetes_sortie:
        entetes_sortie = [COL_DOMAINE if c == COL_COACHING else c for c in entetes_sortie]
        for ligne in lignes:
            ligne[COL_DOMAINE] = ligne.pop(COL_COACHING, "")
        print("   %r -> %r" % (COL_COACHING, COL_DOMAINE))
    else:
        print("   deja renommee")

    # --- 5. Fusion des emails secondaires -----------------------------------
    fusions = []
    if COL_EMAIL2 in entetes_sortie or COL_EMAIL3 in entetes_sortie:
        entetes_sortie = [c for c in entetes_sortie if c not in (COL_EMAIL2, COL_EMAIL3)]
        entetes_sortie.append(COL_EMAILS_SECONDAIRES)
        for ligne in lignes:
            e2 = (ligne.pop(COL_EMAIL2, "") or "").strip()
            e3 = (ligne.pop(COL_EMAIL3, "") or "").strip()
            valeurs = [e for e in (e2, e3) if e]
            ligne[COL_EMAILS_SECONDAIRES] = ";".join(valeurs)
            if valeurs:
                fusions.append((e2, e3, ligne[COL_EMAILS_SECONDAIRES]))

    print()
    print("=== 5. EMAILS SECONDAIRES FUSIONNES (%d lignes concernees) ===" % len(fusions))
    if fusions:
        print("   %-30s %-30s -> %s" % ("E-mail 2", "E-mail 3", COL_EMAILS_SECONDAIRES))
        for e2, e3, fus in fusions[:6]:
            print("   %-30s %-30s -> %s" % (e2 or "(vide)", e3 or "(vide)", fus))
    else:
        print("   deja fusionnees")

    print()
    print("=== RESULTAT ===")
    print("Lignes   : %d (inchange)" % len(lignes))
    print("Colonnes : %d -> %d" % (len(entetes), len(entetes_sortie)))

    if dry_run:
        print()
        print("--dry-run : AUCUNE ecriture. Fichier inchange.")
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
