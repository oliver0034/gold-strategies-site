#!/usr/bin/env python3
"""Génère la section « preuve hebdomadaire » de la page d'accueil depuis le journal de trades.

La section est insérée dans index.html entre deux marqueurs. Le HTML étant produit par
un build Astro dont les sources ne sont pas sur ce Mac, tout rebuild efface la section :
tools/apply-fixes.py rappelle ce script pour la réinjecter (cf. README-MAINTENANCE.md).

Usage :
    python3 tools/build-preuve-hebdo.py            # régénère depuis le journal
    python3 tools/build-preuve-hebdo.py --check    # vérifie sans écrire (code 1 si absent/périmé)

Source des données : ~/Desktop/GOLD STRATEGIES TRADING 2/journal trades/journal_master.csv
Les montants du journal sont en euros (compte libellé en EUR, positions de 0,01 lot).
"""

import argparse
import collections
import csv
import datetime
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
INDEX = ROOT / "index.html"
JOURNAL = pathlib.Path.home() / "Desktop" / "GOLD STRATEGIES TRADING 2" / "journal trades" / "journal_master.csv"

START = "<!-- PREUVE-HEBDO:START (généré par tools/build-preuve-hebdo.py — ne pas éditer à la main) -->"
END = "<!-- PREUVE-HEBDO:END -->"

CAPITAL_DEPART = 300  # euros — capital réellement engagé au démarrage du journal

# Géométrie du graphique (viewBox ; le SVG est fluide en largeur)
W, H = 860, 330
PAD_L, PAD_R, PAD_T, PAD_B = 46, 16, 22, 46


def semaines():
    """Agrège le journal par semaine calendaire (lundi), dans l'ordre chronologique."""
    if not JOURNAL.exists():
        sys.exit(f"Journal introuvable : {JOURNAL}")
    agg = collections.OrderedDict()
    for row in csv.DictReader(JOURNAL.open(encoding="utf-8")):
        jour = datetime.datetime.strptime(row["closeTimeStr"].split()[0], "%d/%m/%Y").date()
        lundi = jour - datetime.timedelta(days=jour.weekday())
        s = agg.setdefault(lundi, {"n": 0, "net": 0.0, "gagnants": 0})
        val = float(row["totalProfit"])
        s["n"] += 1
        s["net"] += val
        s["gagnants"] += val > 0
    out, cumul = [], 0.0
    for lundi, s in sorted(agg.items()):
        cumul += s["net"]
        out.append({"lundi": lundi, "net": s["net"], "cumul": cumul, "n": s["n"], "gagnants": s["gagnants"]})
    return out


def eur(v, signe=True):
    """Formate un montant à la française : +192,73 € / −6,21 €."""
    s = f"{abs(v):,.2f}".replace(",", " ").replace(".", ",")
    if not signe:
        return f"{s} €"
    return ("+" if v >= 0 else "−") + s + " €"


def graphique(sem):
    """SVG : une barre par semaine (résultat) + la courbe du cumul par-dessus."""
    n = len(sem)
    plot_w = W - PAD_L - PAD_R
    plot_h = H - PAD_T - PAD_B
    pas = plot_w / n
    barre_w = min(30, pas * 0.52)

    max_net = max(abs(s["net"]) for s in sem)
    max_cum = max(s["cumul"] for s in sem)
    zone_barres = plot_h * 0.42          # les barres occupent le bas
    # Les semaines négatives se dessinent SOUS la ligne de base : on lui réserve la place,
    # sinon une petite perte devient un trait de 2 px et la transparence ne se voit plus.
    zone_neg = 26
    base_y = H - PAD_B - zone_neg         # ligne de référence des barres

    parts = []

    # lignes de repère horizontales + échelle du cumul
    for i in range(4):
        y = PAD_T + (plot_h * i / 3)
        val = max_cum * (1 - i / 3)
        parts.append(f'<line class="ph-grid" x1="{PAD_L}" y1="{y:.1f}" x2="{W - PAD_R}" y2="{y:.1f}"/>')
        parts.append(f'<text class="ph-ytick" x="{PAD_L - 8}" y="{y + 4:.1f}">{val:,.0f}'.replace(",", " ") + "</text>")

    # ligne de base (zéro des barres)
    parts.append(f'<line class="ph-zero" x1="{PAD_L}" y1="{base_y}" x2="{W - PAD_R}" y2="{base_y}"/>')

    # barres hebdomadaires — positives vers le haut, négatives vers le bas
    for i, s in enumerate(sem):
        cx = PAD_L + pas * (i + 0.5)
        negative = s["net"] < 0
        if negative:
            h = max(9.0, abs(s["net"]) / max_net * zone_barres)
            y = base_y
        else:
            h = max(2.0, s["net"] / max_net * zone_barres)
            y = base_y - h
        cls = "ph-bar" + (" ph-bar-neg" if negative else "")
        titre = f'Semaine du {s["lundi"].strftime("%d/%m")} · {eur(s["net"])} · {s["n"]} trades'
        parts.append(
            f'<rect class="{cls}" x="{cx - barre_w / 2:.1f}" y="{y:.1f}" width="{barre_w:.1f}" '
            f'height="{h:.1f}" rx="3"><title>{titre}</title></rect>'
        )
        # étiquette de date, une sur deux masquée en petit écran
        cls_lbl = "ph-xtick" + ("" if i % 2 == 0 else " ph-xtick-alt")
        parts.append(
            f'<text class="{cls_lbl}" x="{cx:.1f}" y="{H - PAD_B + 16:.1f}">{s["lundi"].strftime("%d/%m")}</text>'
        )
        # la semaine perdante est nommée : c'est elle qui rend le reste crédible
        if negative:
            parts.append(
                f'<text class="ph-neg-lbl" x="{cx:.1f}" y="{base_y + h + 13:.1f}">{eur(s["net"])}</text>'
            )

    # courbe du cumul
    pts = []
    for i, s in enumerate(sem):
        cx = PAD_L + pas * (i + 0.5)
        cy = base_y - (s["cumul"] / max_cum) * plot_h
        pts.append((cx, cy))
    d = "M " + " L ".join(f"{x:.1f} {y:.1f}" for x, y in pts)
    aire = d + f" L {pts[-1][0]:.1f} {base_y} L {pts[0][0]:.1f} {base_y} Z"
    parts.append(f'<path class="ph-area" d="{aire}"/>')
    parts.append(f'<path class="ph-line" d="{d}"/>')
    for i, (x, y) in enumerate(pts):
        s = sem[i]
        parts.append(
            f'<circle class="ph-dot" cx="{x:.1f}" cy="{y:.1f}" r="3.4">'
            f'<title>Cumul au {s["lundi"].strftime("%d/%m")} : {eur(s["cumul"])}</title></circle>'
        )

    corps = "\n        ".join(parts)
    return (
        f'<svg class="ph-chart" viewBox="0 0 {W} {H}" role="img" '
        f'aria-label="Résultat de chaque semaine et cumul depuis le 20 mai 2026">\n        {corps}\n      </svg>'
    )


def section(sem):
    total = sem[-1]["cumul"]
    n_sem = len(sem)
    n_pos = sum(1 for s in sem if s["net"] > 0)
    n_neg = n_sem - n_pos
    n_trades = sum(s["n"] for s in sem)
    debut = sem[0]["lundi"].strftime("%d/%m/%Y")
    fin = (sem[-1]["lundi"] + datetime.timedelta(days=4)).strftime("%d/%m/%Y")
    capital_fin = CAPITAL_DEPART + total
    mot_neg = "une seule semaine négative" if n_neg == 1 else f"{n_neg} semaines négatives"

    return f"""{START}
  <section class="sec" id="preuve">
    <div class="wrap">
      <div class="sec-head rv">
        <span class="eyebrow">La preuve, semaine après semaine</span>
        <h2 class="h2">Pas un coup d'éclat. <span class="sh">{n_sem} semaines</span> bout à bout.</h2>
        <p class="lede">Un complément de revenu ne se construit pas en une fois. Voici le résultat de
        chaque semaine depuis l'ouverture du journal, {mot_neg} comprise — parce qu'un relevé sans
        aucune perte n'est pas un relevé, c'est une publicité.</p>
      </div>

      <div class="ph-card rv">
        {graphique(sem)}
        <p class="ph-legend"><i class="ph-k-bar"></i> résultat de la semaine &nbsp;·&nbsp;
        <i class="ph-k-line"></i> cumul depuis le départ</p>
      </div>

      <div class="stat rv">
        <div><b class="count" data-to="{n_sem}">0</b><span>semaines documentées</span></div>
        <div><b class="count" data-to="{n_pos}">0</b><span>semaines positives</span></div>
        <div><b class="count" data-to="{int(round(total))}" data-suffix="&nbsp;€">0</b><span>cumulés, pertes déduites</span></div>
        <div><b class="count" data-to="{n_trades}">0</b><span>trades consignés</span></div>
      </div>

      <p class="ph-note rv">Journal réel du {debut} au {fin}, alimenté automatiquement, pertes comprises ·
      capital engagé au départ : {CAPITAL_DEPART}&nbsp;€, positions de 0,01 lot · encours au {fin} :
      {eur(capital_fin, signe=False)}. Résultats passés, sur une période courte : ils ne préjugent
      en rien des résultats futurs et ne constituent ni une promesse ni un conseil en investissement.</p>

      <div class="cta-row rv">
        <a href="/resultats/" class="btn btn-primary magnetic">Voir le journal complet <span class="arw">→</span></a>
        <a href="/methode/" class="btn btn-ghost magnetic">Comprendre la méthode</a>
      </div>
    </div>
  </section>
  {END}"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="vérifie sans écrire")
    args = ap.parse_args()

    sem = semaines()
    bloc = section(sem)
    html = INDEX.read_text(encoding="utf-8")

    if args.check:
        if START not in html:
            print("✗ section preuve absente de index.html (rebuild Astro ?) — lancer sans --check")
            return 1
        deb, fin = html.index(START), html.index(END) + len(END)
        if html[deb:fin].strip() != bloc.strip():
            print("✗ section preuve périmée — lancer sans --check")
            return 1
        print(f"✓ section preuve à jour ({len(sem)} semaines, {eur(sem[-1]['cumul'])})")
        return 0

    if START in html:
        deb, fin = html.index(START), html.index(END) + len(END)
        html = html[:deb] + bloc + html[fin:]
        action = "mise à jour"
    else:
        # insertion juste après la section « Le constat »
        ancre = '</section><section class="sec" id="autonomie">'
        if ancre not in html:
            sys.exit("Ancre d'insertion introuvable — le build Astro a changé, vérifier index.html")
        html = html.replace(ancre, "</section>" + bloc + '<section class="sec" id="autonomie">', 1)
        action = "insérée"

    INDEX.write_text(html, encoding="utf-8")
    print(f"✓ section preuve {action} : {len(sem)} semaines, cumul {eur(sem[-1]['cumul'])}, "
          f"{sum(1 for s in sem if s['net'] > 0)}/{len(sem)} positives")
    return 0


if __name__ == "__main__":
    sys.exit(main())
