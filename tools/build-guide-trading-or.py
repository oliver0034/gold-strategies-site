#!/usr/bin/env python3
"""Contenu long de la page /trading-de-lor/, injecté dans le build Astro.

La page est produite par un build Astro dont les sources ne sont pas sur ce Mac :
tout rebuild écrase ce qu'on écrit à la main dedans. Le contenu vit donc ICI, et
tools/apply-fixes.py rappelle ce script pour le réinjecter — même mécanisme que
la section « preuve hebdomadaire » de l'accueil (cf. README-MAINTENANCE.md).

Rôle éditorial de la page : porte d'entrée pour un débutant. Elle pose les bases
— support, unité de compte, horaires, coûts, styles — et renvoie vers les pages
spécialisées. Elle ne refait donc PAS le guide du contrat (/xauusd/), le cours en
direct (/xauusd-cours/) ni les stratégies (/comment-trader-lor/) : la duplication
ferait se cannibaliser quatre pages du même silo.

Longue traîne visée (Haloscan, marché FR, vérifiée le 26/08/2026) :
    trading de l'or (30, CPC 7,71 €) · trader l'or (50) · horaire trading xauusd (50)
    horaire trading gold (30) · cfd or (30) · pips sur l'or · trader l'or scalping

Usage :
    python3 tools/build-guide-trading-or.py            # injecte ou met à jour
    python3 tools/build-guide-trading-or.py --check    # code 1 si absent ou périmé
"""

import argparse
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
PAGE = ROOT / "trading-de-lor" / "index.html"

START = "<!-- GUIDE-OR:START (généré par tools/build-guide-trading-or.py — ne pas éditer à la main) -->"
END = "<!-- GUIDE-OR:END -->"

# Point d'ancrage : juste avant la section FAQ du build.
ANCHOR = '<section class="sec" id="faq">'

L = "color:var(--gold)"   # les liens du corps sont stylés en ligne dans ce build


def section(eyebrow, title_plain, title_shine, lede, body):
    """Une section au gabarit du build : titre en deux tons, chapô, contenu."""
    return (
        '<section class="sec"><div class="wrap">'
        '<div class="sec-head rv"><span class="eyebrow">%s</span>'
        '<h2 class="h2">%s <span class="sh">%s</span></h2>'
        '<p class="lede">%s</p></div>'
        '%s'
        '</div></section>' % (eyebrow, title_plain, title_shine, lede, body)
    )


def cards(items):
    """Grille de cartes numérotées. Chaque grille porte .rv : elle s'anime à l'entrée."""
    out = ['<div class="cards rv">']
    for idx, (tag, title, text) in enumerate(items, start=1):
        out.append(
            '<article class="card"><span class="card-idx">%02d / %s</span>'
            '<h3>%s</h3><p>%s</p></article>' % (idx, tag, title, text)
        )
    out.append("</div>")
    return "".join(out)


def prose(*paragraphs):
    return '<div class="prose rv">%s</div>' % "".join(paragraphs)


# --- 1. Les quatre décisions du départ ---------------------------------------

DEPART = section(
    "Débuter", "Trader l'or quand on part", "de zéro.",
    "Quatre décisions se prennent avant la première position. Aucune ne concerne "
    "le choix d'une stratégie — et pourtant ce sont elles qui déterminent l'essentiel du résultat.",
    prose(
        "<p>La question « comment trader l'or » arrive presque toujours trop tôt. Avant de "
        "choisir une méthode d'entrée, il faut avoir tranché quatre points matériels : sur quel "
        "<strong>support</strong> on travaille, dans quelle <strong>unité</strong> on compte, "
        "quelle <strong>taille</strong> on engage et ce que coûte chaque aller-retour. Un "
        "débutant qui règle ces quatre points survit à ses premiers mois ; un autre qui les "
        "ignore perd son capital avant d'avoir pu juger quoi que ce soit de sa stratégie.</p>"
    )
    + cards([
        ("Support",
         "CFD, contrat à terme, ETF ou or physique",
         "Le <strong>CFD sur XAUUSD</strong> est le support courant du trading actif : ticket "
         "d'entrée faible, levier plafonné à 20:1 pour un particulier européen, coût de "
         "financement si la position dort plusieurs nuits. Le contrat à terme réclame un capital "
         "bien plus élevé et impose de gérer des échéances. L'ETF et le lingot relèvent de "
         "l'investissement patrimonial, pas de la spéculation à court terme — ce sont quatre "
         "métiers différents sous un même mot."),
        ("Unité",
         "Once, lot, dollar : ce que vaut réellement un point",
         "L'or se cote à l'once troy — 31,1035 grammes. Un lot standard porte sur 100 onces : "
         "<strong>une variation d'un dollar sur le cours vaut 100 dollars de résultat</strong>, "
         "10 dollars en mini-lot, 1 dollar en micro. On parle souvent de « pips sur l'or » par "
         "habitude venue du change, mais sur le XAUUSD la plupart des courtiers cotent au "
         "centime : raisonner directement en dollars de prix évite les erreurs de facteur 10."),
        ("Taille",
         "La position se calcule à partir du stop, jamais du levier",
         "L'ordre est toujours le même : on décide d'abord combien on accepte de perdre sur "
         "cette décision, on mesure ensuite la distance jusqu'au niveau d'invalidation, et la "
         "taille en découle. Le levier autorisé par la plateforme n'entre nulle part dans ce "
         "calcul — c'est un plafond réglementaire, pas un objectif. L'or parcourant couramment "
         "40 à 60 dollars dans une journée agitée, l'erreur de dimensionnement se paie vite."),
        ("Coût",
         "Le spread, et pourquoi il n'est jamais stable",
         "L'écart entre prix d'achat et prix de vente est le péage de chaque aller-retour. Sur "
         "l'or il est structurellement plus large que sur les grandes paires de devises, et "
         "surtout il se dilate : à l'ouverture du dimanche soir, autour du report quotidien, et "
         "dans les secondes qui suivent une publication américaine. Un format de trading très "
         "court multiplie ce coût par le nombre d'allers-retours."),
    ])
    + prose(
        "<p>Le détail du contrat — taille de lot, cotation, effet de levier, rollover — est "
        'développé dans le <a href="/xauusd/" style="%s">guide complet du XAUUSD</a>. Pour '
        "vérifier un prix et comprendre pourquoi votre courtier n'affiche pas tout à fait le "
        'même que le graphique, la page <a href="/xauusd-cours/" style="%s">cours du XAUUSD '
        "en direct</a> traite la question.</p>" % (L, L)
    ),
)

# --- 2. Les horaires ----------------------------------------------------------

HORAIRES = section(
    "Horaires", "Quand l'or se trade", "vraiment.",
    "Le marché est ouvert du dimanche soir au vendredi soir, mais l'or n'est réellement "
    "exploitable que sur deux créneaux : l'ouverture de Londres et le recouvrement avec New York.",
    prose(
        "<p>C'est l'une des questions les plus posées, et l'une des plus mal traitées : "
        "« quels sont les horaires du trading de l'or ? » La réponse formelle — presque 24 heures "
        "sur 24, du dimanche soir au vendredi soir, avec une courte coupure quotidienne en fin "
        "de soirée pour le report des positions — n'apprend rien d'utile. <strong>Ouverture "
        "permanente ne veut pas dire activité permanente.</strong> Voici les créneaux réels, en "
        "heure de Paris.</p>",
        '<div class="tbl-wrap" style="overflow-x:auto;margin:1.6rem 0">'
        '<table style="width:100%;border-collapse:collapse;min-width:34rem">'
        "<thead><tr>"
        '<th style="text-align:left;padding:.75rem .9rem;border-bottom:1px solid var(--line);color:var(--gold)">Créneau</th>'
        '<th style="text-align:left;padding:.75rem .9rem;border-bottom:1px solid var(--line);color:var(--gold)">Ce qui s\'y passe</th>'
        '<th style="text-align:left;padding:.75rem .9rem;border-bottom:1px solid var(--line);color:var(--gold)">Intérêt</th>'
        "</tr></thead><tbody>"
        + "".join(
            '<tr><td style="padding:.75rem .9rem;border-bottom:1px solid var(--line)"><strong>%s</strong></td>'
            '<td style="padding:.75rem .9rem;border-bottom:1px solid var(--line)">%s</td>'
            '<td style="padding:.75rem .9rem;border-bottom:1px solid var(--line)">%s</td></tr>' % r
            for r in [
                ("1 h – 8 h<br><span style='opacity:.6'>session asiatique</span>",
                 "Volume faible, dérive lente, fourchettes étroites",
                 "Faible. Le spread coûte souvent plus que l'amplitude ne rapporte."),
                ("9 h – 12 h<br><span style='opacity:.6'>ouverture de Londres</span>",
                 "Premier afflux de volume, sortie fréquente de la fourchette de la nuit",
                 "Bon. C'est souvent là que la journée prend sa direction."),
                ("14 h 30 – 17 h 30<br><span style='opacity:.6'>Londres + New York</span>",
                 "Volume maximal, publications américaines, mouvements les plus larges",
                 "Maximal — et c'est aussi le créneau le plus dangereux."),
                ("après 20 h",
                 "Reflux progressif, spread qui s'élargit",
                 "Faible. Ce qui se dessine tard se défait souvent le lendemain."),
            ]
        )
        + "</tbody></table></div>",
        "<p>Deux moments méritent une vigilance particulière. <strong>L'ouverture du dimanche "
        "soir</strong> produit régulièrement un écart de cotation : le prix rouvre à un niveau "
        "différent de la clôture du vendredi, sans qu'aucune transaction n'ait eu lieu entre les "
        "deux — un ordre stop placé dans cet intervalle sera exécuté au premier prix disponible, "
        "pas au prix demandé. <strong>Les publications macroéconomiques</strong> — inflation "
        "américaine, décision de banque centrale, emploi — produisent le même phénomène en "
        "pleine séance, en quelques secondes.</p>",
        "<p>Pour quelqu'un qui travaille à temps plein, la conséquence est plutôt rassurante : "
        "une lecture du journalier le soir et des ordres placés à l'avance sur des zones "
        "identifiées suffisent. C'est vouloir suivre la séance américaine depuis son bureau qui "
        "ne tient pas.</p>",
    ),
)

# --- 3. Les trois formats -----------------------------------------------------

FORMATS = section(
    "Formats", "Trois façons de", "travailler l'or.",
    "Scalping, intrajournalier, swing : ce ne sont pas trois niveaux de difficulté croissante, "
    "mais trois métiers différents. Le plus court est le plus exigeant, et c'est celui que "
    "choisissent la plupart des débutants.",
    cards([
        ("Scalping",
         "Quelques minutes, beaucoup d'allers-retours",
         "Chercher de petits mouvements répétés, souvent sur l'unité 1 ou 5 minutes. Le format "
         "paraît attirant parce qu'il promet un résultat rapide. En réalité il cumule tous les "
         "handicaps : le spread est payé à chaque aller-retour, la moindre hésitation coûte, et "
         "l'attention exigée est incompatible avec une autre activité. C'est le format le plus "
         "mal choisi par les débutants — et celui qui vide le plus vite un petit compte."),
        ("Intrajournalier",
         "Une à trois décisions, position soldée le soir",
         "Travailler la séance européenne ou américaine et ne rien garder pour la nuit. Le "
         "risque de trou de cotation à l'ouverture disparaît, le coût de financement aussi. En "
         "contrepartie, il faut être disponible sur le créneau choisi — et accepter les journées "
         "où la bonne décision est de ne rien faire."),
        ("Swing",
         "Plusieurs jours, lecture du journalier",
         "Prendre position sur un mouvement de fond et le tenir. Les décisions sont peu "
         "nombreuses, prises au calme, et le format est le seul réellement compatible avec un "
         "emploi. Il faut en revanche supporter de voir la position respirer contre soi, et "
         "assumer le coût de portage. C'est le format que je privilégie sur l'or."),
    ])
    + prose(
        "<p>Le choix ne se fait pas selon le tempérament mais selon la disponibilité réelle. "
        "Un format incompatible avec votre semaine produit des décisions prises dans l'urgence, "
        "et l'urgence est le premier facteur de perte. Le détail des approches d'entrée — suivi "
        "de tendance, retour sur zone, cassure, annonce — est traité dans la page "
        '<a href="/comment-trader-lor/" style="%s">comment trader l\'or</a>.</p>' % L
    ),
)

# --- 4. Les erreurs -----------------------------------------------------------

ERREURS = section(
    "Pièges", "Ce qui fait perdre", "les débutants.",
    "Ce ne sont presque jamais des erreurs d'analyse. Ce sont cinq erreurs de cadre, "
    "et elles se répètent avec une régularité frappante.",
    prose(
        "<p><strong>Augmenter la taille pour « rattraper ».</strong> Après deux pertes, doubler "
        "la position pour revenir à l'équilibre. C'est la manière la plus rapide de transformer "
        "une mauvaise semaine en compte vide, parce qu'elle fait exactement l'inverse de ce qu'il "
        "faudrait : elle augmente le risque au moment où la lecture s'est révélée fausse.</p>",
        "<p><strong>Confondre valeur refuge et absence de risque.</strong> L'or est souvent "
        "présenté comme un abri. Il monte et il descend, parfois violemment, et à effet de levier "
        "il ruine aussi bien qu'un autre actif. Le statut de refuge décrit un comportement de "
        "long terme, pas une garantie sur votre position de la semaine.</p>",
        "<p><strong>Trader hors des heures actives.</strong> Ouvrir une position à trois heures "
        "du matin parce qu'on est disponible, c'est payer le spread pour regarder du bruit.</p>",
        "<p><strong>Empiler les indicateurs.</strong> Cinq oscillateurs ne créent pas "
        "d'information supplémentaire : ils résument tous le même prix et finissent par se "
        "contredire. Cette contradiction est vécue comme une analyse fine ; c'est du bruit.</p>",
        "<p><strong>Ne rien noter.</strong> Sans journal, aucune progression n'est mesurable et "
        "les mêmes erreurs se répètent en croyant chaque fois à un cas particulier. Je publie le "
        'mien, pertes comprises : <a href="/resultats/" style="%s">le journal de trades</a>. '
        'Et mes <a href="/blog/" style="%s">analyses hebdomadaires</a> restent en ligne, datées, '
        "qu'elles aient eu raison ou tort — c'est la même exigence.</p>" % (L, L),
        "<p>Aucun de ces cinq points ne demande de talent particulier. Ils demandent un cadre, "
        "et c'est précisément ce qui s'apprend : la "
        '<a href="/methode/" style="%s">méthode</a> décrit la lecture descendante que j\'applique, '
        'et la <a href="/formation/" style="%s">formation</a> la déroule pas à pas sur l\'or.</p>'
        % (L, L),
    ),
)

BLOCK = START + DEPART + HORAIRES + FORMATS + ERREURS + END


def build():
    return BLOCK


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
    wanted = build()
    have = current(src)

    if args.check:
        if have == wanted:
            print("✓ contenu de /trading-de-lor/ à jour")
            return 0
        print("✗ contenu de /trading-de-lor/ absent ou périmé "
              "→ python3 tools/build-guide-trading-or.py")
        return 1

    if have == wanted:
        print("✓ rien à faire, /trading-de-lor/ est à jour")
        return 0

    if have is not None:
        out = src.replace(have, wanted)
    elif ANCHOR in src:
        out = src.replace(ANCHOR, wanted + ANCHOR, 1)
    else:
        print("✗ ancrage introuvable dans la page (le build a changé) :", ANCHOR)
        return 1

    PAGE.write_text(out, encoding="utf-8")
    print("✓ contenu injecté dans /trading-de-lor/ (%d caractères)" % len(wanted))
    return 0


if __name__ == "__main__":
    sys.exit(main())
