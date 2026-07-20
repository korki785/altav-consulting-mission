#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Verification de l'attribution prenom / nom sur les noms declares par Wix.

Le probleme : dans l'export Wix, prenom et nom sont parfois intervertis.
"lorianelacomme@" porte Prenom=Lacomme, Nom=Loriane.

Pourquoi un modele et pas une regle. Deux heuristiques ont ete testees et
mesurees, les deux echouent :

  a) ORDRE DANS L'EMAIL. Inutilisable : les deux conventions coexistent dans
     la base. Beaucoup de contacts burundais et ouest-africains ecrivent leur
     adresse patronyme-d'abord (nyemtombejosephdaniel, sallelimane216). Sur
     94 inversions proposees par cette regle, la moitie CASSAIT des fiches
     deja correctes.

  b) DICTIONNAIRE DE PRENOMS construit depuis le fichier, comme dans
     deduire_noms.py. Inutilisable comme veto ici : 84% des prenoms de la
     base n'apparaissent qu'une ou deux fois. Il n'en reconnait que 352 sur
     2 145 -- Ferdinand, Philbert, Zephirin, Alix passent au travers.

Trancher demande de savoir que Nitunga est un patronyme burundais et Ferdinand
un prenom. C'est une connaissance du monde, pas une propriete du fichier.

PERIMETRE : uniquement Origine_nom = WIX. Les noms DEDUIT_EMAIL et
DEDUIT_CLAUDE sont deja passes par ce filtre et ont ete valides par Nael.

On ne presente PAS au modele une preselection de candidats : elle viendrait
d'une des heuristiques ci-dessus et lui transmettrait son biais.

Entree  : contacts_hubspot.csv
Sortie  : contacts_hubspot.csv (+ contacts_hubspot.inversions.bak.csv)
          inversions_claude_a_verifier.csv  -- pour relecture humaine

Idempotent : relancer ne represente que des lignes inchangees.

Usage :
    python3 verifier_noms_claude.py --sample 10   # test, aucune ecriture
    python3 verifier_noms_claude.py --dry-run     # tout, aucune ecriture
    python3 verifier_noms_claude.py               # applique
"""

import csv
import json
import os
import sys

CIBLE = "contacts_hubspot.csv"
SAUVEGARDE = "contacts_hubspot.inversions.bak.csv"
REVUE = "inversions_claude_a_verifier.csv"
DELIMITEUR = ";"

COL_PRENOM = "Prénom"
COL_NOM = "Nom de famille"
COL_EMAIL = "E-mail 1"
COL_ORIGINE = "Origine_nom"

MODELE_DEFAUT = "claude-opus-4-8"
TAILLE_LOT = 40
MAX_TOKENS = 8000

FICHIERS_ENV = [
    os.path.expanduser("~/gk-advancing/.env"),
    os.path.expanduser("~/automation-orfeo/.env"),
    os.path.expanduser("~/living-memory/.env"),
]

SYSTEME = """Tu verifies l'attribution prenom / nom de famille de fiches contact.

Pour chaque fiche tu recois : un champ PRENOM, un champ NOM, et l'adresse email. Ces champs viennent d'un export CRM ou ils sont PARFOIS INTERVERTIS.

Ta seule tache : dire si les deux valeurs sont dans le bon champ, et les remettre a l'endroit si elles sont inversees.

REGLE ABSOLUE : ne corrige que si tu es certain. Dans le moindre doute, renvoie "action": "garder". Une fiche laissee telle quelle ne coute rien ; une fiche inversee a tort transforme un contact correct en contact faux, et personne ne le detectera.

N'utilise PAS l'ordre des mots dans l'adresse email comme preuve. Les deux conventions coexistent dans cette base : beaucoup de contacts ecrivent leur adresse patronyme-d'abord (nyemtombejosephdaniel@ est NYEM TOMBE Joseph Daniel, l'attribution est correcte). L'ordre dans l'email ne prouve rien.

Fonde-toi sur ce que tu sais des prenoms et des patronymes.

Le public est majoritairement francophone : France, Belgique, Suisse, Quebec, et surtout Afrique de l'Ouest et centrale -- Burundi, RDC, Cameroun, Senegal, Cote d'Ivoire, Benin, Togo, Mali, Burkina Faso, Niger, Tchad, Gabon, Madagascar -- ainsi que Haiti et les Antilles.

Patronymes burundais et rwandais frequents, a ne jamais confondre avec des prenoms : Ndayishimiye, Nshimirimana, Niyonkuru, Nitunga, Ntakarutimana, Hakizimana, Irakoze, Manirakiza, Bigirimana, Nkurunziza, Ndayikeje, Akimana, Imanishimwe, Ahishakiye, Nduwimana, Bukuru, Kaze, Muco, Ngaruko.

Patronymes ouest-africains frequents : Sall, Diallo, Ndiaye, Fall, Traore, Ouattara, Coulibaly, Kouassi, Kouadio, Sawadogo, Soumare, Cisse, Diop, Sy, Bamba, Konate, Toure.

Prenoms a ne pas prendre pour des patronymes, meme peu courants en France : Ferdinand, Philbert, Zephirin, Prosper, Boniface, Theogene, Arsene, Gentil, Benefice, Almamy, Elimane, Selemani, Fiacre, Alix, Marina, Josue, Egide, Ghislain, Larissa, Tresor, Regis, Aime, Gracieux, Jolis, Nikita.

Cas particuliers :
- Un champ peut contenir plusieurs prenoms ("Bayna Marie Noryam"). C'est normal, ce n'est pas une erreur.
- Si un champ est vide, renvoie "garder" : il n'y a rien a inverser.
- Si les deux valeurs sont des prenoms, ou les deux des patronymes, tu ne peux pas trancher : renvoie "garder".
- Si tu ne connais ni l'une ni l'autre valeur, renvoie "garder". Ne devine pas.

Ne modifie ni l'orthographe, ni la casse, ni les accents. Reprends les valeurs exactement telles qu'elles sont fournies. Tu ne fais que les echanger ou les laisser en place."""

SCHEMA = {
    "type": "object",
    "properties": {
        "resultats": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "action": {"type": "string", "enum": ["garder", "inverser"]},
                    "raison": {"type": "string"},
                },
                "required": ["id", "action", "raison"],
                "additionalProperties": False,
            },
        }
    },
    "required": ["resultats"],
    "additionalProperties": False,
}


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


def interroger(client, modele, lot):
    """lot = [(id, prenom, nom, email)]. Retourne {id: (action, raison)}."""
    liste = "\n".join(
        "%d | PRENOM: %s | NOM: %s | EMAIL: %s" % (i, p, n, e) for i, p, n, e in lot
    )
    reponse = client.messages.create(
        model=modele,
        max_tokens=MAX_TOKENS,
        system=SYSTEME,
        output_config={"format": {"type": "json_schema", "schema": SCHEMA}},
        messages=[{
            "role": "user",
            "content": (
                "Verifie ces %d fiches. Renvoie une entree par fiche, en "
                "reprenant l'id exact. Champ raison : six mots maximum.\n\n%s"
                % (len(lot), liste)
            ),
        }],
    )
    texte = next(b.text for b in reponse.content if b.type == "text")
    sortie = {}
    for item in json.loads(texte).get("resultats", []):
        sortie[item["id"]] = (item["action"], item.get("raison", ""))
    return sortie, reponse.usage


def main():
    args = sys.argv[1:]
    dry_run = "--dry-run" in args
    modele = args[args.index("--model") + 1] if "--model" in args else MODELE_DEFAUT
    echantillon = None
    if "--sample" in args:
        echantillon = int(args[args.index("--sample") + 1])
        dry_run = True                      # un echantillon n'ecrit jamais

    with open(CIBLE, encoding="utf-8-sig", newline="") as f:
        lecteur = csv.DictReader(f, delimiter=DELIMITEUR)
        entetes = lecteur.fieldnames
        lignes = list(lecteur)

    candidats = []
    for i, ligne in enumerate(lignes):
        if (ligne.get(COL_ORIGINE) or "") != "WIX":
            continue
        p = (ligne.get(COL_PRENOM) or "").strip()
        n = (ligne.get(COL_NOM) or "").strip()
        if p and n:
            candidats.append((i, p, n, (ligne.get(COL_EMAIL) or "").strip()))

    if echantillon:
        candidats = candidats[:echantillon]

    print("=== VERIFICATION prenom / nom par Claude ===")
    print("Modele    : %s" % modele)
    print("Perimetre : Origine_nom = WIX, les deux champs remplis")
    print("Fiches    : %d" % len(candidats))
    if echantillon:
        print("Mode      : ECHANTILLON de %d, aucune ecriture" % echantillon)
    elif dry_run:
        print("Mode      : DRY-RUN, aucune ecriture")
    print()

    cle, source = charger_cle()
    print("Cle API   : chargee depuis %s" % source)

    import anthropic
    client = anthropic.Anthropic(api_key=cle)

    verdicts = {}
    tok_in = tok_out = 0
    lots = [candidats[i:i + TAILLE_LOT] for i in range(0, len(candidats), TAILLE_LOT)]
    for num, lot in enumerate(lots, 1):
        try:
            sortie, usage = interroger(client, modele, lot)
        except Exception as e:                       # noqa: BLE001
            print("  lot %d/%d : ECHEC (%s) - ignore" % (num, len(lots), e))
            continue
        verdicts.update(sortie)
        tok_in += usage.input_tokens
        tok_out += usage.output_tokens
        print("  lot %d/%d traite (%d fiches)" % (num, len(lots), len(lot)))

    # --- Application --------------------------------------------------------
    inverses = []
    for idx, p, n, email in candidats:
        action, raison = verdicts.get(idx, ("garder", "non traite"))
        if action != "inverser":
            continue
        lignes[idx][COL_PRENOM], lignes[idx][COL_NOM] = n, p
        inverses.append((email, p, n, n, p, raison))

    print()
    print("=== RESULTAT ===")
    print("Fiches examinees : %d" % len(candidats))
    print("Inversions       : %d" % len(inverses))
    print("Laissees en etat : %d" % (len(candidats) - len(inverses)))

    cout = tok_in / 1e6 * 5 + tok_out / 1e6 * 25
    print("Tokens           : %d entree / %d sortie  (~%.2f USD)" % (tok_in, tok_out, cout))
    print()

    apercu = inverses if echantillon else inverses[:40]
    print("%-32s %-19s|%-19s -> %-19s|%s" % ("EMAIL", "PRENOM", "NOM", "PRENOM", "NOM"))
    print("-" * 118)
    for email, ap, an, np_, nn_, raison in apercu:
        print("%-32s %-19s|%-19s -> %-19s|%-19s %s" % (
            email[:32], ap[:19], an[:19], np_[:19], nn_[:19], raison[:26]))
    if not echantillon and len(inverses) > 40:
        print("... et %d autres (voir %s)" % (len(inverses) - 40, REVUE))

    if dry_run:
        print()
        print("Aucune ecriture.")
        return

    with open(REVUE, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f, delimiter=DELIMITEUR)
        w.writerow(["email", "prenom_avant", "nom_avant", "prenom_apres", "nom_apres", "raison"])
        w.writerows(inverses)

    import shutil
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
    print("A relire   : %s" % REVUE)


if __name__ == "__main__":
    main()
