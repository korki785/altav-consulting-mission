# Mail à Franck — état des lieux base contacts

**Objet :** Base contacts Wix — nettoyage terminé, 3 décisions à valider

---

Bonjour Franck,

J'ai repris l'export Wix des contacts pour le préparer à une migration CRM. Voici ce qui a été fait et les points qui demandent ton arbitrage.

## Point de départ

L'export brut contenait **8 915 lignes**, 51 colonnes, avec 167 libellés d'origine créés au fil des années sans logique commune (noms de fichiers d'import, intitulés de sessions, formulaires). Inexploitable tel quel pour du nurturing.

## Ce qui a été fait

**1. Segmentation commerciale.** Ajout d'une colonne `Tag_CRM` à 4 valeurs, qui répond à une seule question : où en est la relation ?

| Tag | Contacts | Définition |
|---|---|---|
| CLIENT | 753 | A déjà payé quelque chose — base d'upsell |
| CHAUD | 318 | Intention d'achat récente, à relancer en priorité |
| INBOUND | 171 | Venu à nous, sans intention forte — à nurturer |
| FROID | 6 241 | Imports et prospection, outbound à part |

Les libellés d'origine ont été conservés intacts, rien n'a été renommé.

**2. Dédoublonnage.** 531 doublons fusionnés, sans perte : quand deux fiches désignaient la même personne avec des emails différents, les deux adresses ont été gardées. Les doublons venaient surtout des inscriptions répétées au Rattrapage Module 2 Promo 6.

**3. Emails inactifs.** La liste des 976 adresses mortes a été appliquée avec une nuance : les contacts sans relation commerciale ont été supprimés (889), mais les **85 CLIENT et CHAUD ont été conservés** avec une colonne `Email_actif = NON`. Un client dont l'email a bougé reste un client — 44 d'entre eux ont un numéro de téléphone et restent joignables.

**4. Contacts internes retirés.** 12 adresses Altav sorties de la base prospects, dont des collaborateurs qui figuraient avec leur adresse personnelle en principal — la tienne en faisait partie. Sans ça, l'équipe recevait les séquences de prospection.

**5. Enrichissement des noms.** 70 % des contacts n'avaient qu'une adresse email, sans nom : impossible de personnaliser un envoi. Les noms lisibles dans les adresses ont été extraits (`prenom.nom@…`), avec une règle stricte : remplir uniquement quand c'est certain, laisser vide au moindre doute. *(Traitement en cours de finalisation, chiffre définitif à venir.)*

**Résultat : 7 483 contacts propres, segmentés, prêts à importer dans un CRM.**

## Les 3 points qui demandent ta décision

**1. Qui porte le CRM en interne ?** C'est la condition de tout le reste. Un CRM que personne ne tient au quotidien redevient un Excel en trois mois — et le diagnostic de départ était clair : le problème n'est pas l'outil, c'est l'adoption.

**2. Accès au back-office Wix et au fichier Excel des pré-inscrits.** Nécessaires pour brancher les formulaires sur les séquences et vérifier la cohérence avec les 489 pré-inscrits.

**3. Le fichier des certifiés de Stéphane.** Les participants « Certification Promo 4 & 5 » sont actuellement en CHAUD. Ceux qui ont effectivement payé doivent passer en CLIENT — c'est une bascule de quelques minutes une fois le fichier reçu, mais elle change le ciblage des relances.

## Ce que je propose ensuite

Sans attendre le CRM, on peut lancer le premier gain : la séquence de nurturing sur les **489 contacts INBOUND et CHAUD**. Concrètement, le mail de confirmation réécrit, le livre blanc à J+5, la relance à J+30, et le rappel sous 5 minutes après inscription.

C'est le segment le plus rentable et il ne dépend d'aucun des blocages ci-dessus.

Dis-moi ce que tu en penses, notamment sur le point 1 qui conditionne le calendrier.

Bien à toi,
Nael

---

## Notes pour toi (à supprimer avant envoi)

- Le chiffre d'enrichissement des noms est à compléter quand le traitement sera terminé.
- Si tu préfères ne pas mentionner que sa fiche a été retirée de la base, supprime la dernière phrase du point 4.
- Les 706 contacts dont le nom n'a pas pu être déduit automatiquement restent une option d'enrichissement externe payant (Dropcontact, ~0,10 €/contact) — non mentionné ici volontairement, à garder pour plus tard.
