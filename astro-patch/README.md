# Patch à porter dans les sources Astro

Le site en production (`refonte/`) contient deux correctifs posés **par-dessus** le build
Astro, parce que les sources ne sont pas sur le Mac. Tant qu'ils ne sont pas portés dans
les sources, chaque rebuild les efface.

Ce dossier contient de quoi les corriger à la source, une fois pour toutes. Il ne sert
qu'à ça : il n'est pas servi aux visiteurs et peut être supprimé une fois le portage fait.

---

## Patch 1 — Menu mobile (bloquant)

**Symptôme** : sous 1180px, `.navlinks` est masqué par le CSS et aucun bouton burger
n'existe. Sur l'accueil et les 9 pages du menu, un visiteur mobile n'a **aucun moyen de
naviguer**. Les pages du blog ne sont pas concernées (elles ont leur propre menu).

**Correctif** : le composant [`MobileNav.astro`](./MobileNav.astro) de ce dossier.

1. Copier le fichier dans `src/components/MobileNav.astro`.
2. Dans `src/layouts/Layout.astro`, l'importer et l'inclure **une seule fois**, juste
   avant `</body>` :

   ```astro
   ---
   import MobileNav from '../components/MobileNav.astro';
   ---
   ...
     <MobileNav />
   </body>
   ```

3. Faire de même dans `src/pages/index.astro` **tant que l'accueil n'utilise pas le
   Layout** (le HTML de production porte encore le commentaire « la page d'accueil
   n'utilise pas encore Layout.astro »). Si l'accueil passe au Layout, retirer l'inclusion
   en double.

Le composant ne redéclare aucun lien : il reconstruit le menu à partir de ceux déjà
présents dans `.nav .navlinks` et `.nav .nav-cta`. Modifier le menu du site suffit, le
menu mobile suit — rien à maintenir en double.

---

## Patch 2 — Ratio des vignettes d'analyses

**Symptôme** : les bannières d'articles sont au format **40/21** (1600×840, 1200×630).
La galerie les affichait en `820/462` avec un `scale(1.04)` au repos, ce qui rognait les
bords — donc le titre incrusté dans la bannière.

**Correctif**, dans le composant de la galerie (celui qui produit `#galTrack` / `.tile`) :

```diff
- .tile-img { aspect-ratio: 820/462; }
+ .tile-img { aspect-ratio: 40/21; }

- .tile-img img { ...; transform: scale(1.04); }
+ .tile-img img { ...; transform: none; }
  .tile:hover .tile-img img { transform: scale(1.06); }
```

Et corriger les attributs `width`/`height` des `<img>` de tuiles : `820`/`462` → `1600`/`840`.

---

## Après le portage — nettoyage

Une fois les deux patches dans les sources, le build rendu et déployé :

1. Vérifier en mobile 375px sur l'accueil **et** une page du menu : le burger ouvre bien
   le menu, et les vignettes ne sont plus rognées.
2. Supprimer les béquilles du repo de production :
   - `assets/nav-mobile.js`
   - `assets/site-fixes.css`
   - les `<link>` / `<script>` correspondants dans les 10 pages Astro
     (`python3 tools/apply-fixes.py --remove` le fait proprement)
3. Retirer de `tools/check-site.py` la vérification `astro_fixes` (une constante en tête
   du fichier suffit : `EXPECT_FIXES = False`).
4. Supprimer ce dossier `astro-patch/`.

Tant que ce nettoyage n'est pas fait, **garder les béquilles** : `tools/check-site.py`
bloque le push si elles manquent, c'est volontaire.
