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
