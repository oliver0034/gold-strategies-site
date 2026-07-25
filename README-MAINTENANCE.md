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
python3 tools/apply-fixes.py
```

Idempotent : ne fait rien s'il n'y a rien à réparer. Les pages Astro sont détectées
automatiquement (celles qui chargent `/_astro/*.css`), donc ajouter une page au site ne
demande aucune modification de l'outillage.

### Le correctif définitif

`astro-patch/` contient le composant `MobileNav.astro` et les instructions pour porter
les deux correctifs **dans les sources Astro** — c'est ce qu'il faut faire dès qu'on
remet la main sur le projet source. Une fois fait, `python3 tools/apply-fixes.py --remove`
retire les béquilles et `EXPECT_FIXES = False` dans `tools/check-site.py` désactive le
contrôle correspondant.

---

## 3. Cache-busting

`assets/style.css` est appelé avec `?v=AAAAMMJJ` dans les pages legacy.
**Toute modification de `style.css` impose de bumper cette version partout**, sinon les
visiteurs gardent l'ancienne feuille en cache :

```bash
cd "refonte" && grep -rl "style.css?v=20260725" --include="*.html" . | xargs sed -i '' 's|style\.css?v=20260725|style.css?v=NOUVELLE_DATE|g'
```

Même logique pour `site-fixes.css` / `nav-mobile.js` (paramètre `?v=` dans les 10 pages Astro).

### En-têtes de cache

Depuis le 25/07/2026, `.htaccess` fixe explicitement les en-têtes (avant, le HTML n'en
avait aucun et les navigateurs gardaient une page publiée plusieurs heures — une
publication pouvait rester invisible malgré un déploiement réussi) :

| Type | `Cache-Control` |
|---|---|
| `.html` | `no-cache, must-revalidate` (revalidé à chaque visite, l'ETag évite le retéléchargement) |
| `.css` `.js` | `public, max-age=604800` — d'où l'importance du `?v=` |
| images, polices | `public, max-age=31536000` (noms uniques par article) |
| `.xml` `.txt` | `public, max-age=3600` |

Vérification : `curl -sI https://gold-strategies.com/blog/ | grep -i cache-control`.

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

## 5. Outillage

| Commande | Rôle |
|---|---|
| `python3 tools/check-site.py` | contrôles avant déploiement (voir ci-dessous) |
| `python3 tools/apply-fixes.py` | réinjecte les correctifs dans les pages Astro |
| `python3 tools/apply-fixes.py --check` | vérifie sans rien modifier |
| `python3 tools/apply-fixes.py --remove` | retire les correctifs (après portage dans Astro) |
| `sh tools/install-hooks.sh` | (ré)installe le garde-fou `pre-push` |

`check-site.py` vérifie : correctifs présents sur les pages Astro, une seule version de
cache-busting, `sitemap.xml` ↔ dossiers `blog/`, compteur du blog = nombre de cartes,
images référencées présentes, ratio des bannières mises en avant (avertissement).

### Garde-fou pre-push

Un hook `pre-push` lance `check-site.py` et **refuse le push** si le site partirait
cassé — puisqu'un push est un déploiement immédiat. Il est déjà installé sur ce Mac ;
après un nouveau clone, le remettre avec `sh tools/install-hooks.sh`.
En cas d'urgence : `git push --no-verify`.

---

## 6. Vérifications visuelles avant push

```bash
cd "refonte" && python3 -m http.server 8642
```

- Desktop **et** mobile 375 px sur : l'accueil, `/blog/`, le nouvel article
- Mobile : le burger ouvre bien le menu sur les pages Astro **et** sur les pages legacy
- Article en mobile : le tableau défile dans son `.tableau-wrapper` sans faire déborder la page
- Console sans erreur
