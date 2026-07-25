// Parallaxe au scroll pour les visuels .parallax-bg ajoutés hors build Astro
// (ex: .definition-bg sur /complement-revenu/). Même traitement que .vision-bg
// et la photo du fondateur : réimporte le gsap/ScrollTrigger déjà bundlé par
// le site plutôt que d'ajouter une dépendance.
import { n as gsap, t as ScrollTrigger } from '/_astro/ScrollTrigger.DDi3XPDo.js';

gsap.registerPlugin(ScrollTrigger);

if (!matchMedia('(prefers-reduced-motion: reduce)').matches) {
  document.querySelectorAll('.parallax-bg').forEach((el) => {
    const section = el.closest('section');
    gsap.set(el, { scale: 1.18 });
    gsap.fromTo(
      el,
      { yPercent: -9 },
      {
        yPercent: 9,
        ease: 'none',
        scrollTrigger: { trigger: section, start: 'top bottom', end: 'bottom top', scrub: 0.5 },
      }
    );
  });
}
