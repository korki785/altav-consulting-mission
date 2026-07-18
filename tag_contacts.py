#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Taggage CRM + dedoublonnage de l'export de contacts Wix.

Entree  : "CRM Contact.csv"          (jamais modifie, ouvert en lecture seule)
Sortie  : "contacts_wix_tagges.csv"  (UTF-8 avec BOM, separateur ';')

Le script est re-executable : il repart toujours du fichier source et
ecrase la sortie. Il ajoute UNE colonne, Tag_CRM, et ne renomme ni ne
modifie la colonne de libelles d'origine.

Usage :
    python3 tag_contacts.py [source.csv] [sortie.csv]
"""

import csv
import sys
import unicodedata
from collections import Counter, OrderedDict

# ---------------------------------------------------------------------------
# Parametres
# ---------------------------------------------------------------------------

SOURCE_DEFAUT = "CRM Contact.csv"
SORTIE_DEFAUT = "contacts_wix_tagges.csv"
DELIMITEUR = ";"

# Ordre de priorite : le tag le plus fort gagne en cas de conflit.
# ARCHIVE isole un contact hors scope ; CLIENT prime ensuite car une relation
# payante est le signal le plus fort ; la regle CSV place les imports en FROID
# avant les distinctions CHAUD / INBOUND.
PRIORITE = ["ARCHIVE", "CLIENT", "FROID", "CHAUD", "INBOUND", "A_CLASSER"]
RANG = {tag: i for i, tag in enumerate(PRIORITE)}

# Detection tolerante des colonnes : on cherche le premier nom de colonne du
# fichier qui contient l'un de ces fragments (accents et casse ignores).
CANDIDATS_COLONNES = {
    "libelle": ["libelle", "label", "tag", "etiquette"],
    "prenom": ["prenom", "first name", "firstname"],
    "nom": ["nom de famille", "last name", "lastname", "surname"],
    "email": ["e-mail 1", "email 1", "e-mail", "email", "mail"],
}

# Colonnes email secondaires deja presentes dans l'export Wix. Un second email
# trouve lors d'une fusion est range dans le premier de ces emplacements qui
# est libre : pas de colonne "Email_secondaire" en doublon fonctionnel.
FRAGMENTS_EMAILS_SECONDAIRES = ["e-mail 2", "e-mail 3", "e-mail 4", "e-mail 5", "e-mail 6"]

# --- Table de mapping libelle -> Tag_CRM -----------------------------------
# Chaque entree est une liste de fragments cherches dans le libelle normalise
# (minuscules, sans accents). Evaluee dans l'ordre de PRIORITE.

ARCHIVE_MOTS = ["concours", "eglise", "obsolete"]

CLIENT_MOTS = [
    "coaching", "team building", "teambuilding", "irp", "kcb",
    "bravoudi", "brarudi", "rattrapage module", "rattrapage cip",
    "leadership ubuntu", "institut", "certifie",
    "etudiants, 1ere promo", "formation ubuntu",
]

CHAUD_MOTS = [
    "certification promo 4", "certification promo 5",
    "pre-inscri", "preinscri",
    "parcours decouverte", "parcours-decouverte", "parcours découverte",
    "session d'info", "session d info", "session d'information",
    "atelier expe", "atelier expé", "atélier expe",
    "brochure",
]

INBOUND_MOTS = [
    "contact 2", "formulaire livre", "livre blanc", "formulaire",
    "webinaire", "seminaire", "institut francais burundi",
]

# Exception a la regle CSV : ces libelles sont des noms de fichier .csv mais
# designent des inscrits volontaires (venus a nous), pas des imports scrapes.
# Sans cette exception, 195 leads entrants tomberaient en FROID.
CSV_EXCEPTIONS = ["session d'info", "session d info", "parcours decouverte", "parcours-decouverte"]

# Libelles tranches manuellement, qui ne matchent aucune regle ci-dessus.
# Compare sur le libelle normalise complet (egalite stricte).
MAPPING_MANUEL = {
    "ecole ubuntu mailing list": "FROID",
    "leads - an": "FROID",
    "libelle demo": "FROID",
}


# ---------------------------------------------------------------------------
# Utilitaires
# ---------------------------------------------------------------------------

def normaliser(texte):
    """Minuscules, sans accents, espaces externes retires."""
    texte = unicodedata.normalize("NFD", (texte or "").lower())
    return "".join(c for c in texte if unicodedata.category(c) != "Mn").strip()


def cle_comparaison(texte):
    """Normalisation + suppression de TOUS les espaces, pour comparer des noms."""
    return "".join(normaliser(texte).split())


def trouver_colonne(entetes, fragments, obligatoire=True, exclure=()):
    """Retourne le premier entete contenant l'un des fragments donnes."""
    for fragment in fragments:
        for entete in entetes:
            if entete in exclure:
                continue
            if fragment in normaliser(entete):
                return entete
    if obligatoire:
        raise SystemExit(
            "Colonne introuvable pour %r.\nEntetes disponibles : %s"
            % (fragments, ", ".join(entetes))
        )
    return None


# ---------------------------------------------------------------------------
# Etape 2 : attribution du Tag_CRM
# ---------------------------------------------------------------------------

def classer(libelle):
    """Retourne le Tag_CRM d'un libelle d'origine unique."""
    n = normaliser(libelle)

    # Aucun libelle -> FROID (ne nous connait pas).
    if not n:
        return "FROID"

    # Decisions manuelles d'abord : elles priment sur toute heuristique.
    if n in MAPPING_MANUEL:
        return MAPPING_MANUEL[n]

    # Regle CSV : tout libelle contenant "CSV" est un import -> FROID,
    # SAUF les libelles listes en exception (inscrits volontaires).
    if "csv" in n and not any(exc in n for exc in CSV_EXCEPTIONS):
        return "FROID"

    for mots, tag in (
        (ARCHIVE_MOTS, "ARCHIVE"),
        (CLIENT_MOTS, "CLIENT"),
        (CHAUD_MOTS, "CHAUD"),
        (INBOUND_MOTS, "INBOUND"),
    ):
        if any(mot in n for mot in mots):
            return tag

    # Non reconnu : on ne devine pas, on signale.
    return "A_CLASSER"


def tag_le_plus_fort(tags):
    """Retourne le tag le plus prioritaire d'une liste."""
    return min(tags, key=lambda t: RANG.get(t, len(PRIORITE)))


# ---------------------------------------------------------------------------
# Etape 3 : dedoublonnage
# ---------------------------------------------------------------------------

def cle_identite(ligne, col_prenom, col_nom, col_email):
    """
    Cle de dedoublonnage : nom complet si disponible, sinon email.

    64 % des lignes de l'export n'ont aucun nom (email seul) : une cle
    strictement nominale ne dedoublonnerait pas ces lignes du tout.
    """
    nom_complet = cle_comparaison(ligne.get(col_prenom, "")) + cle_comparaison(ligne.get(col_nom, ""))
    if nom_complet:
        return ("nom", nom_complet)
    email = normaliser(ligne.get(col_email, ""))
    if email:
        return ("email", email)
    return None  # ni nom ni email : ligne conservee telle quelle


def fusionner(base, doublon, col_email, colonnes_emails_secondaires):
    """
    Fusionne `doublon` dans `base`, sans perte de donnee :
      - toute cellule vide de base est remplie par celle du doublon ;
      - un email different est range dans le premier emplacement email libre ;
      - Tag_CRM garde le tag le plus fort des deux.
    """
    # Le second email est traite avant le remplissage generique, sinon il
    # serait ecrase par la boucle de completion.
    email_base = normaliser(base.get(col_email, ""))
    email_doublon = normaliser(doublon.get(col_email, ""))

    if email_doublon and email_doublon != email_base:
        # Emails deja presents sur la ligne : on evite d'en ajouter un en double.
        deja = {normaliser(base.get(c, "")) for c in colonnes_emails_secondaires}
        deja.add(email_base)
        if email_doublon not in deja:
            for colonne in colonnes_emails_secondaires:
                if not (base.get(colonne) or "").strip():
                    base[colonne] = doublon.get(col_email, "")
                    break

    for colonne, valeur in doublon.items():
        if colonne == "Tag_CRM":
            continue
        if colonne == col_email:
            continue  # deja gere ci-dessus
        if not (base.get(colonne) or "").strip() and (valeur or "").strip():
            base[colonne] = valeur

    base["Tag_CRM"] = tag_le_plus_fort([base["Tag_CRM"], doublon["Tag_CRM"]])


# ---------------------------------------------------------------------------
# Programme principal
# ---------------------------------------------------------------------------

def main():
    source = sys.argv[1] if len(sys.argv) > 1 else SOURCE_DEFAUT
    sortie = sys.argv[2] if len(sys.argv) > 2 else SORTIE_DEFAUT

    # utf-8-sig : retire le BOM en lecture. Le fichier n'est jamais reecrit.
    with open(source, encoding="utf-8-sig", newline="") as f:
        lecteur = csv.DictReader(f, delimiter=DELIMITEUR)
        entetes = lecteur.fieldnames
        lignes = list(lecteur)

    # --- Detection des colonnes -------------------------------------------
    col_libelle = trouver_colonne(entetes, CANDIDATS_COLONNES["libelle"])
    col_prenom = trouver_colonne(entetes, CANDIDATS_COLONNES["prenom"])
    col_nom = trouver_colonne(entetes, CANDIDATS_COLONNES["nom"])
    col_email = trouver_colonne(entetes, CANDIDATS_COLONNES["email"])
    colonnes_emails_secondaires = [
        c for c in entetes
        if c != col_email and any(f in normaliser(c) for f in FRAGMENTS_EMAILS_SECONDAIRES)
    ]

    print("=== 1. INSPECTION ===")
    print("Fichier      : %s" % source)
    print("Encodage     : UTF-8 (BOM retire en lecture, reecrit en sortie)")
    print("Separateur   : %r" % DELIMITEUR)
    print("Lignes       : %d" % len(lignes))
    print("Colonnes     : %d" % len(entetes))
    print("Colonne libelles : %s" % col_libelle)
    print("Colonne prenom   : %s" % col_prenom)
    print("Colonne nom      : %s" % col_nom)
    print("Colonne email    : %s" % col_email)
    print("Emails secondaires disponibles : %s" % (", ".join(colonnes_emails_secondaires) or "aucun"))

    # --- Etape 2 : Tag_CRM -------------------------------------------------
    a_classer = Counter()
    for ligne in lignes:
        libelle = (ligne.get(col_libelle) or "").strip()
        tag = classer(libelle)
        ligne["Tag_CRM"] = tag
        if tag == "A_CLASSER":
            a_classer[libelle] += 1

    avant = len(lignes)
    tags_avant = Counter(l["Tag_CRM"] for l in lignes)

    # --- Etape 3 : dedoublonnage ------------------------------------------
    fusionnees = OrderedDict()   # cle -> ligne conservee
    sans_cle = []               # ni nom ni email : jamais fusionnees
    nb_fusions = 0

    for ligne in lignes:
        cle = cle_identite(ligne, col_prenom, col_nom, col_email)
        if cle is None:
            sans_cle.append(ligne)
            continue
        if cle in fusionnees:
            fusionner(fusionnees[cle], ligne, col_email, colonnes_emails_secondaires)
            nb_fusions += 1
        else:
            fusionnees[cle] = ligne

    resultat = list(fusionnees.values()) + sans_cle

    # --- Etape 4 : ecriture -----------------------------------------------
    entetes_sortie = list(entetes) + ["Tag_CRM"]
    # utf-8-sig en ecriture : ajoute le BOM, pour qu'Excel lise les accents.
    with open(sortie, "w", encoding="utf-8-sig", newline="") as f:
        ecrivain = csv.DictWriter(
            f, fieldnames=entetes_sortie, delimiter=DELIMITEUR, extrasaction="ignore"
        )
        ecrivain.writeheader()
        ecrivain.writerows(resultat)

    # --- Recapitulatif -----------------------------------------------------
    print()
    print("=== 2. TAG_CRM (avant dedoublonnage) ===")
    for tag in PRIORITE:
        if tags_avant.get(tag):
            print("%-10s %5d" % (tag, tags_avant[tag]))

    print()
    print("=== 3. DEDOUBLONNAGE ===")
    print("Lignes avant   : %d" % avant)
    print("Doublons fusionnes : %d" % nb_fusions)
    print("Lignes apres   : %d" % len(resultat))

    print()
    print("=== 4. TAG_CRM (final) ===")
    tags_apres = Counter(l["Tag_CRM"] for l in resultat)
    for tag in PRIORITE:
        if tags_apres.get(tag):
            print("%-10s %5d" % (tag, tags_apres[tag]))

    if a_classer:
        print()
        print("=== LIBELLES NON CLASSES (a trancher) ===")
        for libelle, n in a_classer.most_common():
            print("%5d  %s" % (n, libelle))
    else:
        print()
        print("Aucun libelle en A_CLASSER.")

    print()
    print("Fichier ecrit : %s" % sortie)
    print("Fichier source inchange : %s" % source)


if __name__ == "__main__":
    main()
