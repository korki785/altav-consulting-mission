#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Applique la liste d'emails inactifs (export Wix) au fichier tagge.

Le fichier "contacts a supprimer.csv" liste des adresses email mortes
(bounces / desabonnements). La regle metier n'est pas "supprimer la
personne" mais "ne plus lui ecrire" :

  - contact FROID ou INBOUND  -> ligne supprimee
        email mort + aucune relation commerciale = aucune valeur.
  - contact CLIENT ou CHAUD   -> ligne CONSERVEE, Email_actif = NON
        la relation vaut plus que l'adresse. On garde le telephone et
        l'historique pour recontacter autrement.

Entrees : contacts_wix_tagges.csv, contacts a supprimer.csv (non modifies
          en lecture ; la cible est sauvegardee avant reecriture)
Sortie  : contacts_wix_tagges.csv (+ contacts_wix_tagges.bak.csv)

Le script est idempotent et re-executable.

Usage :
    python3 appliquer_suppressions.py
"""

import csv
import re
import shutil
import sys
import unicodedata
from collections import Counter

CIBLE = "contacts_wix_tagges.csv"
LISTE_INACTIFS = "contacts a supprimer.csv"
SAUVEGARDE = "contacts_wix_tagges.bak.csv"
DELIMITEUR = ";"

# Tags dont la relation commerciale justifie de garder la ligne meme si
# l'adresse email est morte.
TAGS_A_CONSERVER = {"CLIENT", "CHAUD"}

# Une vraie colonne email : "E-mail", "E-mail 1", "Email 2"...
# Le motif est ancre pour ne PAS attraper "Statut d'abonne aux e-mails",
# qui contient "mail" mais dont les valeurs sont "abonne"/"non abonne".
COLONNE_EMAIL = re.compile(r"^e-?mail\s*\d*$")


def normaliser(texte):
    """Minuscules, sans accents, espaces externes retires."""
    texte = unicodedata.normalize("NFD", (texte or "").lower())
    return "".join(c for c in texte if unicodedata.category(c) != "Mn").strip()


def colonnes_email(entetes):
    return [c for c in entetes if COLONNE_EMAIL.match(normaliser(c))]


def emails_de(ligne, colonnes):
    """Toutes les adresses valides d'une ligne (email principal + secondaires)."""
    trouves = set()
    for colonne in colonnes:
        valeur = normaliser(ligne.get(colonne))
        if valeur and "@" in valeur:
            trouves.add(valeur)
    return trouves


def lire(chemin):
    with open(chemin, encoding="utf-8-sig", newline="") as f:
        lecteur = csv.DictReader(f, delimiter=DELIMITEUR)
        return lecteur.fieldnames, list(lecteur)


def main():
    entetes_cible, lignes = lire(CIBLE)
    entetes_liste, inactifs = lire(LISTE_INACTIFS)

    if "Tag_CRM" not in entetes_cible:
        raise SystemExit(
            "%s ne contient pas de colonne Tag_CRM. Lance d'abord tag_contacts.py." % CIBLE
        )

    cols_cible = colonnes_email(entetes_cible)
    cols_liste = colonnes_email(entetes_liste)

    # Ensemble des adresses mortes.
    emails_morts = set()
    for ligne in inactifs:
        emails_morts |= emails_de(ligne, cols_liste)

    print("=== ENTREES ===")
    print("Cible            : %s (%d lignes)" % (CIBLE, len(lignes)))
    print("Liste inactifs   : %s (%d lignes)" % (LISTE_INACTIFS, len(inactifs)))
    print("Colonnes email cible : %s" % ", ".join(cols_cible))
    print("Adresses mortes distinctes : %d" % len(emails_morts))

    # --- Application ------------------------------------------------------
    conservees = []
    supprimees = Counter()
    marquees = Counter()
    emails_touches = set()

    for ligne in lignes:
        emails = emails_de(ligne, cols_cible)
        touche = emails & emails_morts

        if not touche:
            # Email jamais signale comme mort : actif par defaut.
            ligne["Email_actif"] = ligne.get("Email_actif") or "OUI"
            conservees.append(ligne)
            continue

        emails_touches |= touche
        tag = ligne.get("Tag_CRM", "")

        if tag in TAGS_A_CONSERVER:
            ligne["Email_actif"] = "NON"
            marquees[tag] += 1
            conservees.append(ligne)
        else:
            supprimees[tag] += 1  # ligne non ajoutee = supprimee

    # Adresses de la liste qui n'existent pas dans la base.
    introuvables = emails_morts - emails_touches

    # --- Ecriture ---------------------------------------------------------
    entetes_sortie = list(entetes_cible)
    if "Email_actif" not in entetes_sortie:
        entetes_sortie.append("Email_actif")

    shutil.copy2(CIBLE, SAUVEGARDE)  # filet de securite avant reecriture

    with open(CIBLE, "w", encoding="utf-8-sig", newline="") as f:
        ecrivain = csv.DictWriter(
            f, fieldnames=entetes_sortie, delimiter=DELIMITEUR, extrasaction="ignore"
        )
        ecrivain.writeheader()
        ecrivain.writerows(conservees)

    # --- Recapitulatif ----------------------------------------------------
    print()
    print("=== SUPPRIMES (email mort, aucune relation) ===")
    for tag, n in supprimees.most_common():
        print("  %-8s %5d" % (tag, n))
    print("  %-8s %5d" % ("TOTAL", sum(supprimees.values())))

    print()
    print("=== CONSERVES avec Email_actif = NON (relation existante) ===")
    for tag, n in marquees.most_common():
        print("  %-8s %5d" % (tag, n))
    print("  %-8s %5d" % ("TOTAL", sum(marquees.values())))

    print()
    print("=== RESULTAT ===")
    print("Lignes avant : %d" % len(lignes))
    print("Lignes apres : %d" % len(conservees))
    tags = Counter(l["Tag_CRM"] for l in conservees)
    for tag in ["CLIENT", "CHAUD", "INBOUND", "FROID", "ARCHIVE", "A_CLASSER"]:
        if tags.get(tag):
            print("  %-8s %5d" % (tag, tags[tag]))

    if introuvables:
        print()
        print("=== %d adresse(s) de la liste absente(s) de la base ===" % len(introuvables))
        for email in sorted(introuvables):
            print("  %s" % email)

    print()
    print("Ecrit : %s" % CIBLE)
    print("Sauvegarde de la version precedente : %s" % SAUVEGARDE)


if __name__ == "__main__":
    main()
