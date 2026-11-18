/* Comportements communs aux sept versions : en-tête, choix de la langue, panneau « L'abbaye », apparitions. */
(function () {
  var header = document.querySelector('[data-header]');
  function setH() { if (header) document.documentElement.style.setProperty('--hh', header.offsetHeight + 'px'); }
  setH(); window.addEventListener('resize', setH);
  function onScroll() { if (header) header.classList.toggle('scrolled', window.scrollY > 40); }
  onScroll(); window.addEventListener('scroll', onScroll, { passive: true });

  /* Menus déroulants : langue et « L'abbaye » */
  var langBtn = document.querySelector('[data-lang]');
  var langList = langBtn && langBtn.nextElementSibling;
  var moreBtn = document.querySelector('[data-more]');
  var mega = document.querySelector('[data-mega]');

  function setLang(open) { if (!langBtn) return; langBtn.setAttribute('aria-expanded', String(open)); langList.hidden = !open; }
  function setMega(open) {
    if (!moreBtn) return;
    moreBtn.setAttribute('aria-expanded', String(open)); mega.hidden = !open;
    document.body.classList.toggle('mega-open', open);
    if (open) { setH(); var first = mega.querySelector('a'); if (first) first.focus({ preventScroll: true }); }
  }
  if (langBtn) langBtn.addEventListener('click', function (e) { e.stopPropagation(); setMega(false); setLang(langList.hidden); });
  if (moreBtn) moreBtn.addEventListener('click', function (e) { e.stopPropagation(); setLang(false); setMega(mega.hidden); });
  var closeBtn = document.querySelector('[data-mega-close]');
  if (closeBtn) closeBtn.addEventListener('click', function () { setMega(false); moreBtn.focus(); });
  document.addEventListener('click', function (e) {
    if (langList && !langList.hidden && !langList.contains(e.target)) setLang(false);
    if (mega && !mega.hidden && !mega.contains(e.target)) setMega(false);
  });
  document.addEventListener('keydown', function (e) {
    if (e.key !== 'Escape') return;
    if (mega && !mega.hidden) { setMega(false); moreBtn.focus(); }
    if (langList && !langList.hidden) { setLang(false); langBtn.focus(); }
  });

  /* Version 1 : menu regroupé sur téléphone */
  var navBtn = document.querySelector('[data-menu]'), nav = document.querySelector('[data-nav]');
  if (navBtn && nav) {
    navBtn.addEventListener('click', function () {
      var open = navBtn.getAttribute('aria-expanded') !== 'true';
      navBtn.setAttribute('aria-expanded', String(open)); nav.classList.toggle('open', open);
    });
    nav.querySelectorAll('a').forEach(function (a) { a.addEventListener('click', function () { navBtn.setAttribute('aria-expanded', 'false'); nav.classList.remove('open'); }); });
  }

  /* Menu à gauche (tiroir) : tout le reste du site */
  var drBtn = document.querySelector('[data-drawer]'), drawer = document.querySelector('[data-drawer-panel]');
  function setDrawer(open) {
    if (!drBtn) return;
    drBtn.setAttribute('aria-expanded', String(open)); drawer.hidden = !open;
    document.body.classList.toggle('drawer-open', open);
    if (open) { var f = drawer.querySelector('.drawer-panel a'); if (f) f.focus({ preventScroll: true }); } else drBtn.focus({ preventScroll: true });
  }
  if (drBtn && drawer) {
    drBtn.addEventListener('click', function (e) { e.stopPropagation(); setLang(false); setDrawer(drawer.hidden); });
    drawer.querySelectorAll('[data-drawer-close]').forEach(function (b) { b.addEventListener('click', function () { setDrawer(false); }); });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && !drawer.hidden) setDrawer(false); });
  }

  /* Lien courant dans la barre de navigation : faire défiler la rangée mobile jusqu'à lui */
  var cur = document.querySelector('.main-nav [aria-current]');
  if (cur && cur.scrollIntoView && window.innerWidth < 760) cur.scrollIntoView({ block: 'nearest', inline: 'center' });

  /* Apparitions douces (versions avec la classe .anim) */
  var reveals = document.querySelectorAll('.anim .reveal');
  if ('IntersectionObserver' in window && reveals.length) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) { if (en.isIntersecting) { en.target.classList.add('in'); io.unobserve(en.target); } });
    }, { rootMargin: '0px 0px -6% 0px' });
    reveals.forEach(function (el) { io.observe(el); });
  } else { reveals.forEach(function (el) { el.classList.add('in'); }); }
})();
