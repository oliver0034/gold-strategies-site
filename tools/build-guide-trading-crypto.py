#!/usr/bin/env python3
"""Contenu long de la page /trading-crypto/, injecté dans le build Astro.

Page 17 du backlog SEO (plan-editorial-seo.md), produite le 10/11/2026.

La page est produite par un build Astro dont les sources ne sont pas sur ce Mac :
tout rebuild écrase ce qu'on écrit à la main dedans. Le contenu vit donc ICI, et
tools/apply-fixes.py rappelle ce script pour le réinjecter — même mécanisme que
/trading-de-lor/ (build-guide-trading-or.py) et /capital-finance-prop-firm/.

Deux blocs sont injectés :
  - la signature (auteur, inscription AMF, date) juste sous le hero ;
  - le guide lui-même, juste avant la FAQ du build.

Rôle éditorial : page de CONVERSION du silo crypto. Elle traite le choix du support
(comptant, CFD, perpétuels), le cadre français depuis MiCA, la taille de position et
les erreurs. Elle ne refait PAS :
  - la lecture du graphique → /analyse-technique-crypto/ (page 16)
  - le capital financé crypto → /prop-firm-crypto/ (page 9)
Les deux SERP sont disjointes (0 URL commune sur 10, cluster-plan.json).

Volumes vérifiés le 10/11/2026 (marché FR) :
    Haloscan : trading crypto 100 en SEO, 390 en Ads, CPC 11,07 €, concurrence 0,49
    Google Ads (DataForSEO) : trading crypto / crypto trading / trader crypto 320,
    CPC 9,46 € ; formation trading crypto 30 ; comment trader la crypto 20

Usage :
    python3 tools/build-guide-trading-crypto.py            # injecte ou met à jour
    python3 tools/build-guide-trading-crypto.py --check    # code 1 si absent ou périmé
"""

import argparse
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
PAGE = ROOT / "trading-crypto" / "index.html"

BY_START = "<!-- GUIDE-CRYPTO-SIGNATURE:START (généré par tools/build-guide-trading-crypto.py — ne pas éditer à la main) -->"
BY_END = "<!-- GUIDE-CRYPTO-SIGNATURE:END -->"
START = "<!-- GUIDE-CRYPTO:START (généré par tools/build-guide-trading-crypto.py — ne pas éditer à la main) -->"
END = "<!-- GUIDE-CRYPTO:END -->"

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
    'Publié le <time datetime="2026-11-11">11 novembre 2026</time></p>'
    '<img class="rv" src="/img/pages/trading-crypto-1.jpg?v=20261111" '
    'alt="Balance de précision en laiton qui équilibre une pile de pièces d\'or et une seule pièce '
    'gravée, devant un écran de cours très agité" width="1600" height="840" '
    'style="display:block;width:100%;height:auto;border-radius:8px;margin-top:1.2rem">'
    "</div></section>"
    + BY_END
)

# --- 1. L'essentiel -------------------------------------------------------------

ESSENTIEL = section(
    "L'essentiel", "Le trading crypto en", "cinq phrases.",
    "Ce que je dirais à quelqu'un qui me demande par où commencer, avant d'entrer dans le détail.",
    callout(
        "À retenir",
        "Trader la crypto, c'est spéculer sur la variation du prix du Bitcoin ou d'une autre "
        "cryptomonnaie, à la hausse comme à la baisse, sur une durée de quelques heures à quelques "
        "semaines. On le fait sur trois supports — l'achat au comptant, le CFD, le contrat perpétuel — "
        "qui n'ont ni les mêmes coûts, ni le même levier, ni la même fiscalité. Depuis le 1er juillet "
        "2026, seuls les prestataires agréés au titre du règlement européen MiCA peuvent vous servir "
        "en France. Le Bitcoin bouge trois à cinq fois plus que l'or : la taille de position doit être "
        "réduite d'autant, et c'est là que se perdent la plupart des comptes. Enfin, une grande partie "
        "de ce qu'on appelle « trading crypto » sur les réseaux est en réalité de l'investissement, "
        "ou du pari à fort levier — ni l'un ni l'autre n'est ce que je décris ici."
    )
    + prose(
        "<p>J'ai passé près de 27 ans inscrit à l'AMF comme conseiller financier, puis j'ai fait de "
        "l'or ma spécialité de trader. Le Bitcoin n'est pas mon marché principal, mais je le lis chaque "
        "semaine, dans chacune de mes analyses publiques, avec la même grille que l'or et les indices. "
        "Ce guide dit ce que j'ai appris en appliquant cette grille à un marché qui, sur plusieurs "
        "points matériels, ne ressemble à aucun autre. Il ne contient ni recommandation d'achat, ni "
        "plateforme « conseillée », ni lien d'affiliation.</p>"
    ),
)

# --- 2. Les trois supports ------------------------------------------------------

SUPPORTS = section(
    "Le support", "Comptant, CFD, perpétuel :", "trois métiers.",
    "La première décision n'est pas « quelle crypto », mais « sur quoi ». Le même mouvement du "
    "Bitcoin produit trois résultats différents selon le support choisi.",
    prose(
        "<p>Quand quelqu'un me dit qu'il « trade le Bitcoin », je lui demande toujours où. La réponse "
        "change tout : la possibilité de vendre à découvert, le levier, le coût de détention d'une "
        "position, le risque que la plateforme fasse défaut et la manière de déclarer les gains. "
        "Voici les trois supports, comparés sur ce qui compte réellement.</p>",
        table(
            ["", "Achat au comptant", "CFD sur crypto", "Contrat perpétuel"],
            [
                ["<strong>Vous possédez la crypto ?</strong>", "Oui", "Non, vous détenez un contrat",
                 "Non, vous détenez un contrat"],
                ["<strong>Jouer la baisse</strong>", "Impossible (sauf à vendre ce qu'on a)",
                 "Oui", "Oui"],
                ["<strong>Levier</strong>", "Aucun",
                 "Plafonné à 2 pour 1 pour un particulier européen",
                 "Souvent proposé jusqu'à 50 ou 100 — le piège principal"],
                ["<strong>Coût de détention</strong>", "Aucun", "Financement facturé chaque nuit",
                 "Taux de financement prélevé ou versé à intervalles réguliers"],
                ["<strong>Risque principal</strong>", "Défaillance ou piratage de la plateforme",
                 "Coût de portage sur la durée", "Liquidation automatique de la position"],
                ["<strong>Horaires</strong>", "En continu", "Selon le courtier, souvent réduits le week-end",
                 "En continu"],
            ],
        ),
    )
    + cards([
        ("Comptant",
         "Acheter, attendre, revendre",
         "Vous achetez du Bitcoin sur une plateforme d'échange et vous le revendez plus tard. C'est le "
         "support le plus simple et le seul sans risque de liquidation : si le prix baisse de 30 %, "
         "vous perdez 30 %, pas davantage. En contrepartie, vous ne pouvez gagner qu'à la hausse, et "
         "vous portez un risque que les deux autres supports n'ont pas sous cette forme : celui de la "
         "plateforme elle-même, tant que les fonds y restent."),
        ("CFD",
         "Le Bitcoin comme l'or chez un courtier",
         "Le contrat pour différence réplique la variation du prix sans que vous déteniez la "
         "cryptomonnaie. C'est le support que connaissent tous ceux qui tradent déjà l'or ou les "
         "indices : même plateforme, mêmes ordres, achat comme vente. Le levier est plafonné à 2 pour "
         "1 pour un client particulier en Europe, ce qui est une protection, pas une contrainte. Le "
         "coût de financement nocturne rend ce support peu adapté aux positions tenues des semaines."),
        ("Perpétuel",
         "Le contrat à terme sans échéance",
         "C'est l'instrument dominant sur les grandes plateformes d'échange : un contrat sans date "
         "d'expiration, maintenu proche du prix au comptant par un taux de financement échangé entre "
         "acheteurs et vendeurs. Son défaut n'est pas le contrat, c'est le levier proposé. À 20 pour "
         "1, un mouvement contraire d'environ 5 % suffit à liquider la position — et le Bitcoin fait "
         "5 % dans la journée plusieurs fois par mois."),
    ])
    + prose(
        "<p>Ma position est simple. Pour quelqu'un qui débute, le comptant pour comprendre le marché "
        "avec de petites sommes, ou le CFD pour appliquer une méthode de trading avec un levier "
        "plafonné. Le perpétuel à fort levier ne devrait être touché qu'avec une règle de taille de "
        "position déjà éprouvée ailleurs — et dans ce cas, le levier élevé ne sert plus à rien, puisque "
        "la taille se calcule à partir du stop.</p>"
    ),
)

# --- 3. Le cadre français -------------------------------------------------------

CADRE = section(
    "Le cadre", "Ce que MiCA a changé", "en France.",
    "Depuis le 1er juillet 2026, la question « cette plateforme est-elle autorisée ? » a une réponse "
    "nette. C'est la première vérification à faire, avant même de comparer les frais.",
    prose(
        "<p>Pendant des années, les plateformes d'échange de cryptomonnaies opéraient en France sous "
        "le statut de prestataire de services sur actifs numériques, un simple enregistrement auprès "
        "de l'AMF. Le règlement européen MiCA a remplacé ce régime par un véritable agrément, celui de "
        "<strong>prestataire de services sur crypto-actifs</strong>. La France avait accordé une "
        "période de transition aux acteurs déjà enregistrés ; elle s'est achevée le 1er juillet 2026. "
        "Depuis, une plateforme qui n'a pas obtenu l'agrément, en France ou dans un autre pays de "
        "l'Union avec passeport, n'a plus le droit de démarcher ni de servir des clients français.</p>",
        "<p>Concrètement, trois réflexes :</p>",
        "<ul>"
        "<li><strong>Vérifier le statut sur les registres de l'AMF</strong> avant d'ouvrir un compte, "
        "et consulter ses listes noires, mises à jour en continu. Une plateforme absente des registres "
        "et très présente en publicité est un signal d'alerte, pas une bonne affaire.</li>"
        "<li><strong>Pour un CFD, vérifier l'agrément du courtier</strong> comme pour n'importe quel "
        "CFD : le levier plafonné à 2 pour 1 sur les cryptomonnaies et la protection contre le solde "
        "négatif sont des obligations pour un client particulier. Un courtier qui propose davantage à "
        "un résident français vous fait sortir de ce cadre.</li>"
        "<li><strong>Ne pas laisser dormir sur une plateforme</strong> plus que ce dont le trading a "
        "besoin. L'agrément encadre la conservation des actifs ; il ne rend pas un piratage "
        "impossible.</li>"
        "</ul>",
        "<p>Ce dernier point n'est pas théorique. Dans mon "
        + a("/blog/analyse-hebdo-or-3876-marche-baissier-31-octobre-2026/", "analyse du 31 octobre 2026")
        + ", j'ai dû commenter le piratage d'une grande plateforme d'échange, qui a fait trembler tout le "
        "marché et coûté au Bitcoin son support de 80 500 $ en quelques jours. Ceux qui avaient leurs "
        "fonds sur la plateforme visée ont découvert qu'un risque de contrepartie peut s'ajouter au "
        "risque de marché le même jour. Sur l'or en CFD, ce risque existe aussi, mais sous une forme "
        "beaucoup plus encadrée.</p>",
    ),
)

FISCALITE = section(
    "Fiscalité", "Ce qu'il faut déclarer,", "selon le support.",
    "La fiscalité dépend du support, pas de l'actif. Deux personnes qui tradent le même Bitcoin "
    "peuvent relever de deux régimes différents.",
    prose(
        "<p>Je ne fais pas de conseil fiscal personnalisé, et chaque situation mérite d'être vérifiée "
        "auprès d'un professionnel. Mais trois principes généraux évitent les erreurs les plus "
        "fréquentes, celles que je vois revenir chez les traders qui découvrent la déclaration de "
        "leur première année.</p>",
        table(
            ["Situation", "Principe général", "Point de vigilance"],
            [
                ["<strong>Achat au comptant, revente contre des euros</strong>",
                 "Plus-value imposée au prélèvement forfaitaire unique, 31,4 % depuis 2026 (12,8 % "
                 "d'impôt et 18,6 % de prélèvements sociaux), avec option possible pour le barème",
                 "Un échange d'une crypto contre une autre n'est pas imposable ; c'est le retour vers "
                 "la monnaie classique ou l'achat d'un bien qui déclenche l'impôt"],
                ["<strong>CFD sur crypto</strong>",
                 "Régime des gains sur instruments financiers, et non celui des actifs numériques",
                 "Le courtier fournit en général un récapitulatif annuel ; il reste à le reporter "
                 "correctement"],
                ["<strong>Compte ouvert sur une plateforme étrangère</strong>",
                 "Déclaration du compte obligatoire chaque année, même sans gain et même sans opération",
                 "L'oubli est sanctionné par une amende par compte non déclaré, indépendante du "
                 "résultat"],
            ],
        ),
        "<p>Le cas des gains obtenus via une société de capital financé, payés parfois en "
        "cryptomonnaie stable, est encore différent : je l'ai détaillé sur la page "
        + a("/prop-firm-crypto/", "prop firm crypto")
        + ". Retenez surtout qu'un trader actif sur le comptant multiplie les cessions, et que chaque "
        "retour vers les euros doit pouvoir être reconstitué. Tenir un journal de ses opérations dès "
        "le premier jour coûte dix minutes par semaine ; reconstituer une année en avril coûte des "
        "week-ends.</p>",
    ),
)

# --- 4. Horaires ----------------------------------------------------------------

HORAIRES = section(
    "Le rythme", "Un marché ouvert en continu,", "pas actif en continu.",
    "Le Bitcoin cote le dimanche à 4 heures du matin. Cela ne veut pas dire qu'il faut le trader "
    "à cette heure-là.",
    prose(
        "<p>C'est la différence la plus visible avec l'or : pas de fermeture le vendredi soir, pas de "
        "réouverture le dimanche, pas de jour férié. Le marché ne s'arrête jamais, ce qui a trois "
        "conséquences pratiques que les débutants découvrent souvent à leurs dépens.</p>",
        "<p><strong>La clôture est une convention.</strong> Une bougie journalière se termine à "
        "minuit en temps universel sur la plupart des plateformes, soit 1 heure du matin à Paris en "
        "hiver et 2 heures en été. Une clôture hebdomadaire se lit le dimanche soir. Tant que vous "
        "comparez des graphiques qui n'utilisent pas la même convention, vous comparez des bougies "
        "différentes.</p>",
        "<p><strong>Le week-end est un marché à part.</strong> Les volumes y baissent nettement, les "
        "institutionnels sont absents et le prix peut être déplacé par des montants modestes. Un stop "
        "placé trop près se fait toucher par une mèche le samedi, puis le prix revient à son niveau "
        "le lundi. Je considère qu'une position tenue le week-end doit avoir un stop plus large et donc "
        "une taille plus petite — ou ne pas exister.</p>",
        "<p><strong>Les heures actives restent celles des marchés classiques.</strong> Le Bitcoin "
        "réagit aux publications américaines, à l'ouverture de Wall Street et aux mouvements du "
        "Nasdaq. L'après-midi européen, de 14 h 30 à 18 h, concentre l'essentiel des mouvements "
        "exploitables, comme sur l'or. La nuit asiatique produit surtout du bruit.</p>",
        "<p>Le détail de la lecture du graphique — mèche contre clôture, prix fragmenté entre "
        "plateformes, indicateurs et leurs pièges — fait l'objet d'un guide séparé : "
        + a("/analyse-technique-crypto/", "l'analyse technique crypto, pas à pas")
        + ". Et la manière de croiser les unités de temps est traitée dans "
        + a("/analyse-multi-timeframe/", "l'analyse multi-timeframe")
        + ".</p>",
    ),
)

# --- 5. La taille de position ---------------------------------------------------


def liquidation_table():
    rows = [
        ["2 pour 1", "environ 50 %", "Rare, mais déjà vu sur le Bitcoin en quelques mois"],
        ["5 pour 1", "environ 20 %", "Plusieurs fois par an"],
        ["10 pour 1", "environ 10 %", "Plusieurs fois par trimestre, parfois en une journée"],
        ["20 pour 1", "environ 5 %", "Plusieurs fois par mois"],
        ["50 pour 1", "environ 2 %", "Dans la journée, parfois en une heure"],
    ]
    return table(["Levier utilisé", "Baisse qui liquide la position*", "Fréquence d'un tel mouvement sur le Bitcoin"], rows)


TAILLE = section(
    "Le risque", "La volatilité change", "la taille, pas la règle.",
    "C'est la section la plus importante de ce guide. Les comptes crypto ne meurent pas d'une "
    "mauvaise analyse, ils meurent d'une position trop grosse pour la volatilité du marché.",
    prose(
        "<p>Ma règle ne change pas d'un marché à l'autre : je décide d'abord combien j'accepte de "
        "perdre si mon scénario est invalidé, je mesure ensuite la distance jusqu'au niveau "
        "d'invalidation, et la taille en découle. Ce qui change avec le Bitcoin, c'est la distance. "
        "Un stop raisonnable sur l'or se mesure en dizaines de dollars ; sur le Bitcoin, en "
        "milliers.</p>",
        "<p>Prenons un compte de 10 000 $ et un risque fixé à 1 %, soit 100 $ par position.</p>",
        table(
            ["", "Or (XAUUSD) vers 4 000 $", "Bitcoin vers 76 000 $"],
            [
                ["<strong>Distance du stop</strong>", "15 $ (environ 0,4 %)", "1 500 $ (environ 2 %)"],
                ["<strong>Taille pour risquer 100 $</strong>", "6,7 onces, soit 0,067 lot",
                 "0,067 Bitcoin"],
                ["<strong>Valeur de la position</strong>", "environ 26 700 $", "environ 5 100 $"],
                ["<strong>Marge en CFD (levier 20 pour l'or, 2 pour la crypto)</strong>",
                 "environ 1 340 $", "environ 2 550 $"],
            ],
        ),
        "<p>Le tableau montre deux choses. D'abord, à risque égal, la position Bitcoin vaut cinq fois "
        "moins que la position or : c'est la volatilité qui le commande. Ensuite, le levier de 2 pour 1 "
        "imposé aux particuliers sur les CFD crypto ne gêne en rien une gestion correcte — la marge "
        "requise reste autour d'un quart du compte. Ceux qui trouvent ce levier « trop faible » sont "
        "exactement ceux qui comptent s'en servir pour grossir la position, c'est-à-dire ceux qu'il "
        "protège.</p>",
        "<h3>Le levier et la liquidation</h3>",
        "<p>Sur un contrat perpétuel, le levier n'est pas plafonné de la même manière, et la plateforme "
        "ferme d'office la position dès que la marge ne couvre plus la perte. Le calcul est brutal : "
        "plus le levier est élevé, plus le mouvement contraire qui vous liquide est petit.</p>",
        liquidation_table(),
        '<p style="font-size:.88rem;opacity:.75">* Ordre de grandeur pour une position ouverte avec '
        "toute la marge au levier indiqué, avant frais et marge de maintenance, qui avancent encore le "
        "seuil. Les fréquences décrivent le comportement du Bitcoin ces dernières années, pas une "
        "prévision.</p>",
        "<p>La liquidation est pire qu'un stop : elle intervient au plus mauvais moment, souvent au "
        "creux d'une mèche, et elle alimente elle-même la mèche, puisque des milliers de positions "
        "fermées d'office deviennent autant d'ordres de vente. C'est ce mécanisme qui produit les "
        "chutes de 8 % en une heure suivies d'un retour au prix de départ. Celui qui avait un stop "
        "calculé et une petite taille regarde la mèche ; celui qui était à 50 pour 1 en fait "
        "partie.</p>",
    ),
)

# --- 6. Ce qui fait bouger le Bitcoin, sur le terrain ---------------------------

TERRAIN = section(
    "Sur le terrain", "Trois semaines de Bitcoin,", "lues en direct.",
    "Les principes ne valent que s'ils résistent au marché réel. Voici comment ils se sont appliqués "
    "dans mes analyses publiques de l'automne 2026, publiées avant les faits et toujours en ligne.",
    cards([
        ("24 octobre",
         "Un pivot testé trois semaines de suite",
         "Le Bitcoin se traitait autour de 80 800 $ et touchait pour la troisième semaine consécutive "
         "son pivot de 80 500 $. Ma lecture tenait en une phrase : la dynamique compte davantage que "
         "le niveau exact, tant que le prix reste dans son canal haussier. C'est une règle de "
         "volatilité : sur un actif qui fait 2 % de mèche dans la journée, un niveau est une zone, "
         "pas une ligne. " + a("/blog/analyse-hebdo-or-3997-credit-ia-petrole-24-octobre-2026/",
                               "Relire l'analyse du 24 octobre") + "."),
        ("31 octobre",
         "Le risque de plateforme devient un risque de marché",
         "Le piratage d'une grande plateforme d'échange fait céder le pivot de 80 500 $ ; le "
         "Bitcoin finit la semaine vers 77 960 $. Je ne change pas de scénario pour autant : c'est une "
         "sortie franche et durable du canal qui me ferait changer d'avis, pas une clôture sous un "
         "niveau. Ce que la semaine rappelle surtout, c'est la section sur le cadre plus haut. "
         + a("/blog/analyse-hebdo-or-3876-marche-baissier-31-octobre-2026/",
             "Relire l'analyse du 31 octobre") + "."),
        ("7 novembre",
         "Le Bitcoin suspendu au Nasdaq",
         "Wall Street perd près de 2 900 milliards de dollars en une séance. Le Bitcoin résiste "
         "mieux qu'on pouvait le craindre, mais termine vers 75 850 $, au bas de son canal. J'écris "
         "que le facteur décisif sera le Nasdaq : si l'indice technologique continue de corriger, le "
         "Bitcoin basculera probablement avec lui. " +
         a("/blog/analyse-hebdo-or-4070-krach-ia-midterms-7-novembre-2026/",
           "Relire l'analyse du 7 novembre") + "."),
    ])
    + prose(
        "<p>Ces trois semaines résument ce qui fait bouger le Bitcoin. <strong>La liquidité et "
        "l'appétit pour le risque</strong> d'abord : il se comporte aujourd'hui comme un actif "
        "technologique à fort bêta, et il est rare qu'il monte durablement quand le Nasdaq baisse. "
        "<strong>Les événements propres à l'écosystème</strong> ensuite — piratage, décision "
        "réglementaire, flux des fonds cotés — qui peuvent le décrocher quelques jours du reste des "
        "marchés. <strong>La structure technique</strong> enfin, qui sert à fixer les niveaux "
        "d'invalidation et donc la taille. Les altcoins, elles, suivent le Bitcoin en amplifiant ses "
        "mouvements : dans la baisse du 7 novembre, les cryptomonnaies les plus volatiles ont "
        "davantage reculé.</p>",
        "<p>Je ne cache pas les semaines où ma lecture a été prise en défaut : toutes les analyses "
        "restent " + a("/blog/", "en ligne et datées") + ", et le " + a("/resultats/", "journal de trades")
        + " est publié, pertes comprises.</p>",
    ),
)

# --- 7. Les styles ----------------------------------------------------------------

STYLES = section(
    "Les formats", "Trader, investir, parier :", "ne pas confondre.",
    "Le mot « trading crypto » recouvre trois activités qui n'ont rien à voir. Savoir laquelle on "
    "pratique évite la moitié des erreurs.",
    cards([
        ("Swing",
         "Quelques jours à quelques semaines",
         "Lire le graphique journalier et hebdomadaire, entrer sur une zone préparée, tenir la position "
         "pendant que le mouvement se développe. C'est le format que je recommande à quelqu'un qui "
         "travaille : peu de décisions, prises au calme, et un stop assez large pour survivre aux "
         "mèches du week-end. Il impose une petite taille, puisque le stop est large."),
        ("Intrajournalier",
         "Une position ouverte et soldée dans la séance",
         "Travailler l'après-midi européen, quand le marché américain est ouvert, et ne rien garder "
         "la nuit. Le format évite le coût de portage et le risque du week-end, mais il exige d'être "
         "disponible au bon moment. Le scalping de quelques minutes, lui, se heurte aux frais et au "
         "bruit, encore plus que sur l'or."),
        ("Investissement",
         "Acheter régulièrement et conserver",
         "Acheter une somme fixe chaque mois et ne pas vendre, c'est de l'investissement, pas du "
         "trading. Cette démarche a sa logique, mais elle ne relève pas de la méthode décrite ici et je "
         "ne la commente pas. Le seul conseil que je me permets : ne pas la mélanger avec un compte de "
         "trading, sinon les pertes de l'un finissent toujours par être « compensées » par l'autre."),
    ])
    + prose(
        "<p>La quatrième activité, celle qu'on voit le plus sur les réseaux sociaux, est le pari à fort "
        "levier sur une petite cryptomonnaie à la mode. Ce n'est pas un format de trading : c'est un "
        "billet de loterie dont le prix inclut des frais de financement. Je n'ai rien à en dire, "
        "sinon que les captures d'écran de gains spectaculaires ne montrent jamais les comptes "
        "liquidés qui les accompagnent.</p>"
    ),
)

# --- 8. Les erreurs ---------------------------------------------------------------

ERREURS = section(
    "Pièges", "Sept erreurs", "que je vois revenir.",
    "Aucune ne tient à l'analyse. Toutes tiennent au cadre — et toutes se corrigent avant la "
    "première position.",
    prose(
        "<p><strong>1. Choisir le levier avant la taille.</strong> La plateforme propose 50, on prend "
        "50. La taille se calcule à partir du stop et du risque accepté ; le levier n'est qu'un "
        "plafond, et il ne devrait jamais être atteint.</p>",
        "<p><strong>2. Reprendre ses réflexes de l'or.</strong> Un stop de 0,4 % sur le Bitcoin est "
        "un stop qui sera touché par le bruit. Il faut élargir le stop et réduire la taille dans la "
        "même proportion.</p>",
        "<p><strong>3. Trader le week-end par désœuvrement.</strong> Le marché est ouvert, on a du "
        "temps, on ouvre une position. Volumes faibles, mèches gratuites, et des décisions prises "
        "sans contexte.</p>",
        "<p><strong>4. Fuir vers les petites cryptomonnaies.</strong> Plus elles sont petites, plus "
        "elles sont manipulables, plus l'écart entre achat et vente est large et plus elles chutent "
        "fort quand le Bitcoin recule. Un débutant n'a aucune raison de quitter le Bitcoin et "
        "l'Ether.</p>",
        "<p><strong>5. Choisir une plateforme pour son bonus.</strong> La seule question qui compte "
        "en premier est l'agrément ; les frais viennent après, et les bonus jamais.</p>",
        "<p><strong>6. Copier des signaux.</strong> Un signal sans le raisonnement qui l'a produit ne "
        "vous apprend rien et ne vous dit pas quoi faire quand le prix se retourne. C'est pour cette "
        "raison que mes analyses expliquent la lecture et les conditions qui la feraient changer, au "
        "lieu de donner des ordres.</p>",
        "<p><strong>7. Oublier la déclaration.</strong> Comptes étrangers non déclarés, cessions non "
        "reconstituées : l'erreur coûte souvent plus que les pertes de trading de la première "
        "année.</p>",
    ),
)

# --- 9. Aller plus loin -----------------------------------------------------------

SUITE = section(
    "Et maintenant", "Apprendre une méthode avant", "de choisir un marché.",
    "Le Bitcoin n'est pas un marché pour apprendre, c'est un marché pour appliquer. Voici l'ordre "
    "que je conseille.",
    prose(
        "<p>Ce qui fait progresser n'est pas le choix de l'actif mais la méthode : un cadre de lecture, "
        "une règle de taille, un journal. Elle s'apprend plus facilement sur un marché régulier comme "
        "l'or, puis se transpose au Bitcoin en adaptant la taille à sa volatilité. C'est exactement ce "
        "que déroule la " + a("/formation/", "formation Gold Strategies") + " : la méthode sur l'or, de "
        "zéro, avec les règles de transposition aux autres marchés.</p>",
        "<p>Si votre frein est le capital, le " + a("/capital-finance-prop-firm/", "capital financé")
        + " permet de trader sans exposer ses économies, à condition de respecter des règles de perte "
        "strictes — et les sociétés qui acceptent la crypto les durcissent encore, comme je "
        "l'explique sur la page " + a("/prop-firm-crypto/", "prop firm crypto") + ". Pour lire le "
        "graphique lui-même, le guide " + a("/analyse-technique-crypto/", "analyse technique crypto")
        + " prend le relais. Et si vous partez de zéro sur les marchés en général, commencez par "
        + a("/trading-pour-debutant/", "le trading pour débutant") + ".</p>",
        '<p style="font-size:.88rem;opacity:.75;margin-top:1.4rem">Contenu pédagogique et '
        "informatif, rédigé à titre général. Il ne constitue ni un conseil en investissement "
        "personnalisé, ni une recommandation d'acheter ou de vendre une cryptomonnaie ou un produit "
        "financier, ni un conseil fiscal. Les cryptomonnaies et les CFD présentent un risque élevé de "
        "perte en capital ; la majorité des particuliers qui tradent des CFD perdent de l'argent. "
        "Gold Strategies n'est pas un prestataire agréé et ne perçoit aucune rémunération des "
        "plateformes citées ou non citées.</p>",
    ),
)

BLOCK = START + ESSENTIEL + SUPPORTS + CADRE + FISCALITE + HORAIRES + TAILLE + TERRAIN + STYLES + ERREURS + SUITE + END


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
            print("✓ contenu de /trading-crypto/ à jour")
            return 0
        print("✗ contenu de /trading-crypto/ absent ou périmé "
              "→ python3 tools/build-guide-trading-crypto.py")
        return 1

    if up_to_date:
        print("✓ rien à faire, /trading-crypto/ est à jour")
        return 0

    out = build(src)
    if out is None:
        return 1
    PAGE.write_text(out, encoding="utf-8")
    print("✓ contenu injecté dans /trading-crypto/ (%d caractères)" % (len(SIGNATURE) + len(BLOCK)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
