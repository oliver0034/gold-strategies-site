// Effet spotlight au survol des cartes Solutions (#solutions .solc).
// Même logique que le glow radial déjà utilisé sur .card, dupliquée ici
// car .solc n'est pas ciblé par le script du build Astro.
document.querySelectorAll('.solc').forEach((el) => {
  el.addEventListener('mousemove', (e) => {
    const r = el.getBoundingClientRect();
    el.style.setProperty('--mx', ((e.clientX - r.left) / r.width) * 100 + '%');
    el.style.setProperty('--my', ((e.clientY - r.top) / r.height) * 100 + '%');
  });
});

// Section « preuve hebdomadaire » (#preuve) : déclenche le tracé de la courbe de cumul
// quand la carte entre à l'écran. Volontairement indépendant de GSAP : la classe .rv est
// consommée par le script Astro, qui peut disparaître au prochain rebuild.
(function () {
  var carte = document.querySelector('.ph-card');
  if (!carte) return;
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (reduce || !('IntersectionObserver' in window)) { carte.classList.add('ph-in'); return; }
  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) {
      if (e.isIntersecting) { e.target.classList.add('ph-in'); io.unobserve(e.target); }
    });
  }, { threshold: 0.25 });
  io.observe(carte);
})();
