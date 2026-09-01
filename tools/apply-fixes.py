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
import subprocess
import sys

# Cache-busting des deux correctifs. Ces valeurs doivent être celles réellement
# en ligne : le script REMPLACE le `?v=` existant, donc une constante en retard
# rétrograde silencieusement la version et fait resservir une feuille en cache.
# Les deux fichiers évoluant séparément, ils ont leur propre version.
CSS_VERSION = "20260826"    # assets/site-fixes.css — bumpé le 26/08/2026 (pont de survol du menu)
JS_VERSION = "20260826"     # assets/nav-mobile.js — bumpé le 26/08/2026 (groupes du menu)
SITEJS_VERSION = "20260818"  # assets/site-fixes.js — bumpé le 18/08/2026 (tracé de #preuve)
CSS_TAG = '<link rel="stylesheet" href="/assets/site-fixes.css?v=%s">' % CSS_VERSION
JS_TAG = '<script src="/assets/nav-mobile.js?v=%s" defer></script>' % JS_VERSION
SITEJS_TAG = '<script src="/assets/site-fixes.js?v=%s" defer></script>' % SITEJS_VERSION

CSS_RE = re.compile(r'<link[^>]+assets/site-fixes\.css[^>]*>')
JS_RE = re.compile(r'<script[^>]+assets/nav-mobile\.js[^>]*></script>')
# site-fixes.js était référencé dans le build sans être géré ici : un rebuild le faisait
# donc sauter en silence (spotlight des cartes Solutions, tracé de la section #preuve).
SITEJS_RE = re.compile(r'<script[^>]+assets/site-fixes\.js[^>]*></script>')

# --- retouches de texte sur les pages Astro ----------------------------------
# Un rebuild réécrit aussi le CONTENU des pages, pas seulement les balises de
# ressources : toute correction SEO faite à la main ici disparaît en silence.
# Chaque entrée est un couple (texte du build, texte voulu). L'application est
# idempotente : on ne remplace que si l'ancien texte est là et le nouveau absent.
#
# formation/index.html — plan éditorial du 03/08/2026, page 10 du backlog :
# la page est à 100 % une formation sur l'or et ni « or » ni « XAUUSD »
# n'apparaissait dans son title, son H1 ou sa meta. Voir plan-editorial-seo.md.
# --- graphe d'entité (JSON-LD) — ajouté le 26/08/2026 -------------------------
# Gold Strategies n'est PAS une entreprise locale : pas d'accueil de public, pas de
# déplacement chez le client, donc pas de fiche Google Business Profile possible
# (analyse `seo-local` du 24/08/2026, LOCAL-SEO-ANALYSIS-gold-strategies.com.md).
# Le levier d'entité passe donc entièrement par le JSON-LD et les mentions de marque.
# NE JAMAIS transformer ces blocs en LocalBusiness : ce serait déclarer un
# établissement qui n'existe pas.
#
# Le graphe repose sur trois @id stables, référencés depuis les 84 articles du blog :
#   https://gold-strategies.com/#organization        — Gold Strategies (accueil)
#   https://gold-strategies.com/a-propos/#oliver-sev — l'auteur (page à propos)
#   https://gold-strategies.com/#fiducia-conseils    — l'éditeur légal (EURL)
ORG_OLD = ('{"@context":"https://schema.org","@type":"Organization","name":"Gold Strategies",'
           '"url":"https://gold-strategies.com/","description":"Éducation financière et '
           "accompagnement pour développer son pouvoir d'achat et construire un complément de "
           'revenu de façon prudente et progressive.","logo":"https://gold-strategies.com/img/'
           'logo-gold-strategies.png","sameAs":["https://t.me/objectifsetstrategie",'
           '"https://www.tiktok.com/@gold.strategies"]}')
ORG_NEW = ('{"@context":"https://schema.org","@type":"Organization",'
           '"@id":"https://gold-strategies.com/#organization","name":"Gold Strategies",'
           '"url":"https://gold-strategies.com/","description":"Éducation financière et '
           "accompagnement pour développer son pouvoir d'achat et construire un complément de "
           'revenu de façon prudente et progressive.","logo":{"@type":"ImageObject",'
           '"url":"https://gold-strategies.com/img/logo-gold-strategies.png"},'
           '"founder":{"@id":"https://gold-strategies.com/a-propos/#oliver-sev"},'
           '"parentOrganization":{"@type":"Organization",'
           '"@id":"https://gold-strategies.com/#fiducia-conseils","name":"Fiducia Conseils",'
           '"legalName":"Fiducia Conseils","identifier":[{"@type":"PropertyValue",'
           '"propertyID":"SIREN","value":"529090565"}],"address":{"@type":"PostalAddress",'
           '"streetAddress":"8 rue du Huit Mai 1945, Jardin de l\'Esplanade",'
           '"postalCode":"34530","addressLocality":"Montagnac","addressCountry":"FR"}},'
           '"email":"goldstrategiesvip@gmail.com","contactPoint":{"@type":"ContactPoint",'
           '"contactType":"customer support","email":"goldstrategiesvip@gmail.com",'
           '"availableLanguage":["fr"]},"publishingPrinciples":'
           '"https://gold-strategies.com/politique-conflits-interets/",'
           '"knowsAbout":["Trading de l\'or","XAUUSD","Analyse technique des marchés",'
           '"Éducation financière","Gestion du risque","Complément de revenu"],'
           '"knowsLanguage":"fr","sameAs":["https://t.me/objectifsetstrategie",'
           '"https://www.tiktok.com/@gold.strategies"]}')

SITE_OLD = ('{"@context":"https://schema.org","@type":"WebSite","name":"Gold Strategies",'
            '"url":"https://gold-strategies.com/","inLanguage":"fr"}')
SITE_NEW = ('{"@context":"https://schema.org","@type":"WebSite",'
            '"@id":"https://gold-strategies.com/#website","name":"Gold Strategies",'
            '"url":"https://gold-strategies.com/","inLanguage":"fr",'
            '"publisher":{"@id":"https://gold-strategies.com/#organization"}}')

PERSON_OLD = ('{"@context":"https://schema.org","@type":"Person","name":"Oliver Sev",'
              '"jobTitle":"Fondateur de Gold Strategies","worksFor":{"@type":"Organization",'
              '"name":"Gold Strategies","url":"https://gold-strategies.com/"},'
              '"url":"https://gold-strategies.com/a-propos/",'
              '"description":"Ancien conseiller financier, fondateur de Gold Strategies."}')
PERSON_NEW = ('{"@context":"https://schema.org","@type":"Person",'
              '"@id":"https://gold-strategies.com/a-propos/#oliver-sev","name":"Oliver Sev",'
              '"jobTitle":"Fondateur de Gold Strategies",'
              '"worksFor":{"@id":"https://gold-strategies.com/#organization"},'
              '"url":"https://gold-strategies.com/a-propos/",'
              '"mainEntityOfPage":"https://gold-strategies.com/a-propos/",'
              '"description":"Ancien conseiller financier, inscrit à l\'AMF pendant près de '
              '27 ans. Fondateur de Gold Strategies.",'
              '"knowsAbout":["Trading de l\'or","XAUUSD","Analyse technique des marchés",'
              '"Éducation financière","Gestion du risque"],"knowsLanguage":"fr"}')

TEXT_PATCHES = {
    "capital-finance-prop-firm/index.html": [
        ("Prop firm : devenir trader financé | Gold Strategies",
         "Prop firm : comment \u00e7a marche vraiment | Gold Strategies"),
        ("Le capital financé (prop firm) expliqué : accéder à un capital de trading sans "
         "immobiliser vos économies. À condition d'avoir d'abord la méthode.",
         "Modèle économique, CFD ou futures, perte maximale suiveuse, cadre AMF et fiscal "
         "français : le capital financé expliqué sans lien d'affiliation."),
    ],
    # trading-de-lor — ce H3 faisait doublon avec la section « Quand l'or se trade vraiment »
    # de build-guide-trading-or.py, qui traite le sujet en détail (tableau des créneaux,
    # écart de cotation du dimanche). On retire donc celui du build.
    "trading-de-lor/index.html": [
        # Title (56 car.) et meta (152 car.) recentrés sur l'intention réelle : un débutant
        # qui cherche par où commencer, pas une plaquette de méthode.
        ("Trading de l&#39;or (XAUUSD) : le guide | Gold Strategies",
         "Trading de l&#39;or (XAUUSD) : par o\u00f9 commencer | Gold Strategies"),
        ("Comprendre et trader l'or (XAUUSD) avec méthode et gestion du risque. Une approche "
         "pédagogique, transversale et prudente — pas des signaux à copier.",
         "Support, taille de position, horaires, coûts : les bases du trading de l'or (XAUUSD) "
         "pour débuter, par un ancien conseiller inscrit à l'AMF."),
        ("<h3>Quand et comment se trade l'or</h3><p>Le marché de l'or fonctionne quasiment en "
         "continu du dimanche soir au vendredi soir, porté par le relais des places financières "
         "mondiales (Sydney, Tokyo, Londres, New York). Contrairement à une action ou un indice, "
         "il n'y a pas de véritable « cloche de clôture » quotidienne — la liquidité varie selon "
         "les sessions, avec des pics d'activité au croisement des séances européenne et "
         "américaine. Comprendre ces horaires fait partie de la méthode : trader hors des heures "
         "actives expose à des écarts de prix plus larges et moins prévisibles.</p>",
         ""),
    ],
    "index.html": [
        (ORG_OLD, ORG_NEW),
        (SITE_OLD, SITE_NEW),
    ],
    "a-propos/index.html": [
        (PERSON_OLD, PERSON_NEW),
    ],
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

# --- menu déroulant « Services » -------------------------------------------
# Le build Astro sert un menu figé (ni Guide XAUUSD, ni Cours du XAUUSD, aucun
# groupe) : un rebuild reviendrait donc en arrière en silence, comme pour les
# retouches de texte ci-dessus. On régénère le contenu du panneau à partir de
# la liste ci-dessous, seule source de vérité. Les intitulés .dd-group sont
# stylés par assets/site-fixes.css. Harmonisé le 26/08/2026 sur les 105 pages.
DROPDOWN = [
    ("group", None, "L'or"),
    ("link", "/trading-de-lor/", "Trading de l'or"),
    ("link", "/xauusd/", "Guide XAUUSD"),
    ("link", "/xauusd-cours/", "Cours du XAUUSD"),
    ("link", "/comment-trader-lor/", "Comment trader l'or"),
    ("link", "/investir-dans-lor/", "Investir dans l'or"),
    ("group", None, "Autres marchés"),
    ("link", "/trading-crypto/", "Trading crypto"),
    ("link", "/trading-indices/", "Trading indices"),
    ("group", None, "Se former"),
    ("link", "/methode/", "La méthode"),
    ("link", "/formation/", "Formation"),
    ("link", "/capital-finance-prop-firm/", "Prop firm / Capital financé"),
    ("link", "/analyses/", "Analyses"),
    ("link", "/communaute/", "Communauté"),
]
DROPDOWN_RE = re.compile(r'(<div class="dd-panel">)(.*?)(</div>)', re.S)


def dropdown_html(path):
    """Panneau attendu pour cette page. L'apostrophe suit l'échappement du build."""
    rel = path.relative_to(ROOT).as_posix()
    current = "/" if rel == "index.html" else "/" + rel[: -len("index.html")]
    out = []
    for kind, href, label in DROPDOWN:
        label = label.replace("'", "&#39;")
        if kind == "group":
            out.append('<span class="dd-group">%s</span>' % label)
        else:
            cur = ' aria-current="page"' if href == current else ""
            out.append('<a href="%s"%s>%s</a>' % (href, cur, label))
    return "".join(out)


def fix_dropdown(text, path):
    m = DROPDOWN_RE.search(text)
    if not m:
        return text
    wanted = dropdown_html(path)
    if m.group(2) == wanted:
        return text
    return text[: m.start(2)] + wanted + text[m.end(2):]


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
    """Retouches encore à appliquer : l'ancien texte est là, le nouveau non.

    Cas particulier de la SUPPRESSION (`new` vide) : la chaîne vide est toujours
    « déjà présente », donc le test habituel ne déclencherait jamais. Seule la
    présence de l'ancien texte compte alors.
    """
    src = src if src is not None else path.read_text(encoding="utf-8")
    return [(old, new) for old, new in text_patches(path)
            if old in src and (not new or new not in src)]


def apply(path):
    """Retourne True si le fichier a été modifié."""
    src = path.read_text(encoding="utf-8")
    out = src

    for old, new in missing_text_patches(path, out):
        out = out.replace(old, new)

    out = fix_dropdown(out, path)

    if CSS_RE.search(out):
        out = CSS_RE.sub(CSS_TAG, out, count=1)   # remet la bonne version si elle a dérivé
    elif "</head>" in out:
        out = out.replace("</head>", CSS_TAG + "</head>", 1)

    if JS_RE.search(out):
        out = JS_RE.sub(JS_TAG, out, count=1)
    elif "</body>" in out:
        out = out.replace("</body>", JS_TAG + "</body>", 1)

    if SITEJS_RE.search(out):
        out = SITEJS_RE.sub(SITEJS_TAG, out, count=1)
    elif "</body>" in out:
        out = out.replace("</body>", SITEJS_TAG + "</body>", 1)

    if out != src:
        path.write_text(out, encoding="utf-8")
        return True
    return False


def remove(path):
    src = path.read_text(encoding="utf-8")
    out = SITEJS_RE.sub("", JS_RE.sub("", CSS_RE.sub("", src)))
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
        if subprocess.run([sys.executable, str(ROOT / "tools" / "build-preuve-hebdo.py"), "--check"]).returncode:
            missing.append((pathlib.Path("index.html"), "section #preuve (build-preuve-hebdo.py)"))
        if subprocess.run([sys.executable, str(ROOT / "tools" / "build-guide-trading-or.py"), "--check"]).returncode:
            missing.append((pathlib.Path("trading-de-lor/index.html"), "contenu long (build-guide-trading-or.py)"))
        if subprocess.run([sys.executable, str(ROOT / "tools" / "build-guide-prop-firm.py"), "--check"]).returncode:
            missing.append((pathlib.Path("capital-finance-prop-firm/index.html"), "contenu long (build-guide-prop-firm.py)"))
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

    # La section « preuve hebdomadaire » de l'accueil est du contenu ajouté par-dessus le
    # build : un rebuild l'efface. On la régénère depuis le journal de trades.
    subprocess.run([sys.executable, str(ROOT / "tools" / "build-preuve-hebdo.py")])
    subprocess.run([sys.executable, str(ROOT / "tools" / "build-guide-trading-or.py")])
    subprocess.run([sys.executable, str(ROOT / "tools" / "build-guide-prop-firm.py")])

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
