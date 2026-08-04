# 3. Mise en œuvre dans HubSpot

Abonnement actuel : **Starter** *(~15 €/mois — formule exacte à confirmer)*. Le tableau ci-dessous
décrit ce qui était déjà acquis en Free :

| Brique | Free | Rôle |
|---|---|---|
| Propriété custom `type_compte` (liste déroulante) | ✅ | Porter l'axe 2 |
| Formulaires à **champ caché** (Hidden + Default value) | ✅ | **Classer à la source** — le levier principal |
| Segments actifs sur propriété de contact | ✅ 10 actifs | Isoler B2B / B2C |
| Objet Entreprise + association auto par domaine email | ✅ | Documenter l'employeur, **sans piloter `type_compte`** |
| Pipelines de transaction | ⚠️ 1 seul | Starter en donne 2 = split B2B / B2C |
| Workflows | ❌ Professional | Classement automatique sur signaux 3 à 5 |

### Écarté, et pourquoi

| Piste | Raison du rejet |
|---|---|
| Propriété calculée | Une équation n'accepte qu'**une seule** propriété non-numérique, et seulement du même objet. Ne peut pas évaluer « domaine hors freemail ET poste décideur ». |
| Classement par domaine email | HubSpot ne sait pas tester un domaine contre une liste de freemails sans action codée (Ops Hub Pro) ou énumération manuelle. |
| Inférence sur `Société` / intitulé de poste | Basculerait ~800 individuels à tort (voir plus haut). |

### Trajectoire de palier

- **Free** — tout ce qui précède. Suffisant pour classer proprement.
- **Starter** *(souscrit)* — 2 pipelines de transaction, soit exactement le split B2B / B2C.
- **Professional** — workflows : classement automatique et bascule rétroactive.

> ⚠️ **Le compteur à surveiller n'est pas le prix mensuel, c'est le nombre de contacts
> *marketing*.** HubSpot facture les contacts démarchés, pas les contacts stockés. Le chantier
> de réactivation des **6 241 dormants** peut donc coûter bien plus que l'abonnement de base.
> À chiffrer avant de le lancer, pas après.

