/**
 * Remarques des frères sur les maquettes du site de Sept-Fons.
 * À coller dans le Google Sheet : Extensions > Apps Script, puis Déployer > Nouveau déploiement > Application Web
 * (Exécuter en tant que : moi ; Qui a accès : Tout le monde).
 * Chaque remarque est une ligne de l'onglet « Remarques ». Une remarque supprimée garde sa ligne (colonne « supprime »).
 */
var SHEET = 'Remarques';
var COLS = ['id', 'date', 'modifie', 'auteur', 'version', 'page', 'element', 'extrait', 'verdict', 'texte',
            'ecran', 'largeur', 'image', 'selecteur', 'path', 'titre_page', 'supprime'];

function sheet_() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var sh = ss.getSheetByName(SHEET);
  if (!sh) {
    sh = ss.insertSheet(SHEET);
    sh.appendRow(COLS);
    sh.setFrozenRows(1);
    sh.getRange(1, 1, 1, COLS.length).setFontWeight('bold');
  }
  return sh;
}

function out_(o) {
  return ContentService.createTextOutput(JSON.stringify(o)).setMimeType(ContentService.MimeType.JSON);
}

/* Empêche qu'un texte soit interprété comme une formule, et limite la longueur. */
function clean_(v) {
  if (v === undefined || v === null) return '';
  if (typeof v === 'number') return v;
  var s = String(v).slice(0, 3000);
  return /^[=+\-@]/.test(s) ? "'" + s : s;
}

function rows_(sh) {
  var v = sh.getDataRange().getDisplayValues();
  var head = v.shift();
  return v.map(function (r) {
    var o = {};
    head.forEach(function (k, i) { o[k] = r[i]; });
    return o;
  });
}

function doGet() {
  var items = rows_(sheet_()).filter(function (o) { return o.id && !o.supprime; });
  items.forEach(function (o) {
    o.largeur = Number(o.largeur) || 0;
    if (o.texte && o.texte.charAt(0) === "'") o.texte = o.texte.slice(1);
  });
  return out_({ ok: true, items: items });
}

function doPost(e) {
  var lock = LockService.getScriptLock();
  lock.waitLock(15000);
  try {
    var d = JSON.parse(e.postData.contents);
    var sh = sheet_();
    var n = Math.max(sh.getLastRow() - 1, 0);
    var ids = n ? sh.getRange(2, 1, n, 1).getDisplayValues().map(function (r) { return r[0]; }) : [];
    var id = String((d.item && d.item.id) || d.id || '');
    if (!id) return out_({ ok: false, error: 'id manquant' });
    var row = ids.indexOf(id) + 2;            // 1 si absent
    var col = function (k) { return COLS.indexOf(k) + 1; };

    if (d.op === 'add') {
      if (row < 2) sh.appendRow(COLS.map(function (k) { return k === 'supprime' ? '' : clean_(d.item[k]); }));
    } else if (d.op === 'update' && row >= 2) {
      sh.getRange(row, col('verdict')).setValue(clean_(d.verdict));
      sh.getRange(row, col('texte')).setValue(clean_(d.texte));
      sh.getRange(row, col('modifie')).setValue(new Date().toISOString());
    } else if (d.op === 'delete' && row >= 2) {
      sh.getRange(row, col('supprime')).setValue(new Date().toISOString());
    }
    return out_({ ok: true });
  } catch (err) {
    return out_({ ok: false, error: String(err) });
  } finally {
    lock.releaseLock();
  }
}
