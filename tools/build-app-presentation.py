#!/usr/bin/env python3
"""Bloc « Gold Strategies App » de la page d'accueil, juste après la preuve hebdomadaire.

Contenu ajouté par-dessus le build Astro : un rebuild l'efface. Le bloc est donc inséré entre
deux marqueurs par ce script, appelé par tools/apply-fixes.py (09/11/2026, décision d'Olivier :
une section courte sur l'accueil qui renvoie vers la page /application/).

    python3 tools/build-app-presentation.py            # (ré)insère le bloc dans index.html
    python3 tools/build-app-presentation.py --check    # code 1 s'il est absent ou modifié

Image servie : img/gold-strategies-app-640.webp (logo de l'application, essai B du 09/11/2026 ;
sources : ~/claude/gold-strategies/identite-gold-strategies-app/ sur le Mac).
Styles dans le bloc lui-même : rien à versionner dans site-fixes.css.
Chaque phrase décrit une fonction présente dans l'application (src/config/plans.js et
src/config/schedule.js du dépôt application-gold-strategies) : la relire si l'offre change.
"""
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
INDEX = ROOT / "index.html"
IMAGE = "img/gold-strategies-app-640.webp"
START = "<!-- APP-PRESENTATION:START (généré par tools/build-app-presentation.py — ne pas éditer à la main) -->"
END = "<!-- APP-PRESENTATION:END -->"
ANCRE = '<section class="sec" id="autonomie">'      # le bloc se pose juste après la preuve hebdomadaire

BLOC = START + """<section class="gs-app" id="application" aria-labelledby="gs-app-titre"><div class="gs-app__in"><a href="/application/" class="gs-app__logo" tabindex="-1" aria-hidden="true"><img src="/img/gold-strategies-app-640.webp" alt="" width="640" height="640" loading="lazy"></a><div class="gs-app__txt"><p class="gs-app__eyebrow">Nouveau · Gold Strategies App</p><h2 id="gs-app-titre">L'espace membre, sur ordinateur et sur téléphone.</h2><p>Le cadrage du jour, des outils de discipline et, au niveau Premium, les analyses de 02:15, 09:15 et 15:45 et les indicateurs Gold Strategies, réunis au même endroit. Inscription gratuite, sans carte bancaire.</p><div class="gs-app__cta"><a href="/application/" class="gs-app__btn gs-app__btn--or">Découvrir l'app</a><a href="https://app.gold-strategies.com/#/connexion" class="gs-app__btn">Se connecter</a></div></div></div><style>.gs-app{padding:64px 24px}.gs-app__in{max-width:980px;margin:0 auto;display:grid;grid-template-columns:200px 1fr;gap:40px;align-items:center;padding:32px;border:1px solid var(--line,#d4a24c2e);border-radius:18px;background:linear-gradient(135deg,#14120e,#0b0a08)}.gs-app__logo img{display:block;width:100%;height:auto;border-radius:22%;border:1px solid #3a3120;box-shadow:0 12px 36px rgba(0,0,0,.55)}.gs-app__eyebrow{margin:0 0 .5rem;color:var(--gold,#d4a24c);font:500 .72rem "IBM Plex Mono",monospace;letter-spacing:.16em;text-transform:uppercase}.gs-app h2{margin:0 0 .8rem;color:var(--gold-light,#f2dfa8);font:500 clamp(1.5rem,2.6vw,2.1rem)/1.15 "Bodoni Moda",Georgia,serif}.gs-app__txt>p:not(.gs-app__eyebrow){margin:0 0 1.4rem;color:var(--paper,#ede8df);opacity:.85;font:300 1rem/1.6 "IBM Plex Sans",sans-serif;max-width:56ch}.gs-app__cta{display:flex;flex-wrap:wrap;gap:12px}.gs-app__btn{display:inline-flex;align-items:center;padding:12px 20px;border-radius:10px;border:1px solid #d4a24c80;color:var(--paper,#ede8df);text-decoration:none;font:500 .92rem "IBM Plex Sans",sans-serif}.gs-app__btn:hover,.gs-app__btn:focus-visible{border-color:var(--gold-light,#f2dfa8)}.gs-app__btn--or{background:linear-gradient(180deg,#f2dfa8,#d4a24c);border-color:transparent;color:#0b0a08}@media(max-width:720px){.gs-app{padding:44px 16px}.gs-app__in{grid-template-columns:1fr;justify-items:center;text-align:center;gap:24px;padding:26px 20px}.gs-app__logo{width:160px}.gs-app__cta{justify-content:center}}</style></section>""" + END


def main():
    check = "--check" in sys.argv
    html = INDEX.read_text(encoding="utf-8")
    if not (ROOT / IMAGE).exists():
        print("✗ image manquante :", IMAGE); return 1
    if START in html:
        deb, fin = html.index(START), html.index(END) + len(END)
        if html[deb:fin] == BLOC:
            if not check: print("✓ bloc Gold Strategies App déjà en place.")
            return 0
        if check:
            print("✗ bloc Gold Strategies App modifié ou périmé — lancer sans --check"); return 1
        html = html[:deb] + BLOC + html[fin:]
    else:
        if check:
            print("✗ bloc Gold Strategies App absent de index.html (rebuild Astro ?) — lancer sans --check"); return 1
        if html.count(ANCRE) != 1:
            sys.exit("Ancre d'insertion introuvable — le build Astro a changé, vérifier index.html")
        html = html.replace(ANCRE, BLOC + ANCRE, 1)
    INDEX.write_text(html, encoding="utf-8")
    print("bloc Gold Strategies App inséré dans index.html — à committer.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
