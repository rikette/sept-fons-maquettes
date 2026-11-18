/* Page « Toutes les remarques » : lit le recueil en ligne et classe les remarques par version, puis par page. */
(function () {
  'use strict';
  var KEY = 'septfons-remarques-v1';
  var cfg = JSON.parse(document.getElementById('rv-config').textContent);
  var ENDPOINT = cfg.endpoint;
  var ICON = { like: '👍', dislike: '👎', note: '💬' };
  var VERB = { like: 'J’aime', dislike: 'Je n’aime pas', note: 'Remarque' };
  var all = [], state = { version: '', verdict: '', auteur: '', q: '' };
  var $ = function (s) { return document.querySelector(s); };

  function h(tag, attrs, kids) {
    var el = document.createElement(tag);
    for (var k in attrs || {}) {
      if (k === 'text') el.textContent = attrs[k];
      else if (k.slice(0, 2) === 'on') el.addEventListener(k.slice(2), attrs[k]);
      else el.setAttribute(k, attrs[k]);
    }
    (kids || []).forEach(function (c) { if (c != null && c !== false) el.appendChild(typeof c === 'string' ? document.createTextNode(c) : c); });
    return el;
  }
  function vname(v) { return v === 'choix' ? 'Page de choix' : (cfg.versions[v] || v); }
  function vorder(v) { var i = cfg.order.indexOf(v); return i < 0 ? 99 : i; }
  function pname(p) { return cfg.pages[p] || p; }
  function porder(p) { var i = cfg.pageOrder.indexOf(p); return i < 0 ? 99 : i; }
  function when(d) {
    var t = new Date(d); if (isNaN(t)) return '';
    return t.toLocaleDateString('fr-FR', { day: 'numeric', month: 'short' }) + ', ' + t.toLocaleTimeString('fr-FR', { hour: '2-digit', minute: '2-digit' });
  }
  function counts(list) { var c = { like: 0, dislike: 0, note: 0 }; list.forEach(function (x) { c[x.verdict] = (c[x.verdict] || 0) + 1; }); return c; }
  function tally(list) {
    var c = counts(list);
    return h('span', { class: 'tally' }, [h('span', { class: 'like', text: '👍 ' + c.like }), h('span', { class: 'dislike', text: '👎 ' + c.dislike }), h('span', { class: 'note', text: '💬 ' + c.note })]);
  }

  function load() {
    $('#status').textContent = 'Chargement…';
    if (!ENDPOINT) {
      try { var S = JSON.parse(localStorage.getItem(KEY)) || {}; all = (S.items || []).concat(S.imported || []); } catch (e) { all = []; }
      $('#status').textContent = 'Le recueil en ligne n’est pas encore branché : seules les remarques laissées sur cet appareil apparaissent.';
      render(); return;
    }
    fetch(ENDPOINT + (ENDPOINT.indexOf('?') < 0 ? '?' : '&') + 't=' + Date.now())
      .then(function (r) { return r.json(); })
      .then(function (d) {
        if (!d || !d.ok) throw new Error();
        all = d.items;
        $('#status').textContent = 'Mis à jour à ' + new Date().toLocaleTimeString('fr-FR', { hour: '2-digit', minute: '2-digit' }) + '.';
        render();
      })
      .catch(function () { $('#status').textContent = 'Impossible de lire le recueil. Vérifiez la connexion, puis « Actualiser ».'; });
  }

  function filtered() {
    var q = state.q.toLowerCase();
    return all.filter(function (c) {
      return (!state.version || c.version === state.version) && (!state.verdict || c.verdict === state.verdict) &&
        (!state.auteur || c.auteur === state.auteur) &&
        (!q || [c.texte, c.extrait, c.element, c.auteur].join(' ').toLowerCase().indexOf(q) >= 0);
    });
  }

  function options(sel, values, label, fmt) {
    var cur = sel.value; sel.textContent = '';
    sel.appendChild(h('option', { value: '', text: label }));
    values.forEach(function (v) { sel.appendChild(h('option', { value: v, text: fmt ? fmt(v) : v })); });
    sel.value = values.indexOf(cur) >= 0 ? cur : '';
  }

  function render() {
    var versions = Array.from(new Set(all.map(function (c) { return c.version; }))).sort(function (a, b) { return vorder(a) - vorder(b); });
    var auteurs = Array.from(new Set(all.map(function (c) { return c.auteur; }).filter(Boolean))).sort();
    options($('#f-version'), versions, 'Toutes les versions', vname);
    options($('#f-auteur'), auteurs, 'Tous les frères');

    // bilan par version
    var sum = $('#summary'); sum.textContent = '';
    if (all.length) {
      var tb = h('tbody');
      cfg.order.concat(versions.filter(function (v) { return cfg.order.indexOf(v) < 0; })).forEach(function (v) {
        var L = all.filter(function (c) { return c.version === v; });
        var c = counts(L);
        tb.appendChild(h('tr', { class: L.length ? '' : 'none' }, [
          h('th', { scope: 'row' }, [L.length ? h('a', { href: '#v-' + v, text: vname(v) }) : vname(v)]),
          h('td', { text: String(c.like) }), h('td', { text: String(c.dislike) }), h('td', { text: String(c.note) }),
          h('td', { text: String(L.length) }),
          h('td', { text: Array.from(new Set(L.map(function (x) { return x.auteur; }))).join(', ') })
        ]));
      });
      sum.appendChild(h('table', {}, [h('thead', {}, [h('tr', {}, [h('th', { text: 'Version' }), h('th', { text: '👍' }), h('th', { text: '👎' }), h('th', { text: '💬' }), h('th', { text: 'Total' }), h('th', { text: 'Frères' })])]), tb]));
    }

    // détail : version > page > remarques
    var list = filtered(), out = $('#list'); out.textContent = '';
    $('#count').textContent = list.length + ' remarque' + (list.length > 1 ? 's' : '') + (list.length !== all.length ? ' (sur ' + all.length + ')' : '');
    if (!list.length) { out.appendChild(h('p', { class: 'empty', text: all.length ? 'Aucune remarque ne correspond à ces filtres.' : 'Aucune remarque pour l’instant.' })); return; }
    var byV = {};
    list.forEach(function (c) { (byV[c.version] = byV[c.version] || []).push(c); });
    Object.keys(byV).sort(function (a, b) { return vorder(a) - vorder(b); }).forEach(function (v) {
      var sec = h('section', { class: 'version', id: 'v-' + v }, [h('h2', {}, [vname(v), tally(byV[v])])]);
      var byP = {};
      byV[v].forEach(function (c) { (byP[c.page] = byP[c.page] || []).push(c); });
      Object.keys(byP).sort(function (a, b) { return porder(a) - porder(b); }).forEach(function (p) {
        var href = (v === 'choix' ? '' : v + '/') + p;
        sec.appendChild(h('h3', {}, [h('a', { href: href, target: '_blank', rel: 'noopener', text: pname(p) }), tally(byP[p])]));
        var ol = h('ol', { class: 'items' });
        byP[p].sort(function (a, b) { return String(a.date).localeCompare(String(b.date)); }).forEach(function (c) {
          ol.appendChild(h('li', { class: 'it ' + c.verdict }, [
            h('div', { class: 'ih' }, [
              h('span', { class: 'verdict', text: (ICON[c.verdict] || '') + ' ' + (VERB[c.verdict] || '') }),
              h('span', { class: 'who', text: c.auteur || 'anonyme' }),
              h('span', { class: 'when', text: when(c.date) + (c.ecran ? ' · ' + c.ecran : '') })
            ]),
            h('div', { class: 'el', text: c.element + (c.extrait ? ' — « ' + c.extrait + ' »' : '') }),
            c.texte ? h('p', { class: 'txt', text: c.texte }) : null,
            h('a', { class: 'see', href: href + '#rv=' + c.id, target: '_blank', rel: 'noopener', text: 'Voir sur la page →' })
          ]));
        });
        sec.appendChild(ol);
      });
      out.appendChild(sec);
    });
  }

  function csv() {
    var cols = ['version', 'page', 'element', 'extrait', 'verdict', 'texte', 'auteur', 'date', 'ecran'];
    var esc = function (v) { v = v == null ? '' : String(v); return /[";\n]/.test(v) ? '"' + v.replace(/"/g, '""') + '"' : v; };
    var rows = [cols.join(';')].concat(filtered().map(function (c) {
      return cols.map(function (k) { return esc(k === 'version' ? vname(c.version) : k === 'page' ? pname(c.page) : k === 'verdict' ? VERB[c.verdict] : c[k]); }).join(';');
    }));
    var url = URL.createObjectURL(new Blob(['﻿' + rows.join('\r\n')], { type: 'text/csv;charset=utf-8' }));
    var a = h('a', { href: url, download: 'remarques-sept-fons.csv' }); document.body.appendChild(a); a.click(); a.remove();
    setTimeout(function () { URL.revokeObjectURL(url); }, 4000);
  }

  $('#f-version').addEventListener('change', function (e) { state.version = e.target.value; render(); });
  $('#f-verdict').addEventListener('change', function (e) { state.verdict = e.target.value; render(); });
  $('#f-auteur').addEventListener('change', function (e) { state.auteur = e.target.value; render(); });
  $('#f-q').addEventListener('input', function (e) { state.q = e.target.value.trim(); render(); });
  $('#refresh').addEventListener('click', load);
  $('#csv').addEventListener('click', csv);
  load();
  setInterval(function () { if (!document.hidden && ENDPOINT) load(); }, 60000);
})();
