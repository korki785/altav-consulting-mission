#!/usr/bin/env python3
"""
Requalifie en CHAUD les contacts qui se sont pre-inscrits a la formation UBUNTU
mais que le pipeline de juillet a classes FROID ou INBOUND.

Pourquoi : le Tag_CRM de juillet est deduit du champ `Libelles` de l'export Wix.
Le formulaire de pre-inscription de l'ancienne appli n'ecrit aucun libelle : ses
repondants tombaient donc dans la regle 1 (libelle vide -> FROID). Une
pre-inscription est pourtant une intention explicite, donc CHAUD par definition.

Ne touche pas aux CLIENT : la priorite ARCHIVE > CLIENT > FROID > CHAUD > INBOUND
dit qu'une relation payante prime sur une intention. Un client qui s'est
pre-inscrit reste un client.

Ajoute aussi la colonne `date_preinscription` (derniere soumission connue), pour
pouvoir relancer par anciennete.

Entree  : donnees/travail/contacts_hubspot.csv
          donnees/source/preinscriptions_wix_cms.csv  (JAMAIS modifie)
Sortie  : donnees/travail/contacts_hubspot.csv
          (+ donnees/sauvegardes/contacts_hubspot.preinscrits.bak.csv)

Usage :
    python3 scripts/11_requalifier_preinscrits.py --dry-run             # tout, sans ecrire
    python3 scripts/11_requalifier_preinscrits.py --dry-run --echantillon 10
    python3 scripts/11_requalifier_preinscrits.py                       # applique
"""

import csv
import re
import shutil
import sys

import chemins

CIBLE = chemins.TRAVAIL / "contacts_hubspot.csv"
SOURCE_PRE = chemins.SOURCE / "preinscriptions_wix_cms.csv"
SAUVEGARDE = chemins.SAUVEGARDES / "contacts_hubspot.preinscrits.bak.csv"
DELIMITEUR = ";"

COL_TAG = "Tag_CRM"
COL_DATE = "date_preinscription"
TAGS_A_REQUALIFIER = {"FROID", "INBOUND"}
TAG_CIBLE = "CHAUD"

COLONNE_EMAIL = re.compile(r"^e-?mails?\b", re.I)


def normaliser(email):
    return (email or "").strip().strip("'\"").lower()


def emails_de(ligne):
    """Toutes les adresses portees par une fiche, principale et secondaires."""
    trouves = []
    for champ, valeur in ligne.items():
        if champ and COLONNE_EMAIL.match(champ):
            for e in re.split(r"[;,]", valeur or ""):
                e = normaliser(e)
                if e:
                    trouves.append(e)
    return trouves


def charger_preinscriptions():
    """email -> date de la derniere pre-inscription (ISO)."""
    with open(SOURCE_PRE, encoding="utf-8-sig", newline="") as f:
        lignes = list(csv.DictReader(f))
    derniere = {}
    for l in lignes:
        e = normaliser(l.get("E-mail"))
        d = (l.get("Date et heure de l'envoi") or "")[:10]
        if e and (e not in derniere or d > derniere[e]):
            derniere[e] = d
    return derniere, len(lignes)


def main():
    dry = "--dry-run" in sys.argv
    echantillon = 0
    if "--echantillon" in sys.argv:
        echantillon = int(sys.argv[sys.argv.index("--echantillon") + 1])

    preinscrits, nb_lignes_source = charger_preinscriptions()

    with open(CIBLE, encoding="utf-8-sig", newline="") as f:
        lecteur = csv.DictReader(f, delimiter=DELIMITEUR)
        colonnes = list(lecteur.fieldnames)
        base = list(lecteur)

    if COL_DATE not in colonnes:
        colonnes.append(COL_DATE)

    changements, dates_seules, deja_client = [], 0, 0

    for ligne in base:
        date = None
        for e in emails_de(ligne):
            if e in preinscrits and (date is None or preinscrits[e] > date):
                date = preinscrits[e]
        if date is None:
            continue

        ligne[COL_DATE] = date
        avant = ligne.get(COL_TAG, "")
        if avant in TAGS_A_REQUALIFIER:
            changements.append((ligne, avant, date))
        else:
            dates_seules += 1
            if avant == "CLIENT":
                deja_client += 1

    a_appliquer = changements[:echantillon] if echantillon else changements

    print("=== SOURCE ===")
    print("pre-inscriptions            : %d soumissions, %d adresses distinctes"
          % (nb_lignes_source, len(preinscrits)))
    print("contacts reconnus en base   : %d" % (len(changements) + dates_seules))
    print("  dont deja CLIENT          : %d  (intacts, CLIENT prime sur CHAUD)" % deja_client)
    print("\n=== REQUALIFICATIONS %s -> %s ==="
          % ("/".join(sorted(TAGS_A_REQUALIFIER)), TAG_CIBLE))
    print("candidats                   : %d" % len(changements))
    if echantillon:
        print("ECHANTILLON                 : %d premiers\n" % len(a_appliquer))

    print("%-38s %-26s %-9s %-6s %s"
          % ("E-mail", "Nom", "Avant", "Apres", "Pre-inscrit le"))
    print("-" * 100)
    for ligne, avant, date in a_appliquer:
        nom = ("%s %s" % (ligne.get("Prénom", ""), ligne.get("Nom de famille", ""))).strip() or "(sans nom)"
        print("%-38s %-26s %-9s %-6s %s"
              % (emails_de(ligne)[0][:38], nom[:26], avant, TAG_CIBLE, date))

    if dry:
        print("\nDRY-RUN — aucun fichier modifie.")
        return

    for ligne, _, _ in a_appliquer:
        ligne[COL_TAG] = TAG_CIBLE

    shutil.copy(CIBLE, SAUVEGARDE)
    with open(CIBLE, "w", encoding="utf-8-sig", newline="") as f:
        ecrivain = csv.DictWriter(f, fieldnames=colonnes, delimiter=DELIMITEUR)
        ecrivain.writeheader()
        for ligne in base:
            ecrivain.writerow({c: ligne.get(c, "") for c in colonnes})

    print("\n%d tags requalifies, %d dates ecrites." % (len(a_appliquer), len(changements) + dates_seules))
    print("Sauvegarde : %s" % SAUVEGARDE)


if __name__ == "__main__":
    main()
