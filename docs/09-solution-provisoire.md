# 9. Solution provisoire — sans workflows, sans payer

**Décision du 5 août 2026.** Les workflows sont verrouillés sur l'abonnement actuel : HubSpot
renvoie vers **Sales Hub Pro**. Plutôt que de payer avant d'avoir quoi que ce soit à automatiser,
on installe tout ce qui fonctionne sans eux et on garde l'essai de 14 jours pour plus tard.

> **Le raisonnement.** L'essai de 14 jours est une cartouche unique. Le déclencher pendant qu'on
> débogue encore le mapping des formulaires, c'est le gaspiller à regarder des erreurs de
> configuration. On teste la plomberie gratuitement ; l'essai sert à éprouver les séquences, une
> fois la plomberie prouvée.

---

## Ce qui fonctionne dès maintenant, sans rien payer

**Tout le cœur du dispositif.** C'est le point important : le provisoire ne touche pas
l'essentiel.

| Fonction | État | Pourquoi ça marche |
|---|---|---|
| Formulaires HubSpot | ✅ disponible | inclus dès la version gratuite |
| **Champs cachés** — `Température CRM`, `Type de compte` | ✅ disponible | c'est un réglage de champ, pas une automatisation |
| Classement du lead à la seconde de la soumission | ✅ disponible | conséquence directe du point précédent |
| Notification par e-mail à Franck | ✅ disponible | réglage natif du formulaire |
| Message de confirmation à l'écran | ✅ disponible | réglage natif |
| Propriétés custom · cycle de vie · pipelines | ✅ disponible | configuration, pas automatisation |
| Vues de contacts filtrées et enregistrées | ✅ disponible | remplacent les listes actives |

**Rien de tout cela ne sera à refaire au moment de l'upgrade.** Le classement à la source — le
cœur de la mission — n'attend aucun palier.

---

## Ce qui est réellement provisoire

Trois lignes, et une seule coûte quelque chose.

| Cible | Provisoire | Coût de bascule le jour J |
|---|---|---|
| Tâche assignée à Franck | **notification par e-mail** | nul — une case à cocher dans le formulaire |
| Mail de confirmation automatique | **mail de suivi natif du formulaire** | nul |
| **J+5 · J+30 · bascule promo** | **manuel, depuis des vues enregistrées** | c'est ici que ça pique |

### Les vues enregistrées — le substitut concret

Trois vues de contacts, filtrées, à créer une fois :

| Vue | Filtre | Franck y fait quoi |
|---|---|---|
| **Livre blanc à envoyer** | `Température CRM = INBOUND` **et** date de création > il y a 5 jours **et** livre blanc non envoyé | envoie le PDF |
| **Pré-inscrits à relancer** | `Date de pré-inscription` entre 30 et 60 jours **et** cycle de vie = *Pré-inscrit* | relance |
| **Non convertis de la promo en cours** | cycle de vie = *Pré-inscrit* **et** `Date de pré-inscription` > 60 jours | bascule sur la promo suivante |

**À dire sans l'enjoliver :** ces trois vues demandent à Franck de les ouvrir chaque semaine. Il
est seul et porte 70 à 80 % du chiffre d'affaires. **Il y a un risque réel qu'elles ne soient pas
ouvertes.** C'est précisément ce que l'upgrade supprime — et c'est l'argument chiffré à lui
présenter le jour venu.

---

## Le déclencheur de sortie du provisoire

Le provisoire ne s'arrête pas « quand on y pensera ». Il s'arrête sur un **événement vérifiable** :

> **Quand les 6 formulaires sont créés, testés, et que le mapping est vérifié dans HubSpot —
> c'est-à-dire quand une soumission de test produit un contact correctement classé — on lance
> l'essai de 14 jours.**

Pendant ces 14 jours : configuration des séquences, fonctionnement en vraie grandeur, mesure.
À l'issue, deux sorties propres — on convertit avec des chiffres en main, ou on arrête en sachant
exactement ce qu'on perd.

**Ordre imposé, et il compte :**

1. Formulaires créés et testés *(gratuit)*
2. Mapping vérifié — un contact de test arrive bien classé *(gratuit)*
3. Anciens liens repointés *(gratuit)*
4. **Alors seulement** : essai de 14 jours
5. Séquences configurées et éprouvées pendant l'essai
6. Décision d'upgrade, sur les chiffres

Inverser 3 et 4 gaspille l'essai. C'est la seule erreur vraiment coûteuse de cette phase.

---

## À faire le jour de l'upgrade

Checklist de bascule, pour que rien ne soit oublié ni laissé en double.

- [ ] Basculer les 6 formulaires de « notification par e-mail » vers **création de tâche assignée
      à Franck**
- [ ] Créer les workflows : rappel sous 5 min, livre blanc J+5, relance J+30, bascule promo
- [ ] **Désactiver les trois vues manuelles** — sinon Franck fait le travail deux fois, et c'est
      le meilleur moyen de lui faire abandonner l'outil
- [ ] Vérifier qu'aucun contact ne reçoit deux fois la même relance pendant la période de
      recouvrement
- [ ] Consigner la date de bascule dans le [journal](05-journal.md)

---

## Ce qu'on saura le jour de la décision, et qu'on ne sait pas aujourd'hui

- Le **volume réel** de leads entrants une fois les formulaires branchés — aujourd'hui on
  extrapole depuis Wix : ~17 pré-inscriptions par mois en 2026.
- Le **temps réel** que Franck passe sur les trois vues manuelles.
- Le **prix d'une formation Ubuntu** — je ne l'ai pas. C'est le chiffre qui tranche : si
  récupérer **une seule** des 110 personnes non relancées de la promo 8 couvre l'année
  d'abonnement, la question ne se pose plus.
