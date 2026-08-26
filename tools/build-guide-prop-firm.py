#!/usr/bin/env python3
"""Contenu long de la page /capital-finance-prop-firm/, injecté dans le build Astro.

Même mécanisme que build-guide-trading-or.py et build-preuve-hebdo.py : la page est
produite par un build Astro dont les sources ne sont pas sur ce Mac, donc le contenu
vit ici et tools/apply-fixes.py le réinjecte (cf. README-MAINTENANCE.md).

Arbitrage tranché par Olivier le 26/08/2026 : on nomme des sociétés tierces —
FTMO, Topstep, Taurus Arena. Le plan éditorial supposait que Google ne récompensait
ici que des comparatifs d'affiliation ; la SERP relevée le 22/08/2026 dit autre chose,
la position 1 est un guide FISCAL et comptable. L'angle de la page est donc le cadre
réglementaire et fiscal français — ce que les sites d'affiliation ne traitent pas, et
ce que 27 ans d'inscription AMF légitiment.

Règles de véracité appliquées :
  - aucun tarif chiffré (ça périme en quelques mois et c'est invérifiable dans la durée) ;
  - seulement des différences STRUCTURELLES (marché couvert, type de perte maximale,
    nombre de phases), relevées le 26/08/2026 et datées comme telles dans la page ;
  - aucun lien d'affiliation, aucun classement « meilleur » ;
  - la fiscalité est décrite dans son principe, jamais chiffrée, et renvoie à un
    expert-comptable — Fiducia Conseils n'est plus agréée AMF.

Volumes Haloscan (FR, vérifiés le 26/08/2026) :
    prop firm (2 100, CPC 3,18 €) · ftmo challenge (6 100) · prop firm futures (210)
    prop firm crypto (140, CPC 13,08 €) · prop firm forex (127) · ftmo fiscalité (90)

Usage :
    python3 tools/build-guide-prop-firm.py            # injecte ou met à jour
    python3 tools/build-guide-prop-firm.py --check    # code 1 si absent ou périmé
"""

import argparse
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
PAGE = ROOT / "capital-finance-prop-firm" / "index.html"

START = "<!-- GUIDE-PROPFIRM:START (généré par tools/build-guide-prop-firm.py — ne pas éditer à la main) -->"
END = "<!-- GUIDE-PROPFIRM:END -->"
ANCHOR = '<section class="sec" id="faq">'

L = "color:var(--gold)"
RELEVE = "août 2026"


def section(eyebrow, title_plain, title_shine, lede, body):
    return (
        '<section class="sec"><div class="wrap">'
        '<div class="sec-head rv"><span class="eyebrow">%s</span>'
        '<h2 class="h2">%s <span class="sh">%s</span></h2>'
        '<p class="lede">%s</p></div>%s</div></section>'
        % (eyebrow, title_plain, title_shine, lede, body)
    )


def cards(items):
    out = ['<div class="cards rv">']
    for i, (tag, title, text) in enumerate(items, start=1):
        out.append('<article class="card"><span class="card-idx">%02d / %s</span>'
                   '<h3>%s</h3><p>%s</p></article>' % (i, tag, title, text))
    out.append("</div>")
    return "".join(out)


def prose(*p):
    return '<div class="prose rv">%s</div>' % "".join(p)


def table(headers, rows):
    th = "".join(
        '<th style="text-align:left;padding:.75rem .9rem;border-bottom:1px solid var(--line);'
        'color:var(--gold)">%s</th>' % h for h in headers)
    tr = "".join(
        "<tr>" + "".join(
            '<td style="padding:.75rem .9rem;border-bottom:1px solid var(--line)">%s</td>' % c
            for c in row) + "</tr>"
        for row in rows)
    return ('<div class="tbl-wrap" style="overflow-x:auto;margin:1.6rem 0">'
            '<table style="width:100%%;border-collapse:collapse;min-width:38rem">'
            "<thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (th, tr))


# --- 1. Le modèle économique -------------------------------------------------

MODELE = section(
    "Le modèle", "Comment une prop firm", "gagne de l'argent.",
    "Elle vend des évaluations. C'est le point de départ de toute lecture honnête du sujet — "
    "et celui que les pages de comparaison rémunérées passent le plus vite.",
    prose(
        "<p>Une société de trading pour compte propre — <em>proprietary trading firm</em>, "
        "abrégée en prop firm — met un capital à disposition de traders qu'elle ne connaît pas, "
        "en échange d'une part des gains. Le trader ne dépose pas ce capital : il paie un droit "
        "d'entrée pour passer une <strong>évaluation</strong>, et il n'accède au compte financé "
        "qu'après l'avoir réussie.</p>",
        "<p>D'où vient l'argent de la société ? De deux sources, et leur proportion change tout. "
        "La première, ce sont <strong>les frais d'évaluation payés par ceux qui échouent</strong> "
        "— l'immense majorité. La seconde, c'est sa part des gains des traders financés. Une "
        "maison qui vit surtout de la première n'a aucun intérêt à ce que vous réussissiez ; une "
        "maison qui vit de la seconde en a un, direct.</p>",
        "<p>Ce n'est pas une raison de fuir le modèle. C'est une raison de le regarder pour ce "
        "qu'il est : <strong>vous achetez un examen, pas un capital</strong>. Et comme tout "
        "examen payant, il est conçu avec un taux de réussite qui fait tenir l'économie de "
        "celui qui le vend.</p>",
    ),
)

# --- 2. CFD ou futures -------------------------------------------------------

MARCHES = section(
    "La vraie ligne de partage", "CFD ou contrats à terme :", "deux mondes.",
    "C'est la première question à trancher, avant même le choix d'une société. Elle détermine "
    "sur quel instrument vous traderez l'or, avec quelle taille minimale, et sous quelle "
    "réglementation.",
    prose(
        "<p>On range sous le même mot deux métiers différents. Les prop firms <strong>CFD</strong> "
        "donnent accès au XAUUSD, aux paires de devises et aux indices via des contrats de "
        "différence. Les prop firms <strong>futures</strong> donnent accès aux contrats à terme "
        "négociés sur les marchés organisés américains — pour l'or, le contrat GC de 100 onces "
        "ou son format réduit MGC de 10 onces.</p>",
        "<p>Pour un lecteur de ce site, la conséquence est directe : <strong>sur une prop firm "
        "futures, vous ne tradez pas le XAUUSD</strong>. Vous tradez un contrat à terme sur l'or, "
        "qui a ses propres horaires, ses échéances à faire rouler et une taille minimale bien "
        "moins souple que le micro-lot d'un CFD. La lecture de marché reste la même ; la "
        "mécanique du contrat, non — c'est le sujet de mon "
        '<a href="/xauusd/" style="%s">guide du XAUUSD</a>.</p>' % L,
        "<p>Voici où se situent les trois sociétés les plus souvent citées. Relevé en %s, "
        "d'après leurs conditions publiées : <strong>ces règles changent souvent, vérifiez-les "
        "à la source avant de payer quoi que ce soit</strong>. Je ne suis lié à aucune de ces "
        "sociétés et aucun lien de cette page n'est rémunéré." % RELEVE,
        table(
            ["", "FTMO", "Topstep", "Taurus Arena"],
            [
                ["<strong>Marché</strong>", "CFD — forex, indices, matières premières (dont XAUUSD), crypto",
                 "Futures CME uniquement (dont l'or GC)", "Futures"],
                ["<strong>L'or, concrètement</strong>", "XAUUSD au micro-lot", "Contrat GC ou micro MGC",
                 "Contrat à terme"],
                ["<strong>Évaluation</strong>", "Une ou deux phases selon la formule",
                 "Une phase, avec un nombre minimum de journées gagnantes",
                 "Une phase, ou accès direct sans évaluation"],
                ["<strong>Perte maximale</strong>",
                 "Fixe sur la formule en deux phases, <strong>suiveuse</strong> sur celle en une phase",
                 "<strong>Suiveuse</strong> — c'est sa caractéristique la plus structurante",
                 "Pas de limite de perte journalière par défaut"],
                ["<strong>Ancienneté</strong>", "Depuis 2015", "Ancienne maison du monde des futures",
                 "Acteur récent"],
            ],
        ),
        "<p>Un mot sur ce tableau : il ne classe rien et ne désigne aucune « meilleure » société. "
        "Le choix dépend du marché sur lequel vous savez travailler, pas d'un palmarès. Si vous "
        "avez construit votre lecture sur le XAUUSD, aller passer une évaluation sur des contrats "
        "à terme que vous n'avez jamais tradés revient à changer deux variables à la fois.</p>",
    ),
)

# --- 3. La perte maximale suiveuse -------------------------------------------

DRAWDOWN = section(
    "Le piège n°1", "La perte maximale suiveuse,", "et pourquoi elle élimine.",
    "Ce n'est pas le niveau de l'objectif de gain qui fait échouer la majorité des candidats. "
    "C'est un mécanisme de perte maximale que beaucoup découvrent une fois le compte fermé.",
    prose(
        "<p>Toutes les évaluations imposent une perte maximale. La différence tient à sa façon "
        "de bouger, et elle est décisive.</p>",
        "<p>Une <strong>perte maximale fixe</strong> se calcule une fois pour toutes sur le "
        "solde de départ. Sur un compte de 100 000 avec 10 % de perte maximale, le seuil "
        "d'élimination reste à 90 000, quoi qu'il arrive. C'est lisible.</p>",
        "<p>Une <strong>perte maximale suiveuse</strong> monte avec vos gains et ne redescend "
        "jamais. Le seuil se recale sur votre plus haut, si bien qu'après un bon début vous ne "
        "défendez plus votre capital de départ : vous défendez vos gains. Un trader qui prend "
        "6 % puis rend 5 % n'a rien perdu au tableau — mais son seuil, lui, a monté de 6 %, et "
        "il peut être éliminé alors qu'il est encore positif.</p>",
        "<p>C'est la principale cause d'échec, et elle n'a rien à voir avec la qualité de la "
        "lecture de marché. Elle a à voir avec le fait de traiter une évaluation comme un compte "
        "ordinaire. Elle impose une conduite précise : <strong>réduire la taille après une bonne "
        "série</strong>, exactement à l'inverse du réflexe naturel.</p>",
        "<p>C'est aussi la raison pour laquelle je considère qu'une évaluation ne se tente pas "
        "avant d'avoir une méthode stable et un historique à soi. Le mien est public, pertes "
        'comprises : <a href="/resultats/" style="%s">le journal de trades</a>. Sans ce '
        "préalable, payer une évaluation revient à acheter un billet de loterie un peu cher.</p>" % L,
    ),
)

# --- 4. Cadre français -------------------------------------------------------

CADRE = section(
    "France", "Ce que dit — et ne dit pas —", "la réglementation.",
    "Aucune prop firm n'est agréée par l'AMF, et ce n'est pas une anomalie. Encore faut-il "
    "comprendre ce que cette absence d'agrément vous retire concrètement.",
    prose(
        "<p>Commençons par le fait qui surprend le plus : <strong>il n'existe aujourd'hui aucune "
        "réglementation spécifique aux prop firms, ni en France ni au niveau européen</strong>. "
        "Elles ne sont pas interdites, elles ne sont pas agréées — elles se situent en dehors du "
        "périmètre, pour une raison logique : elles ne détiennent pas les fonds de leurs clients "
        "et ne gèrent pas d'épargne pour compte de tiers. Vous ne leur confiez pas d'argent à "
        "placer ; vous payez un service d'évaluation.</p>",
        "<p>Cette absence d'agrément a des conséquences que peu de pages énoncent clairement :</p>",
        "<ul>"
        "<li>Aucune <strong>garantie des dépôts</strong> ne s'applique — il n'y a pas de dépôt.</li>"
        "<li>Aucun <strong>médiateur</strong> compétent en cas de litige sur un retrait : le "
        "recours est contractuel, souvent dans un pays étranger.</li>"
        "<li>Les <strong>règles internes font loi</strong>, et la société peut les modifier. "
        "Lire les conditions générales n'est pas une précaution de juriste, c'est le contrat.</li>"
        "<li>L'AMF publie régulièrement des <strong>listes noires d'acteurs non autorisés</strong>. "
        "Y figurer est éliminatoire ; ne pas y figurer ne vaut pas approbation.</li>"
        "</ul>",
        "<p><strong>Côté fiscal</strong>, les sommes reversées par une prop firm sont un revenu "
        "imposable en France, et la question de la déclaration d'un compte détenu à l'étranger se "
        "pose selon la nature exacte du compte. Le régime applicable dépend de votre situation, "
        "de la fréquence de l'activité et de la forme juridique retenue — c'est précisément le "
        "genre de sujet où une réponse générale trouvée sur un forum coûte cher. "
        "<strong>Faites-le trancher par un expert-comptable avant votre premier retrait</strong>, "
        "pas après.</p>",
        "<p>Un mot sur ma position : j'ai été conseiller financier inscrit à l'AMF pendant "
        "27 ans, ce qui me rend attentif à ces distinctions — et Fiducia Conseils n'est plus "
        "agréée aujourd'hui. Ce que vous lisez ici est de l'information pédagogique, pas un "
        "conseil en investissement personnalisé, et encore moins un conseil fiscal.</p>",
    ),
)

# --- 5. Les erreurs ----------------------------------------------------------

ERREURS = section(
    "Passer l'évaluation", "Ce qui fait échouer", "les candidats.",
    "Quatre erreurs reviennent, et aucune n'est une erreur d'analyse de marché.",
    cards([
        ("Précipitation",
         "Tenter l'évaluation avant d'avoir une méthode",
         "L'évaluation ne fabrique pas la compétence, elle la mesure. Sans plusieurs mois de "
         "résultats documentés sur son propre compte, on paie pour découvrir qu'on n'est pas "
         "prêt. C'est l'ordre inverse du bon — et le plus coûteux."),
        ("Objectif",
         "Viser le gain plutôt que la survie",
         "L'objectif de gain est atteignable ; c'est la perte maximale qui élimine. Le bon cadre "
         "consiste à traiter l'évaluation comme un exercice de préservation du capital dont le "
         "gain est le sous-produit, jamais l'inverse."),
        ("Taille",
         "Augmenter la position après une bonne série",
         "Avec une perte maximale suiveuse, c'est exactement ce qu'il ne faut pas faire : le "
         "seuil vient de monter, donc la marge d'erreur vient de se réduire. Le réflexe naturel "
         "est ici le contraire du réflexe utile."),
        ("Lecture",
         "Ne pas lire les conditions générales",
         "Journées minimales, règle de régularité, instruments interdits, comportement autorisé "
         "autour des annonces, délai entre deux retraits : ces clauses décident du résultat "
         "autant que le marché. Elles diffèrent d'une société à l'autre et changent."),
    ])
    + prose(
        "<p>La conclusion tient en une phrase : <strong>le capital financé résout un problème de "
        "capital, jamais un problème de méthode</strong>. Si la méthode n'est pas là, le "
        "financement ne fait qu'accélérer le constat. C'est pour cette raison que je place la "
        '<a href="/formation/" style="%s">formation</a> et la '
        '<a href="/methode/" style="%s">méthode</a> avant l\'évaluation, et pas l\'inverse — et '
        'que mes <a href="/blog/" style="%s">analyses hebdomadaires</a> restent en ligne, datées, '
        "qu'elles aient eu raison ou tort.</p>" % (L, L, L),
    ),
)

BLOCK = START + MODELE + MARCHES + DRAWDOWN + CADRE + ERREURS + END


def current(text):
    if START not in text or END not in text:
        return None
    return text[text.index(START): text.index(END) + len(END)]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()

    if not PAGE.exists():
        print("✗ page introuvable :", PAGE)
        return 1

    src = PAGE.read_text(encoding="utf-8")
    have = current(src)

    if args.check:
        if have == BLOCK:
            print("✓ contenu de /capital-finance-prop-firm/ à jour")
            return 0
        print("✗ contenu de /capital-finance-prop-firm/ absent ou périmé "
              "→ python3 tools/build-guide-prop-firm.py")
        return 1

    if have == BLOCK:
        print("✓ rien à faire, /capital-finance-prop-firm/ est à jour")
        return 0

    if have is not None:
        out = src.replace(have, BLOCK)
    elif ANCHOR in src:
        out = src.replace(ANCHOR, BLOCK + ANCHOR, 1)
    else:
        print("✗ ancrage introuvable (le build a changé) :", ANCHOR)
        return 1

    PAGE.write_text(out, encoding="utf-8")
    print("✓ contenu injecté dans /capital-finance-prop-firm/ (%d caractères)" % len(BLOCK))
    return 0


if __name__ == "__main__":
    sys.exit(main())
