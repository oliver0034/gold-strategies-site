#!/usr/bin/env python3
"""
apply-fixes.py — (ré)injecte les correctifs maison dans les pages générées par Astro.

Les sources Astro ne sont pas sur ce Mac : seul le build est committé. Chaque rebuild
écrase les pages et retire les références à `assets/site-fixes.css` et
`assets/nav-mobile.js` (menu mobile + ratio des vignettes). Ce script les remet.

Il est idempotent : le relancer ne fait rien s'il n'y a rien à réparer.
Les pages Astro sont détectées automatiquement (celles qui chargent `/_astro/…css`),
donc l'ajout d'une page au site ne demande aucune modification ici.

Usage :
    python3 tools/apply-fixes.py            # répare
    python3 tools/apply-fixes.py --check    # ne modifie rien, code de sortie 1 si à réparer
    python3 tools/apply-fixes.py --remove   # retire les correctifs (après portage dans Astro)

À lancer depuis la racine du site (`refonte/`).
"""

import pathlib
import re
import sys

# Cache-busting des deux correctifs. Ces valeurs doivent être celles réellement
# en ligne : le script REMPLACE le `?v=` existant, donc une constante en retard
# rétrograde silencieusement la version et fait resservir une feuille en cache.
# Les deux fichiers évoluant séparément, ils ont leur propre version.
CSS_VERSION = "202607261"   # assets/site-fixes.css — bumpé le 26/07/2026
JS_VERSION = "20260725"     # assets/nav-mobile.js
CSS_TAG = '<link rel="stylesheet" href="/assets/site-fixes.css?v=%s">' % CSS_VERSION
JS_TAG = '<script src="/assets/nav-mobile.js?v=%s" defer></script>' % JS_VERSION

CSS_RE = re.compile(r'<link[^>]+assets/site-fixes\.css[^>]*>')
JS_RE = re.compile(r'<script[^>]+assets/nav-mobile\.js[^>]*></script>')

# --- retouches de texte sur les pages Astro ----------------------------------
# Un rebuild réécrit aussi le CONTENU des pages, pas seulement les balises de
# ressources : toute correction SEO faite à la main ici disparaît en silence.
# Chaque entrée est un couple (texte du build, texte voulu). L'application est
# idempotente : on ne remplace que si l'ancien texte est là et le nouveau absent.
#
# formation/index.html — plan éditorial du 03/08/2026, page 10 du backlog :
# la page est à 100 % une formation sur l'or et ni « or » ni « XAUUSD »
# n'apparaissait dans son title, son H1 ou sa meta. Voir plan-editorial-seo.md.
TEXT_PATCHES = {
    "formation/index.html": [
        ("Formation trading : apprendre de zéro | Gold Strategies",
         "Formation trading sur l'or (XAUUSD), de zéro | Gold Strategies"),
        ("La formation Gold Strategies pour apprendre à trader de zéro :",
         "La formation Gold Strategies pour apprendre à trader l'or (XAUUSD) de zéro :"),
        ('<h1 class="h1split">Apprendre à trader de zéro,',
         '<h1 class="h1split">Apprendre à trader l\'or de zéro,'),
        ("Vous ne deviendrez pas régulier sur les marchés avec des intuitions.",
         "Vous ne deviendrez pas régulier sur le XAUUSD avec des intuitions."),
    ],
}

ROOT = pathlib.Path(__file__).resolve().parent.parent
SKIP_DIRS = {"_astro", "img", "assets", "tools", "astro-patch", ".git", "blog"}


def astro_pages():
    """Pages HTML issues du build Astro : elles chargent une feuille /_astro/*.css."""
    found = []
    for path in sorted(ROOT.rglob("*.html")):
        rel = path.relative_to(ROOT)
        if rel.parts[0] in SKIP_DIRS:
            continue
        # 8000 et pas 4000 : la moitié des pages Astro ont un <head> plus long
        # (schémas JSON-LD) et passaient sous le radar — check-site.py, lui, en
        # voyait 12. Garder les deux scripts sur la même fenêtre.
        head = path.read_text(encoding="utf-8", errors="ignore")[:8000]
        if "/_astro/" in head and "stylesheet" in head:
            found.append(path)
    return found


def text_patches(path):
    """Retouches de texte attendues sur cette page (liste éventuellement vide)."""
    return TEXT_PATCHES.get(path.relative_to(ROOT).as_posix(), [])


def missing_text_patches(path, src=None):
    """Retouches encore à appliquer : l'ancien texte est là, le nouveau non."""
    src = src if src is not None else path.read_text(encoding="utf-8")
    return [(old, new) for old, new in text_patches(path)
            if new not in src and old in src]


def apply(path):
    """Retourne True si le fichier a été modifié."""
    src = path.read_text(encoding="utf-8")
    out = src

    for old, new in missing_text_patches(path, out):
        out = out.replace(old, new)

    if CSS_RE.search(out):
        out = CSS_RE.sub(CSS_TAG, out, count=1)   # remet la bonne version si elle a dérivé
    elif "</head>" in out:
        out = out.replace("</head>", CSS_TAG + "</head>", 1)

    if JS_RE.search(out):
        out = JS_RE.sub(JS_TAG, out, count=1)
    elif "</body>" in out:
        out = out.replace("</body>", JS_TAG + "</body>", 1)

    if out != src:
        path.write_text(out, encoding="utf-8")
        return True
    return False


def remove(path):
    src = path.read_text(encoding="utf-8")
    out = JS_RE.sub("", CSS_RE.sub("", src))
    if out != src:
        path.write_text(out, encoding="utf-8")
        return True
    return False


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else ""
    pages = astro_pages()

    if not pages:
        print("✗ aucune page Astro détectée — lancer le script depuis la racine du site")
        return 1

    if mode == "--remove":
        touched = [p for p in pages if remove(p)]
        for p in touched:
            print("correctifs retirés :", p.relative_to(ROOT))
        print("%d page(s) nettoyée(s) sur %d." % (len(touched), len(pages)))
        print("Penser à supprimer assets/site-fixes.css et assets/nav-mobile.js.")
        print("Les retouches de texte (TEXT_PATCHES) ne sont PAS annulées : les "
              "rétablir reviendrait à remettre en ligne les anciens title/H1.")
        return 0

    if mode == "--check":
        missing = []
        for p in pages:
            s = p.read_text(encoding="utf-8")
            if not (CSS_RE.search(s) and JS_RE.search(s)):
                missing.append((p.relative_to(ROOT), "correctifs CSS/JS"))
            for old, _ in missing_text_patches(p, s):
                missing.append((p.relative_to(ROOT), "texte : « %s… »" % old[:48]))
        if missing:
            print("✗ %d correctif(s) à réappliquer :" % len(missing))
            for m, what in missing:
                print("   -", m, "—", what)
            print("  → python3 tools/apply-fixes.py")
            return 1
        print("✓ correctifs présents sur les %d pages Astro." % len(pages))
        return 0

    touched = [p for p in pages if apply(p)]
    for p in touched:
        print("patché :", p.relative_to(ROOT))
    if touched:
        print("%d page(s) réparée(s) sur %d — à committer." % (len(touched), len(pages)))
    else:
        print("✓ rien à faire, les %d pages Astro sont à jour." % len(pages))
    return 0


if __name__ == "__main__":
    sys.exit(main())
