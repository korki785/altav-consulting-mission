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

> 🟢 **Forfait Wix vérifié le 7 août — le point de blocage n'existe pas.** Le site est en forfait
> **Business (Premium)**, dans le compte Wix Studio de Nael, sous le nom `Altav Consulting`
> *(metaSiteId `33a9d668-ce43-4734-b906-9665bf97cd31`)*. L'intégration de code est donc autorisée.
> C'était la dernière inconnue de la partie C.

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

### Relevé du 7 août — trois choses que la spec ne disait pas

**1. Le pied de page est masqué sur la page d'accueil.**

Vérifié à la fois sur le site en ligne et dans l'éditeur : sur `/`, l'élément `SITE_FOOTER` est en
`display: none`. Il s'affiche sur les autres pages — `/formationubuntu`, `/coaching-ubuntu`, etc.

> **Conséquence directe sur le pilote : le formulaire ne sera pas visible sur la page la plus
> visitée du site.** Ce n'est pas un défaut de l'intégration, c'est l'état actuel du site, et il
> précède la mission. Deux lectures possibles, à trancher avec Franck :
>
> - **on n'y touche pas** — le pilote reste un pilote, et le pied de page se juge là où il vit ;
> - **on affiche le pied de page sur l'accueil** — mais c'est une modification du design du site,
>   pas de la plomberie CRM, et elle sort du périmètre de l'étape 19.
>
> **Ne pas la faire en passant.** Le jour où l'accueil affiche un pied de page qu'il n'affichait
> pas, quelqu'un le remarquera, et ce sera mis sur le compte du CRM.

**2. Le formulaire vit dans le pied de page global, pas dans une page.**

Chaîne réelle : `SITE_FOOTER` → `comp-k6unhq8n` → formulaire `comp-k6unhq9b`, le tout porté par la
`masterPage`. **Une seule modification couvre donc toutes les pages qui affichent le pied de
page.** Corollaire pratique : le pied de page ne s'édite pas depuis l'accueil, puisqu'il y est
masqué — **ouvrir l'éditeur sur `La Formation Ubuntu`** pour y accéder.

**3. Le calage visuel n'est plus « du travail à l'œil ».**

Valeurs relevées sur le site en ligne, à reporter dans l'onglet **Style** du formulaire HubSpot :

| Élément | Valeur |
|---|---|
| Champs *(Nom, E-mail, Téléphone, Statut)* | `492 × 39 px` |
| Zone de message | `492 × 126 px` |
| Fond des champs | `#243853` |
| Bordure des champs | `2px solid #FFFFFF`, angles droits *(rayon `0`)* |
| Texte saisi et texte d'espace réservé | `#FFFFFF` |
| Police | `avenir-lt-w01_35-light`, `15px` |
| Bouton `Envoyer` | `93 × 39 px`, fond transparent, bordure `2px solid #106F9A`, libellé blanc |
| **Bloc du formulaire entier** | **`501 × 451 px`** |

> ⚠️ **Le formulaire HubSpot ne tiendra pas dans 451 px de haut.** Il porte 6 champs visibles
> *(Prénom et Nom sur une ligne)*, le composant téléphone avec son sélecteur de pays, **deux cases
> de consentement RGPD** et le bouton. Le Wix n'a ni consentement, ni prénom séparé.
>
> **Le pied de page va donc grandir.** C'est la conséquence mécanique de deux décisions déjà
> prises et assumées — le scindement `Prénom` / `Nom` et le bloc RGPD — pas un défaut d'intégration.
> Mais cela touche la **condition n° 1 de Franck** *(« parfaitement intégré au design du site »)* :
> à signaler avant la recette, pas pendant.

**4. Le site est multilingue.** L'éditeur porte un sélecteur de langue *(Français)*. Le formulaire
HubSpot intégré, lui, sera **en français uniquement**, quelle que soit la langue affichée. Sans
gravité tant que le pilote tourne ; à reprendre au moment des 5 formulaires suivants.

1. *(déjà fait — code ci-dessus)* Dans HubSpot, après publication → **Obtenir un code intégré** →
   onglet **Intégrer le code**.
2. Dans l'éditeur Wix : ouvrir le **pied de page**, sélectionner le formulaire natif existant.
   **Ne pas le supprimer** — le déplacer temporairement hors écran ou le masquer.
3. **Ajouter** → **Intégrer** → **Intégrer un code / HTML iframe** → coller le code HubSpot.
4. Redimensionner le bloc : le formulaire HubSpot doit occuper la même place que l'ancien.
5. Publier le site, puis **regarder la page en navigation privée** — pas dans l'éditeur.

**Trois pièges connus sur cette partie :**

- ~~**L'intégration de code Wix demande un forfait payant.**~~ — **levé le 7 août** : le site est
  en forfait **Business**, l'intégration de code est autorisée.
- **Le bloc HTML se pose dans la section survolée, pas dans le pied de page.** Ajouté depuis le
  panneau **+**, il s'attache à la section visible au centre de l'écran — ici *La formation Ubuntu 2*,
  celle des logos clients. Il faut ensuite le **faire glisser** dans le pied de page et attendre
  la mention **« Attacher à : Pied de page »** avant de relâcher. Sans cela, le formulaire vit
  dans une page et non dans le pied de page global : il ne sera présent que sur celle-là.
- **Le bloc d'intégration Wix est une iframe** : le formulaire n'hérite **pas** des polices ni
  des couleurs du site. Le calage se fait dans l'onglet **Style** du formulaire HubSpot —
  police, taille, couleur du bouton — relevées sur le site. C'est la condition n° 1 de Franck,
  et c'est du travail à l'œil, pas un réglage.
- **Vérifier sur mobile.** Le pied de page est l'endroit du site le plus souvent cassé en petite
  largeur, et une iframe ne se redimensionne pas toujours seule.

### ⚠️ Le piège RGPD de la partie C — la question des cookies, posée une seule fois

Au moment où l'on valide le code, Wix demande : **« Quels cookies ou technologies similaires sont
définis par votre code ? »**. Il propose **`Essentiels`** par défaut, et **ce défaut est faux**.

Le script HubSpot dépose `hubspotutk`, un cookie de **suivi** : il relie la soumission du
formulaire à l'historique de navigation du visiteur. Ce n'est pas un cookie essentiel au
fonctionnement du site.

> **Pourquoi ça compte, et pas qu'un peu.** La catégorie choisie décide **à quel moment le script
> a le droit de se charger** vis-à-vis de la bannière de consentement du site. Laissé en
> `Essentiels`, il se charge **avant** tout consentement — sur un site qui affiche une politique
> de confidentialité et un bloc de consentement RGPD dans ce même formulaire. La contradiction est
> visible à l'œil nu.
>
> **À trancher, pas à subir** — et c'est une question juridique, pas technique : elle remonte à
> Franck, au même titre que les textes de consentement.

### État au 1er septembre — le bloc est posé, la hauteur est le sujet

**Fait et sauvegardé dans Wix** *(non publié)* :

| | Élément |
|---|---|
| 🟢 | Bloc **HTML intégré** dans le pied de page — enfant de `SITE_FOOTER`, donc présent sur toutes les pages qui l'affichent |
| 🟢 | Code d'intégration posé, formulaire HubSpot rendu |
| 🟢 | Largeur **501 px**, celle du formulaire Wix |

**Fait et publié dans HubSpot** — style des champs :

| Réglage | Valeur |
|---|---|
| Police | Nunito Sans, 15 px — substitut d'Avenir LT Light, indisponible hors Wix |
| Fond des champs | `#243853` |
| Texte saisi · placeholder · texte d'aide · libellé | `#FFFFFF` |
| Bordure | `#FFFFFF`, `2px`, solide |
| Message d'erreur | `e51520` |

> **Reste `Arrondissement des angles` à `0`** — il est encore à `3`. Le formulaire Wix a les
> angles droits.

### La hauteur : 918 px contre 451, et d'où ça vient

Mesuré sur le formulaire **publié**, à 501 px de large — la largeur réelle dans le pied de page.

| Bloc | Pleine largeur | **À 501 px** |
|---|---|---|
| Prénom + Nom *(même ligne, elles y restent)* | 56 | 56 |
| E-mail | 56 | 56 |
| Téléphone *(étiquette visible, imposée)* | 76 | 76 |
| `Vous êtes` + liste Statut | 76 | 76 |
| Message | 81 | 81 |
| **Bloc RGPD** | **195** | **310** |
| Bouton `Envoyer` | 43 | 43 |
| **Total** | 803 | **918** |

> **Le bloc RGPD fait un tiers du formulaire, et il enfle de 115 px rien qu'en rétrécissant à
> 501.** Les deux paragraphes explicatifs passent de une à deux lignes chacun. **La largeur
> achète de la hauteur** — c'est le levier le moins cher si le pied de page est refait.

*Deux artefacts de l'éditeur corrigés au passage :* le drapeau 🇺🇸 du champ téléphone n'apparaît
que dans l'éditeur — le formulaire publié affiche 🇫🇷, HubSpot géolocalise. Et le
`Commencer la saisie...` gris au-dessus des champs est l'invite d'une étiquette vide, pas une
étiquette réelle : les placeholders fonctionnent.

### Décision du 1er septembre — Nael refait le pied de page et raccourcit les consentements

**451 px est hors d'atteinte et on cesse de le viser.** Le bloc RGPD seul en fait 310, et il
n'est pas négociable. Le pied de page sera refait pour accueillir un formulaire plus haut.

**Textes de consentement retenus** — ils remplacent ceux de HubSpot, dont les deux paragraphes
d'introduction disparaissent, leur contenu passant dans les libellés des cases :

| | Texte |
|---|---|
| Case 1 *(facultative, abonnement `Marketing Information`)* | `Je souhaite recevoir les communications d'Altav Consulting.` |
| Case 2 *(obligatoire)* | `J'accepte le traitement de mes données pour répondre à ma demande.` |
| Ligne finale, 12 px | `Désabonnement à tout moment. Voir notre politique de confidentialité.` |

Cible : **≈ 660 px** — −170 sur le RGPD, −20 en vidant l'étiquette `Vous êtes`, −70 en
resserrant l'espacement.

> **Les deux cases restent séparées.** Répondre à quelqu'un ne demande aucun consentement
> marketing. Les fusionner conditionnerait « je réponds à ta question » à « j'accepte la
> publicité ».
>
> **Rien sous 12 px** pour le texte de consentement. En dessous, l'argument « c'était écrit »
> ne tient plus.

> ⚠️ **Deux fautes dans la traduction française de HubSpot**, à corriger quoi qu'il arrive :
> « de Altav » et « que Altav », pour `d'Altav` et `qu'Altav`.

### Où ces textes s'éditent — et pourquoi ce n'est pas là où on croit

Le panneau **Modifier la confidentialité des données** du bloc, dans le formulaire, ne contient
**pas** les textes. Il l'annonce lui-même : *« Vous pouvez modifier les textes par défaut de
consentement et de politique de confidentialité dans les paramètres »*.

Ils vivent au **niveau du compte, par langue**. Le piège de la Partie B bis s'applique donc
intégralement : régler les textes **avant** de reposer le bloc, et vérifier qu'on édite bien la
variante **Français**.

État constaté du bloc au 1er septembre, tout est conforme : consentements séparés, les deux
consentements collectés, abonnement `Marketing Information` non obligatoire, et la déclaration
de politique de confidentialité **décochée** — retirée parce que le lien existe déjà à gauche
dans le pied de page.

**Reste à faire à la souris** :

| | Geste |
|---|---|
| 🟢 | ~~Raccourcir les textes de consentement~~ — fait, mais l'ancien bloc ne les a jamais repris *(voir ci-dessous)* |
| 🟢 | ~~Vider l'étiquette `Vous êtes`~~ · ~~`Arrondissement des angles` à `0`~~ — repris dans la v2 |
| 🔴 | Refaire le pied de page Wix à la nouvelle hauteur, puis positionner le bloc |

---

## Partie C bis — Le formulaire v2, et pourquoi il a fallu le refaire

*1er septembre 2026.*

### Le figeage du bloc de consentement est confirmé, et il est définitif

La Partie B bis annonçait que le bloc de consentement fige son texte à la pose. **Vérifié à
l'usage, et pire que prévu : il n'existe aucun moyen de le rafraîchir sur un formulaire existant.**

Ce qui a été essayé, dans l'ordre, sur le formulaire du 6 août :

| Tentative | Résultat |
|---|---|
| Modifier les textes dans les paramètres, en **Français** | textes bien enregistrés, bloc inchangé |
| Republier le formulaire | inchangé |
| Supprimer le bloc | **impossible** — il est imposé dès que la conformité RGPD est active sur le compte |
| Décocher puis recocher les deux consentements | **impossible** — « Envoyer des communications » dépend de « Stocker et traiter des données », et aucun des deux ne se décoche |
| Changer de mode de consentement, puis revenir | seule manœuvre qui a reconstruit le bloc |

> **La seule voie fiable est un formulaire neuf.** Un bloc de consentement créé aujourd'hui lit
> les paramètres d'aujourd'hui. Vérifié : la v2 a affiché les textes courts dès sa création, sans
> aucune manipulation.

### Deuxième raison de refaire : le formulaire publié avait divergé du brouillon

Constaté le 1er septembre : le brouillon contenait ses six champs, et **la version publiée n'en
servait plus qu'un — l'e-mail**, hauteur 220 px au lieu de 803. Republier n'y changeait rien.

Cause probable, non confirmée : le réglage **« Formulaires raccourcis »**, qui masque
automatiquement les champs que HubSpot pense pouvoir remplir seul. Il est **désactivé par
défaut** sur un formulaire neuf — à vérifier sur tout formulaire dont l'affichage rétrécit sans
raison.

### Le formulaire v2

**`ALTAV — Contact général (pied de page) v2`**
`data-form-id` = **`5d78e7c0-72db-463a-ae45-0532bf6557a0`**

Construit à partir du modèle **page blanche**, dans le même éditeur que la v1 — l'éditeur hérité
produirait un code d'intégration d'une autre forme, et il faudrait remplacer tout le bloc dans
Wix au lieu du seul identifiant.

> **Dans l'éditeur HubSpot, on ne glisse rien.** Un clic sur une propriété dans le panneau
> **Propriétés** l'ajoute au formulaire. Et le panneau de réglages ne suit pas la sélection : il
> faut cliquer le **crayon** de la barre d'outils du champ pour l'ouvrir.

### Le consentement retenu — décision de Nael

**Mode implicite + case à cocher pour les communications.**

| | Consentements séparés | **Implicite** *(retenu)* |
|---|---|---|
| Traitement des données | case cochée, acte affirmatif | phrase déclarative |
| Communications marketing | case à cocher | **case à cocher — inchangé** |

Le principe de la Partie B bis tient : la case marketing reste séparée et facultative, on ne
conditionne pas « je réponds à ta question » à « j'accepte la publicité ». Ce qui change, c'est
que le consentement au traitement devient présumé — défendable, puisque répondre à quelqu'un qui
écrit spontanément ne repose pas sur le consentement mais sur la demande elle-même.

**Textes en vigueur :**

| | |
|---|---|
| Intro communication | `Désabonnement à tout moment.` |
| Case marketing *(facultative, `Marketing Information`)* | `J'accepte de recevoir d'autres communications d'Altav Consulting.` |
| Traitement | `Nous traitons vos données pour répondre à votre demande.` |

La déclaration de politique de confidentialité est **décochée** : le lien existe déjà à gauche
dans le pied de page.

### ⚠️ Le piège du compte revient sur chaque formulaire neuf

**« Créer automatiquement de nouveaux contacts à partir d'adresses e-mail inconnues » était de
nouveau désactivé sur la v2.** Ce n'est pas un réglage de compte, c'est un réglage **par
formulaire**, et son défaut est « désactivé ».

Il se trouve dans la roue crantée du panneau de gauche → **Paramètres** → onglet **Général**,
premier interrupteur. **À vérifier sur les 5 formulaires suivants, un par un.**

*Au même endroit, onglet **Paramètres des soumissions** : la notification était déjà réglée sur
`franck.pecastaing@altav-consulting.com`, HubSpot reprenant le créateur du formulaire. Ces
notifications suivent les paramètres globaux du compte — à revérifier à la recette.*

### La hauteur, enfin

Mesurée dans le bloc Wix, à 501 px de large :

| Étape | Hauteur |
|---|---|
| Formulaire du 6 août | **937** |
| v2, consentement raccourci, étiquette `Vous êtes` retirée | 777 |
| Remplissage des champs `10px` → `6px` | **737** |

**−200 px.** Contre les 451 du formulaire Wix, le pied de page grandit de **286 px**.

> **On ne descend pas plus bas sans perdre quelque chose.** Ce qui reste, ce sont les deux cases
> de consentement, le composant téléphone et le prénom séparé — trois décisions prises et
> assumées, pas du gras.


## Partie C ter — Le filtre anti-spam de HubSpot, quatrième défaut silencieux

*1er septembre 2026, découvert à la recette.*

**HubSpot bloque les soumissions venues d'un domaine qu'il ne connaît pas.** Motif : « Domaine
de site non enregistré ». La soumission n'apparaît alors **nulle part** — ni contact, ni
notification, ni compteur de soumissions. Elle vit dans une vue dédiée que rien ne signale, et
elle est **supprimée automatiquement au bout de 90 jours** :

```
https://app-eu1.hubspot.com/submissions-spam/148924865
```

> **C'est le quatrième défaut silencieux de la mission**, après `Inbound` ≠ `INBOUND`, la
> création automatique de contacts désactivée, et le bloc de consentement figé. Celui-ci est le
> plus coûteux : il détruit des leads sans laisser de trace.

### Ce que « domaine » veut dire ici — et le piège du tiret

C'est le domaine de **la page qui héberge le formulaire**, pas celui de l'e-mail du visiteur.
Un seul enregistrement suffit donc, une fois pour toutes — les `@gmail.com`, `@brarudi.bi` et
autres adresses des visiteurs n'y sont pour rien.

**Le piège trouvé sur ce portail :** le domaine enregistré était `altav-consulting.com` — celui
des **e-mails**, avec un tiret. Le **site**, lui, est `altavconsulting.com`, sans tiret. Deux
chaînes différentes ; celle qui héberge le formulaire n'était pas déclarée.

**Réglé le 1er septembre** : `altavconsulting.com` ajouté dans ⚙️ → **Suivi et analyse** →
**Code de suivi** → onglet **Suivi avancé** → *Domaines de sites supplémentaires*. Le champ
n'accepte qu'un domaine nu — sans `https://`, sans `www.`, sans chemin.

### Le vrai domaine du formulaire n'est ni l'un ni l'autre — c'est l'iframe Wix

Relevé sur une soumission bloquée, champ `Valeur de champ` lu **avant** suppression :

```
33a9d668-ce43-4734-b906-9665bf97cd31.filesusr.com
```

**Le bloc HTML de Wix est une iframe, et cette iframe est servie depuis `filesusr.com`** — le
domaine d'hébergement Wix — préfixé du metaSiteId du site. Le formulaire HubSpot vit dans
l'iframe : c'est donc **ce domaine-là** qu'il déclare, pas `altavconsulting.com`. Enregistrer le
domaine du site ne suffisait pas, et ne suffira pas non plus après publication.

**Réglé le 2 septembre** en ajoutant ce domaine à la même liste :

```
33a9d668-ce43-4734-b906-9665bf97cd31.filesusr.com
```

> **Pas `filesusr.com` tout court** — ça accepterait les iframes de n'importe quel site Wix au
> monde. Le préfixe metaSiteId est propre à ce site et stable dans le temps.

**Vérifié dans la foulée :** soumission depuis l'Aperçu Wix → acceptée, fiche créée, vue spam
vide, page de conversion enregistrée `https://33a9d668-….filesusr.com/html/…`. L'Aperçu est
donc un banc de test valable une fois ce domaine enregistré.

> ⚠️ **Le site publié utilise un TROISIÈME domaine — attrapé le 2 septembre, après
> publication.** L'iframe de production est servie depuis :
>
> ```
> www-altavconsulting-com.filesusr.com
> ```
>
> Ce n'est ni le domaine du site, ni celui de l'Aperçu (`33a9d668-….filesusr.com`). Sans son
> enregistrement, **toutes les soumissions réelles partaient en spam** alors que tous les tests
> passaient. Enregistré le 2 septembre, soumission depuis le site publié vérifiée passante.
>
> **Bilan : trois domaines enregistrés, chacun nécessaire.**
>
> | Domaine | Couvre |
> |---|---|
> | `altavconsulting.com` | par principe — si Wix change un jour de mécanisme |
> | `33a9d668-ce43-4734-b906-9665bf97cd31.filesusr.com` | l'Aperçu Wix *(banc de test)* |
> | `www-altavconsulting-com.filesusr.com` | **le site publié** |

### Confirmation à faire le jour de la publication

1. Ouvrir `www.altavconsulting.com/formationubuntu` en navigation privée, soumettre
2. Ouvrir la vue des soumissions de spam
3. **Vide** → confirmé, la fiche est dans Contacts. **Sinon** → ouvrir la soumission, lire
   **`Valeur de champ`** — la chaîne exacte reçue — et enregistrer précisément celle-là, puis
   resoumettre. Ça converge en un tour.

> **Ne jamais supprimer une soumission en spam sans avoir lu sa `Valeur de champ`.** C'est la
> seule trace de ce que HubSpot a reçu, et donc le seul diagnostic. Une suppression prématurée
> a coûté un aller-retour de test le 2 septembre.

**Et ensuite :** surveiller cette vue les premières semaines. Le motif « domaine » sera réglé,
mais les autres motifs — fondés sur le contenu — restent actifs et peuvent bloquer un vrai
prospect qui écrit trois mots. Compte tenu de la base ALTAV, largement hors des sentiers que ce
genre de filtre connaît, ce n'est pas une hypothèse d'école.

### 🟢 Recette du 2 septembre — la chaîne complète fonctionne

Vérifié en deux temps :

- **Catégorisation** — sur fiche : **`Température CRM = INBOUND`**, **`Type de compte =
  INDIVIDUEL`**, statut déclaré et message bien mappés. **Le lead naît classé.**
- **Anti-spam** — après enregistrement du domaine `filesusr.com` du site : soumission depuis
  l'Aperçu **acceptée directement**, fiche créée, vue spam vide.

### 🟢 2 septembre, suite — le site est publié, le pilote est en ligne

Décision de Nael. Séquence exécutée : ancien formulaire Wix retiré du pied de page, publication,
enregistrement du domaine de production, soumission de test depuis le site publié **acceptée**.

**Mobile vérifié sur le site publié** *(rendu forcé via `?showMobileView=true`)* : bloc
**300 × 902**, pied de page mobile 1208, tous les champs affichés, bouton `Envoyer` visible
sans défilement interne. Le formulaire charge **en différé** — un visiteur qui arrive
directement au pied de page voit un vide navy pendant un instant ; c'est un comportement de
chargement, pas un défaut.

**Restent ouverts :**

| Point | Pour qui |
|---|---|
| Les **3 critères de Franck** — intégré, transparent, alimente HubSpot — se parcourent avec lui | **Franck** |
| **Franck n'a pas validé les textes de consentement ni la catégorie de cookies** — le site a été publié sur décision de Nael ; à lui signaler, pas à lui cacher | **Nael → Franck** |
| Deux textes figés dans le bloc v2 : « de Altav » *(pour `d'Altav`)* et la phrase longue du consentement implicite. Remède : corriger dans les paramètres, puis basculer le mode de consentement aller-retour pour forcer la relecture | — |
| Destinataire des notifications — Franck seul pour l'instant | étape 22 bis |

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
| **Valider les textes de consentement RGPD** — posés, mais ce sont ceux de HubSpot | **Franck** | la mise en ligne : ils engagent ALTAV |
| **reCAPTCHA** — désactivé, signalé par HubSpot | — | rien tant que le volume est faible ; à activer au premier spam |
| Signaler à Franck l'ajout de `Prénom` — il a validé « à l'identique » sans connaître la conséquence sur les séquences | **Franck** | rien |
| Destinataire des notifications : Franck, Stéphane, ou les deux | **Franck** | étape 22 bis |
| Texte de confirmation définitif | **Franck** | étape 17 bis |
| ~~Forfait Wix autorisant l'intégration de code~~ — **levé le 07/08, forfait Business** | — | rien |
| **Le pied de page grandit** — le formulaire HubSpot est plus haut que les 451 px du Wix | **Franck** | sa condition n° 1, à la recette |
| **Catégorie de cookies du script HubSpot** — Wix propose `Essentiels`, ce qui est faux : `hubspotutk` est un cookie de suivi | **Franck** | la mise en ligne, au même titre que les textes de consentement |
| **Le pied de page est masqué sur l'accueil** — l'afficher est une décision de design, hors étape 19 | **Franck** | rien techniquement |

---

## Partie B bis — Le bloc de consentement RGPD

🟢 **Posé le 6 août 2026.** La conformité RGPD était déjà activée sur le compte ; il ne restait
qu'à poser le bloc.

**Chemin :** panneau **+** → onglet **Autre** → section *Sécurité et confidentialité* →
**Confidentialité des données**, à glisser sous le champ Message.

**Configuration retenue :**

| Réglage | Valeur |
|---|---|
| Enregistrement de l'autorisation | **Consentements séparés (cases à cocher individuelles)** |
| Consentement *Stocker et traiter des données* | ✅ **obligatoire** |
| Consentement *Envoyer des communications* | abonnement **`Marketing Information`**, **facultatif**, décoché par défaut |
| Déclaration de politique de confidentialité | ✅ activée, lien vers `altavconsulting.com/politique-de-confidentialité` |

> **Les deux cases doivent rester distinctes.** Répondre à quelqu'un qui écrit ne demande aucun
> consentement — la demande elle-même fonde le traitement. L'ajouter aux **envois marketing**, si.
> Conditionner « je réponds à ta question » à « j'accepte de recevoir de la publicité » n'est pas
> acceptable, et c'est précisément ce que la configuration en cases séparées empêche.
>
> **Les textes sont ceux de HubSpot, non réécrits.** Neutres, génériques, suffisants pour un
> formulaire de contact. Une formulation sur mesure engagerait ALTAV — **elle reste à valider par
> Franck.**

### ⚠️ Deux pièges, vérifiés à l'usage — ils coûtent une heure si on les découvre seul

**1. Les textes de consentement sont stockés par langue.**

L'écran ⚙️ → **Confidentialité et consentement** → **Options de consentement** porte un sélecteur
**« Vue actuelle »**, avec la mention *« Vous ne modifiez que cette langue »*. Le formulaire étant
en français, il lit la variante **Français** — ni **Anglais**, ni **Français (Canada)**, qui a son
propre texte, différent.

Modifier la mauvaise variante **ne produit aucun effet visible**, et rien ne le signale.

**2. Le bloc fige son texte au moment où on le pose.**

Il ne relit **jamais** les paramètres ensuite. Modifier le texte après coup, republier le
formulaire, décocher puis recocher l'option : rien ne le met à jour.

> **La règle qui découle des deux, et qui vaut pour les 5 formulaires suivants :**
>
> **Régler les textes de consentement AVANT de poser le bloc.**
>
> Si c'est déjà posé, la seule issue est de **supprimer le bloc et de le reposer**. Il revient
> alors **nu** : il faut reconfigurer l'abonnement `Marketing Information` et sa case, sinon le
> consentement marketing disparaît sans bruit.
