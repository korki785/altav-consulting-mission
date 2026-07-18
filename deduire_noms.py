#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Deduit prenom et nom depuis l'adresse email, quand la deduction est certaine.

70 % des contacts de l'export Wix n'ont ni prenom ni nom, seulement un email.
Beaucoup d'adresses portent pourtant le nom en clair : susana.scaveli@gmail.com.
Ce script extrait ces noms UNIQUEMENT quand la deduction ne fait aucun doute,
et ignore tout le reste. Mieux vaut une case vide qu'un faux prenom dans un
publipostage.

Le dictionnaire de prenoms est construit depuis le fichier lui-meme (les lignes
deja nommees), donc sans dependance externe et calibre sur la base reelle.

Entree  : contacts_wix_tagges.csv  (sauvegarde avant reecriture)
Sortie  : contacts_wix_tagges.csv (+ contacts_wix_tagges.bak.csv)

Le script est idempotent et re-executable.

Usage :
    python3 deduire_noms.py --dry-run   # affiche les deductions, n'ecrit rien
    python3 deduire_noms.py             # applique
"""

import csv
import re
import shutil
import sys
import unicodedata
from collections import Counter

CIBLE = "contacts_wix_tagges.csv"
SAUVEGARDE = "contacts_wix_tagges.bak.csv"
DELIMITEUR = ";"

# Colonnes attendues (detection tolerante plus bas).
FRAGMENTS_PRENOM = ["prenom", "first name"]
FRAGMENTS_NOM = ["nom de famille", "last name"]

# Motif ancre : "E-mail 1", pas "Statut d'abonne aux e-mails".
COLONNE_EMAIL = re.compile(r"^e-?mail\s*1?$")

# Tokens qui ne sont jamais un nom de personne : roles, services, formes
# juridiques, mots-cles metier presents dans les adresses de la base.
BLOCKLIST = {
    "contact", "info", "infos", "admin", "direction", "secretariat",
    "service", "bureau", "commercial", "rh", "drh", "dg", "ceo",
    "president", "manager", "test", "demo", "hello", "support", "compta",
    "sarl", "consulting", "experts", "formation", "logistique",
    "afrique", "ubuntu", "altav", "www", "b2b", "team", "agency",
    "business", "entreprise", "societe", "groupe",
}

# Fragments commerciaux : quand ils apparaissent dans le token candidat au NOM,
# c'est une raison sociale ou un suffixe metier, pas un patronyme
# (eric.haroinvest@, abdoul.budget@, nathan.assistanceetservices@).
# Le prenom reste exploitable, seul le nom est ecarte.
FRAGMENTS_COMMERCIAUX = [
    "invest", "budget", "assistance", "service", "enterprise", "ticket",
    "consult", "immo", "digital", "finance", "market", "shop", "store",
    "avocat", "conseil", "transport", "logistic",
]

# Suffixe "pro" colle a un patronyme : zitounipro, agouapro. Teste en fin de
# token uniquement, et sur un token assez long, pour ne pas casser les prenoms
# et noms qui commencent par "pro" (Prosper, Proteau...).
SUFFIXE_PRO = "pro"

VOYELLES = set("aeiouy")

# Seuil applique UNIQUEMENT a l'ordre inverse (nom.prenom@).
#
# L'ordre direct (prenom.nom@) est la convention majoritaire : une seule
# occurrence du prenom suffit a le confirmer. L'inversion, elle, repose
# entierement sur le dictionnaire, donc un singleton parasite y produit une
# erreur : "kayembe" (1 occurrence en Prenom) inversait reagan.kayembe@ en
# "Kayembe Reagan". Exiger 2 occurrences pour inverser coute quelques
# deductions et supprime cette classe d'erreur.
#
# Un seuil global de 2 a ete teste : il faisait perdre 67 deductions correctes
# et en cassait de nouvelles (virginia.king@, ou "king" apparait 2 fois et
# "virginia" 1 seule). Ne pas generaliser ce seuil a l'ordre direct.
SEUIL_INVERSION = 2


# ---------------------------------------------------------------------------
# Utilitaires
# ---------------------------------------------------------------------------

def normaliser(texte):
    """Minuscules, sans accents, espaces externes retires."""
    texte = unicodedata.normalize("NFD", (texte or "").lower())
    return "".join(c for c in texte if unicodedata.category(c) != "Mn").strip()


def trouver_colonne(entetes, fragments, motif=None):
    """Premier entete correspondant au motif, sinon contenant l'un des fragments."""
    if motif is not None:
        for entete in entetes:
            if motif.match(normaliser(entete)):
                return entete
    for fragment in fragments:
        for entete in entetes:
            if fragment in normaliser(entete):
                return entete
    raise SystemExit(
        "Colonne introuvable (%s).\nEntetes : %s" % (fragments, ", ".join(entetes))
    )


def ressemble_a_un_nom(token):
    """
    Un patronyme plausible : au moins 4 lettres et au moins une voyelle.

    Ecarte les sigles colles (bgrh, dft, lnd) que la blocklist ne peut pas
    enumerer, ainsi que les fragments commerciaux (haroinvest, budget,
    assistanceetservices) et le suffixe metier "pro" (zitounipro, agouapro).

    Dans tous ces cas on garde le prenom et on laisse le nom vide plutot que
    d'ecrire une valeur fausse : une sequence peut dire "Bonjour Moussa" sans
    risque, "Moussa Bgrh" est visiblement faux.
    """
    if len(token) < 4 or not any(c in VOYELLES for c in token):
        return False
    if any(frag in token for frag in FRAGMENTS_COMMERCIAUX):
        return False
    if token.endswith(SUFFIXE_PRO) and len(token) >= 7:
        return False
    return True


# ---------------------------------------------------------------------------
# Etape 1 : dictionnaire de prenoms construit depuis le fichier
# ---------------------------------------------------------------------------

def construire_dictionnaire(lignes, col_prenom):
    """
    Retourne (prenoms_connus, table_accents).

    Les prenoms viennent des lignes deja nommees de l'export : le dictionnaire
    reflete donc la base reelle (prenoms burundais, ivoiriens, senegalais)
    sans gazetteer externe.
    """
    prenoms = Counter()
    accents = {}
    for ligne in lignes:
        brut = ligne.get(col_prenom) or ""
        for token in re.split(r"[^a-zA-ZÀ-ÿ]+", brut):
            if len(token) < 3:
                continue
            cle = normaliser(token)
            prenoms[cle] += 1
            # Memorise la forme accentuee pour la restituer plus tard :
            # l'email donne "celine", la base contient "Céline".
            if any(c in token for c in "éèêëàâäîïôöûüçÉÈÊÀÂÎÏÔÛÜÇ"):
                accents.setdefault(cle, token.capitalize())
    return prenoms, accents


# ---------------------------------------------------------------------------
# Etape 2 : deduction
# ---------------------------------------------------------------------------

def deduire(email, prenoms, accents):
    """
    Retourne (prenom, nom, motif) ou None si la deduction n'est pas certaine.

    `nom` peut valoir "" quand le token ne ressemble pas a un patronyme.
    """
    local = normaliser((email or "").split("@")[0])
    local = re.sub(r"[0-9]+$", "", local)  # axel.nonguierma99 -> axel.nonguierma

    parts = [p for p in re.split(r"[._-]", local) if p]
    if len(parts) != 2:
        return None
    if any(len(p) < 3 for p in parts):
        return None
    if any(p in BLOCKLIST for p in parts):
        return None

    a, b = parts
    freq_a, freq_b = prenoms.get(a, 0), prenoms.get(b, 0)

    # Exactement un des deux tokens est un prenom connu : cela determine
    # l'ordre sans heuristique de position. droussi.abdou -> Abdou Droussi.
    if freq_a and not freq_b:
        prenom_tok, nom_tok, motif = a, b, "direct"
    elif freq_b and not freq_a:
        # Inversion : exiger un prenom bien atteste (voir SEUIL_INVERSION).
        if freq_b < SEUIL_INVERSION:
            return None
        prenom_tok, nom_tok, motif = b, a, "inverse"
    else:
        return None  # deux prenoms connus (ambigu) ou aucun -> on ne devine pas

    prenom = accents.get(prenom_tok, prenom_tok.capitalize())
    if ressemble_a_un_nom(nom_tok):
        nom = accents.get(nom_tok, nom_tok.capitalize())
    else:
        nom = ""  # sigle : prenom seul
        motif += " (nom ecarte)"

    return prenom, nom, motif


# ---------------------------------------------------------------------------
# NOTE : les blocs colles ne sont volontairement PAS decoupes.
#
# juniorkoudoyor@, paulemilekeita@ ... : sans separateur, plusieurs coupures
# sont valides et rien ne permet de trancher. Un test sur les donnees reelles
# donnait "Paule Milekeita" au lieu de "Paul Emile Keita" et "Issa Kaabdoulaye"
# au lieu de "Issaka Abdoulaye". Un faux prenom dans une sequence de
# prospection coute plus cher que l'absence de prenom.
# Ne pas "ameliorer" ce script en ajoutant ce decoupage.
# ---------------------------------------------------------------------------


def main():
    dry_run = "--dry-run" in sys.argv

    with open(CIBLE, encoding="utf-8-sig", newline="") as f:
        lecteur = csv.DictReader(f, delimiter=DELIMITEUR)
        entetes = lecteur.fieldnames
        lignes = list(lecteur)

    col_prenom = trouver_colonne(entetes, FRAGMENTS_PRENOM)
    col_nom = trouver_colonne(entetes, FRAGMENTS_NOM)
    col_email = trouver_colonne(entetes, ["e-mail", "email"], motif=COLONNE_EMAIL)

    prenoms, accents = construire_dictionnaire(lignes, col_prenom)

    print("=== DICTIONNAIRE ===")
    print("Prenoms connus (issus du fichier) : %d" % len(prenoms))
    print("Prenoms accentues restituables    : %d" % len(accents))
    print()

    deductions = []   # (ligne, prenom, nom, motif)
    sans_nom = 0

    for ligne in lignes:
        deja_nomme = bool(
            (ligne.get(col_prenom) or "").strip() or (ligne.get(col_nom) or "").strip()
        )
        if deja_nomme:
            # Ne jamais ecraser une valeur venue de l'export Wix.
            ligne["Origine_nom"] = ligne.get("Origine_nom") or "WIX"
            continue

        sans_nom += 1
        resultat = deduire(ligne.get(col_email), prenoms, accents)
        if resultat is None:
            ligne["Origine_nom"] = ligne.get("Origine_nom") or ""
            continue

        prenom, nom, motif = resultat
        deductions.append((ligne, prenom, nom, motif))
        if not dry_run:
            ligne[col_prenom] = prenom
            ligne[col_nom] = nom
            ligne["Origine_nom"] = "DEDUIT_EMAIL"

    # --- Affichage des deductions ----------------------------------------
    print("=== DEDUCTIONS (%d) ===" % len(deductions))
    print("%-38s | %-14s | %-16s | %s" % ("EMAIL", "PRENOM", "NOM", "ORDRE"))
    print("-" * 92)
    for ligne, prenom, nom, motif in deductions:
        print("%-38s | %-14s | %-16s | %s"
              % (ligne.get(col_email), prenom, nom or "(vide)", motif))

    # --- Controles automatiques ------------------------------------------
    fautifs = [
        (l.get(col_email), p, n)
        for l, p, n, _ in deductions
        if normaliser(p) in BLOCKLIST or (n and normaliser(n) in BLOCKLIST)
    ]
    noms_vides = sum(1 for _, _, n, _ in deductions if not n)

    print()
    print("=== CONTROLES ===")
    print("Lignes sans nom au depart      : %d" % sans_nom)
    print("Deductions certaines           : %d" % len(deductions))
    print("  dont ordre inverse           : %d"
          % sum(1 for _, _, _, m in deductions if m.startswith("inverse")))
    print("  dont nom ecarte (prenom seul): %d" % noms_vides)
    print("Toujours sans nom              : %d" % (sans_nom - len(deductions)))
    print("Valeurs en blocklist           : %d %s"
          % (len(fautifs), "<-- ANOMALIE" if fautifs else "(ok)"))
    for email, p, n in fautifs:
        print("   %s -> %s %s" % (email, p, n))

    # --- Ecriture ---------------------------------------------------------
    if dry_run:
        print()
        print("--dry-run : AUCUNE ecriture. Fichier inchange.")
        return

    entetes_sortie = list(entetes)
    if "Origine_nom" not in entetes_sortie:
        entetes_sortie.append("Origine_nom")

    shutil.copy2(CIBLE, SAUVEGARDE)

    with open(CIBLE, "w", encoding="utf-8-sig", newline="") as f:
        ecrivain = csv.DictWriter(
            f, fieldnames=entetes_sortie, delimiter=DELIMITEUR, extrasaction="ignore"
        )
        ecrivain.writeheader()
        ecrivain.writerows(lignes)

    print()
    print("=== RESULTAT ===")
    print("Lignes ecrites : %d" % len(lignes))
    origines = Counter(l.get("Origine_nom") or "(vide)" for l in lignes)
    for cle, n in origines.most_common():
        print("  %-14s %5d" % (cle, n))
    print()
    print("Ecrit : %s" % CIBLE)
    print("Sauvegarde de la version precedente : %s" % SAUVEGARDE)


if __name__ == "__main__":
    main()
