#!/usr/bin/env python3
"""Section vidéo « Gold Strategies en 90 secondes » de la page d'accueil, juste sous le hero.

Contenu ajouté par-dessus le build Astro : un rebuild l'efface. La section est donc insérée
entre deux marqueurs par ce script, appelé par tools/apply-fixes.py.

    python3 tools/build-video-presentation.py            # (ré)insère la section dans index.html
    python3 tools/build-video-presentation.py --check    # code 1 si elle est absente ou modifiée

Fichiers servis : assets/gold-strategies-presentation.mp4 et .jpg (image d'attente).
Pour changer de vidéo : remplacer ces deux fichiers et incrémenter VERSION.
Styles et script sont dans le bloc lui-même : rien à versionner dans site-fixes.css.
"""
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
INDEX = ROOT / "index.html"
VERSION = "20261005"
START = "<!-- VIDEO-PRESENTATION:START (généré par tools/build-video-presentation.py — ne pas éditer à la main) -->"
END = "<!-- VIDEO-PRESENTATION:END -->"
ANCRE = '<section class="sec" id="constat">'      # la section se pose juste avant « Le constat »

BLOC = START + """<section class="gs-video" id="presentation" aria-label="Gold Strategies en 90 secondes"><figure class="gs-video__frame"><video id="gs-video" muted loop playsinline preload="none" width="1920" height="1080" poster="/assets/gold-strategies-presentation.jpg?v=%(v)s" aria-label="Présentation animée de Gold Strategies : le constat, la philosophie, la méthode, les services, le journal de résultats"><source src="/assets/gold-strategies-presentation.mp4?v=%(v)s" type="video/mp4"></video><button type="button" id="gs-video-son" class="gs-video__son" aria-pressed="false">Activer le son</button><figcaption class="gs-video__cap">Gold Strategies en 90 secondes</figcaption></figure><style>.gs-video{padding:56px 24px 8px}.gs-video__frame{position:relative;max-width:980px;margin:0 auto;border-radius:14px;overflow:hidden;border:1px solid var(--line,#d4a24c2e);background:#0b0a08}.gs-video__frame video{display:block;width:100%%;height:auto;aspect-ratio:16/9}.gs-video__son{position:absolute;right:14px;bottom:14px;padding:8px 14px;border-radius:10px;border:1px solid #d4a24c80;background:rgba(11,10,8,.74);color:#ede8df;font:500 .85rem "IBM Plex Sans",sans-serif;cursor:pointer}.gs-video__son:hover,.gs-video__son:focus-visible{border-color:#f2dfa8}.gs-video__cap{position:absolute;left:16px;bottom:16px;color:#9a9285;font:500 .72rem "IBM Plex Mono",monospace;letter-spacing:.14em;text-transform:uppercase;pointer-events:none}@media(max-width:640px){.gs-video{padding:36px 16px 0}.gs-video__cap{display:none}.gs-video__son{right:8px;bottom:8px;padding:4px 9px;font-size:.7rem}}</style><script>(function(){var v=document.getElementById("gs-video"),b=document.getElementById("gs-video-son");if(!v||!b)return;b.addEventListener("click",function(){v.muted=!v.muted;if(!v.muted){v.currentTime=0;v.play()}b.textContent=v.muted?"Activer le son":"Couper le son";b.setAttribute("aria-pressed",String(!v.muted))});if(window.matchMedia&&window.matchMedia("(prefers-reduced-motion: reduce)").matches){v.controls=true;return}if(!("IntersectionObserver" in window)){v.play().catch(function(){});return}new IntersectionObserver(function(e){if(e[0].isIntersecting){v.play().catch(function(){})}else{v.pause()}},{threshold:.3}).observe(v)})();</script></section>""" % {"v": VERSION} + END


def main():
    check = "--check" in sys.argv
    html = INDEX.read_text(encoding="utf-8")
    manquants = [f for f in ("assets/gold-strategies-presentation.mp4", "assets/gold-strategies-presentation.jpg") if not (ROOT / f).exists()]
    if manquants:
        print("✗ fichier(s) vidéo manquant(s) :", ", ".join(manquants)); return 1
    if START in html:
        deb, fin = html.index(START), html.index(END) + len(END)
        if html[deb:fin] == BLOC:
            if not check: print("✓ section vidéo déjà en place.")
            return 0
        if check:
            print("✗ section vidéo modifiée ou périmée — lancer sans --check"); return 1
        html = html[:deb] + BLOC + html[fin:]
    else:
        if check:
            print("✗ section vidéo absente de index.html (rebuild Astro ?) — lancer sans --check"); return 1
        if html.count(ANCRE) != 1:
            sys.exit("Ancre d'insertion introuvable — le build Astro a changé, vérifier index.html")
        html = html.replace(ANCRE, BLOC + ANCRE, 1)
    INDEX.write_text(html, encoding="utf-8")
    print("section vidéo insérée dans index.html — à committer.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
