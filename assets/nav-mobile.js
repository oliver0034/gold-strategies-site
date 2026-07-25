/* =========================================================================
   nav-mobile.js — menu mobile pour les pages générées par Astro.

   Le build Astro masque `.navlinks` sous 1180px sans fournir de bouton
   burger : la navigation devient impossible sur mobile et tablette.
   Ce script reconstruit le menu à partir des liens déjà présents dans le
   DOM — si le menu change côté Astro, le menu mobile suit automatiquement.

   Aucune dépendance. À réinjecter après chaque rebuild Astro
   (voir README-MAINTENANCE.md).
   ========================================================================= */
(function () {
  'use strict';

  function init() {
    var nav = document.querySelector('.nav');
    var navlinks = nav && nav.querySelector('.navlinks');
    if (!nav || !navlinks || document.querySelector('.burger-mobile')) return;

    var panel = document.createElement('div');
    panel.className = 'mobile-nav';
    panel.id = 'mobileNav';
    panel.setAttribute('data-open', 'false');
    panel.setAttribute('aria-label', 'Navigation principale (mobile)');

    // Liens de premier niveau + entrées du menu déroulant "Services".
    Array.prototype.forEach.call(navlinks.children, function (li) {
      var dd = li.querySelector('.dd-panel');
      if (dd) {
        var trigger = li.querySelector('.dd-trigger');
        var label = document.createElement('span');
        label.className = 'mn-group';
        label.textContent = trigger ? trigger.textContent.trim() : 'Services';
        panel.appendChild(label);
        Array.prototype.forEach.call(dd.querySelectorAll('a'), function (a) {
          panel.appendChild(cloneLink(a));
        });
        return;
      }
      var link = li.querySelector('a');
      if (link) panel.appendChild(cloneLink(link));
    });

    // Boutons d'appel à l'action repris de la barre de navigation.
    var ctas = nav.querySelectorAll('.nav-cta .btn');
    if (ctas.length) {
      var box = document.createElement('div');
      box.className = 'mn-cta';
      Array.prototype.forEach.call(ctas, function (btn) {
        var a = cloneLink(btn);
        a.className = btn.classList.contains('btn-primary') ? 'is-gold' : '';
        box.appendChild(a);
      });
      panel.appendChild(box);
    }

    document.body.appendChild(panel);

    var burger = document.createElement('button');
    burger.type = 'button';
    burger.className = 'burger-mobile';
    burger.setAttribute('aria-label', 'Ouvrir le menu');
    burger.setAttribute('aria-expanded', 'false');
    burger.setAttribute('aria-controls', 'mobileNav');
    burger.innerHTML = icon(false);

    var ctaBox = nav.querySelector('.nav-cta');
    if (ctaBox) ctaBox.appendChild(burger);
    else nav.querySelector('.wrap').appendChild(burger);

    function setOpen(open) {
      panel.setAttribute('data-open', open ? 'true' : 'false');
      burger.setAttribute('aria-expanded', open ? 'true' : 'false');
      burger.setAttribute('aria-label', open ? 'Fermer le menu' : 'Ouvrir le menu');
      burger.innerHTML = icon(open);
      document.body.classList.toggle('mobile-nav-open', open);
    }

    burger.addEventListener('click', function () {
      setOpen(panel.getAttribute('data-open') !== 'true');
    });
    panel.addEventListener('click', function (e) {
      if (e.target.tagName === 'A') setOpen(false);
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') setOpen(false);
    });
    window.addEventListener('resize', function () {
      if (window.innerWidth > 1180) setOpen(false);
    });
  }

  function cloneLink(source) {
    var a = document.createElement('a');
    a.href = source.getAttribute('href') || '#';
    a.textContent = source.textContent.trim();
    if (source.getAttribute('target')) a.target = source.getAttribute('target');
    if (source.getAttribute('rel')) a.rel = source.getAttribute('rel');
    if (source.getAttribute('aria-current')) a.setAttribute('aria-current', source.getAttribute('aria-current'));
    return a;
  }

  function icon(open) {
    var path = open ? '<path d="M6 6l12 12M18 6L6 18"/>' : '<path d="M4 7h16M4 12h16M4 17h16"/>';
    return '<svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round">' + path + '</svg>';
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
