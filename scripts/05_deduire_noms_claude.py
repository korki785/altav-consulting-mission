#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase 2 de la deduction de noms : les cas que la regle deterministe ne sait
pas trancher, soumis a Claude.

`deduire_noms.py` traite les adresses ou un separateur isole deux tokens dont
un seul est un prenom connu de la base. Restent :
  - les local-parts a separateur dont aucun token n'est dans le dictionnaire
    (lauriano.latifou@, rasmane.zongo@) melanges a du bruit (beicg.sarl@) ;
  - les blocs colles sans separateur (juniorkoudoyor@), que la regle refuse
    par construction car plusieurs coupures sont valides.

Un modele tranche ces deux familles la ou une regex ne peut pas. La consigne
est stricte : remplir uniquement si certain, sinon renvoyer des chaines vides.

Entree  : contacts_wix_tagges.csv
Sortie  : contacts_wix_tagges.csv (+ contacts_wix_tagges.bak.csv)
          Origine_nom = DEDUIT_CLAUDE sur les lignes enrichies.

Idempotent : ne retraite jamais une ligne deja nommee.

Usage :
    python3 deduire_noms_claude.py --sample 10   # test, aucune ecriture
    python3 deduire_noms_claude.py --dry-run     # tout, aucune ecriture
    python3 deduire_noms_claude.py               # applique
    python3 deduire_noms_claude.py --model claude-sonnet-5
"""

import csv
import json
import os
import re
import shutil
import sys
import unicodedata
from collections import Counter

import chemins

CIBLE = chemins.TRAVAIL / "contacts_wix_tagges.csv"
SAUVEGARDE = chemins.SAUVEGARDES / "contacts_wix_tagges.bak.csv"
DELIMITEUR = ";"

MODELE_DEFAUT = "claude-opus-4-8"
TAILLE_LOT = 40          # local-parts par requete
MAX_TOKENS = 8000

# Fichiers ou chercher la cle si elle n'est pas dans l'environnement.
FICHIERS_ENV = chemins.FICHIERS_ENV

COLONNE_EMAIL = re.compile(r"^e-?mail\s*1?$")

SYSTEME = """Tu extrais un prenom et un nom de famille depuis la partie locale d'une adresse email (ce qui precede le @).

REGLE ABSOLUE : ne remplis que si tu es certain. Dans le moindre doute, renvoie des chaines vides. Une case vide ne coute rien ; un faux prenom dans un mailing de prospection est une erreur visible par le destinataire.

Renvoie des chaines vides ("") pour prenom ET nom quand l'adresse est :
- une raison sociale ou une marque (beicg.sarl, anapex.afrique, ivoire.forage, transli.benin)
- un service ou une fonction (drh.confidentiel, dft.formation, contact, info, direction)
- un sigle ou un acronyme non decodable (lnd.divb, caefc.consulting)
- un pseudo ou un identifiant (saveandearnwithsarahp, bitumen.arbeiter226)
- un decoupage ambigu, ou plusieurs coupures sont defendables

Remplis quand le nom d'une personne est lisible sans ambiguite :
- separateur explicite : lauriano.latifou -> Lauriano / Latifou
- ordre inverse, frequent : sayegh.bilal -> Bilal / Sayegh (Bilal est le prenom)
- bloc colle SEULEMENT si la coupure est evidente : rogeragass -> Roger / Agass

Attention aux blocs colles : ils sont souvent piegeux. paulemilekeita se coupe
en Paul Emile Keita, pas en Paule Milekeita. issakaabdoulaye est Issaka
Abdoulaye, pas Issa Kaabdoulaye. Si tu hesites entre deux coupures, renvoie vide.

Si seul le prenom est identifiable et que le reste est un fragment commercial
ou un sigle, renvoie le prenom et un nom vide.

Le public est majoritairement francophone : France, Belgique, Suisse, Quebec,
Afrique de l'Ouest et centrale (Burundi, RDC, Cameroun, Senegal, Cote d'Ivoire,
Benin, Togo, Mali, Burkina Faso, Niger, Tchad, Gabon, Madagascar), Haiti et
Antilles. Les prenoms et patronymes de ces regions sont attendus.

ACCENTS : les adresses email ne portent jamais d'accent, mais les prenoms
francophones courants en ont. Restitue l'orthographe usuelle du prenom :
nadege -> Nadege devient Nadege ecrit "Nadege" avec accent grave (Nadege),
andree -> Andree, eugene -> Eugene, celine -> Celine, herve -> Herve,
josue -> Josue, theogene -> Theogene, felicite -> Felicite, arsene -> Arsene.
Autrement dit : ecris le prenom comme il s'ecrit reellement en francais, avec
ses accents. N'ajoute pas d'accent a un prenom non francophone (Ousmane,
Mamadou, Tarek, Prosper, Boniface n'en prennent pas).

Pour les NOMS de famille, ne mets un accent que s'il est certain. Dans le doute,
laisse le nom sans accent : un patronyme mal accentue est plus visible qu'un
patronyme neutre.

Ne corrige pas l'orthographe d'un patronyme : reprends-le tel qu'il apparait
dans l'adresse. Retire seulement les chiffres parasites en fin de token
(nonguierma99 -> Nonguierma)."""

SCHEMA = {
    "type": "object",
    "properties": {
        "resultats": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "local_part": {"type": "string"},
                    "prenom": {"type": "string"},
                    "nom": {"type": "string"},
                },
                "required": ["local_part", "prenom", "nom"],
                "additionalProperties": False,
            },
        }
    },
    "required": ["resultats"],
    "additionalProperties": False,
}


def normaliser(texte):
    texte = unicodedata.normalize("NFD", (texte or "").lower())
    return "".join(c for c in texte if unicodedata.category(c) != "Mn").strip()


def charger_cle():
    """Cle depuis l'environnement, sinon depuis un .env connu. Jamais affichee."""
    cle = os.environ.get("ANTHROPIC_API_KEY")
    if cle:
        return cle, "environnement"
    for chemin in FICHIERS_ENV:
        if not os.path.exists(chemin):
            continue
        with open(chemin, encoding="utf-8") as f:
            for ligne in f:
                if ligne.strip().startswith("ANTHROPIC_API_KEY"):
                    valeur = ligne.split("=", 1)[1].strip().strip("'\"")
                    if valeur:
                        return valeur, chemin
    raise SystemExit(
        "ANTHROPIC_API_KEY introuvable (environnement et %s)." % ", ".join(FICHIERS_ENV)
    )


def trouver_colonne(entetes, fragments, motif=None):
    if motif is not None:
        for entete in entetes:
            if motif.match(normaliser(entete)):
                return entete
    for fragment in fragments:
        for entete in entetes:
            if fragment in normaliser(entete):
                return entete
    raise SystemExit("Colonne introuvable (%s)." % fragments)


def local_part(email):
    """Partie locale nettoyee, ou None si inexploitable."""
    brut = (email or "").split("@")[0].strip()
    if not brut or len(brut) < 4:
        return None
    return brut


def interroger(client, modele, lot):
    """Envoie un lot de local-parts, retourne {local_part: (prenom, nom)}."""
    liste = "\n".join(lot)
    reponse = client.messages.create(
        model=modele,
        max_tokens=MAX_TOKENS,
        system=SYSTEME,
        output_config={"format": {"type": "json_schema", "schema": SCHEMA}},
        messages=[{
            "role": "user",
            "content": (
                "Traite ces %d parties locales d'adresses email. "
                "Renvoie une entree par ligne, dans le meme ordre, en reprenant "
                "la valeur exacte dans local_part.\n\n%s" % (len(lot), liste)
            ),
        }],
    )
    texte = next(b.text for b in reponse.content if b.type == "text")
    donnees = json.loads(texte)
    sortie = {}
    for item in donnees.get("resultats", []):
        cle = item.get("local_part", "").strip()
        if cle:
            sortie[cle] = (item.get("prenom", "").strip(), item.get("nom", "").strip())
    return sortie, reponse.usage


def main():
    args = sys.argv[1:]
    dry_run = "--dry-run" in args
    modele = MODELE_DEFAUT
    if "--model" in args:
        modele = args[args.index("--model") + 1]
    echantillon = None
    if "--sample" in args:
        echantillon = int(args[args.index("--sample") + 1])
        dry_run = True  # un echantillon n'ecrit jamais

    with open(CIBLE, encoding="utf-8-sig", newline="") as f:
        lecteur = csv.DictReader(f, delimiter=DELIMITEUR)
        entetes = lecteur.fieldnames
        lignes = list(lecteur)

    col_prenom = trouver_colonne(entetes, ["prenom", "first name"])
    col_nom = trouver_colonne(entetes, ["nom de famille", "last name"])
    col_email = trouver_colonne(entetes, ["e-mail", "email"], motif=COLONNE_EMAIL)

    # Uniquement les lignes encore sans nom.
    candidats = []
    for ligne in lignes:
        if (ligne.get(col_prenom) or "").strip() or (ligne.get(col_nom) or "").strip():
            continue
        lp = local_part(ligne.get(col_email))
        if lp:
            candidats.append((ligne, lp))

    if echantillon:
        candidats = candidats[:echantillon]

    print("=== PHASE 2 : deduction par Claude ===")
    print("Modele    : %s" % modele)
    print("Candidats : %d" % len(candidats))
    if echantillon:
        print("Mode      : ECHANTILLON de %d, aucune ecriture" % echantillon)
    elif dry_run:
        print("Mode      : DRY-RUN, aucune ecriture")
    print()

    cle, source = charger_cle()
    print("Cle API   : chargee depuis %s" % source)

    import anthropic
    client = anthropic.Anthropic(api_key=cle)

    resultats = {}
    tok_in = tok_out = 0
    lots = [candidats[i:i + TAILLE_LOT] for i in range(0, len(candidats), TAILLE_LOT)]
    for i, lot in enumerate(lots, 1):
        parts = [lp for _, lp in lot]
        try:
            sortie, usage = interroger(client, modele, parts)
        except Exception as e:                      # noqa: BLE001
            print("  lot %d/%d : ECHEC (%s) - ignore" % (i, len(lots), e))
            continue
        resultats.update(sortie)
        tok_in += usage.input_tokens
        tok_out += usage.output_tokens
        print("  lot %d/%d traite (%d items)" % (i, len(lots), len(parts)))

    # --- Application ------------------------------------------------------
    enrichis = []
    for ligne, lp in candidats:
        prenom, nom = resultats.get(lp, ("", ""))
        if not prenom:
            continue        # rien de certain : on laisse vide
        enrichis.append((ligne, lp, prenom, nom))
        if not dry_run:
            ligne[col_prenom] = prenom
            ligne[col_nom] = nom
            ligne["Origine_nom"] = "DEDUIT_CLAUDE"

    print()
    print("=== DEDUCTIONS (%d / %d) ===" % (len(enrichis), len(candidats)))
    print("%-40s | %-14s | %s" % ("LOCAL-PART", "PRENOM", "NOM"))
    print("-" * 76)
    for _, lp, prenom, nom in enrichis:
        print("%-40s | %-14s | %s" % (lp[:40], prenom, nom or "(vide)"))

    ignores = len(candidats) - len(enrichis)
    print()
    print("=== BILAN ===")
    print("Enrichis          : %d" % len(enrichis))
    print("  dont nom vide   : %d" % sum(1 for _, _, _, n in enrichis if not n))
    print("Laisses vides     : %d" % ignores)
    cout = tok_in / 1e6 * 5 + tok_out / 1e6 * 25 if "opus" in modele else tok_in / 1e6 * 2 + tok_out / 1e6 * 10
    print("Tokens            : %d entree / %d sortie" % (tok_in, tok_out))
    print("Cout de ce run    : ~%.2f USD" % cout)

    if dry_run:
        print()
        print("Aucune ecriture. Fichier inchange.")
        return

    shutil.copy2(CIBLE, SAUVEGARDE)
    with open(CIBLE, "w", encoding="utf-8-sig", newline="") as f:
        ecrivain = csv.DictWriter(
            f, fieldnames=entetes, delimiter=DELIMITEUR, extrasaction="ignore"
        )
        ecrivain.writeheader()
        ecrivain.writerows(lignes)

    print()
    origines = Counter(l.get("Origine_nom") or "(vide)" for l in lignes)
    for cle_o, n in origines.most_common():
        print("  %-15s %5d" % (cle_o, n))
    print()
    print("Ecrit : %s" % CIBLE)
    print("Sauvegarde : %s" % SAUVEGARDE)


if __name__ == "__main__":
    main()
