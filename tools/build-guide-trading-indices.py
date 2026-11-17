#!/usr/bin/env python3
"""Contenu long de la page /trading-indices/, injecté dans le build Astro.

Page 18 du backlog SEO (plan-editorial-seo.md), produite le 17/11/2026.

La page est produite par un build Astro dont les sources ne sont pas sur ce Mac :
tout rebuild écrase ce qu'on écrit à la main dedans. Le contenu vit donc ICI, et
tools/apply-fixes.py rappelle ce script pour le réinjecter — même mécanisme que
/trading-crypto/ (build-guide-trading-crypto.py) et /trading-de-lor/.

Deux blocs sont injectés :
  - la signature (auteur, inscription AMF, date) et la bannière juste sous le hero ;
  - le guide lui-même, juste avant la FAQ du build.

Rôle éditorial : page de CONVERSION du silo « autres marchés ». Elle traite ce qu'est un
indice (pondération), le choix du support (CFD, contrats à terme, ETF), les horaires vus de
Paris, la taille de position à risque égal, les coûts cachés et la méthode de lecture.

Volumes vérifiés le 17/11/2026 (marché FR) :
    Haloscan : trading indices 50 en SEO, 50 en Ads, CPC 3,11 €, concurrence 0,11
    Google Ads (DataForSEO) : trading indices / trading indice 40, CPC 2,93 €
    (10 à 20/mois de juillet à octobre 2026, pics à 90-140) ; trading nasdaq 70, CPC 6,03 € ;
    trader les indices, comment trader les indices, trading sp500, trader le cac 40 : 10 chacun.
    Le « ~170 » du plan d'origine n'est plus d'actualité.

SERP du 17/11/2026 : AI Overview (définition, CFD/ETF/futures, pondération), puis guides
pédagogiques des courtiers (« que sont les indices, comment les trader »), agrégateurs de
cotations et vidéos. Aucun site éditorial indépendant en tête.

Usage :
    python3 tools/build-guide-trading-indices.py            # injecte ou met à jour
    python3 tools/build-guide-trading-indices.py --check    # code 1 si absent ou périmé
"""

import argparse
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
PAGE = ROOT / "trading-indices" / "index.html"

BY_START = "<!-- GUIDE-INDICES-SIGNATURE:START (généré par tools/build-guide-trading-indices.py — ne pas éditer à la main) -->"
BY_END = "<!-- GUIDE-INDICES-SIGNATURE:END -->"
START = "<!-- GUIDE-INDICES:START (généré par tools/build-guide-trading-indices.py — ne pas éditer à la main) -->"
END = "<!-- GUIDE-INDICES:END -->"

# Points d'ancrage dans le build : fin du hero, et début de la FAQ.
BY_ANCHOR = "</header><section class=\"sec\">"
BY_ANCHOR_INSERT_AT = len("</header>")
ANCHOR = '<section class="sec" id="faq">'

L = "color:var(--gold)"   # les liens du corps sont stylés en ligne dans ce build

TH = 'style="text-align:left;padding:.75rem .9rem;border-bottom:1px solid var(--line);color:var(--gold)"'
TD = 'style="padding:.75rem .9rem;border-bottom:1px solid var(--line);vertical-align:top"'


def a(href, text):
    return '<a href="' + href + '" style="' + L + '">' + text + "</a>"


def section(eyebrow, title_plain, title_shine, lede, body):
    """Une section au gabarit du build : titre en deux tons, chapô, contenu."""
    return (
        '<section class="sec"><div class="wrap">'
        '<div class="sec-head rv"><span class="eyebrow">' + eyebrow + "</span>"
        '<h2 class="h2">' + title_plain + ' <span class="sh">' + title_shine + "</span></h2>"
        '<p class="lede">' + lede + "</p></div>"
        + body +
        "</div></section>"
    )


def cards(items):
    out = ['<div class="cards rv">']
    for idx, (tag, title, text) in enumerate(items, start=1):
        out.append(
            '<article class="card"><span class="card-idx">%02d / %s</span>'
            "<h3>%s</h3><p>%s</p></article>" % (idx, tag, title, text)
        )
    out.append("</div>")
    return "".join(out)


def prose(*paragraphs):
    return '<div class="prose rv">' + "".join(paragraphs) + "</div>"


def table(headers, rows, min_width="38rem"):
    head = "".join("<th " + TH + ">" + h + "</th>" for h in headers)
    body = "".join(
        "<tr>" + "".join("<td " + TD + ">" + c + "</td>" for c in r) + "</tr>" for r in rows
    )
    return (
        '<div class="tbl-wrap" style="overflow-x:auto;margin:1.6rem 0">'
        '<table style="width:100%;border-collapse:collapse;min-width:' + min_width + '">'
        "<thead><tr>" + head + "</tr></thead><tbody>" + body + "</tbody></table></div>"
    )


def callout(title, text):
    return (
        '<div class="rv" style="border:1px solid var(--line);border-left:3px solid var(--gold);'
        'border-radius:6px;padding:1.1rem 1.3rem;margin:1.6rem 0">'
        '<p style="margin:0 0 .4rem;color:var(--gold);font-weight:600">' + title + "</p>"
        '<p style="margin:0">' + text + "</p></div>"
    )


# --- 0. Signature ---------------------------------------------------------------

SIGNATURE = (
    BY_START
    + '<section class="sec" style="padding-top:1.2rem;padding-bottom:0"><div class="wrap">'
    '<p class="rv" style="font-size:.92rem;opacity:.85;margin:0">'
    'Par <a href="/a-propos/" style="color:var(--gold);text-decoration:none">Oliver Sev</a>'
    " — ancien conseiller financier inscrit à l'AMF pendant 27 ans · "
    'Publié le <time datetime="2026-11-17">17 novembre 2026</time></p>'
    '<img class="rv" src="/img/pages/trading-indices-1.jpg?v=20261117" '
    'alt="Baromètre de précision en laiton posé sur une table sombre, devant trois écrans '
    'affichant des courbes de bougies aux tendances opposées" width="1600" height="840" '
    'style="display:block;width:100%;height:auto;border-radius:8px;margin-top:1.2rem">'
    "</div></section>"
    + BY_END
)

# --- 1. L'essentiel -------------------------------------------------------------

ESSENTIEL = section(
    "L'essentiel", "Le trading d'indices en", "cinq phrases.",
    "Ce que je réponds à quelqu'un qui me demande s'il doit trader le CAC 40 ou le Nasdaq, avant "
    "d'entrer dans le détail.",
    callout(
        "À retenir",
        "Trader un indice, c'est spéculer sur la variation d'un panier d'actions — le CAC 40, le "
        "S&amp;P 500, le Nasdaq 100, le DAX — sans acheter aucune des sociétés qui le composent. "
        "On le fait le plus souvent par CFD, parfois par contrats à terme, plus rarement par ETF, "
        "et ces trois supports n'ont ni le même coût, ni le même levier, ni la même fiscalité. Un "
        "indice n'est pas une moyenne : il est pondéré, et quelques sociétés peuvent porter à elles "
        "seules la hausse de cinq cents. Le Nasdaq 100 bouge nettement plus que le CAC 40, la taille "
        "de position doit donc changer d'un indice à l'autre pour un même risque. Enfin, les "
        "meilleures heures pour trader ne sont pas les mêmes selon l'indice : vu de Paris, le "
        "S&amp;P 500 se joue surtout entre 15h30 et 18h."
    )
    + prose(
        "<p>J'ai passé près de 27 ans inscrit à l'AMF comme conseiller financier, puis j'ai fait de "
        "l'or ma spécialité de trader. Les indices ne sont pas le marché sur lequel je prends le plus "
        "de positions, mais je les lis chaque semaine, dans chacune de mes analyses publiques, parce "
        "qu'ils disent mieux que n'importe quel commentaire ce que les marchés pensent de la "
        "croissance, des taux et du risque. Ce guide rassemble ce qu'il faut savoir avant de trader "
        "un indice, et ce que la lecture hebdomadaire de quatre d'entre eux m'a appris en 2026. Il "
        "ne contient ni recommandation d'achat, ni courtier « conseillé », ni lien d'affiliation.</p>"
    ),
)

# --- 2. Ce qu'est un indice ---------------------------------------------------------

INDICE = section(
    "Le sous-jacent", "Un indice n'est pas", "une moyenne.",
    "Avant de choisir un support, il faut savoir ce que l'on trade. Les grands indices ne sont pas "
    "construits de la même façon, et cela change leur comportement.",
    prose(
        "<p>Un indice boursier mesure la valeur d'un panier d'actions selon une règle de calcul "
        "publiée. La règle la plus courante est la <strong>pondération par la capitalisation "
        "flottante</strong> : chaque société pèse dans l'indice à proportion de la valeur de ses "
        "actions réellement échangeables. Une société dix fois plus grosse qu'une autre pèse dix fois "
        "plus. C'est la règle du S&amp;P 500, du Nasdaq 100, du CAC 40 et du DAX.</p>",
        "<p>Conséquence directe, que beaucoup de débutants ignorent : un indice peut monter pendant "
        "que la majorité de ses actions baissent. Je l'ai relevé dans mon "
        + a("/blog/analyse-hebdo-or-4454-jackson-hole-29-aout-2026/", "analyse du 29 août 2026")
        + " : un jeudi de cette semaine-là, la quasi-totalité de la hausse du S&amp;P 500 avait été "
        "produite par deux sociétés sur cinq cents, et deux tiers des valeurs de l'indice avaient "
        "fini dans le rouge. Celui qui trade l'indice trade donc d'abord ses plus grosses "
        "capitalisations — aujourd'hui, essentiellement la technologie américaine.</p>",
        table(
            ["Indice", "Composition", "Calcul", "Ce qu'il faut savoir"],
            [
                ["<strong>CAC 40</strong>", "Les 40 principales valeurs de la Bourse de Paris",
                 "Capitalisation flottante, poids d'une valeur plafonné à 15 %",
                 "Très exposé au luxe, à l'industrie et à la banque ; souvent le plus lent des "
                 "grands indices"],
                ["<strong>DAX</strong>", "Les 40 principales valeurs de la Bourse de Francfort",
                 "Capitalisation flottante, <strong>dividendes réinvestis</strong>",
                 "Un indice de performance : il ne chute pas mécaniquement quand une société verse "
                 "son dividende, contrairement au CAC 40"],
                ["<strong>S&amp;P 500</strong>", "Environ 500 grandes sociétés américaines",
                 "Capitalisation flottante",
                 "La référence mondiale ; une poignée de géants de la technologie en représente une "
                 "part considérable"],
                ["<strong>Nasdaq 100</strong>",
                 "Les 100 plus grosses sociétés non financières cotées au Nasdaq",
                 "Capitalisation, avec des règles de plafonnement",
                 "Concentré sur la technologie : plus nerveux que le S&amp;P 500, dans les deux sens"],
                ["<strong>Dow Jones</strong>", "30 grandes sociétés américaines",
                 "<strong>Pondéré par le prix</strong> de l'action, pas par la taille",
                 "Une action chère pèse plus qu'une société plus grosse à l'action moins chère : "
                 "un indice historique plus qu'un baromètre fidèle"],
                ["<strong>Nikkei 225</strong>", "225 valeurs de la Bourse de Tokyo",
                 "Pondéré par le prix", "Très sensible au yen ; il cote pendant la nuit européenne"],
            ],
        ),
        "<p>Deux remarques pratiques. Le nom affiché chez votre courtier n'est pas toujours celui de "
        "l'indice : on trouve « US 500 », « US Tech 100 », « France 40 » ou « Germany 40 », parce "
        "que les noms officiels sont des marques déposées. Et le prix que vous tradez n'est pas "
        "toujours l'indice lui-même : en dehors des heures de la Bourse, les CFD suivent le plus "
        "souvent le contrat à terme, qui intègre un écart de financement et de dividendes. Un "
        "« France 40 » qui cote à 22 heures n'est pas le CAC 40, c'est une estimation de ce qu'il "
        "vaudra à l'ouverture.</p>",
    ),
)

# --- 3. Les supports ----------------------------------------------------------------

SUPPORTS = section(
    "Le support", "CFD, contrat à terme, ETF :", "trois métiers.",
    "La première décision n'est pas « quel indice », mais « sur quoi ». Le même mouvement du "
    "S&amp;P 500 produit trois résultats différents selon le support choisi.",
    prose(
        "<p>Un indice ne s'achète pas directement : c'est un calcul, pas un titre. Pour en tirer "
        "parti, on passe par un produit dérivé ou par un fonds qui le réplique. Voici les trois "
        "supports qu'un particulier français rencontre, comparés sur ce qui compte réellement.</p>",
        table(
            ["", "CFD sur indice", "Contrat à terme (micro)", "ETF indiciel"],
            [
                ["<strong>Usage naturel</strong>", "Trading de quelques heures à quelques jours",
                 "Trading, pour qui accepte un format standardisé",
                 "Investissement de long terme, pas trading"],
                ["<strong>Jouer la baisse</strong>", "Oui", "Oui",
                 "Non (sauf ETF inversés, à éviter pour débuter)"],
                ["<strong>Levier</strong>",
                 "Plafonné à 20 pour 1 sur les grands indices pour un particulier européen",
                 "Fixé par la marge exigée par la bourse, souvent plus élevé", "Aucun"],
                ["<strong>Taille minimale</strong>", "Très fine : quelques centimes par point",
                 "Fixe : 5 $ par point sur le micro S&amp;P 500, 2 $ sur le micro Nasdaq 100",
                 "Le prix d'une part"],
                ["<strong>Coût de détention</strong>",
                 "Financement facturé chaque nuit, ajustement des dividendes",
                 "Intégré au prix du contrat, échéance à renouveler chaque trimestre", "Frais annuels du fonds"],
                ["<strong>Horaires</strong>", "Souvent près de 24 h sur 24 en semaine sur les "
                 "indices américains", "Près de 23 h sur 24, du dimanche soir au vendredi soir",
                 "Horaires de la bourse de cotation"],
            ],
        ),
    )
    + cards([
        ("CFD",
         "Le support du particulier",
         "Le contrat pour différence réplique la variation de l'indice. C'est le support que "
         "connaissent tous ceux qui tradent déjà l'or : même plateforme, mêmes ordres, achat comme "
         "vente, taille ajustable au centime par point. Le levier est plafonné à 20 pour 1 sur les "
         "grands indices pour un client particulier en Europe, avec protection contre le solde "
         "négatif. Son coût caché est le financement nocturne, qui pénalise les positions tenues "
         "plusieurs semaines."),
        ("Contrat à terme",
         "Le format des professionnels, en version réduite",
         "Le contrat à terme est négocié sur une bourse organisée, avec un prix unique pour tout le "
         "monde et une échéance trimestrielle (mars, juin, septembre, décembre). Les versions micro "
         "l'ont rendu accessible, mais la taille reste fixe : avec 5 $ par point sur le micro "
         "S&amp;P 500, un stop de 40 points engage 200 $, sans possibilité de faire plus petit. Il "
         "convient à un compte déjà conséquent, pas à un premier compte."),
        ("ETF",
         "Investir, pas trader",
         "Le fonds indiciel coté réplique l'indice et s'achète comme une action, y compris dans un "
         "PEA pour certains. C'est un excellent outil d'investissement de long terme, à frais très "
         "bas. Ce n'est pas un outil de trading : pas de vente à découvert simple, des horaires "
         "limités à la bourse de cotation, et un intérêt qui tient précisément à la durée de "
         "détention."),
    ])
    + prose(
        "<p>Ma position est simple. Pour appliquer une méthode de trading sur un indice avec un "
        "petit compte, le CFD chez un courtier agréé est le seul support qui permet de calculer une "
        "taille de position exacte. Le contrat à terme vient ensuite, quand la taille fixe ne pose "
        "plus de problème. Et si votre horizon se compte en années, ce guide ne vous concerne pas : "
        "un ETF dans une enveloppe fiscale adaptée fera mieux que n'importe quel trading.</p>"
    ),
)

# --- 4. Horaires --------------------------------------------------------------------

HORAIRES = section(
    "Le rythme", "Quand trader un indice,", "vu de Paris.",
    "Un CFD sur le S&amp;P 500 cote à 3 heures du matin. Cela ne veut pas dire qu'il faut le "
    "trader à cette heure-là.",
    prose(
        "<p>Chaque indice vit au rythme de sa bourse. En dehors de la séance officielle, le prix "
        "existe toujours sur les contrats à terme et sur les CFD qui les suivent, mais avec moins de "
        "volume, un écart entre achat et vente plus large et des mouvements qui peuvent être effacés "
        "à l'ouverture. Voici les créneaux qui comptent, en heure de Paris.</p>",
        table(
            ["Créneau (heure de Paris)", "Ce qui se passe", "Ce que j'en fais"],
            [
                ["<strong>9h00 – 9h30</strong>",
                 "Ouverture d'Euronext Paris et de Francfort : le CAC 40 et le DAX rattrapent ce "
                 "qui s'est passé pendant la nuit", "J'observe, je ne prends pas de position dans "
                 "le premier quart d'heure"],
                ["<strong>9h30 – 12h00</strong>",
                 "Séance européenne pleine, liquidité correcte sur les indices européens",
                 "Le meilleur créneau pour le CAC 40 et le DAX"],
                ["<strong>14h30</strong>",
                 "Statistiques américaines majeures : emploi le premier vendredi du mois, inflation "
                 "vers le milieu du mois", "Aucune position ouverte dans les minutes qui entourent "
                 "la publication"],
                ["<strong>15h30 – 18h00</strong>",
                 "Ouverture de Wall Street et chevauchement avec la fin de séance européenne : le "
                 "plus fort volume de la journée", "Le créneau principal pour le S&amp;P 500 et "
                 "le Nasdaq 100"],
                ["<strong>17h30</strong>", "Clôture de Paris et de Francfort",
                 "Les indices européens perdent leur liquidité, les CFD suivent alors les contrats "
                 "à terme"],
                ["<strong>20h00</strong>",
                 "Décisions de la banque centrale américaine, huit fois par an",
                 "Pas de nouvelle position avant ; souvent deux mouvements opposés dans l'heure"],
                ["<strong>22h00</strong>", "Clôture de Wall Street",
                 "Les résultats des grandes sociétés tombent souvent juste après : risque d'écart "
                 "de cours le lendemain"],
            ],
        ),
        "<p>Deux pièges d'horloge. Les États-Unis et l'Europe ne changent pas d'heure le même jour : "
        "pendant deux à trois semaines en mars et une semaine fin octobre ou début novembre, Wall "
        "Street ouvre à 14h30 heure de Paris, et les statistiques tombent à 13h30. Et une "
        "<strong>saison de résultats</strong> — quatre fois par an, sur environ six semaines — "
        "change la nature d'un indice concentré : quand les cinq plus grosses sociétés du Nasdaq 100 "
        "publient la même semaine, le marché trade cinq annonces, pas une tendance.</p>",
    ),
)

# --- 5. Ce qui fait bouger un indice ----------------------------------------------

MOTEURS = section(
    "Les moteurs", "Ce qui fait bouger", "un indice.",
    "Un indice actions n'obéit pas aux mêmes forces que l'or. Les connaître évite d'acheter une "
    "cassure la veille d'une décision de taux.",
    cards([
        ("Taux", "Le coût de l'argent",
         "Une action vaut la somme de ses bénéfices futurs, actualisés. Quand les taux longs "
         "montent, ces bénéfices valent moins aujourd'hui : les indices de croissance, Nasdaq en "
         "tête, y sont les plus sensibles. Le rendement du 10 ans américain est le premier chiffre "
         "que je regarde le lundi matin."),
        ("Résultats", "Les bénéfices des grandes sociétés",
         "Dans un indice pondéré par la taille, les résultats d'une dizaine de géants pèsent plus "
         "que ceux des quatre cents autres. Une déception sur l'un d'eux peut faire reculer "
         "l'indice entier un jour où la majorité des sociétés publient de bons chiffres."),
        ("Risque", "L'appétit ou la peur",
         "Le VIX mesure ce que coûte la protection contre une baisse du S&amp;P 500 sur trente "
         "jours. Un VIX bas ne dit pas que le marché va monter, il dit que personne ne paie pour se "
         "couvrir. C'est précisément quand il est au plancher qu'un choc fait le plus de dégâts."),
        ("Devises", "Le dollar et l'euro",
         "Un euro fort pénalise les exportateurs européens et pèse sur le CAC 40 et le DAX. Un yen "
         "faible porte le Nikkei. Ces effets sont lents, mais ils expliquent souvent pourquoi "
         "l'Europe et Wall Street divergent sur plusieurs semaines."),
    ])
    + prose(
        "<p><strong>Et l'or dans tout ça ?</strong> On lit partout que l'or monte quand les actions "
        "baissent. C'est vrai parfois, et c'est exactement le genre de règle qu'il ne faut pas "
        "trader. Deux semaines de cet automne le montrent. Dans mon "
        + a("/blog/analyse-hebdo-or-4166-inflation-nasdaq-17-octobre-2026/", "analyse du 17 octobre 2026")
        + ", le Nasdaq 100 venait de perdre 5,5 % en cinq séances — et l'or avait aussi reculé, de "
        "4 195 à 4 166 $, parce que la même semaine les taux s'étaient tendus. Trois semaines plus "
        "tard, dans celle du "
        + a("/blog/analyse-hebdo-or-4070-krach-ia-midterms-7-novembre-2026/", "7 novembre 2026")
        + ", le Nasdaq 100 perdait 4,9 % et l'or reprenait près de 200 $, de 3 876 à 4 070. Même "
        "baisse des actions, réaction opposée de l'or : ce qui décide, ce sont les taux et le "
        "dollar, pas la baisse des actions en elle-même.</p>"
    ),
)

# --- 6. Taille de position -----------------------------------------------------------

TAILLE = section(
    "Le risque", "Même risque,", "tailles différentes.",
    "C'est la section la plus importante de ce guide. Passer de l'or au Nasdaq sans changer sa "
    "taille de position, c'est changer de risque sans le savoir.",
    prose(
        "<p>La règle ne change pas d'un marché à l'autre : on fixe d'abord la somme qu'on accepte de "
        "perdre si le scénario échoue, on place le stop là où le scénario est invalidé, et la "
        "taille découle des deux. Ce qui change d'un indice à l'autre, c'est la distance du stop, "
        "parce que les indices n'ont pas la même amplitude. Le Nasdaq 100 fait couramment des "
        "journées à plus de 1 %, le CAC 40 beaucoup moins souvent.</p>",
        "<p>Exemple pour un compte de 10 000 € qui risque 1 % par position, soit 100 €. Les distances "
        "de stop sont des ordres de grandeur pour une position tenue dans la journée, à adapter au "
        "graphique et non à recopier.</p>",
        table(
            ["Marché", "Niveau indicatif", "Stop", "Taille pour 100 € de risque",
             "Exposition totale", "Marge à 20 pour 1"],
            [
                ["<strong>CAC 40</strong>", "≈ 8 000 points", "40 points", "2,50 € par point",
                 "≈ 20 000 €", "≈ 1 000 €"],
                ["<strong>S&amp;P 500</strong>", "≈ 7 500 points", "35 points",
                 "≈ 2,85 € par point", "≈ 21 000 €", "≈ 1 070 €"],
                ["<strong>Nasdaq 100</strong>", "≈ 28 000 points", "200 points", "0,50 € par point",
                 "≈ 14 000 €", "≈ 700 €"],
                ["<strong>Or (XAUUSD)</strong>", "≈ 3 900 $", "15 $", "≈ 6,70 € par dollar",
                 "≈ 26 000 €", "≈ 1 300 €"],
            ],
            min_width="44rem",
        ),
        "<p>Ce tableau dit deux choses. D'abord, à risque égal, la position sur le Nasdaq 100 est "
        "nettement plus petite en exposition que celle sur le CAC 40 : c'est normal, chaque point "
        "y vaut moins de risque. Ensuite, la marge immobilisée n'a aucun rapport avec le risque : "
        "elle mesure ce que le courtier bloque, pas ce que vous pouvez perdre. Une position qui "
        "immobilise 700 € peut faire perdre bien plus que 700 € sans stop.</p>",
        callout(
            "Le cas qui ruine les comptes",
            "Prenez la même position de 0,50 € par point sur le Nasdaq 100, sans stop, la semaine du "
            "17 octobre 2026 : l'indice a perdu environ 1 700 points en cinq séances. La perte "
            "aurait été de 850 €, soit 8,5 fois le risque prévu — et à 2,50 € par point, la taille "
            "utilisée sur le CAC 40, elle aurait atteint 4 250 €. Ce n'est pas le levier qui ruine, "
            "c'est l'absence de stop combinée à une taille calculée pour un autre marché.",
        ),
        "<p>Le calcul détaillé, avec la conversion des devises et la gestion des positions "
        "successives, est déroulé pas à pas dans mon guide pour "
        + a("/apprendre-le-trading/", "apprendre le trading") + ". Sur un indice, une seule "
        "particularité à ajouter : vérifiez la valeur du point chez votre courtier, car certains "
        "expriment la taille en contrats de 1, 10 ou 25 unités de devise par point, et une erreur "
        "d'un facteur dix ne se voit qu'au premier stop.</p>",
    ),
)

# --- 7. Coûts cachés ----------------------------------------------------------------

COUTS = section(
    "Les coûts", "Ce que coûte une position", "qu'on garde.",
    "L'écart entre achat et vente se voit. Les trois autres coûts d'un CFD sur indice se "
    "découvrent sur le relevé.",
    prose(
        "<ul>"
        "<li><strong>Le financement nocturne.</strong> Chaque nuit, une position acheteuse sur CFD "
        "paie un intérêt calculé sur toute l'exposition, pas sur la marge : un taux monétaire de "
        "référence, plus une marge du courtier de l'ordre de 2 à 3 % par an. Sur les 20 000 € "
        "d'exposition de l'exemple du CAC 40, cela représente quelques euros par nuit. Négligeable "
        "sur une journée, sensible sur un mois, rédhibitoire sur un an. Le vendredi soir, on paie "
        "en général trois nuits d'un coup.</li>"
        "<li><strong>L'ajustement des dividendes.</strong> Quand une société de l'indice détache son "
        "dividende, l'indice baisse mécaniquement d'autant. Le courtier compense : il débite les "
        "positions acheteuses et crédite les vendeuses. Sur le CAC 40, ces détachements se "
        "concentrent au printemps. Le DAX, indice de performance, n'est pas concerné.</li>"
        "<li><strong>L'écart hors séance.</strong> L'écart entre prix d'achat et de vente d'un "
        "« France 40 » peut être plusieurs fois plus large à 23 heures qu'à 10 heures. Un stop "
        "placé trop près peut être touché par le seul élargissement de l'écart, sans que le marché "
        "ait réellement bougé.</li>"
        "<li><strong>L'échéance, sur les contrats à terme.</strong> Le contrat expire le troisième "
        "vendredi du dernier mois du trimestre. Garder sa position impose de la reporter sur "
        "l'échéance suivante, avec un écart de prix et des frais à chaque fois.</li>"
        "</ul>",
        "<p>Côté fiscalité, les gains sur CFD et contrats à terme d'un particulier relèvent en "
        "général du régime des instruments financiers : prélèvement forfaitaire unique de 31,4 % "
        "depuis 2026, avec option possible pour le barème, et déclaration du compte chaque année si "
        "le courtier est établi à l'étranger. Ce n'est pas du conseil fiscal personnalisé : chaque "
        "situation se vérifie auprès d'un professionnel.</p>",
    ),
)

# --- 8. La méthode ------------------------------------------------------------------

METHODE = section(
    "La méthode", "Comment je lis un indice,", "en cinq étapes.",
    "La même grille que sur l'or, avec trois réglages propres aux indices. C'est elle que vous "
    "retrouvez chaque samedi dans mes analyses.",
    cards([
        ("Contexte", "Les taux et le calendrier d'abord",
         "Avant le graphique, je note le rendement du 10 ans américain, la prochaine décision de "
         "banque centrale et les résultats attendus dans la semaine. Un indice à quelques jours "
         "des résultats de ses trois plus grosses sociétés n'est pas un indice en tendance, c'est "
         "un pari sur des annonces."),
        ("Cadre", "L'unité de temps longue donne le sens",
         "Le graphique hebdomadaire et journalier dit si l'indice est en tendance, en consolidation "
         "ou en train de casser un support. Je ne prends pas de position contre ce cadre, sauf à "
         "taille réduite et avec une raison écrite — la logique est détaillée dans mon guide "
         + a("/analyse-multi-timeframe/", "d'analyse multi-timeframe") + "."),
        ("Largeur", "Vérifier qui porte le mouvement",
         "Un record du S&amp;P 500 porté par deux sociétés n'a pas la même solidité qu'un record "
         "porté par la majorité de la cote. Je compare l'indice à sa version où chaque valeur pèse "
         "le même poids, et le Nasdaq aux semi-conducteurs."),
        ("Volatilité", "Le VIX règle la taille",
         "Quand le VIX double, l'amplitude des journées double à peu près aussi. Je n'élargis pas "
         "seulement mon stop : je réduis la taille d'autant, pour que le risque en euros reste le "
         "même."),
        ("Exécution", "Le bon créneau, le bon niveau",
         "J'entre pendant la séance de la bourse de l'indice, sur un niveau repéré à l'avance, avec "
         "un stop qui correspond à l'invalidation du scénario. Jamais dans le premier quart d'heure "
         "après l'ouverture, jamais juste avant une statistique majeure."),
    ]),
)

# --- 9. Le terrain ------------------------------------------------------------------

TERRAIN = section(
    "Le terrain", "Ce que les indices m'ont dit", "cet automne.",
    "Trois semaines de 2026, lues en direct dans mes analyses du samedi, avec ce qu'elles "
    "enseignent pour trader un indice.",
    prose(
        "<p><strong>Le 7 novembre : la volatilité change de régime en une séance.</strong> Dans mon "
        + a("/blog/analyse-hebdo-or-4070-krach-ia-midterms-7-novembre-2026/", "analyse du 7 novembre")
        + ", le S&amp;P 500 avait perdu 2,7 % sur la semaine et le Nasdaq 100 4,9 %, avec la pire "
        "séance du Nasdaq Composite depuis avril 2025. Le VIX était passé de 16,6 à 28,2 en une "
        "seule séance. Concrètement, un stop qui suffisait le mardi était trop court le jeudi : "
        "c'est la raison pour laquelle la taille se recalcule quand la volatilité change, au lieu "
        "de rester figée. La même semaine, le CAC 40 gagnait 2,1 %. Un trader qui croyait "
        "« jouer le marché » en vendant n'importe quel indice aurait perdu d'un côté de "
        "l'Atlantique ce qu'il gagnait de l'autre.</p>",
        "<p><strong>Le 14 novembre : un rebond n'est pas un retournement.</strong> Une semaine plus "
        "tard, dans mon "
        + a("/blog/analyse-hebdo-or-3884-fed-taux-14-novembre-2026/", "analyse du 14 novembre")
        + ", le S&amp;P 500 signait sa meilleure semaine depuis août (+2,5 %) et le DAX clôturait sur "
        "un record. Mais techniquement, le S&amp;P 500 restait sous le niveau qu'il avait cassé deux "
        "semaines plus tôt, et il montait la semaine même où le 10 ans américain repassait au-dessus "
        "de 5 %. Un indice qui monte pendant que les taux s'emballent mérite une taille réduite, pas "
        "un achat à pleine taille sur l'euphorie du vendredi.</p>",
        "<p><strong>Le 29 août : regarder sous le capot.</strong> L'"
        + a("/blog/analyse-hebdo-or-4454-jackson-hole-29-aout-2026/", "analyse du 29 août")
        + " notait déjà un S&amp;P 500 proche de ses sommets porté par une poignée de valeurs, "
        "pendant que les petites capitalisations reculaient. Ce déséquilibre n'annonçait pas une "
        "date, mais il expliquait la fragilité de l'automne : quand si peu de sociétés portent un "
        "indice, il suffit qu'elles déçoivent pour que tout recule. C'est ce qui s'est produit en "
        "octobre avec les semi-conducteurs.</p>",
        "<p>Ces analyses ne sont pas des signaux : elles décrivent une lecture et les conditions "
        "qui la feraient changer. Elles sont toutes datées et en ligne, avec leurs erreurs, sur le "
        + a("/blog/", "blog") + ".</p>",
    ),
)

# --- 10. Les erreurs ------------------------------------------------------------------

ERREURS = section(
    "Les pièges", "Six erreurs", "que je vois souvent.",
    "Elles reviennent chez presque tous ceux qui passent de l'or ou du Forex aux indices.",
    prose(
        "<p><strong>1. Garder la même taille d'un indice à l'autre.</strong> 2,50 € par point sur le "
        "CAC 40 et 2,50 € par point sur le Nasdaq 100 ne représentent pas le même risque. La taille "
        "se recalcule à chaque marché, à chaque position.</p>",
        "<p><strong>2. Trader la nuit un indice qui dort.</strong> Le « France 40 » à 23 heures n'est "
        "pas le CAC 40 : c'est un prix dérivé, peu liquide, à l'écart large. Les indices se tradent "
        "pendant la séance de leur bourse.</p>",
        "<p><strong>3. Ignorer le calendrier des résultats.</strong> Ouvrir une position sur le "
        "Nasdaq 100 la veille de la publication de ses plus grosses sociétés, c'est parier sur une "
        "annonce en croyant suivre une tendance.</p>",
        "<p><strong>4. Garder un CFD des mois.</strong> Le financement nocturne transforme un bon "
        "trade lent en mauvais placement. Un horizon de plusieurs mois appelle un ETF, pas un "
        "CFD.</p>",
        "<p><strong>5. Croire que l'or protège à coup sûr.</strong> La semaine du 17 octobre l'a "
        "rappelé : actions et or peuvent baisser ensemble quand les taux montent.</p>",
        "<p><strong>6. Confondre marge et risque.</strong> La marge, c'est ce que le courtier "
        "immobilise. Le risque, c'est la distance au stop multipliée par la taille. Seul le second "
        "compte.</p>",
    ),
)

# --- 11. Aller plus loin ----------------------------------------------------------

SUITE = section(
    "Et maintenant", "Apprendre une méthode avant", "de choisir un marché.",
    "Un indice n'est pas un marché pour apprendre, c'est un marché pour appliquer. Voici l'ordre "
    "que je conseille.",
    prose(
        "<p>Ce qui fait progresser n'est pas le choix de l'indice mais la méthode : un cadre de "
        "lecture, une règle de taille, un journal. Elle s'apprend sur un seul marché, régulier et "
        "bien documenté, puis se transpose aux autres en ajustant la taille. C'est ce que déroule la "
        + a("/formation/", "formation Gold Strategies") + " : la méthode sur l'or, de zéro, avec les "
        "règles de transposition aux indices et aux cryptomonnaies.</p>",
        "<p>Si votre frein est le capital, le "
        + a("/capital-finance-prop-firm/", "capital financé")
        + " permet de trader sans exposer ses économies : les sociétés de capital financé proposent "
        "presque toutes les grands indices, avec des règles de perte journalière que la volatilité "
        "d'un Nasdaq met à rude épreuve — raison de plus pour maîtriser la taille de position avant "
        "le challenge. Si vous partez de zéro sur les marchés, commencez par "
        + a("/trading-pour-debutant/", "le trading pour débutant") + ". Et pour l'autre grand "
        "marché secondaire du site, le guide " + a("/trading-crypto/", "trading crypto")
        + " applique la même démarche au Bitcoin.</p>",
        '<p style="font-size:.88rem;opacity:.75;margin-top:1.4rem">Contenu pédagogique et '
        "informatif, rédigé à titre général. Il ne constitue ni un conseil en investissement "
        "personnalisé, ni une recommandation d'acheter ou de vendre un indice ou un produit "
        "financier, ni un conseil fiscal. Les CFD et les contrats à terme sont des instruments "
        "complexes à effet de levier, qui présentent un risque élevé de perte en capital ; la "
        "majorité des particuliers qui tradent des CFD perdent de l'argent. Les niveaux cités sont "
        "des ordres de grandeur à la date de rédaction. Gold Strategies ne perçoit aucune "
        "rémunération des courtiers ou sociétés cités ou non cités.</p>",
    ),
)

BLOCK = (START + ESSENTIEL + INDICE + SUPPORTS + HORAIRES + MOTEURS + TAILLE + COUTS + METHODE
         + TERRAIN + ERREURS + SUITE + END)


def current(text, start, end):
    if start not in text or end not in text:
        return None
    return text[text.index(start): text.index(end) + len(end)]


def build(src):
    """Retourne la page avec les deux blocs à jour, ou None si un ancrage manque."""
    out = src
    have = current(out, BY_START, BY_END)
    if have is not None:
        out = out.replace(have, SIGNATURE)
    elif BY_ANCHOR in out:
        i = out.index(BY_ANCHOR) + BY_ANCHOR_INSERT_AT
        out = out[:i] + SIGNATURE + out[i:]
    else:
        print("✗ ancrage de la signature introuvable (le build a changé) :", BY_ANCHOR)
        return None

    have = current(out, START, END)
    if have is not None:
        out = out.replace(have, BLOCK)
    elif ANCHOR in out:
        out = out.replace(ANCHOR, BLOCK + ANCHOR, 1)
    else:
        print("✗ ancrage du guide introuvable (le build a changé) :", ANCHOR)
        return None
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()

    if not PAGE.exists():
        print("✗ page introuvable :", PAGE)
        return 1

    src = PAGE.read_text(encoding="utf-8")
    up_to_date = (current(src, BY_START, BY_END) == SIGNATURE
                  and current(src, START, END) == BLOCK)

    if args.check:
        if up_to_date:
            print("✓ contenu de /trading-indices/ à jour")
            return 0
        print("✗ contenu de /trading-indices/ absent ou périmé "
              "→ python3 tools/build-guide-trading-indices.py")
        return 1

    if up_to_date:
        print("✓ rien à faire, /trading-indices/ est à jour")
        return 0

    out = build(src)
    if out is None:
        return 1
    PAGE.write_text(out, encoding="utf-8")
    print("✓ contenu injecté dans /trading-indices/ (%d caractères)" % (len(SIGNATURE) + len(BLOCK)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
