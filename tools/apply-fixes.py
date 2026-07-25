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

VERSION = "20260725"
CSS_TAG = '<link rel="stylesheet" href="/assets/site-fixes.css?v=%s">' % VERSION
JS_TAG = '<script src="/assets/nav-mobile.js?v=%s" defer></script>' % VERSION

CSS_RE = re.compile(r'<link[^>]+assets/site-fixes\.css[^>]*>')
JS_RE = re.compile(r'<script[^>]+assets/nav-mobile\.js[^>]*></script>')

ROOT = pathlib.Path(__file__).resolve().parent.parent
SKIP_DIRS = {"_astro", "img", "assets", "tools", "astro-patch", ".git", "blog"}


def astro_pages():
    """Pages HTML issues du build Astro : elles chargent une feuille /_astro/*.css."""
    found = []
    for path in sorted(ROOT.rglob("*.html")):
        rel = path.relative_to(ROOT)
        if rel.parts[0] in SKIP_DIRS:
            continue
        head = path.read_text(encoding="utf-8", errors="ignore")[:4000]
        if "/_astro/" in head and "stylesheet" in head:
            found.append(path)
    return found


def apply(path):
    """Retourne True si le fichier a été modifié."""
    src = path.read_text(encoding="utf-8")
    out = src

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
        return 0

    if mode == "--check":
        missing = []
        for p in pages:
            s = p.read_text(encoding="utf-8")
            if not (CSS_RE.search(s) and JS_RE.search(s)):
                missing.append(p.relative_to(ROOT))
        if missing:
            print("✗ correctifs absents de %d page(s) :" % len(missing))
            for m in missing:
                print("   -", m)
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
