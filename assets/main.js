(function(){
    var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    // Nav background on scroll
    var nav = document.getElementById('nav');
    var onScroll = function(){ nav.classList.toggle('scrolled', window.scrollY > 24); };
    onScroll(); window.addEventListener('scroll', onScroll, {passive:true});

    // Nav shim : met a jour l'ancien menu des pages HTML pas encore redeployees.
    // Detection : si le lien /analyses/ manque dans .links, on remplace par le menu canonique.
    // DOIT s'executer AVANT la construction du menu mobile (qui clone .links a).
    // Accents en echappements unicode (\\u00e9...) pour survivre a l'editeur web Hostinger.
    (function(){
      var links = document.querySelector('.nav .links');
      if(!links || links.querySelector('a[href="/analyses/"]')) return;
      links.innerHTML =
        '<a href="/">Accueil</a>' +
        '<a href="/complement-revenu/">Compl\u00e9ment de revenu</a>' +
        '<div class="nav-dropdown">' +
          '<button class="dd-trigger" aria-haspopup="true">Services <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M6 9l6 6 6-6"/></svg></button>' +
          '<div class="dd-panel">' +
            '<span class="dd-group">L\'or</span>' +
            '<a href="/trading-de-lor/">Trading de l\'or</a>' +
            '<a href="/xauusd/">Guide XAUUSD</a>' +
            '<a href="/xauusd-cours/">Cours du XAUUSD</a>' +
            '<a href="/comment-trader-lor/">Comment trader l\'or</a>' +
            '<a href="/investir-dans-lor/">Investir dans l\'or</a>' +
            '<span class="dd-group">Autres march\u00e9s</span>' +
            '<a href="/trading-crypto/">Trading crypto</a>' +
            '<a href="/trading-indices/">Trading indices</a>' +
            '<span class="dd-group">Se former</span>' +
            '<a href="/methode/">La m\u00e9thode</a>' +
            '<a href="/formation/">Formation</a>' +
            '<a href="/capital-finance-prop-firm/">Prop firm / Capital financ\u00e9</a>' +
            '<a href="/analyses/">Analyses</a>' +
            '<a href="/communaute/">Communaut\u00e9</a>' +
          '</div>' +
        '</div>' +
        '<a href="/resultats/">R\u00e9sultats</a>' +
        '<a href="/blog/">Blog</a>' +
        '<a href="/a-propos/">\u00c0 propos</a>';
    })();

    // Menu mobile (drawer) : construit dynamiquement a partir des liens desktop existants
    (function(){
      var burger = document.querySelector('.burger');
      var navEl = document.querySelector('.nav');
      if(!burger || !navEl) return;
      var ctaLinks = navEl.querySelectorAll('.nav-cta > a.btn');

      var backdrop = document.createElement('div');
      backdrop.className = 'mobile-backdrop';
      var panel = document.createElement('div');
      panel.className = 'mobile-menu';
      panel.setAttribute('role','dialog');
      panel.setAttribute('aria-label','Menu de navigation');

      var closeBtn = document.createElement('button');
      closeBtn.className = 'mm-close';
      closeBtn.setAttribute('aria-label','Fermer le menu');
      closeBtn.innerHTML = '<svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M6 6l12 12M18 6L6 18"/></svg>';
      panel.appendChild(closeBtn);

      // Reflete la hierarchie du menu desktop : liens directs + groupe "Services" indente
      var navList = document.createElement('nav');
      Array.prototype.forEach.call(navEl.querySelector('.links').children, function(el){
        if(el.tagName === 'A'){ navList.appendChild(el.cloneNode(true)); }
        else if(el.classList && el.classList.contains('nav-dropdown')){
          var grp = document.createElement('div');
          grp.className = 'mm-group';
          var lbl = document.createElement('span');
          lbl.className = 'mm-group-label';
          var trig = el.querySelector('.dd-trigger');
          lbl.textContent = trig ? trig.textContent.trim() : 'Services';
          grp.appendChild(lbl);
          el.querySelectorAll('.dd-panel a, .dd-panel .dd-group').forEach(function(n){ grp.appendChild(n.cloneNode(true)); });
          navList.appendChild(grp);
        }
      });
      panel.appendChild(navList);

      var ctaWrap = document.createElement('div');
      ctaWrap.className = 'mm-cta';
      ctaLinks.forEach(function(a){
        var clone = a.cloneNode(true);
        ctaWrap.appendChild(clone);
      });
      panel.appendChild(ctaWrap);

      document.body.appendChild(backdrop);
      document.body.appendChild(panel);

      function openMenu(){
        panel.classList.add('open'); backdrop.classList.add('open');
        document.body.classList.add('menu-open');
        burger.setAttribute('aria-expanded','true');
      }
      function closeMenu(){
        panel.classList.remove('open'); backdrop.classList.remove('open');
        document.body.classList.remove('menu-open');
        burger.setAttribute('aria-expanded','false');
      }
      burger.setAttribute('aria-expanded','false');
      burger.addEventListener('click', function(){
        if(panel.classList.contains('open')) closeMenu(); else openMenu();
      });
      backdrop.addEventListener('click', closeMenu);
      closeBtn.addEventListener('click', closeMenu);
      panel.querySelectorAll('a').forEach(function(a){ a.addEventListener('click', closeMenu); });
      window.addEventListener('keydown', function(e){ if(e.key==='Escape') closeMenu(); });
      window.addEventListener('resize', function(){ if(window.innerWidth>640) closeMenu(); });
    })();

    // Scroll reveal
    var items = document.querySelectorAll('.reveal');
    function revealNow(el){ el.classList.add('in'); }
    if(reduce || !('IntersectionObserver' in window)){
      items.forEach(revealNow);
    } else {
      var io = new IntersectionObserver(function(entries){
        entries.forEach(function(e){ if(e.isIntersecting){ revealNow(e.target); io.unobserve(e.target); } });
      }, {threshold:.08, rootMargin:'0px 0px -6% 0px'});
      items.forEach(function(el){ io.observe(el); });
      // Passe immediate : revele ce qui est deja visible (le callback initial de l'IO peut tarder)
      requestAnimationFrame(function(){
        var vh = window.innerHeight || document.documentElement.clientHeight;
        items.forEach(function(el){ if(el.getBoundingClientRect().top < vh*0.96){ revealNow(el); io.unobserve(el); } });
      });
      // Filet de securite : tout reveler apres 1.6s quoi qu'il arrive
      setTimeout(function(){ items.forEach(revealNow); }, 1600);
    }

    // Faisceaux lumineux verticaux (grille cybercore adaptee) — desactive si reduced-motion
    if(!reduce){
      var beams = document.getElementById('beams');
      if(beams){
        for(var k=0;k<56;k++){
          var bm=document.createElement('i');
          // distribution en cloche -> densite concentree au centre
          var cx=(Math.random()+Math.random()+Math.random())/3;
          bm.style.left=(cx*100).toFixed(2)+'%';
          bm.style.width=(0.6+Math.random()*1.6).toFixed(2)+'px';
          bm.style.height=(150+Math.random()*380).toFixed(0)+'px';
          var bdur=(2.6+Math.random()*3.2);
          bm.style.animationDuration=bdur.toFixed(1)+'s';
          bm.style.animationDelay=(-Math.random()*bdur).toFixed(1)+'s';
          bm.style.opacity=(0.4+Math.random()*0.5).toFixed(2);
          beams.appendChild(bm);
        }
      }
    }

    // Hero sparks (decoratif, desactive si reduced-motion)
    if(!reduce){
      var hero = document.querySelector('.hero');
      for(var i=0;i<6;i++){
        var s=document.createElement('span'); s.className='spark';
        var sz=(Math.random()*3+2).toFixed(1);
        s.style.width=sz+'px'; s.style.height=sz+'px';
        s.style.left=(Math.random()*100)+'%'; s.style.top=(30+Math.random()*55)+'%';
        s.style.animationDelay=(Math.random()*7).toFixed(1)+'s';
        s.style.animationDuration=(5+Math.random()*5).toFixed(1)+'s';
        hero.appendChild(s);
      }
    }

    // Titre kinetic : reveal mot par mot
    var h1=document.getElementById('heroH1');
    if(h1){
      var ws=h1.querySelectorAll('.w');
      ws.forEach(function(w,i){ w.style.transitionDelay=(0.15+i*0.06).toFixed(2)+'s'; });
      requestAnimationFrame(function(){ h1.classList.add('animate'); });
    }

    // Barre de progression au scroll
    var prog=document.getElementById('progress');
    if(prog){
      var updP=function(){ var h=document.documentElement; var max=h.scrollHeight-h.clientHeight; prog.style.width=(max>0?(h.scrollTop/max*100):0)+'%'; };
      updP(); window.addEventListener('scroll', updP, {passive:true});
    }

    // Cartes solutions : spotlight + tilt 3D
    document.querySelectorAll('.sol-card').forEach(function(card){
      card.addEventListener('mousemove', function(ev){
        var r=card.getBoundingClientRect();
        card.style.setProperty('--mx', (ev.clientX-r.left)+'px');
        card.style.setProperty('--my', (ev.clientY-r.top)+'px');
        if(reduce) return;
        var rx=(((ev.clientY-r.top)/r.height)-.5)*-6, ry=(((ev.clientX-r.left)/r.width)-.5)*6;
        card.style.transform='perspective(800px) rotateX('+rx.toFixed(2)+'deg) rotateY('+ry.toFixed(2)+'deg) translateY(-6px)';
      });
      card.addEventListener('mouseleave', function(){ card.style.transform=''; });
    });

    // Boutons or : effet magnetique
    if(!reduce){
      document.querySelectorAll('.btn-gold').forEach(function(b){
        b.addEventListener('mousemove', function(ev){
          var r=b.getBoundingClientRect();
          b.style.transform='translate('+((ev.clientX-r.left-r.width/2)*.18).toFixed(1)+'px,'+((ev.clientY-r.top-r.height/2)*.28-2).toFixed(1)+'px)';
        });
        b.addEventListener('mouseleave', function(){ b.style.transform=''; });
      });
    }

    // Champ d'etoiles + etoiles filantes (heros cosmiques, hors accueil) — desactive si reduced-motion
    (function(){
      if(reduce) return;
      var heroEl = document.querySelector('.hero');
      if(!heroEl || document.getElementById('beams')) return; // accueil (avec fils) exclu
      var sf=document.createElement('div'); sf.className='starfield'; sf.setAttribute('aria-hidden','true');
      heroEl.insertBefore(sf, heroEl.firstChild);
      for(var st=0; st<70; st++){
        var s=document.createElement('span'); s.className='star';
        var sz=(Math.random()<0.85?1:2);
        s.style.width=sz+'px'; s.style.height=sz+'px';
        s.style.left=(Math.random()*100).toFixed(2)+'%';
        s.style.top=(Math.random()*100).toFixed(2)+'%';
        s.style.animationDuration=(2+Math.random()*4).toFixed(1)+'s';
        s.style.animationDelay=(Math.random()*4).toFixed(1)+'s';
        sf.appendChild(s);
      }
      var spawnMeteor=function(){
        var m=document.createElement('span'); m.className='meteor';
        m.style.left=(35+Math.random()*60).toFixed(1)+'%';
        m.style.top=(Math.random()*45).toFixed(1)+'%';
        m.style.animationDuration=(0.9+Math.random()*0.7).toFixed(2)+'s';
        sf.appendChild(m);
        m.addEventListener('animationend', function(){ if(m.parentNode) m.parentNode.removeChild(m); });
      };
      var loop=function(){ spawnMeteor(); setTimeout(loop, 1500+Math.random()*2800); };
      setTimeout(loop, 1000);
    })();
  })();
