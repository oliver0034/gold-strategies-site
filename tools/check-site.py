#!/usr/bin/env python3
"""
check-site.py — contrôles à passer avant de déployer gold-strategies.com.

Vérifie ce qui casse silencieusement en production et qu'un coup d'œil ne rattrape pas :

  1. correctifs maison présents sur les pages Astro (sinon : plus de menu mobile)
  2. une seule version de cache-busting pour assets/style.css sur les pages legacy
  3. sitemap.xml et dossiers blog/ cohérents entre eux
  4. compteur « N analyses & réflexions » = nombre réel de cartes du blog
  5. images référencées par l'accueil et l'index du blog présentes sur le disque
  6. ratio des bannières récentes (avertissement seulement)
  7. bannière du dernier article hebdo TITRÉE (OCR macOS : date de l'article + titre et cartes lisibles)

Code de sortie 1 si un contrôle bloquant échoue — c'est ce qui arrête le hook pre-push.
À lancer depuis la racine du site (`refonte/`) : python3 tools/check-site.py
"""

import pathlib
import re
import shutil
import struct
import subprocess
import sys
import unicodedata

ROOT = pathlib.Path(__file__).resolve().parent.parent
EXPECT_FIXES = True          # passer à False une fois les patches portés dans les sources Astro
BANNER_RATIO = 40 / 21
RATIO_TOLERANCE = 0.04

errors = []
warnings = []


def jpeg_size(path):
    """Dimensions d'un JPEG sans dépendance externe. None si illisible."""
    try:
        with open(path, "rb") as fh:
            if fh.read(2) != b"\xff\xd8":
                return None
            while True:
                b = fh.read(1)
                while b and b != b"\xff":
                    b = fh.read(1)
                marker = fh.read(1)
                while marker == b"\xff":
                    marker = fh.read(1)
                if not marker:
                    return None
                m = marker[0]
                if 0xC0 <= m <= 0xCF and m not in (0xC4, 0xC8, 0xCC):
                    fh.read(3)
                    h, w = struct.unpack(">HH", fh.read(4))
                    return w, h
                size = struct.unpack(">H", fh.read(2))[0]
                fh.seek(size - 2, 1)
    except Exception:
        return None


def legacy_pages():
    return [p for p in ROOT.rglob("*.html") if "assets/style.css" in p.read_text(encoding="utf-8", errors="ignore")[:4000]]


def astro_pages():
    out = []
    for p in sorted(ROOT.rglob("*.html")):
        rel = p.relative_to(ROOT)
        if rel.parts[0] in {"_astro", "img", "assets", "tools", "astro-patch", ".git", "blog"}:
            continue
        head = p.read_text(encoding="utf-8", errors="ignore")[:8000]
        if "/_astro/" in head and "stylesheet" in head:
            out.append(p)
    return out


# --- 1. correctifs sur les pages Astro ---------------------------------------
pages = astro_pages()
if EXPECT_FIXES:
    missing = [p.relative_to(ROOT) for p in pages
               if not ("assets/site-fixes.css" in p.read_text(encoding="utf-8")
                       and "assets/nav-mobile.js" in p.read_text(encoding="utf-8"))]
    if missing:
        errors.append(
            "correctifs absents de %d page(s) Astro (menu mobile HS) : %s\n"
            "    → python3 tools/apply-fixes.py, puis committer"
            % (len(missing), ", ".join(str(m) for m in missing[:5]))
        )
    for asset in ("assets/site-fixes.css", "assets/nav-mobile.js"):
        if not (ROOT / asset).exists():
            errors.append("fichier manquant : %s" % asset)

# --- 2. cache-busting cohérent ------------------------------------------------
versions = set()
for p in legacy_pages():
    versions.update(re.findall(r'assets/style\.css\?v=(\d+)', p.read_text(encoding="utf-8")))
if len(versions) > 1:
    errors.append(
        "plusieurs versions de style.css en circulation : %s\n"
        "    → harmoniser (voir README-MAINTENANCE.md §3)" % ", ".join(sorted(versions))
    )

# --- 3. sitemap ↔ dossiers blog ----------------------------------------------
sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
in_sitemap = set(re.findall(r'gold-strategies\.com/blog/([^/<]+)/', sitemap))
on_disk = {d.name for d in (ROOT / "blog").iterdir() if d.is_dir() and (d / "index.html").exists()}
for slug in sorted(on_disk - in_sitemap):
    errors.append("article absent du sitemap : blog/%s/" % slug)
for slug in sorted(in_sitemap - on_disk):
    errors.append("sitemap : URL sans dossier correspondant : blog/%s/" % slug)

# --- 4. compteur du blog ------------------------------------------------------
blog_index = (ROOT / "blog" / "index.html").read_text(encoding="utf-8")
cards = re.findall(r'class="blog-card', blog_index)
counter = re.search(r'<h2>(\d+) analyses', blog_index)
if not counter:
    errors.append("compteur « N analyses & réflexions » introuvable dans blog/index.html")
elif int(counter.group(1)) != len(cards):
    errors.append(
        "compteur du blog faux : affiche %s, %d cartes réellement présentes"
        % (counter.group(1), len(cards))
    )

# --- 5. images référencées présentes ------------------------------------------
for page in ("index.html", "blog/index.html"):
    html = (ROOT / page).read_text(encoding="utf-8")
    for src in set(re.findall(r'src="(/img/[^"]+)"', html)):
        if not (ROOT / src.lstrip("/")).exists():
            errors.append("image manquante : %s (référencée par %s)" % (src, page))

# --- 6. ratio des bannières mises en avant (avertissement) --------------------
home = (ROOT / "index.html").read_text(encoding="utf-8")
for src in re.findall(r'<img src="(/img/blog/[^"]+)"', home):
    f = ROOT / src.lstrip("/")
    dims = jpeg_size(f) if f.exists() else None
    if dims:
        ratio = dims[0] / dims[1]
        if abs(ratio - BANNER_RATIO) / BANNER_RATIO > RATIO_TOLERANCE:
            warnings.append(
                "%s en %dx%d (ratio %.3f) — attendu 40/21 (%.3f), l'image sera rognée"
                % (src, dims[0], dims[1], ratio, BANNER_RATIO)
            )

# --- 7. bannière hebdo titrée (OCR) -------------------------------------------
# Le 21/11/2026, /banniere a rendu une image SANS AUCUN TEXTE et elle est partie en
# production : les abonnés ont vu une page hors charte (les bannières hebdo portent
# logo, bandeau « ANALYSE HEBDOMADAIRE – date », titre, cartes chiffrées). Ce contrôle
# lit le texte de la bannière de la 1re tuile de la galerie d'accueil avec l'OCR de
# macOS (Vision) et bloque si le bandeau daté est absent.
def _norm(t):
    t = unicodedata.normalize("NFD", t.upper())
    t = "".join(c for c in t if unicodedata.category(c) != "Mn")
    return re.sub(r"[^A-Z0-9]+", " ", t).strip()


def _ocr_bin():
    src = ROOT / "tools" / "ocr-banniere.swift"
    out = ROOT / "tools" / ".bin" / "ocr-banniere"
    if out.exists() and out.stat().st_mtime >= src.stat().st_mtime:
        return out
    if not shutil.which("swiftc"):
        return None
    out.parent.mkdir(exist_ok=True)
    r = subprocess.run(["swiftc", "-O", str(src), "-o", str(out)], capture_output=True, text=True)
    return out if r.returncode == 0 else None


m = re.search(r'id="galTrack"><a class="tile" href="/blog/(analyse-hebdo[^"]+)/".*?<img src="(/img/blog/[^"]+)".*?class="tile-date">([^<]+)<', home, re.S)
if m:
    slug, src, date = m.groups()
    ocr = _ocr_bin()
    if ocr is None:
        warnings.append("OCR indisponible (swiftc absent) : bannière hebdo %s non contrôlée — la REGARDER" % src)
    else:
        r = subprocess.run([str(ocr), str(ROOT / src.lstrip("/"))], capture_output=True, text=True)
        txt = _norm(r.stdout)
        lignes = [l for l in r.stdout.splitlines() if l.strip()]
        # Critère commun à toutes les bannières hebdo publiées (vérifié du 24/10 au 21/11) :
        # la date de l'article écrite dessus, et un vrai bloc de texte (titre + cartes).
        if _norm(date) not in txt or len(lignes) < 5:
            errors.append(
                "bannière hebdo hors charte : %s — texte lu : « %s ».\n"
                "    Attendu : bandeau « ANALYSE HEBDOMADAIRE – %s », titre, cartes chiffrées\n"
                "    (modèle : la bannière de l'article précédent). Régénérer avec la consigne de\n"
                "    format en tête du prompt, et changer le nom du fichier (cache CDN d'un an)."
                % (src, (r.stdout.strip().replace("\n", " / ") or "AUCUN TEXTE")[:120], date.upper())
            )

# --- aurore WebGL des pages piliers -------------------------------------------
# Les 4 pages piliers legacy embarquent le composant GoldAurora de l'accueil en
# le referencant par son nom de fichier HASHE (/_astro/GoldAurora.<hash>.js et
# /_astro/client.<hash>.js). Un rebuild Astro change ces hashs : sans ce controle,
# l'aurore disparaitrait en silence et le hero redeviendrait un fond plat.
for page in sorted(ROOT.glob("*/index.html")):
    html = page.read_text(encoding="utf-8")
    if 'class="hero hero-webgl"' not in html:
        continue
    for attr in ("component-url", "renderer-url"):
        m = re.search(attr + r'="(/_astro/[^"]+)"', html)
        if not m:
            errors.append("%s : attribut %s absent du bloc hero-bg" % (page.parent.name, attr))
            continue
        if not (ROOT / m.group(1).lstrip("/")).exists():
            errors.append(
                "%s : l'aurore WebGL pointe sur %s, qui n'existe plus - un rebuild "
                "Astro a change le hash. Recopier le bloc hero-bg depuis index.html "
                "dans les pages .hero-webgl." % (page.parent.name, m.group(1))
            )

# --- rapport ------------------------------------------------------------------
for w in warnings:
    print("⚠  %s" % w)
for e in errors:
    print("✗  %s" % e)

if errors:
    print("\n%d problème(s) bloquant(s). Rien n'a été modifié." % len(errors))
    sys.exit(1)

print("✓ %d pages Astro, %d articles, sitemap et compteur cohérents." % (len(pages), len(on_disk)))
if warnings:
    print("  (%d avertissement(s) non bloquant(s))" % len(warnings))
sys.exit(0)
