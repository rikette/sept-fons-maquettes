/* Remarques des frères : cliquer un élément pour dire « j'aime », « je n'aime pas » et laisser une remarque.
   En ligne (data-endpoint renseigné) : les remarques sont enregistrées dans un Google Sheet et partagées entre les frères.
   Sinon : elles restent dans ce navigateur (localStorage) et « Envoyer les remarques » produit un fichier. */
(function () {
  'use strict';
  var KEY = 'septfons-remarques-v1';
  var script = document.currentScript || document.querySelector('script[src*="review.js"]');
  var EMAIL = (script && script.getAttribute('data-email')) || '';
  /* En ligne : adresse de l'application Google Apps Script qui enregistre les remarques dans un Google Sheet */
  var ENDPOINT = (script && script.getAttribute('data-endpoint')) || '';
  var ONLINE = !!ENDPOINT;

  /* ---------- où sommes-nous ? ---------- */
  var parts = decodeURIComponent(location.pathname).replace(/\\/g, '/').split('/').filter(Boolean);
  var file = parts[parts.length - 1] || 'index.html';
  if (!/\.html?$/.test(file)) { parts.push('index.html'); file = 'index.html'; }
  var folder = parts[parts.length - 2] || '';
  var inVersion = /^\d+-/.test(folder);
  var VERSION = inVersion ? folder : 'choix';
  var PAGE = file;
  var HERE = inVersion ? folder + '/' + file : file;   // chemin depuis la racine du dossier envoyé
  var ROOT = inVersion ? '../' : '';
  var VLABEL = function (v) { return v === 'choix' ? 'Page de choix' : 'Version ' + v.replace(/^(\d+)-(.*)$/, function (m, n, s) { return n + ' · ' + s.replace(/-/g, ' '); }); };

  /* ---------- stockage ---------- */
  var storeOk = true, S;
  function blank() { return { name: '', items: [], imported: [], queue: [], hidden: false }; }
  function load() {
    try { S = JSON.parse(localStorage.getItem(KEY)) || blank(); } catch (e) { storeOk = false; S = blank(); }
    S.items = S.items || []; S.imported = S.imported || []; S.queue = S.queue || [];
  }
  function save() {
    try { localStorage.setItem(KEY, JSON.stringify(S)); storeOk = true; } catch (e) { storeOk = false; }
    render();
  }
  load();
  window.addEventListener('storage', function (e) { if (e.key === KEY) { load(); render(); } });

  /* ---------- en ligne : envoi des remarques et lecture de celles des autres ---------- */
  var net = { busy: false, ok: null, last: 0 };
  function queue(op) { if (!ONLINE) return; S.queue.push(op); flush(); }
  function flush() {
    if (!ONLINE || net.busy || !S.queue.length) return;
    net.busy = true;
    fetch(ENDPOINT, { method: 'POST', headers: { 'Content-Type': 'text/plain;charset=utf-8' }, body: JSON.stringify(S.queue[0]) })
      .then(function (r) { return r.json(); })
      .then(function (d) { if (!d || !d.ok) throw new Error(d && d.error); S.queue.shift(); net.ok = true; net.busy = false; save(); flush(); })
      .catch(function () { net.ok = false; net.busy = false; render(); setTimeout(flush, 20000); });
  }
  function pull() {
    if (!ONLINE) return;
    fetch(ENDPOINT + (ENDPOINT.indexOf('?') < 0 ? '?' : '&') + 't=' + Date.now())
      .then(function (r) { return r.json(); })
      .then(function (d) {
        if (!d || !d.ok) throw new Error();
        var mine = {}, pendingDel = {};
        S.items.forEach(function (c) { mine[c.id] = 1; });
        S.queue.forEach(function (op) { if (op.op === 'delete') pendingDel[op.id] = 1; });
        var others = [];
        d.items.forEach(function (c) {
          if (mine[c.id] || pendingDel[c.id]) return;
          if (S.name && c.auteur === S.name) { S.items.push(c); return; }   // ses remarques laissées sur un autre appareil
          c.imported = true; others.push(c);
        });
        S.imported = others; net.ok = true; net.last = Date.now(); save();
      })
      .catch(function () { net.ok = false; render(); });
  }

  function uid() { return Date.now().toString(36) + Math.random().toString(36).slice(2, 7); }
  function all() { return S.items.concat(S.imported); }
  function onPage(list) { return list.filter(function (c) { return c.path === HERE; }); }

  /* ---------- repérer un élément ---------- */
  var TARGETS = 'img,figure,h1,h2,h3,h4,h5,p,li,blockquote,summary,details,a,button,label,input,select,textarea,nav,header,footer,section,article,aside,form,.btn,.card';
  var BLOCKS = 'section,header,footer,nav,article,aside,form,details,figure,main>div';
  function cssPath(el) {
    if (el === document.body) return 'body';
    var path = [];
    while (el && el.nodeType === 1 && el !== document.body && el !== document.documentElement) {
      if (el.id && document.querySelectorAll('#' + CSS.escape(el.id)).length === 1) { path.unshift('#' + CSS.escape(el.id)); break; }
      var tag = el.tagName.toLowerCase(), i = 1, s = el;
      while ((s = s.previousElementSibling)) if (s.tagName === el.tagName) i++;
      path.unshift(tag + ':nth-of-type(' + i + ')');
      el = el.parentElement;
    }
    if (path[0] && path[0].charAt(0) !== '#') path.unshift('body');
    return path.join(' > ');
  }
  function find(sel) { try { return document.querySelector(sel); } catch (e) { return null; } }
  function describe(el) {
    if (el === document.body) return { kind: 'Remarque générale', text: '' };
    var tag = el.tagName.toLowerCase();
    var img = tag === 'img' ? el : el.querySelector && !(el.textContent || '').trim() && el.querySelector('img');
    var text = (el.innerText || el.textContent || el.value || el.placeholder || '').replace(/\s+/g, ' ').trim();
    var kinds = { img: 'Image', figure: 'Image', h1: 'Titre', h2: 'Titre', h3: 'Titre', h4: 'Titre', h5: 'Titre', p: 'Paragraphe', li: 'Élément de liste',
      blockquote: 'Citation', summary: 'Question dépliante', details: 'Question dépliante', a: 'Lien / bouton', button: 'Bouton', nav: 'Menu',
      header: 'En-tête', footer: 'Pied de page', section: 'Section', form: 'Formulaire', label: 'Champ du formulaire', input: 'Champ du formulaire',
      select: 'Champ du formulaire', textarea: 'Champ du formulaire' };
    var kind = kinds[tag] || 'Bloc';
    if (el.closest && el.closest('header') && tag !== 'header' && kind !== 'Menu') kind += ' (en-tête)';
    var src = img ? (img.getAttribute('src') || '').split('/').pop() : '';
    return { kind: kind, text: (text.length > 140 ? text.slice(0, 137) + '…' : text) || (src ? 'image ' + src : ''), img: src };
  }

  /* ---------- interface ---------- */
  function h(tag, attrs, kids) {
    var el = document.createElement(tag);
    for (var k in attrs || {}) {
      if (k === 'text') el.textContent = attrs[k];
      else if (k.slice(0, 2) === 'on') el.addEventListener(k.slice(2), attrs[k]);
      else el.setAttribute(k, attrs[k]);
    }
    (kids || []).forEach(function (c) { if (c) el.appendChild(typeof c === 'string' ? document.createTextNode(c) : c); });
    return el;
  }
  var ICON = { like: '👍', dislike: '👎', note: '💬' };
  var VERB = { like: 'J’aime', dislike: 'Je n’aime pas', note: 'Remarque' };

  var ui = h('div', { id: 'rv-ui', 'data-rv': '' });
  var pins = h('div', { class: 'rv-pins', 'data-rv': '', 'aria-hidden': 'true' });
  var hover = h('div', { class: 'rv-hover', 'data-rv': '' });
  var bar = h('div', { class: 'rv-bar', role: 'toolbar', 'aria-label': 'Remarques' });
  var bMode = h('button', { type: 'button', class: 'rv-b rv-main', 'aria-pressed': 'false', onclick: function () { setMode(!mode); } }, ['✎ Commenter']);
  var bEye = h('button', { type: 'button', class: 'rv-b', title: 'Afficher / masquer les remarques', onclick: function () { S.hidden = !S.hidden; save(); } });
  var bList = h('button', { type: 'button', class: 'rv-b', title: 'Mes remarques', onclick: function () { togglePanel(); } });
  bar.appendChild(bMode); bar.appendChild(bEye); bar.appendChild(bList);
  var tip = h('div', { class: 'rv-tip', role: 'status' });
  var panel = h('aside', { class: 'rv-panel', hidden: '', 'aria-label': 'Mes remarques' });
  ui.appendChild(tip); ui.appendChild(bar); ui.appendChild(panel);

  /* ---------- mode commentaire ---------- */
  var mode = false, bubble = null;
  function setMode(on) {
    mode = on; bMode.setAttribute('aria-pressed', String(on));
    bMode.textContent = on ? '✓ Terminer' : '✎ Commenter';
    document.documentElement.classList.toggle('rv-on', on);
    tip.textContent = on ? 'Cliquez sur un élément de la page (titre, photo, menu, bouton…) pour donner votre avis.' : '';
    tip.hidden = !on;
    if (!on) { hover.style.display = 'none'; closeBubble(); }
    try { sessionStorage.setItem('rv-mode', on ? '1' : ''); } catch (e) {}
  }
  function isUI(t) { return t && t.closest && t.closest('[data-rv],#rv-ui'); }
  function pick(t) {
    if (!t || t.nodeType !== 1) return null;
    var el = t.closest(TARGETS);
    return el && el !== document.documentElement ? el : (t === document.body ? null : t);
  }
  document.addEventListener('mouseover', function (e) {
    if (!mode || bubble || isUI(e.target)) { if (!bubble) hover.style.display = 'none'; return; }
    var el = pick(e.target); if (!el) return; frame(hover, el);
  }, true);
  function frame(box, el) {
    var r = el.getBoundingClientRect();
    box.style.display = 'block';
    box.style.top = (r.top + scrollY - 3) + 'px'; box.style.left = (r.left + scrollX - 3) + 'px';
    box.style.width = (r.width + 6) + 'px'; box.style.height = (r.height + 6) + 'px';
  }
  ['click', 'auxclick', 'submit', 'pointerup', 'mouseup'].forEach(function (type) {
    window.addEventListener(type, function (e) {
      if (isUI(e.target)) return;
      if (!mode) { if (type === 'click' && bubble) closeBubble(); return; }
      e.preventDefault(); e.stopPropagation(); e.stopImmediatePropagation();
      if (type !== 'click') return;
      if (bubble) { closeBubble(); return; }
      var el = pick(e.target); if (el) openBubble(el, null, e.clientX, e.clientY);
    }, true);
  });
  document.addEventListener('keydown', function (e) {
    if (e.key !== 'Escape') return;
    if (bubble) closeBubble(); else if (!panel.hidden) togglePanel(false); else if (mode) setMode(false);
  });

  /* ---------- bulle ---------- */
  function closeBubble() { if (bubble) { bubble.remove(); bubble = null; } hover.style.display = 'none'; }
  function openBubble(el, item, x, y) {
    closeBubble();
    var readOnly = item && item.imported;
    var cur = { el: el, verdict: item ? item.verdict : '', };
    frame(hover, el);
    var d = describe(el);
    var b = h('div', { class: 'rv-bubble', role: 'dialog', 'aria-label': 'Votre avis' });
    var head = h('div', { class: 'rv-bh' }, [h('strong', { text: d.kind }), d.text ? h('span', { text: ' — ' + d.text }) : null]);
    b.appendChild(head);
    if (readOnly) {
      b.appendChild(h('p', { class: 'rv-ro' }, [ICON[item.verdict] + ' ' + VERB[item.verdict] + ' · ' + (item.auteur || 'anonyme')]));
      if (item.texte) b.appendChild(h('p', { class: 'rv-ro rv-q', text: item.texte }));
      b.appendChild(h('div', { class: 'rv-act' }, [h('button', { type: 'button', class: 'rv-b', text: 'Fermer', onclick: closeBubble })]));
    } else {
      var nameIn = null;
      if (!S.name) {
        nameIn = h('input', { type: 'text', class: 'rv-in', placeholder: 'Votre prénom (une seule fois)', 'aria-label': 'Votre prénom', autocomplete: 'given-name' });
        b.appendChild(nameIn);
      }
      var row = h('div', { class: 'rv-verdicts', role: 'radiogroup', 'aria-label': 'Votre avis' });
      ['like', 'dislike'].forEach(function (v) {
        var btn = h('button', { type: 'button', class: 'rv-v rv-' + v, role: 'radio', 'aria-checked': String(cur.verdict === v), onclick: function () {
          cur.verdict = cur.verdict === v ? '' : v;
          row.querySelectorAll('button').forEach(function (x) { x.setAttribute('aria-checked', String(x === btn && cur.verdict === v)); }); ta.focus();
        } }, [ICON[v] + ' ' + VERB[v]]);
        row.appendChild(btn);
      });
      b.appendChild(row);
      var ta = h('textarea', { class: 'rv-in', rows: '3', placeholder: 'Votre remarque (facultatif)', 'aria-label': 'Votre remarque' });
      ta.value = item ? item.texte || '' : '';
      b.appendChild(ta);
      var up = !item && el !== document.body && el.parentElement && el.parentElement.closest(BLOCKS);
      var err = h('p', { class: 'rv-err', hidden: '' });
      b.appendChild(err);
      var act = h('div', { class: 'rv-act' }, [
        up ? h('button', { type: 'button', class: 'rv-link', text: '↥ Le bloc entier', title: 'Commenter la section qui contient cet élément', onclick: function () { openBubble(up, null, x, y); } }) : null,
        item ? h('button', { type: 'button', class: 'rv-link rv-del', text: 'Supprimer', onclick: function () { remove(item.id); closeBubble(); } }) : null,
        h('span', { class: 'rv-sp' }),
        h('button', { type: 'button', class: 'rv-b', text: 'Annuler', onclick: closeBubble }),
        h('button', { type: 'button', class: 'rv-b rv-main', text: 'Enregistrer', onclick: function () {
          if (nameIn) { var n = nameIn.value.trim(); if (!n) { err.textContent = 'Indiquez votre prénom.'; err.hidden = false; nameIn.focus(); return; } S.name = n; }
          var verdict = cur.verdict || (ta.value.trim() ? 'note' : '');
          if (!verdict) { err.textContent = 'Choisissez « J’aime » ou « Je n’aime pas », ou écrivez une remarque.'; err.hidden = false; return; }
          cur.verdict = verdict;
          if (item) {
            item.verdict = cur.verdict; item.texte = ta.value.trim(); item.modifie = new Date().toISOString();
            queue({ op: 'update', id: item.id, verdict: item.verdict, texte: item.texte });
          } else {
            var dd = describe(el);
            var it = { id: uid(), auteur: S.name, version: VERSION, page: PAGE, path: HERE, titre_page: document.title,
              selecteur: cssPath(el), element: dd.kind, extrait: dd.text, image: dd.img || '', verdict: cur.verdict,
              texte: ta.value.trim(), ecran: innerWidth < 760 ? 'téléphone' : (innerWidth < 1100 ? 'tablette' : 'ordinateur'),
              largeur: innerWidth, date: new Date().toISOString() };
            S.items.push(it); queue({ op: 'add', item: it });
          }
          S.items.forEach(function (c) { if (!c.auteur) c.auteur = S.name; });
          S.hidden = false; closeBubble(); save();
          flashTip(ONLINE ? 'Remarque enregistrée. Les autres frères la voient.' : 'Remarque enregistrée. Elle reste dans ce navigateur jusqu’à l’envoi.');
        } })
      ]);
      b.appendChild(act);
    }
    ui.appendChild(b); bubble = b;
    // placement près du clic, dans la fenêtre
    var bw = Math.min(360, innerWidth - 24);
    b.style.width = bw + 'px';
    var bh = b.offsetHeight;
    var r = el.getBoundingClientRect();
    var px = x != null ? x : r.left + 8, py = y != null ? y : r.top + 8;
    b.style.left = Math.max(12, Math.min(px - 20, innerWidth - bw - 12)) + 'px';
    var top = py + bh + 24 < innerHeight ? py + 14 : py - bh - 14;
    b.style.top = Math.max(12, Math.min(top, innerHeight - bh - 12)) + 'px';
    var f = b.querySelector('input, .rv-v[aria-checked="true"], .rv-v, button'); if (f) f.focus({ preventScroll: true });
  }
  function remove(id) { if (S.items.some(function (c) { return c.id === id; })) queue({ op: 'delete', id: id }); S.items = S.items.filter(function (c) { return c.id !== id; }); S.imported = S.imported.filter(function (c) { return c.id !== id; }); save(); }
  var tipT;
  function flashTip(msg) {
    tip.textContent = msg; tip.hidden = false; clearTimeout(tipT);
    tipT = setTimeout(function () { if (mode) setMode(true); else tip.hidden = true; }, 3200);
  }

  /* ---------- pastilles ---------- */
  function layout() {
    pins.textContent = '';
    if (S.hidden) return;
    onPage(all()).forEach(function (c, i) {
      var el = find(c.selecteur); if (!el) return;
      var r = el.getBoundingClientRect(); if (!r.width && !r.height) return;
      var fixed = el === document.body;
      var p = h('button', { type: 'button', class: 'rv-pin rv-' + c.verdict + (c.imported ? ' rv-imp' : ''), title: (c.auteur || '') + ' — ' + VERB[c.verdict] + (c.texte ? ' : ' + c.texte : ''),
        onclick: function (e) { e.preventDefault(); e.stopPropagation(); openBubble(el, c, e.clientX, e.clientY); } }, [String(i + 1)]);
      p.style.top = (fixed ? 8 : Math.max(0, r.top + scrollY - 10)) + 'px';
      p.style.left = (fixed ? 8 : Math.max(0, Math.min(r.right + scrollX - 14, document.documentElement.scrollWidth - 30))) + 'px';
      if (fixed) p.style.position = 'fixed';
      pins.appendChild(p);
    });
  }
  var raf;
  function relayout() { cancelAnimationFrame(raf); raf = requestAnimationFrame(layout); }
  window.addEventListener('resize', relayout);
  window.addEventListener('load', relayout);
  document.addEventListener('toggle', relayout, true);
  setInterval(relayout, 1500);

  /* ---------- panneau ---------- */
  var filter = 'page';
  function togglePanel(force) {
    var open = force != null ? force : panel.hidden;
    panel.hidden = !open; if (open) { closeBubble(); renderPanel(); if (ONLINE && Date.now() - net.last > 5000) pull(); }
  }
  function goto(c) {
    if (c.path === HERE) {
      togglePanel(false);
      var el = find(c.selecteur);
      if (el) { el.scrollIntoView({ behavior: 'smooth', block: 'center' }); S.hidden = false; save(); setTimeout(function () { frame(hover, el); hover.classList.add('rv-flash'); setTimeout(function () { hover.style.display = 'none'; hover.classList.remove('rv-flash'); }, 1600); }, 500); }
      return;
    }
    location.href = ROOT + c.path + '#rv=' + c.id;
  }
  function renderPanel() {
    if (panel.hidden) return;
    panel.textContent = '';
    var list = all(), here = onPage(list);
    var shown = filter === 'page' ? here : list;
    panel.appendChild(h('div', { class: 'rv-ph' }, [
      h('strong', { text: 'Remarques' + (S.name ? ' de ' + S.name : '') }),
      h('button', { type: 'button', class: 'rv-x', 'aria-label': 'Fermer', text: '×', onclick: function () { togglePanel(false); } })
    ]));
    if (!storeOk) panel.appendChild(h('p', { class: 'rv-err', text: 'Ce navigateur ne garde pas les remarques. Ouvrez le site avec Chrome ou Edge, ou envoyez vos remarques avant de fermer la page.' }));
    var tabs = h('div', { class: 'rv-tabs' }, [
      h('button', { type: 'button', 'aria-pressed': String(filter === 'page'), text: 'Cette page (' + here.length + ')', onclick: function () { filter = 'page'; renderPanel(); } }),
      h('button', { type: 'button', 'aria-pressed': String(filter === 'all'), text: 'Tout le site (' + list.length + ')', onclick: function () { filter = 'all'; renderPanel(); } })
    ]);
    panel.appendChild(tabs);
    panel.appendChild(h('button', { type: 'button', class: 'rv-link rv-gen', text: '＋ Remarque générale sur cette page', onclick: function () { togglePanel(false); openBubble(document.body, null, innerWidth / 2 - 180, 80); } }));
    var ul = h('ol', { class: 'rv-list' });
    var lastGroup = '';
    shown.forEach(function (c) {
      var g = VLABEL(c.version) + ' — ' + c.page;
      if (filter === 'all' && g !== lastGroup) { ul.appendChild(h('li', { class: 'rv-g', text: g })); lastGroup = g; }
      var num = onPage(list).indexOf(c) + 1;
      ul.appendChild(h('li', { class: 'rv-it rv-' + c.verdict }, [
        h('div', { class: 'rv-ih' }, [
          num ? h('span', { class: 'rv-n', text: String(num) }) : null,
          h('span', { text: ICON[c.verdict] + ' ' + VERB[c.verdict] }),
          c.imported || (S.name && c.auteur !== S.name) ? h('em', { text: ' · ' + (c.auteur || 'anonyme') }) : null
        ]),
        h('div', { class: 'rv-ie', text: c.element + (c.extrait ? ' — « ' + c.extrait + ' »' : '') }),
        c.texte ? h('div', { class: 'rv-iq', text: c.texte }) : null,
        h('div', { class: 'rv-ia' }, [
          h('button', { type: 'button', class: 'rv-link', text: c.path === HERE ? 'Voir' : 'Aller à la page', onclick: function () { goto(c); } }),
          !c.imported && c.path === HERE ? h('button', { type: 'button', class: 'rv-link', text: 'Modifier', onclick: function () { var el = find(c.selecteur) || document.body; togglePanel(false); el.scrollIntoView({ block: 'center' }); setTimeout(function () { openBubble(el, c); }, 60); } }) : null,
          ONLINE && c.imported ? null : h('button', { type: 'button', class: 'rv-link rv-del', text: c.imported ? 'Retirer' : 'Supprimer', onclick: function () { if (confirm('Supprimer cette remarque ?')) remove(c.id); } })
        ])
      ]));
    });
    if (!shown.length) ul.appendChild(h('li', { class: 'rv-empty', text: filter === 'page' ? 'Aucune remarque sur cette page. Cliquez « ✎ Commenter », puis sur un élément.' : 'Aucune remarque pour l’instant.' }));
    panel.appendChild(ul);
    if (ONLINE) {
      var st = S.queue.length ? '⏳ ' + S.queue.length + ' remarque(s) en cours d’envoi' + (net.ok === false ? ' : connexion impossible, nouvel essai dans un instant.' : '…')
        : (net.ok === false ? '⚠ Connexion impossible : vos remarques sont gardées et partiront dès que possible.' : '✓ Vos remarques sont enregistrées en ligne. Tous les frères les voient.');
      panel.appendChild(h('div', { class: 'rv-pf' }, [
        h('p', { class: 'rv-status' + (net.ok === false ? ' rv-warn' : ''), text: st }),
        h('div', { class: 'rv-pm' }, [
          h('button', { type: 'button', class: 'rv-link', text: 'Actualiser', onclick: pull }),
          h('button', { type: 'button', class: 'rv-link', text: 'Télécharger toutes les remarques', onclick: exportAll }),
          S.name ? h('button', { type: 'button', class: 'rv-link', text: 'Changer de prénom', onclick: function () { var n = prompt('Votre prénom', S.name); if (n && n.trim()) { S.name = n.trim(); save(); } } }) : null
        ])
      ]));
      return;
    }
    var fileIn = h('input', { type: 'file', accept: '.json,application/json', multiple: '', hidden: '', onchange: function () { importFiles(fileIn.files); } });
    panel.appendChild(h('div', { class: 'rv-pf' }, [
      h('button', { type: 'button', class: 'rv-b rv-main rv-send', text: 'Envoyer les remarques (' + (S.items.length + S.imported.length) + ')', onclick: exportAll }),
      h('p', { class: 'rv-help', text: 'Un fichier est enregistré dans vos Téléchargements. Il contient vos remarques et celles des frères que vous avez importées : transmettez-le au frère suivant ou renvoyez-le' + (EMAIL ? ' (un courriel s’ouvre, joignez-y le fichier).' : ' par courriel.') }),
      h('div', { class: 'rv-pm' }, [
        h('button', { type: 'button', class: 'rv-link', text: 'Ouvrir un fichier de remarques reçu…', onclick: function () { fileIn.click(); } }),
        fileIn,
        S.items.length || S.imported.length ? h('button', { type: 'button', class: 'rv-link rv-del', text: 'Tout effacer', onclick: function () {
          if (confirm('Effacer toutes les remarques de ce navigateur ? Pensez à les envoyer d’abord.')) { S.items = []; S.imported = []; save(); }
        } }) : null,
        S.name ? h('button', { type: 'button', class: 'rv-link', text: 'Changer de prénom', onclick: function () { var n = prompt('Votre prénom', S.name); if (n && n.trim()) { S.name = n.trim(); S.items.forEach(function (c) { c.auteur = S.name; }); save(); } } }) : null
      ])
    ]));
  }

  /* ---------- export / import ---------- */
  function stamp() { var d = new Date(); return d.getFullYear() + '-' + ('0' + (d.getMonth() + 1)).slice(-2) + '-' + ('0' + d.getDate()).slice(-2); }
  function safe(s) { return (s || 'frere').normalize('NFD').replace(/[̀-ͯ]/g, '').replace(/[^\w-]+/g, '-').toLowerCase(); }
  function exportAll() {
    if (!S.items.length && !S.imported.length) { alert('Il n’y a encore aucune remarque.'); return; }
    if (!S.name && !ONLINE) askName();
    var data = { format: 'septfons-remarques', version: 1, auteur: S.name, exporte_le: new Date().toISOString(), navigateur: navigator.userAgent, remarques: S.items.concat(S.imported).map(function (c) { var o = {}; for (var k in c) if (k !== 'imported') o[k] = c[k]; return o; }) };
    var name = (ONLINE ? 'remarques-tous-' : 'remarques-' + safe(S.name) + '-') + stamp() + '.json';
    var url = URL.createObjectURL(new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' }));
    var a = h('a', { href: url, download: name }); document.body.appendChild(a); a.click(); a.remove();
    setTimeout(function () { URL.revokeObjectURL(url); }, 4000);
    if (EMAIL && !ONLINE) {
      var counts = { like: 0, dislike: 0, note: 0 }; S.items.forEach(function (c) { counts[c.verdict]++; });
      var body = 'Bonjour,\n\nVoici mes remarques sur les maquettes du site (' + S.items.length + ' remarques : ' + counts.like + ' j’aime, ' + counts.dislike + ' je n’aime pas, ' + counts.note + ' remarques).\n\n' +
        '>>> Merci de joindre à ce courriel le fichier « ' + name + ' » qui vient d’être enregistré dans vos Téléchargements. <<<\n\n' + S.name;
      setTimeout(function () { location.href = 'mailto:' + EMAIL + '?subject=' + encodeURIComponent('Site de Sept-Fons — remarques de ' + S.name) + '&body=' + encodeURIComponent(body); }, 600);
    }
    flashTip('Fichier « ' + name + ' » enregistré dans vos Téléchargements.');
  }
  function importFiles(files) {
    var n = 0, pending = files.length;
    Array.prototype.forEach.call(files, function (f) {
      var r = new FileReader();
      r.onload = function () {
        try {
          var d = JSON.parse(r.result);
          (d.remarques || []).forEach(function (c) {
            if (S.items.some(function (x) { return x.id === c.id; }) || S.imported.some(function (x) { return x.id === c.id; })) return;
            c.auteur = c.auteur || d.auteur; if (S.name && c.auteur === S.name) S.items.push(c); else { c.imported = true; S.imported.push(c); } n++;
          });
        } catch (e) { alert('Le fichier « ' + f.name + ' » n’a pas pu être lu.'); }
        if (--pending === 0) { save(); filter = 'all'; renderPanel(); flashTip(n + ' remarque(s) importée(s).'); }
      };
      r.readAsText(f);
    });
  }

  /* ---------- rendu ---------- */
  function render() {
    var n = S.items.length + S.imported.length, here = onPage(all()).length;
    bList.textContent = '☰ ' + (here ? here + ' ici · ' : '') + n + (ONLINE && S.queue.length ? ' ⏳' : '');
    bList.setAttribute('aria-label', 'Remarques : ' + here + ' sur cette page, ' + n + ' en tout');
    bEye.textContent = S.hidden ? '◌' : '◉';
    bEye.setAttribute('aria-pressed', String(!S.hidden));
    bEye.setAttribute('aria-label', S.hidden ? 'Afficher les remarques' : 'Masquer les remarques');
    bEye.title = S.hidden ? 'Afficher les remarques' : 'Masquer les remarques';
    document.documentElement.classList.toggle('rv-hidden', !!S.hidden);
    layout(); renderPanel();
  }

  function askName() { var n = prompt('Votre prénom, pour signer vos remarques :', S.name || ''); if (n && n.trim()) { S.name = n.trim(); save(); } }
  function welcome() {
    if (S.name || document.querySelector('.rv-welcome')) return;
    var inp = h('input', { type: 'text', class: 'rv-in', placeholder: 'Votre prénom', 'aria-label': 'Votre prénom', autocomplete: 'given-name' });
    var fileIn = h('input', { type: 'file', accept: '.json,application/json', multiple: '', hidden: '', onchange: function () { ok(); importFiles(fileIn.files); } });
    function ok() { var n = inp.value.trim(); if (!n) { inp.focus(); return false; } S.name = n; w.remove(); save(); pull(); return true; }
    var w = h('div', { class: 'rv-welcome', role: 'dialog', 'aria-modal': 'true', 'aria-label': 'Bienvenue' }, [h('form', { class: 'rv-wbox', onsubmit: function (e) { e.preventDefault(); if (ok()) flashTip('Merci ' + S.name + '. Cliquez « ✎ Commenter » pour donner votre avis.'); } }, [
      h('strong', { class: 'rv-wt', text: 'Bienvenue' }),
      h('p', { text: 'Vous pouvez donner votre avis directement sur ces maquettes : cliquez « ✎ Commenter » en bas à droite, puis sur un élément de la page.' }),
      h('label', { class: 'rv-wl', text: 'Votre prénom, pour signer vos remarques' }), inp,
      h('div', { class: 'rv-act' }, [
        h('button', { type: 'button', class: 'rv-link', text: 'Plus tard', onclick: function () { w.remove(); } }),
        h('span', { class: 'rv-sp' }),
        h('button', { type: 'submit', class: 'rv-b rv-main', text: 'Commencer' })
      ]),
      ONLINE ? h('p', { class: 'rv-help', text: 'Vos remarques sont partagées : chaque frère voit celles des autres, signées de leur prénom.' }) :
      h('p', { class: 'rv-help' }, ['Un frère vous a transmis un fichier de remarques ? ',
        h('button', { type: 'button', class: 'rv-link', text: 'Ouvrez-le ici', onclick: function () { if (!inp.value.trim()) { inp.focus(); inp.placeholder = 'Votre prénom d’abord'; return; } fileIn.click(); } }), fileIn])
    ])]);
    ui.appendChild(w); inp.focus();
  }
  function start() {
    document.body.appendChild(pins); document.body.appendChild(hover); document.body.appendChild(ui);
    tip.hidden = true; render();
    if (!S.name && (storeOk || ONLINE)) setTimeout(welcome, 600);
    if (ONLINE) {
      pull(); flush();
      setInterval(function () { if (!document.hidden) pull(); }, 30000);
      document.addEventListener('visibilitychange', function () { if (!document.hidden && Date.now() - net.last > 10000) pull(); });
    }
    var m = /#rv=([\w]+)/.exec(location.hash);
    if (m) { var c = all().filter(function (x) { return x.id === m[1]; })[0]; if (c) setTimeout(function () { history.replaceState(null, '', location.pathname + location.search); goto(c); }, 400); }
    try { if (sessionStorage.getItem('rv-mode')) setMode(true); } catch (e) {}
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', start); else start();
})();
