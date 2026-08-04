#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Nettoyage des noms declares par Wix.

Les noms DEDUIT_EMAIL et DEDUIT_CLAUDE sont propres : ils ont ete produits par
regle ou par modele, puis relus. Les noms d'origine WIX ne l'ont jamais ete --
ils ont ete crus fiables parce que declares. 917 des 2 211 sont abimes.

Quatre operations :

1. CASSE : "DIEDHIOU" / "estelle koffi" -> Titlecase. Gere les particules
   (de, van, del), les traits d'union (Simon-Pierre) et les apostrophes
   (N'Diaye). Ces noms serviront a personnaliser des emails : "Bonjour
   Jean-Pierre DUPONT" se lit comme un cri.

2. INVERSION : DESACTIVEE. Option --inverser, a ne pas utiliser.

   Tentative abandonnee apres mesure. La regle testee etait : ordre des deux
   valeurs dans le local-part de l'email, avec veto par dictionnaire de
   prenoms. Sur 94 inversions proposees, environ la moitie CASSAIENT des
   fiches deja correctes :

       nitungaferdinand@    Ferdinand / NITUNGA  -> NITUNGA / Ferdinand  FAUX
       niyonkuruphilbert40@ Philbert / Niyonkuru -> Niyonkuru / Philbert FAUX
       sallelimane216@      Elimane / SALL       -> SALL / Elimane       FAUX

   Deux causes, toutes deux structurelles :

   a) La position ne dit rien. Une grande partie de la base ecrit son email
      nom-d'abord (convention courante au Burundi et en Afrique de l'Ouest).
      Les deux conventions coexistent, aucune n'est majoritaire.

   b) Le dictionnaire ne peut pas servir de veto ici : 84% des prenoms de la
      base n'apparaissent qu'une ou deux fois. Il n'en reconnait que 352 sur
      2 145. Ferdinand, Philbert, Zephirin, Alix n'ont pas ete reconnus.

   C'est le meme piege que celui documente dans JOURNAL.md pour
   deduire_noms.py : "resout l'ordre inverse sans heuristique de position".
   La detection d'inversion passe par un jugement au cas par cas, pas par une
   regle. Ne pas "ameliorer" ce script en reactivant l'option.

3. TOKEN REPETE : "Claire Cornic" / "cornic" -> le doublon est retire du
   patronyme.

4. DECHET : email dans le champ nom, chiffres, contacts de test Wix.
   Champs vides -- une case vide vaut mieux qu'une fausse valeur.

Les operations 2, 3 et 4 ne s'appliquent qu'aux lignes Origine_nom = WIX.
L'operation 1 s'applique a tout le monde (sans effet sur ce qui est deja propre).

Entree  : contacts_hubspot.csv
Sortie  : contacts_hubspot.csv (+ contacts_hubspot.noms.bak.csv)

Idempotent : une seconde execution ne change plus rien.

Usage :
    python3 nettoyer_noms.py --dry-run              # tout, sans ecrire
    python3 nettoyer_noms.py --dry-run --limite 50  # 50 par categorie
    python3 nettoyer_noms.py                        # applique
    python3 nettoyer_noms.py --majuscules-patronyme # variante DUPONT
"""

import collections
import csv
import re
import shutil
import sys
import unicodedata

import chemins

CIBLE = chemins.TRAVAIL / "contacts_hubspot.csv"
SAUVEGARDE = chemins.SAUVEGARDES / "contacts_hubspot.noms.bak.csv"
DELIMITEUR = ";"

COL_PRENOM = "Prénom"
COL_NOM = "Nom de famille"
COL_EMAIL = "E-mail 1"
COL_ORIGINE = "Origine_nom"

# Particules qui restent en minuscules, sauf en tete de champ.
PARTICULES = {
    "de", "du", "des", "da", "das", "do", "dos", "di", "della", "del",
    "la", "le", "les", "van", "von", "der", "den", "ter", "ten", "el", "al",
}

# Un patronyme credible : au moins 4 lettres et une voyelle. Meme garde-fou
# que dans deduire_noms.py -- ecarte les sigles (bgrh, dft).
def credible(token):
    t = re.sub(r"[^a-z]", "", nrm(token))
    return len(t) >= 4 and any(v in t for v in "aeiouy")


def nrm(texte):
    texte = unicodedata.normalize("NFD", (texte or "").lower())
    return "".join(c for c in texte if unicodedata.category(c) != "Mn").strip()


def cle(texte):
    return re.sub(r"[^a-z]", "", nrm(texte))


# ---------------------------------------------------------------------------
# 1. Casse
# ---------------------------------------------------------------------------

def titre_mot(mot):
    """Capitalise un mot en respectant traits d'union et apostrophes."""
    for sep in ("-", "'", "’"):
        if sep in mot:
            return sep.join(titre_mot(p) for p in mot.split(sep))
    if not mot:
        return mot
    return mot[0].upper() + mot[1:].lower()


def normaliser_casse(valeur, majuscules=False, patronyme=False):
    """Titlecase. Les particules restent minuscules, y compris en tete du champ
    patronyme : "de Mane" est la forme correcte, pas "De Mane"."""
    mots = (valeur or "").split()
    sortie = []
    for i, mot in enumerate(mots):
        if majuscules:
            sortie.append(mot.upper())
        elif nrm(mot) in PARTICULES and (i > 0 or patronyme):
            sortie.append(nrm(mot))
        else:
            sortie.append(titre_mot(mot))
    return " ".join(sortie)


# ---------------------------------------------------------------------------
# Dictionnaire de prenoms, construit depuis le fichier
# ---------------------------------------------------------------------------

def construire_dictionnaire(lignes):
    prenoms, patronymes = collections.Counter(), collections.Counter()
    for ligne in lignes:
        for t in nrm(ligne.get(COL_PRENOM) or "").split():
            if len(t) > 2:
                prenoms[t] += 1
        for t in nrm(ligne.get(COL_NOM) or "").split():
            if len(t) > 2:
                patronymes[t] += 1
    return prenoms, patronymes


def main():
    dry_run = "--dry-run" in sys.argv
    majuscules = "--majuscules-patronyme" in sys.argv
    inverser = "--inverser" in sys.argv
    limite = None
    if "--limite" in sys.argv:
        limite = int(sys.argv[sys.argv.index("--limite") + 1])

    with open(CIBLE, encoding="utf-8-sig", newline="") as f:
        lecteur = csv.DictReader(f, delimiter=DELIMITEUR)
        entetes = lecteur.fieldnames
        lignes = list(lecteur)

    prenoms, patronymes = construire_dictionnaire(lignes)

    def est_prenom(t):
        return prenoms[t] >= 3 and prenoms[t] > patronymes[t] * 2

    journaux = collections.OrderedDict(
        (k, []) for k in ("DECHET", "INVERSION", "TOKEN REPETE", "CASSE")
    )

    for ligne in lignes:
        wix = (ligne.get(COL_ORIGINE) or "") == "WIX"
        p0, n0 = (ligne.get(COL_PRENOM) or "").strip(), (ligne.get(COL_NOM) or "").strip()
        if not p0 and not n0:
            continue
        p, n = p0, n0
        email = ligne.get(COL_EMAIL) or ""

        # --- 4. Dechet ----------------------------------------------------
        if wix:
            complet = ("%s %s" % (p, n)).strip()
            if ("@" in complet or re.search(r"\d", complet)
                    or nrm(p).startswith("contact test")):
                journaux["DECHET"].append((email, p0, n0, "", ""))
                ligne[COL_PRENOM], ligne[COL_NOM] = "", ""
                continue
            # "X" / "XX" : bouchon saisi dans les formulaires Wix. Ne vider que
            # le champ concerne -- le prenom d'a cote est valide.
            if nrm(n) in ("x", "xx"):
                journaux["DECHET"].append((email, p0, n0, p, ""))
                n = ""
            if nrm(p) in ("x", "xx"):
                journaux["DECHET"].append((email, p0, n0, "", n))
                p = ""

        # --- 2. Inversion (DESACTIVEE PAR DEFAUT) ---------------------------
        # Ne PAS reactiver sans lire le commentaire en tete de fichier.
        # La regle produit ~50% de faux positifs : elle casse les fiches
        # correctes des gens qui ecrivent leur email nom-d'abord, convention
        # majoritaire au Burundi et en Afrique de l'Ouest.
        if inverser and wix and p and n:
            cp, cn = cle(p), cle(n)
            loc = re.sub(r"[^a-z]", "", nrm(email.split("@")[0]))
            if len(cp) >= 4 and len(cn) >= 4 and cp in loc and cn in loc:
                if loc.index(cn) < loc.index(cp):
                    toks = [t for t in nrm(p).split() if len(t) > 2]
                    if not (toks and any(est_prenom(t) for t in toks)):
                        p, n = n, p
                        journaux["INVERSION"].append((email, p0, n0, p, n))

        # --- 3. Token repete ------------------------------------------------
        # Motif dominant : le champ Prenom porte le nom COMPLET et le champ Nom
        # repete le patronyme ("Claire Cornic" / "cornic"). On retire le
        # doublon du PRENOM et on garde le patronyme, jamais l'inverse --
        # amputer le champ Nom detruirait la seule donnee sure de la ligne.
        if wix and p and n:
            cn = {cle(t) for t in n.split() if cle(t)}
            restants = [t for t in p.split() if cle(t) not in cn]
            if cn and restants and len(restants) != len(p.split()):
                avant_p, avant_n = p, n
                p = " ".join(restants)
                journaux["TOKEN REPETE"].append((email, avant_p, avant_n, p, n))
            # Cas miroir : le patronyme repete le prenom ("Michel" /
            # "LAPIERRE Michel"). On retire le doublon du champ Nom, a
            # condition qu'il en reste quelque chose.
            elif cle(p) != cle(n):
                cp = {cle(t) for t in p.split() if cle(t)}
                reste = [t for t in n.split() if cle(t) not in cp]
                if cp and reste and len(reste) != len(n.split()):
                    avant_p, avant_n = p, n
                    n = " ".join(reste)
                    journaux["TOKEN REPETE"].append((email, avant_p, avant_n, p, n))
            # Prenom et Nom strictement identiques : garder le prenom, vider le
            # patronyme. cle() doit etre non vide, sinon deux ecritures non
            # latines (cyrillique) se comparent comme egales a tort.
            elif cle(p) and cle(p) == cle(n):
                avant_p, avant_n = p, n
                n = ""
                journaux["TOKEN REPETE"].append((email, avant_p, avant_n, p, n))

        # --- 1. Casse -------------------------------------------------------
        np_ = normaliser_casse(p)
        nn_ = normaliser_casse(n, majuscules, patronyme=True)
        if (np_, nn_) != (p, n):
            journaux["CASSE"].append((email, p, n, np_, nn_))
        p, n = np_, nn_

        ligne[COL_PRENOM], ligne[COL_NOM] = p, n

    # --- Rapport ------------------------------------------------------------
    total = 0
    for nom_cat, entrees in journaux.items():
        total += len(entrees)
        print("=" * 100)
        print("%s : %d contacts%s" % (
            nom_cat, len(entrees),
            "" if limite is None or len(entrees) <= limite else "  (affichage limite a %d)" % limite,
        ))
        print("=" * 100)
        print("%-32s %-21s|%-21s -> %-19s|%s" % ("EMAIL", "PRENOM AVANT", "NOM AVANT", "PRENOM APRES", "NOM APRES"))
        print("-" * 100)
        for email, ap, an, np_, nn_ in entrees[:limite]:
            print("%-32s %-21s|%-21s -> %-19s|%s" % (
                email[:32], ap[:21], an[:21],
                (np_ or "(vide)")[:19], nn_ or "(vide)",
            ))
        print()

    print("TOTAL : %d modifications sur %d contacts" % (total, len(lignes)))
    print("Style patronyme : %s" % ("MAJUSCULES" if majuscules else "Titlecase"))

    if dry_run:
        print()
        print("--dry-run : AUCUNE ecriture. Fichier inchange.")
        return

    shutil.copy2(CIBLE, SAUVEGARDE)
    with open(CIBLE, "w", encoding="utf-8-sig", newline="") as f:
        ecrivain = csv.DictWriter(
            f, fieldnames=entetes, delimiter=DELIMITEUR, extrasaction="ignore"
        )
        ecrivain.writeheader()
        ecrivain.writerows(lignes)

    print()
    print("Ecrit      : %s" % CIBLE)
    print("Sauvegarde : %s" % SAUVEGARDE)


if __name__ == "__main__":
    main()
