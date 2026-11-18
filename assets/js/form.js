/* Formulaire « Nous écrire » : rédige le message automatiquement à partir de quelques champs.
   ENVOI : si FORM_ENDPOINT est renseigné (ex. un formulaire Formspree, ou un script PHP chez l'hébergeur),
   le message part directement depuis le site. Sinon, la messagerie du visiteur s'ouvre avec le message prêt. */
(function () {
  var FORM_ENDPOINT = '';            // ex. 'https://formspree.io/f/xxxxxxx' — à configurer avec les frères
  var RECIPIENTS = {                 // adresses à confirmer avec les frères
    question: { label: 'La communauté', email: 'abbaye@septfons.com' },
    sejour:   { label: 'Le Père Hôtelier', email: 'abbaye@septfons.com' },
    commande: { label: 'Moulin de la Trappe — commandes', email: 'abbaye@septfons.com' }
  };

  var form = document.getElementById('smart-form');
  if (!form) return;
  var $ = function (s) { return form.querySelector(s); };
  var msg = $('[data-message]'), subj = $('[data-subject]'), resetBtn = $('[data-reset]');
  var errorsEl = $('[data-errors]'), statusEl = $('[data-status]'), toEl = $('[data-to]');
  var edited = false;

  function val(n) { var el = form.elements[n]; return el ? String(el.value || '').trim() : ''; }
  function objet() { return form.querySelector('input[name=objet]:checked').value; }
  function fmtDate(v) {
    if (!v) return '';
    var d = new Date(v + 'T12:00:00');
    return d.toLocaleDateString('fr-FR', { weekday: 'long', day: 'numeric', month: 'long', year: 'numeric' });
  }
  function nights(a, b) {
    if (!a || !b) return 0;
    return Math.round((new Date(b + 'T12:00:00') - new Date(a + 'T12:00:00')) / 86400000);
  }
  function signature() {
    var who = [val('prenom'), val('nom')].filter(Boolean).join(' ');
    return [who, val('tel') ? 'Tél. : ' + val('tel') : '', val('email')].filter(Boolean).join('\n');
  }

  function compose() {
    var o = objet(), lines = [], subject = '';
    if (o === 'question') {
      var s = val('situation');
      subject = 'Une question sur la vie monastique';
      lines.push('Bonjour,', '');
      if (s === 'questions') lines.push('Je me pose des questions sur la vie monastique et sur un possible appel de Dieu, et je me permets de vous écrire pour vous dire simplement où j’en suis.');
      if (s === 'rencontre') lines.push('Je m’interroge sur la vie monastique et j’aimerais, si c’est possible, pouvoir en parler avec un frère.');
      if (s === 'decouvrir') { subject = 'Venir découvrir la vie de la communauté'; lines.push('Je m’interroge sur la vie monastique et j’aimerais venir quelques jours à Sept-Fons pour découvrir la vie de la communauté.'); }
      if (val('age')) lines.push('', 'J’ai ' + val('age') + ' ans.');
      if (val('question')) lines.push('', val('question'));
      if (val('langue') && val('langue') !== 'Français') lines.push('', 'Si possible, je préférerais une réponse en ' + val('langue') + '.');
      lines.push('', 'Je vous remercie par avance de votre réponse.');
    }
    if (o === 'sejour') {
      var a = val('arrivee'), b = val('depart'), n = nights(a, b), p = parseInt(val('personnes') || '1', 10);
      var types = { retraite: 'faire une retraite', premiere: 'faire un premier séjour', groupe: 'faire un séjour en groupe', jeunes: 'venir avec un groupe de jeunes' };
      subject = 'Demande de séjour à l’hôtellerie' + (a ? ' — ' + new Date(a + 'T12:00:00').toLocaleDateString('fr-FR', { day: 'numeric', month: 'long' }) : '');
      lines.push('Bonjour mon Père,', '');
      lines.push('J’aimerais ' + (types[val('type_sejour')] || 'faire une retraite') + ' à l’abbaye de Sept-Fons.');
      if (a && b) lines.push('Serait-il possible de venir du ' + fmtDate(a) + ' au ' + fmtDate(b) + (n > 0 ? ' (' + n + ' nuit' + (n > 1 ? 's' : '') + ')' : '') + (p > 1 ? ', pour ' + p + ' personnes' : '') + ' ?');
      else lines.push('Serait-il possible de venir du … au … ?');
      if (form.elements.vocation.checked) lines.push('', 'Je m’interroge sur la vie monastique et j’aimerais, si c’est possible, pouvoir parler avec un frère pendant mon séjour.');
      if (val('precisions')) lines.push('', val('precisions'));
      lines.push('', 'Je vous remercie par avance de votre réponse.');
    }
    if (o === 'commande') {
      subject = 'Commande';
      lines.push('Bonjour,', '', 'Je souhaiterais passer la commande suivante :');
      var rows = form.querySelectorAll('[data-lines] .line'), any = false;
      rows.forEach(function (r) {
        var prod = r.querySelector('[name=produit]').value.trim(), q = r.querySelector('[name=quantite]').value || '1';
        if (prod) { any = true; lines.push('– ' + q + ' × ' + prod); }
      });
      if (!any) lines.push('– …');
      if (val('adresse')) lines.push('', 'À livrer à l’adresse suivante :', val('adresse'));
      lines.push('', 'Pourriez-vous m’indiquer le montant total, frais de port compris, ainsi que les modalités de règlement ?', '', 'Je vous remercie par avance.');
    }
    lines.push('', 'Bien cordialement,', signature());
    return { subject: subject, body: lines.join('\n') };
  }

  function refresh() {
    var o = objet();
    form.querySelectorAll('.grp').forEach(function (g) {
      var on = g.getAttribute('data-for') === o;
      g.hidden = !on;
      g.querySelectorAll('input,select,textarea').forEach(function (el) { el.disabled = !on; });
    });
    toEl.textContent = RECIPIENTS[o].label;
    if (!edited) { var c = compose(); msg.value = c.body; subj.value = c.subject; }
  }

  /* Dates : pas avant aujourd'hui, départ après l'arrivée */
  var today = new Date(); today.setMinutes(today.getMinutes() - today.getTimezoneOffset());
  var iso = today.toISOString().slice(0, 10);
  form.elements.arrivee.min = iso; form.elements.depart.min = iso;
  form.elements.arrivee.addEventListener('change', function () {
    var a = form.elements.arrivee.value; form.elements.depart.min = a || iso;
    if (a && (!form.elements.depart.value || form.elements.depart.value <= a)) {
      var d = new Date(a + 'T12:00:00'); d.setDate(d.getDate() + 3); form.elements.depart.value = d.toISOString().slice(0, 10);
    }
  });

  form.addEventListener('input', function (e) { if (e.target === msg || e.target === subj) { edited = true; resetBtn.hidden = false; return; } refresh(); });
  form.addEventListener('change', function (e) { if (e.target !== msg && e.target !== subj) refresh(); });
  resetBtn.addEventListener('click', function () { edited = false; resetBtn.hidden = true; refresh(); });

  form.querySelector('[data-add-line]').addEventListener('click', function () {
    var box = form.querySelector('[data-lines]'), line = box.querySelector('.line').cloneNode(true);
    line.querySelectorAll('input').forEach(function (i) { i.value = i.type === 'number' ? '1' : ''; });
    box.appendChild(line); line.querySelector('input').focus(); refresh();
  });

  /* Objet pré-sélectionné par l'adresse : ecrire.html?objet=sejour */
  var q = new URLSearchParams(location.search).get('objet');
  if (q && RECIPIENTS[q]) form.querySelector('input[name=objet][value=' + q + ']').checked = true;
  refresh();

  function validate() {
    var o = objet(), errs = [];
    if (!val('prenom') || !val('nom')) errs.push('Indiquez votre prénom et votre nom.');
    if (!val('tel')) errs.push('Indiquez votre numéro de téléphone.');
    if (!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(val('email'))) errs.push('Indiquez une adresse e-mail valide.');
    if (o === 'sejour') {
      if (!val('arrivee') || !val('depart')) errs.push('Choisissez vos dates d’arrivée et de départ.');
      else if (nights(val('arrivee'), val('depart')) < 1) errs.push('La date de départ doit suivre la date d’arrivée.');
    }
    if (o === 'commande') {
      var any = Array.prototype.some.call(form.querySelectorAll('[name=produit]'), function (i) { return i.value.trim(); });
      if (!any) errs.push('Indiquez au moins un produit.');
      if (!val('adresse')) errs.push('Indiquez l’adresse de livraison.');
    }
    return errs;
  }

  form.addEventListener('submit', function (e) {
    e.preventDefault();
    var errs = validate();
    errorsEl.innerHTML = errs.map(function (x) { return '<span>' + x + '</span>'; }).join('');
    if (errs.length) return;
    var o = objet(), r = RECIPIENTS[o];
    if (FORM_ENDPOINT) {
      statusEl.textContent = 'Envoi en cours…';
      fetch(FORM_ENDPOINT, {
        method: 'POST', headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
        body: JSON.stringify({ objet: o, destinataire: r.email, _subject: subj.value, message: msg.value,
          nom: val('prenom') + ' ' + val('nom'), telephone: val('tel'), email: val('email') })
      }).then(function (res) {
        if (!res.ok) throw new Error();
        form.reset(); edited = false; refresh();
        statusEl.textContent = 'Merci, votre message a bien été envoyé. Nous vous répondrons dès que possible.';
      }).catch(function () { statusEl.textContent = 'L’envoi n’a pas abouti. Vous pouvez réessayer ou nous téléphoner au 04 70 48 14 90.'; });
    } else {
      location.href = 'mailto:' + r.email + '?subject=' + encodeURIComponent(subj.value) + '&body=' + encodeURIComponent(msg.value);
      statusEl.textContent = 'Votre messagerie s’ouvre avec le message prêt à envoyer.';
    }
  });
})();
