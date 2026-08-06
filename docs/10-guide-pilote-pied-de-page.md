# 10. Guide d'exécution — le pilote du pied de page

Étapes **18** et **19** de la [checklist](00-checklist.md). Procédure à exécuter dans
HubSpot, écran par écran.

> **Ce document a une seconde vie.** C'est le brouillon du mode d'emploi d'administration remis à
> Stéphane *(étape 48)*. Il est donc écrit pour quelqu'un qui n'a jamais créé de formulaire
> HubSpot — pas pour quelqu'un qui connaît déjà le dossier. Chaque écart constaté à l'exécution
> se corrige **ici**, pas dans un fil de discussion.

**Pourquoi ce formulaire et pas un autre :** 5 champs, aucun chiffre d'affaires en jeu, et il
n'existe nulle part ailleurs qu'en pied de page du site. C'est le terrain d'essai le moins cher
de toute la mission. Décision de Franck du 6 août.

---

## Avant de commencer

| | Vérification |
|---|---|
| ☐ | Compte HubSpot ouvert, droits **Super administrateur** *(sinon la création de propriété est grisée)* |
| ☐ | Accès à l'éditeur Wix de `altavconsulting.com` — nécessaire en partie C uniquement |
| ☐ | Les 4 propriétés `Température CRM`, `Type de compte`, `Email actif`, `Date de pré-inscription` existent déjà — créées en juillet |

**On ne touche pas au formulaire Wix existant pendant tout ce guide.** Il continue de tourner. La
bascule est l'étape 21, elle vient après la recette.

---

## Partie A — Créer la propriété `Statut du visiteur`

*Étape 18, réduite à ce dont le pilote a besoin. Les 7 autres propriétés de la
[spec](08-formulaires-hubspot.md#propriétés-hubspot-à-créer) se créent au même endroit, plus
tard, quand leur formulaire arrive.*

> 🟢 **Fait le 6 août 2026.** Propriété créée dans le portail **Altav Consulting** *(ID
> `148924865`, instance **EU** — les URL sont en `app-eu1.hubspot.com`)*.
> **Nom interne : `statut_du_visiteur`.** Groupe *Informations sur le contact*, le même que
> `Température CRM`. Vérification : le compteur de propriétés Contact est passé de 230 à 231.
>
> *La création est attribuée à **Franck Pecastaing** dans le journal d'audit — c'est le compte
> sous lequel la session est ouverte.*

**Chemin :** roue crantée ⚙️ *(en haut à droite)* → **Gestion des données** → **Propriétés** →
bouton **Créer une propriété** *(en haut à droite)*.

**Écran 1 — Informations de base**

| Champ | Valeur à saisir |
|---|---|
| Type d'objet | **Contact** |
| Groupe | le **même groupe que `Température CRM`** — à vérifier d'abord *(voir encadré)* |
| Libellé | `Statut du visiteur` |
| Description | `Déclaré par le visiteur dans le formulaire de contact du pied de page. Signal 5 de la grille : candidat à revue manuelle, jamais un ENTREPRISE automatique.` |

> **Vérifier le groupe avant de créer.** Dans la liste des propriétés, filtrer sur
> `Température CRM` et lire sa colonne **Groupe**. Reprendre exactement le même. Une propriété
> ALTAV rangée ailleurs devient invisible pour quelqu'un qui cherche au bon endroit — c'est
> exactement le genre de détail qui fait qu'un administrateur n'ose plus toucher à l'outil.

**Écran 2 — Type de champ**

- Type de champ : **Sélection déroulante** *(menu déroulant, un seul choix)*
- Options, dans cet ordre, **libellés repris mot pour mot du formulaire Wix** :

| # | Libellé de l'option |
|---|---|
| 1 | `Entrepreneur (Chef d'entreprise)` |
| 2 | `En cours de création d'entreprise` |
| 3 | `En questionnement` |
| 4 | `Profession libérale` |
| 5 | `Autre` |

> ⚠️ **Écart entre deux documents, tranché ici.** La [spec des formulaires](08-formulaires-hubspot.md)
> abrège ces libellés en « Chef d'entreprise · En création · … ». Le [relevé sur le
> site](06-decisions-franck.md) donne la version longue ci-dessus. **C'est la version longue qui
> fait foi** — principe de la spec : on reproduit, on ne refond pas. Un visiteur qui a lu
> « En cours de création d'entreprise » ne doit pas trouver « En création ».
>
> **La majuscule de `Chef` compte.** Elle vient du relevé DOM du 6 août ; le relevé à l'œil du
> 5 août l'écrivait en minuscule. Reproduire, c'est reproduire jusque-là.

> **Le nom interne des options se fige à la création — vérifié le 6 août.** Au chargement en
> bloc, HubSpot recopie le libellé dans le nom interne, parenthèses et apostrophe comprises, puis
> **le verrouille**. Corriger le libellé ensuite ne corrige pas le nom interne : les deux
> divergent, et l'écart ne se voit qu'en export CSV ou par l'API.
>
> **Conséquence pratique :** saisir les libellés **exacts du premier coup**. Si un libellé doit
> changer après coup et que l'alignement compte, la seule voie propre est de supprimer la
> propriété et de la recréer — sans perte tant qu'aucun contact ne la porte.

**Écran 3 — Règles**

- Laisser les valeurs internes **générées automatiquement**. Ne pas les saisir à la main.
- Ne pas cocher « Afficher dans les formulaires » — le formulaire choisit ses champs lui-même.

**Vérification de sortie :** noter le **nom interne** de la propriété *(visible en survolant son
nom dans la liste, ou dans l'onglet Règles)*. Il ressemblera à `statut_du_visiteur`. **On en aura
besoin le jour d'un import CSV** — c'est lui que HubSpot remappe de travers.

---

## Partie B — Créer le formulaire

*Étape 19.*

**Chemin :** menu **Marketing** → **Capture de leads** → **Formulaires** → **Créer un
formulaire** → type **Formulaire intégré** → modèle **Vierge**.

> Choisir **Formulaire intégré**, pas « page de destination » ni « pop-up ». C'est le seul type
> qui s'incruste dans une page existante, condition n° 2 de Franck : *le visiteur ne doit pas
> voir qu'il change d'outil*.

**Nom du formulaire** *(interne, jamais vu par le visiteur)* : `ALTAV — Contact général (pied de page)`

### Les 5 champs visibles, dans cet ordre

| Ordre | Champ à glisser | Propriété HubSpot | Texte affiché | Obligatoire |
|---|---|---|---|---|
| 1 | Prénom | `Prénom` *(firstname)* | `Prénom` | ✅ *(imposé par HubSpot)* |
| 2 | Nom | `Nom` *(lastname)* | `Nom` | ✅ |
| 3 | E-mail | `E-mail` *(email)* | `E-mail` | ✅ |
| 4 | Téléphone | `Numéro de téléphone` *(phone)* | `Téléphone` *(libellé conservé)* | — |
| 5 | Statut du visiteur | `Statut du visiteur` *(créée en partie A)* | `Statut` | ✅ |
| 6 | Message | `Message` *(propriété standard HubSpot)* | `Parlez-nous de votre projet...` | ✅ |

*Prénom et Nom sont posés **côte à côte sur une même ligne**, pour ne pas allonger le formulaire.*

> ⚠️ **Ces textes sont des placeholders, pas des libellés — relevé DOM du 6 août.** Le formulaire
> Wix n'affiche **aucun libellé au-dessus des champs** : `Nom`, `E-mail`, `Téléphone` et
> `Parlez-nous de votre projet...` sont écrits **à l'intérieur** des champs, et `Statut` est
> l'option vide en tête de la liste déroulante.
>
> **Dans l'éditeur HubSpot, pour chacun des 5 champs :** vider le libellé *(ou décocher son
> affichage)* et porter le texte dans le champ **Texte d'espace réservé**. Pour le champ 4,
> l'équivalent est le texte affiché quand aucune valeur n'est sélectionnée.
>
> **Ce n'est pas un détail cosmétique.** Un formulaire à libellés visibles occupe environ le
> double de hauteur. Posé dans le pied de page à la place de l'actuel, il se verra — et la
> condition n° 1 de Franck, *parfaitement intégré au design du site*, tombe à la première
> capture d'écran.
>
> *Noter les points de suspension de `Parlez-nous de votre projet...` : ils sont dans l'original.*

> **Décision du 6 août — le téléphone s'écarte volontairement du Wix, et c'est assumé.**
>
> Le formulaire Wix est un champ **texte libre**. HubSpot impose son propre composant dès que le
> champ est relié à la propriété `Numéro de téléphone` : sélecteur de pays, validation de format,
> et **type de champ verrouillé** — j'ai essayé un champ texte simple, HubSpot l'a reconverti en
> affichant *« toutes les modifications seront écrasées »*.
>
> **Nael tranche : on garde le composant HubSpot.** La raison n'est pas qu'on subit la
> contrainte, c'est qu'elle est meilleure — **un champ téléphone valide le format, un champ texte
> libre non**. Le Wix accepte n'importe quoi ; le nouveau non.
>
> **Ce champ garde donc son libellé visible**, contrairement aux quatre autres : le composant
> n'accepte pas de texte d'espace réservé.
>
> *Conséquence acceptée :* le sélecteur s'ouvre sur 🇺🇸 **+1**. Un visiteur français doit changer
> le pays. Écarté comme non bloquant — *« ils savent le faire »*. **Ne pas « corriger » ce champ
> plus tard au nom de la reproduction à l'identique : c'est une décision, pas un oubli.**

**Deux points de mapping qui ne se devinent pas :**

- **Le champ 5 ne se crée pas.** HubSpot a déjà une propriété standard `Message`, prévue pour ça.
  On la réutilise et on **change son libellé affiché** dans l'éditeur de formulaire — le libellé
  du formulaire et le nom de la propriété sont deux choses différentes. Créer une propriété
  « Parlez-nous de votre projet » serait un doublon de plus.
- **Le champ 4 affiche `Statut`, pas `Statut du visiteur`.** C'est le libellé du formulaire Wix
  actuel. La propriété, elle, garde son nom complet côté CRM.

> **Décision du 6 août — le champ `Nom` unique est scindé en `Prénom` + `Nom`.** C'est le second
> écart volontaire avec le Wix, et il est plus lourd que celui du téléphone.
>
> **Le formulaire Wix a un seul champ `Nom`.** Reproduit à l'identique, il verse « Jean Dupont »
> dans le champ **Nom de famille**, prénom compris, et laisse `Prénom` vide.
>
> **Ce qui a tranché, c'est la personnalisation des séquences** *(argument de Nael)* :
>
> | Ce qu'on écrit dans une séquence | Ce que reçoit Jean Dupont |
> |---|---|
> | `Bonjour {{firstname}},` | **`Bonjour ,`** |
> | `Bonjour {{lastname}},` | `Bonjour Jean Dupont,` |
>
> Le premier est une séquence visiblement cassée, le second est bancal. Toute la **phase 3**
> repose sur ces envois. Et le rattrapage coûterait un nouveau script de déduction prénom/nom —
> exactement le chantier de juillet, qui a fait passer les contacts nommés de 33 % à 48 % au prix
> de deux scripts et d'une vérification manuelle.
>
> **Sur la validation Q9 de Franck** *(« à l'identique »)* : elle tient toujours, mais elle a été
> donnée **sans connaissance de cette conséquence**. L'écart est donc à lui signaler, pas à lui
> cacher — il n'est pas contredit, il est informé d'un élément qu'il n'avait pas.
>
> *Note :* HubSpot **impose** `Prénom` comme obligatoire — impossible de le rendre facultatif.

### Les 2 champs cachés

Dans l'éditeur, onglet des champs, section **Champs masqués** — les glisser comme les autres,
puis fixer leur valeur :

| Propriété | Valeur fixe |
|---|---|
| `Température CRM` | `INBOUND` |
| `Type de compte` | `INDIVIDUEL` |

> **C'est tout le cœur de la mission, dans deux champs.** Le contact naît classé, à la seconde de
> la soumission. Personne ne requalifie après coup — c'est le défaut de requalification qui avait
> produit 68 pré-inscrits classés `FROID`.
>
> `INBOUND` et non `CHAUD` : le visiteur est venu à nous **sans intention d'achat affirmée**.
> `INDIVIDUEL` même si le visiteur répond « Entrepreneur » : le statut déclaré est le **signal 5**
> de la grille, jamais suffisant pour basculer un compte en `ENTREPRISE`. Ce qui tranche, c'est
> qui paie la facture.

**Vérifier l'orthographe et la casse des deux valeurs** contre la liste d'options de chaque
propriété. `Inbound` ≠ `INBOUND` : HubSpot crée alors une valeur parasite, et le contact
n'apparaît dans aucune vue filtrée.

### Options du formulaire

**Onglet Options :**

| Réglage | Valeur |
|---|---|
| Texte du bouton | `Envoyer` — *celui du formulaire actuel* |
| Message après envoi | **Afficher un message** *(pas de redirection — le visiteur reste sur le site)* |
| Texte du message | `Merci pour votre envoi !` — *celui du formulaire actuel* |
| Envoyer une notification par e-mail | ✅ **activé** |
| Destinataire | **Franck**, en attendant l'arbitrage de l'étape 22 bis |
| Type de notification | E-mail. *La création de tâche est grisée — workflows verrouillés, vérifié le 5 août.* |

> **Le bouton et le message de confirmation sont repris du site, mot pour mot** — relevé DOM du
> 6 août. Ce n'était pas prévu par la spec, qui annonçait un « accusé de réception » à écrire.
> Reprendre l'existant est plus juste : c'est déjà le ton d'ALTAV, et ça évite de faire relire à
> Franck un texte que personne n'a demandé.
>
> **Si un texte plus complet est voulu un jour**, il vient de Franck : on lui demande un exemple
> de mail qu'il envoie habituellement, et on s'en sert de modèle *(étape 17 bis)*. Écrire de zéro
> puis lui faire corriger serait plus de travail pour lui, et moins juste.

**Onglet Style :** ne rien régler pour l'instant. Le calage visuel se fait en partie C, sur le
site, où l'on voit le résultat.

### Les deux réglages de compte qu'il faut ouvrir à chaque formulaire

*Roue crantée du panneau de gauche → **Paramètres** → onglet **Général**.*

| Réglage | État par défaut sur ce portail | Ce qu'il faut |
|---|---|---|
| **Créer automatiquement de nouveaux contacts à partir d'adresses e-mail inconnues** | 🔴 **désactivé** | ✅ **activé** |
| **Définir les nouveaux contacts comme contacts marketing** | 🟢 activé | ✅ activé |

> ⚠️ **Le premier réglage est le piège le plus coûteux de tout ce guide — trouvé désactivé le
> 6 août.** Sans lui, le formulaire enregistre bien les soumissions dans son propre tableau,
> mais **ne crée aucune fiche de contact** pour les adresses qu'il ne connaît pas — c'est-à-dire
> pour la totalité des nouveaux leads.
>
> **Rien n'a l'air cassé.** Le visiteur voit son message de confirmation, la notification part,
> le compteur de soumissions monte. Seul le CRM reste vide. On peut déclarer le pilote réussi et
> ne s'apercevoir de rien pendant des semaines.
>
> **À vérifier sur les 5 formulaires suivants**, un par un. C'est un défaut du compte, pas du
> formulaire : chaque nouveau formulaire naîtra avec.

*Sur le second réglage :* il fait passer chaque personne qui écrit en **contact marketing**,
donc dans le compteur facturé par HubSpot. C'est voulu — quelqu'un qui écrit spontanément est
précisément la personne à qui envoyer un livre blanc, et la phase 3 repose là-dessus. Attention
au « **ou mis à jour** » : un dormant qui remplit le formulaire bascule lui aussi. Voir
[journal](05-journal.md) pour l'état de départ de la base.

---

## Partie C — Poser le formulaire dans le pied de page Wix

*Toujours l'étape 19. C'est ici que se jouent les conditions n° 1 et n° 2 de Franck.*

> 🟢 **Formulaire publié le 6 août 2026.** Code d'intégration, valable tel quel :
>
> ```html
> <script src="https://js-eu1.hsforms.net/forms/embed/148924865.js" defer></script>
> <div class="hs-form-frame" data-region="eu1" data-form-id="988b724a-88b5-499b-961d-ac8394e25e5c" data-portal-id="148924865"></div>
> ```
>
> *Publier ne met rien en ligne : le formulaire n'existe pour le public que le jour où ce code
> est posé dans le site.*

1. *(déjà fait — code ci-dessus)* Dans HubSpot, après publication → **Obtenir un code intégré** →
   onglet **Intégrer le code**.
2. Dans l'éditeur Wix : ouvrir le **pied de page**, sélectionner le formulaire natif existant.
   **Ne pas le supprimer** — le déplacer temporairement hors écran ou le masquer.
3. **Ajouter** → **Intégrer** → **Intégrer un code / HTML iframe** → coller le code HubSpot.
4. Redimensionner le bloc : le formulaire HubSpot doit occuper la même place que l'ancien.
5. Publier le site, puis **regarder la page en navigation privée** — pas dans l'éditeur.

**Trois pièges connus sur cette partie :**

- **L'intégration de code Wix demande un forfait payant.** Si le bouton est grisé, c'est un
  point de blocage à remonter à Franck, pas un problème HubSpot.
- **Le bloc d'intégration Wix est une iframe** : le formulaire n'hérite **pas** des polices ni
  des couleurs du site. Le calage se fait dans l'onglet **Style** du formulaire HubSpot —
  police, taille, couleur du bouton — relevées sur le site. C'est la condition n° 1 de Franck,
  et c'est du travail à l'œil, pas un réglage.
- **Vérifier sur mobile.** Le pied de page est l'endroit du site le plus souvent cassé en petite
  largeur, et une iframe ne se redimensionne pas toujours seule.

---

## Partie D — Recette

*Étape 19 bis. Les trois critères sont ceux que Franck a posés en Q9. Aucun ne se coche à sa
place : cette liste se parcourt **avec lui**.*

**Le test technique, à faire seul avant de le solliciter :**

| | Contrôle | Comment on vérifie |
|---|---|---|
| ☐ | Une soumission de test crée bien un contact | HubSpot → Contacts, trier par date de création |
| ☐ | `Température CRM` = `INBOUND` | sur la fiche du contact de test |
| ☐ | `Type de compte` = `INDIVIDUEL` | idem |
| ☐ | `Statut du visiteur` contient la valeur choisie, **libellé exact** | idem |
| ☐ | Le message du champ 5 est bien dans `Message` | idem |
| ☐ | La notification par e-mail arrive | boîte de Franck |
| ☐ | Une **seconde** soumission avec le même e-mail **met à jour** la fiche, sans créer de doublon | comportement natif — mais il se vérifie |
| ☐ | Le contact de test est supprimé après recette | sinon il pollue les vues |

**Les trois critères de Franck :**

| | Critère *(Q9)* | Ce qui le prouve |
|---|---|---|
| ☐ | **Parfaitement intégré au design du site** | le formulaire, vu en navigation privée sur mobile et sur ordinateur, ne détonne pas |
| ☐ | **Transparent pour le visiteur** | pas de redirection, pas de logo HubSpot, pas de changement de page à l'envoi |
| ☐ | **Alimente directement HubSpot** | démontré par le test technique ci-dessus, sur sa fiche à lui |

**Ce que la recette débloque, et c'est le vrai enjeu :** une fois ces cases cochées, la méthode
est prouvée. On arrive devant Stéphane avec un formulaire qui tourne, pas avec une proposition —
et l'étape 20 devient une conversation sur ce qu'on améliore, pas sur ce qu'on tente.

---

## Ce qui reste ouvert à la fin de ce guide

| Point | Pour qui | Bloque |
|---|---|---|
| **Mention de consentement RGPD** — signalée par HubSpot à la publication, absente du formulaire | **Franck** | rien techniquement, **mais c'est une collecte de données personnelles sur un site français** |
| **reCAPTCHA** — désactivé, signalé par HubSpot | — | rien tant que le volume est faible ; à activer au premier spam |
| Signaler à Franck l'ajout de `Prénom` — il a validé « à l'identique » sans connaître la conséquence sur les séquences | **Franck** | rien |
| Destinataire des notifications : Franck, Stéphane, ou les deux | **Franck** | étape 22 bis |
| Texte de confirmation définitif | **Franck** | étape 17 bis |
| Forfait Wix autorisant l'intégration de code | **Franck** | partie C, s'il est absent |

> **Sur le consentement RGPD.** HubSpot affiche l'avertissement à chaque publication : *« Ajouter
> un champ de confidentialité des données… important si vous avez besoin de recueillir le
> consentement de vos contacts. »* La [spec](08-formulaires-hubspot.md) l'avait anticipé — elle
> remplaçait la case « J'accepte les termes et conditions », jamais cochée sur 525 soumissions,
> par « une mention de consentement explicite ». **Cette mention n'est pas encore posée.**
>
> Ce n'est pas une question technique et je ne la tranche pas : le texte engage ALTAV. Il vient
> de Franck, ou de qui le conseille.
