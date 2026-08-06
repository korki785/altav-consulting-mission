# 7. Roadmap — de l'état actuel à la fin de mission

L'objectif de la mission est une seule chose : **lever le goulot de conversion.** Pas installer
un CRM. Le CRM n'est que le socle sans lequel rien ne se déclenche.

Le chiffre qui mesure la réussite existe déjà : **promo 8 — 136 pré-inscrits, 26 confirmés.**
Les 110 autres n'ont pas été relancés, non par négligence mais parce que rien ne déclenchait la
relance. La mission est finie quand ce ratio se pilote et s'améliore tout seul.

Six phases. Chacune se lit : ce qu'on installe, ce qui la débloque, ce qu'elle produit, et à
quoi on sait qu'elle est terminée.

---

## Phase 0 — Le socle *(terminée)*

Base nettoyée, classée, importée, requalifiée. **7 483 contacts**, 4 axes de classification,
propriétaire du CRM désigné.

**Terminée quand :** ✅ le CRM contient une base fiable et un propriétaire nommé.

> **Précision du 6 août.** Franck est propriétaire et décideur ; **Stéphane administrera l'outil
> en exploitation** — *« ce n'est pas moi qui vais gérer une fois en exploitation »*. Le
> propriétaire nommé ne change pas, celui qui tient l'outil au quotidien, si. D'où la
> [phase 6](#phase-6--la-passation--que-loutil-survive-à-la-mission).

---

## Phase 1 — Acquisition : que le lead naisse déjà classé

*C'est la phase en cours. Rien de ce qui suit ne fonctionne sans elle.*

Aujourd'hui aucun formulaire n'alimente HubSpot. La base est un instantané figé au 20/07 :
chaque nouveau lead entre par Wix, tombe dans une boîte que personne ne relève, et repart dans
le désordre qu'on vient de nettoyer.

**Ce qu'on installe**

1. Les **6 formulaires HubSpot** — pré-inscription, demande d'information, contact général,
   « je souhaite former mes équipes », livre blanc, et session d'info *(proposée, pas demandée)*. Chacun porte un champ caché qui
   écrit `Température CRM` et `Type de compte` **à la seconde de la soumission**.
2. Le **formulaire du pied de page** refait et embarqué dans le site, champ `Statut` conservé.
3. La **bascule des anciens liens** : chaque ancien formulaire d'acquisition est vidé et
   repointé. Les QR codes imprimés et les liens WhatsApp continuent de fonctionner.

**Priorité absolue :** l'ancien formulaire de pré-inscription et le formulaire du pied de page.
Ce sont les deux seuls canaux réellement vivants — les quatre formulaires nommés
« Pré-inscription » dans l'appli Wix ne reçoivent plus rien depuis février 2025.

**Dans quel ordre — arbitré le 6 août par Franck.** Le **pied de page passe en premier**, comme
pilote : *« Faisons d'abord un test par celui du bas de page comme test. »* C'est le formulaire
le plus petit et celui qui ne porte aucun chiffre d'affaires — il éprouve la plomberie sans
risque. La pré-inscription vient ensuite, **avec Stéphane**, parce qu'elle n'est pas un terrain
vierge : *« il y a plusieurs choses qui ont été mises en place, il faudra sûrement les
améliorer »*. On inventorie avant d'écraser quoi que ce soit.

**Débloqué par :** accord de Franck avant toute création sur son compte · disponibilité de
Stéphane pour la pré-inscription.

**Terminée quand :** une soumission de test arrive dans HubSpot **déjà étiquetée**, sans
intervention humaine, et notifie qui de droit. *(Notification par e-mail, pas tâche : les
workflows sont verrouillés — vérifié le 5 août. Destinataire à trancher : Franck, Stéphane, ou
les deux.)*

---

## Phase 2 — Le cycle de vie : savoir où en est chacun

Sans étape, pas de mesure. Sans mesure, pas de pilotage.

**Ce qu'on installe**

- Les **7 étapes** définies par Franck : Prospect → Pré-inscrit → Frais réglés → Affecté à une
  promotion → Participant → Certifié → Alumni.
- La propriété interne **`promo`**, renseignée par Altav **après** encaissement — jamais
  demandée au prospect.
- Le **pipeline de transaction**, dédoublé B2B / B2C. *(Starter en autorise 2 : c'est
  exactement le split.)*
- L'articulation avec `Tag_CRM` : `Tag_CRM` reste l'axe d'origine et ne bouge plus, le cycle de
  vie devient l'axe opérationnel.

**Terminée quand :** on peut répondre, sans ouvrir un fichier, à « combien de pré-inscrits
n'ont pas encore payé, et depuis combien de temps ».

---

## Phase 3 — Les séquences : le premier gain rentable

C'est ici que la mission produit du chiffre d'affaires.

**Ce qu'on installe**

| Déclencheur | Action |
|---|---|
| À la soumission | mail de confirmation réécrit *(l'actuel est trop brut)* + notification à Franck |
| Sous 5 minutes | rappel téléphonique du pré-inscrit |
| J + 5 | envoi du livre blanc |
| J + 30 | relance des non-confirmés |
| Fin de promo | bascule automatique sur la promo suivante |

**⚠️ Point de décision — le palier HubSpot.** *Vérifié le 5 août : les workflows sont
verrouillés.* HubSpot renvoie vers **Sales Hub Pro** et cite « créez des tâches » parmi ce qu'ils
débloquent. Un **essai de 14 jours** est proposé, sans frais ni renouvellement automatique.
Trois issues :

1. **Monter en Professional** — la seule qui donne les séquences complètes.
2. **Rester en Starter** et se limiter aux automatisations natives des formulaires
   *(mail de confirmation, notification par e-mail)*. Le J+5 / J+30 / bascule promo devient manuel.
3. **Différer** — installer les phases 1 et 2, mesurer un mois, décider sur des chiffres réels.

*Recommandation : option 3.* Après un mois de phase 1, on connaît le volume réel de leads
entrants et le coût du travail manuel. Le palier se justifie alors par un calcul, pas par une
intuition. **À arbitrer avec Franck, pas seul.**

**L'essai de 14 jours est une cartouche unique.** Le déclencher pendant qu'on débogue encore le
mapping, c'est le gaspiller à regarder des erreurs de configuration. Ordre imposé : formulaires
testés et mapping vérifié **d'abord**, essai **ensuite**, décision **après**.

En attendant, tout ce qui ne demande pas de workflow est installé et fonctionne — voir
[solution provisoire](09-solution-provisoire.md), qui porte aussi la checklist de bascule du jour
de l'upgrade.

**Terminée quand :** un pré-inscrit qui ne paie pas reçoit trois relances sans que personne
n'y pense.

---

## Phase 4 — Les dormants et la facturation : le chiffre déjà acquis

Deux chantiers indépendants, tous deux du CA laissé sur la table.

**Réactivation des 6 196 dormants** — des contacts accumulés depuis 2017, jamais réexploités.
Segmentation puis séquences de contenu.

> **⚠️ À chiffrer avant de lancer, pas après.** HubSpot facture les contacts **marketing**, pas
> les contacts stockés. Basculer 6 196 dormants en marketing peut coûter bien plus que
> l'abonnement de base. Le compteur à surveiller n'est pas le prix mensuel.

**Relances de facturation** — les échéances en 11 fois occupent aujourd'hui **un salarié à 80 %
de son temps**. C'est le gain le plus mesurable de toute la mission : du temps rendu au suivi
commercial, immédiatement.

**Terminée quand :** les relances de paiement partent seules, et le salarié concerné fait autre
chose.

---

## Phase 5 — La mesure : rendre le pilotage possible

Franck a demandé quatre choses de chaque formulaire : qualifier, déclencher, alimenter les
tableaux de bord, mesurer les taux de conversion. Les trois premières sortent des phases 1 à 3.
La quatrième se construit ici.

- Tableau de bord : entrées par canal, taux de conversion par étape du cycle de vie, délai
  moyen entre pré-inscription et paiement.
- Le ratio de la promo 8 recalculé automatiquement à chaque promo.

**Limite connue et non résolue :** l'objectif **80 % B2B / 20 % B2C se pilote par zone**, or
`Pays` n'est renseigné que sur **8 %** de la base. Deux voies : capter le pays à la source dans
les nouveaux formulaires *(gratuit, mais ne règle que le futur)*, ou enrichir l'existant
*(payant, à arbitrer)*. Le fichier des 525 pré-inscriptions apporte déjà **société, poste et
secteur pour 437 personnes** — de quoi commencer sur le B2B/B2C, à défaut de la géographie.

**Terminée quand :** Franck ouvre un écran et voit son taux de conversion sans demander à
personne.

---

## Phase 6 — La passation : que l'outil survive à la mission

*Ouverte le 6 août. Franck : « il faudra que Stéphane sache l'administrer, ce n'est pas moi qui
vais gérer une fois en exploitation. »*

Tout ce qui précède est construit par quelqu'un qui part. Un CRM que l'administrateur n'ose pas
modifier se fige, puis se contourne — et le désordre des 167 libellés se reconstitue par la même
mécanique qu'en 2022 : un formulaire créé ailleurs parce que le bon endroit fait peur.

**Ce qu'on installe**

- Le **périmètre administré par Stéphane**, arbitré avec Franck : formulaires, propriétés, vues.
- Un **accès HubSpot** aux droits correspondants.
- Un **mode d'emploi d'administration** — créer un formulaire, poser un champ caché, modifier
  une vue enregistrée.
- Une **passation à blanc** : Stéphane crée seul un formulaire de bout en bout.

**Débloqué par :** la phase 1 *(il faut quelque chose à administrer)* · la disponibilité de
Stéphane.

**Terminée quand :** Stéphane crée et modifie un formulaire sans nous appeler, et un lead entré
par ce formulaire arrive classé.

> Le critère est la passation à blanc, **pas** le mode d'emploi. Un document que personne n'a
> exécuté ne prouve rien.

---

## Ce qui peut faire échouer la mission

Trois risques, par ordre de probabilité. Aucun n'est technique.

1. **L'adoption — et elle se joue maintenant à deux endroits.** Un CRM que personne ne tient
   redevient un Excel. Franck décide et porte 70 à 80 % du chiffre d'affaires : **chaque
   automatisation doit lui retirer un geste**, une seule qui lui en crée un et le système sera
   contourné. Mais c'est **Stéphane** qui tiendra l'outil, et il n'aura pas assisté à sa
   construction : ce qui est astucieux pour Franck peut être intouchable pour lui. Les deux
   contraintes ne tirent pas dans le même sens, et arbitrer en faveur de la seule commodité de
   Franck fait perdre l'administrateur.
2. **Le désordre qui se reconstitue.** La cause racine des 167 libellés, c'est un formulaire
   neuf à chaque événement pendant quatre ans. Franck s'est engagé sur le principe ; l'engagement
   tient tant que créer un formulaire dans HubSpot reste plus simple que dans Wix.
3. **Le palier différé indéfiniment.** Sans workflows, les phases 1 et 2 posent le socle mais le
   gain reste théorique. Décider, même de rester en Starter — mais décider.
