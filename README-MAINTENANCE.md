# gold-strategies.com — maintenance du site

Ce dossier **est** le site en production. Il n'y a pas d'étape de build ici :
`git push origin main` déploie directement sur Hostinger (déploiement Git natif,
mise en ligne en ~30 s).

- Repo : https://github.com/oliver0034/gold-strategies-site — branche `main`
- Serveur local : `.claude/launch.json` → configuration `site-gold-strategies`
  (python3 http.server sur le port 8642, racine `refonte/`)

---

## 1. Deux chartes coexistent

| Zone | Pages | Feuille de style | Origine |
|---|---|---|---|
| **Astro** | `/` + les 9 pages du menu (`a-propos`, `analyses`, `capital-finance-prop-firm`, `communaute`, `complement-revenu`, `formation`, `methode`, `resultats`, `trading-de-lor`) | `_astro/gold.*.css` (build hashé) | refonte du 25/07/2026 |
| **Legacy** | `/blog/` + les ~80 articles + `contact`, `mentions-legales`, `disclaimer-risque`, `politique-conflits-interets`, `augmenter-pouvoir-achat` | `assets/style.css` | site d'origine |

**Le blog reste volontairement en charte legacy** : migrer 80 articles n'apporterait
rien de mesurable pour un coût élevé. Un nouvel article se rédige donc dans la charte
legacy (voir §4).

### ⚠ Les sources Astro ne sont pas dans ce repo

Ce qui est committé, c'est **le résultat du build** (HTML minifié + `_astro/`). Il n'y a
pas d'`astro.config.*` ni de `Layout.astro` sur le Mac : les sources vivent ailleurs
(session Cowork). Conséquence directe :

> **Tout rebuild Astro écrase les 10 pages ci-dessus et supprime les correctifs du §2.**
> Après un rebuild, relire ce fichier et réappliquer les correctifs.

---

## 2. Correctifs appliqués par-dessus le build Astro

Deux fichiers non générés par Astro, donc jamais écrasés :

- `assets/site-fixes.css`
- `assets/nav-mobile.js`

Ils sont référencés dans les 10 pages Astro (`<link>` avant `</head>`,
`<script defer>` avant `</body>`). C'est **cette référence** qu'un rebuild fait sauter.

### Ce qu'ils corrigent

1. **Navigation mobile absente.** Le build masque `.navlinks` sous 1180px sans fournir
   de bouton burger : plus aucune navigation possible sur mobile et tablette.
   `nav-mobile.js` reconstruit un menu à partir des liens déjà présents dans le DOM
   (il suit donc automatiquement les changements de menu côté Astro).
2. **Vignettes rognées.** `.tile-img` était en ratio 820/462 alors que les bannières
   d'articles sont en 40/21 (1600×840, 1200×630) : les bords étaient coupés, donc le
   titre incrusté dans la bannière aussi.

### Réappliquer après un rebuild

```bash
cd "refonte" && python3 - <<'PY'
import pathlib
pages = ['index.html','a-propos/index.html','analyses/index.html','capital-finance-prop-firm/index.html',
         'communaute/index.html','complement-revenu/index.html','formation/index.html','methode/index.html',
         'resultats/index.html','trading-de-lor/index.html']
CSS = '<link rel="stylesheet" href="/assets/site-fixes.css?v=20260725">'
JS  = '<script src="/assets/nav-mobile.js?v=20260725" defer></script>'
for rel in pages:
    p = pathlib.Path(rel); s = p.read_text(encoding='utf-8')
    if 'site-fixes.css' in s: print('déjà patché :', rel); continue
    p.write_text(s.replace('</head>', CSS+'</head>', 1).replace('</body>', JS+'</body>', 1), encoding='utf-8')
    print('patché :', rel)
PY
```

Le vrai correctif, à terme : porter ces deux points dans les sources Astro
(`Layout.astro` + le composant de galerie) pour pouvoir supprimer ces fichiers.

---

## 3. Cache-busting

`assets/style.css` est appelé avec `?v=AAAAMMJJ` dans les pages legacy.
**Toute modification de `style.css` impose de bumper cette version partout**, sinon les
visiteurs gardent l'ancienne feuille en cache :

```bash
cd "refonte" && grep -rl "style.css?v=20260725" --include="*.html" . | xargs sed -i '' 's|style\.css?v=20260725|style.css?v=NOUVELLE_DATE|g'
```

Même logique pour `site-fixes.css` / `nav-mobile.js` (paramètre `?v=` dans les 10 pages Astro).

---

## 4. Publier un article hebdo — les 5 points d'intégration

Le skill `~/.claude/skills/analyse-hebdo-gold-strategies/` automatise tout ça. En manuel,
ne pas oublier un seul de ces points :

1. `blog/[slug]/index.html` — l'article, charte legacy (gabarit de référence :
   `blog/analyse-hebdo-petrole-100-taux-4-pourcent-25-juillet-2026/`)
2. `blog/index.html` — carte en **première position** de `.blog-grid` **et** compteur
   « N analyses & réflexions » incrémenté
3. `index.html` — tuile en première position de la galerie `#galTrack` (garder 6 tuiles :
   retirer la plus ancienne)
4. `sitemap.xml` — URL de l'article, priorité 0.5
5. `img/blog/[slug-tronqué]-1.jpg` — bannière convertie :
   `sips -s format jpeg -s formatOptions 82 --resampleWidth 1600 [source] --out img/blog/[nom].jpg`
   (viser < 300 Ko, **ratio 40/21** pour ne pas être rognée)

La bannière contient le titre → le `h1` de l'article doit être `class="sr-only"`.
Pas de schéma `FAQPage` (convention du site).

---

## 5. Vérifications avant push

```bash
cd "refonte" && python3 -m http.server 8642
```

- Desktop **et** mobile 375 px sur : l'accueil, `/blog/`, le nouvel article
- Mobile : le burger ouvre bien le menu sur les pages Astro **et** sur les pages legacy
- Article en mobile : le tableau défile dans son `.tableau-wrapper` sans faire déborder la page
- Console sans erreur
