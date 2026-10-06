(function () {
  'use strict';
  var doc = document;

  /* ---------- in-page anchors: jump to whichever layout is showing ---------- */
  function visible(el) { return el && el.offsetParent !== null; }
  function findTarget(id) {
    if (!id) return null;
    var a = doc.getElementById(id), b = doc.getElementById('m-' + id), c = id.indexOf('m-') === 0 ? doc.getElementById(id.slice(2)) : null;
    return [a, b, c].filter(visible)[0] || null;
  }
  function jump(id, smooth) {
    var t = findTarget(id);
    if (!t) return false;
    t.scrollIntoView({ behavior: smooth ? 'smooth' : 'auto', block: 'start' });
    return true;
  }
  doc.addEventListener('click', function (e) {
    var a = e.target.closest('a[href]');
    if (!a) return;
    var href = a.getAttribute('href');
    var here = location.pathname.split('/').pop() || 'index.html';
    var m = href.match(/^([^#]*)#(.+)$/);
    if (!m) return;
    if (m[1] && m[1] !== here) return;
    if (jump(m[2], true)) { e.preventDefault(); closeMenu(); history.replaceState(null, '', '#' + m[2].replace(/^m-/, '')); }
  });
  window.addEventListener('load', function () { if (location.hash) setTimeout(function () { jump(location.hash.slice(1), false); }, 60); });

  /* ---------- mobile menu ---------- */
  var menu = doc.getElementById('menu');
  var page = doc.body.getAttribute('data-page');
  var pageFile = { index: 'index.html', services: 'services.html', resources: 'resources.html', contact: 'contact.html' }[page];
  if (pageFile) menu.querySelectorAll('.menu-nav a').forEach(function (a) { if (a.getAttribute('href') === pageFile) a.setAttribute('aria-current', 'page'); });
  function openMenu() { menu.hidden = false; doc.body.style.overflow = 'hidden'; menu.querySelector('.menu-close').focus(); }
  function closeMenu() { if (!menu.hidden) { menu.hidden = true; doc.body.style.overflow = ''; } }
  doc.querySelectorAll('[aria-label="Open menu"]').forEach(function (b) { b.addEventListener('click', openMenu); });
  menu.querySelector('.menu-close').addEventListener('click', closeMenu);
  menu.addEventListener('click', function (e) { if (e.target.closest('a')) closeMenu(); });
  doc.addEventListener('keydown', function (e) { if (e.key === 'Escape') closeMenu(); });

  /* ---------- testimonials, chips and scales ---------- */
  doc.addEventListener('click', function (e) {
    var b = e.target.closest('[data-on]');
    if (!b) return;
    var v = b.getAttribute('data-on').split(':');
    if (v[0] === 'prev' || v[0] === 'next' || v[0] === 'go') return slide(b, v);
    if (v[0] === 'chip') return chip(b, v[1], v[2] === 'm', v.slice(3).join(':'));
    if (v[0] === 'scale') return scale(b, v[1], +v[2]);
  });

  function slide(btn, v) {
    var sec = btn.closest('section');
    var slides = sec.querySelectorAll('.tslide'), dots = sec.querySelectorAll('[data-on^="go:"]');
    var cur = 0;
    slides.forEach(function (s, i) { if (!s.hidden) cur = i; });
    var n = slides.length, next = v[0] === 'go' ? +v[1] : (cur + (v[0] === 'next' ? 1 : -1) + n) % n;
    slides.forEach(function (s, i) {
      s.hidden = i !== next;
      if (i === next) { var f = s.querySelector('.t-fade'); if (f) { f.style.animation = 'none'; void f.offsetWidth; f.style.animation = ''; } }
    });
    dots.forEach(function (d, i) { var bar = d.firstElementChild; bar.style.width = (i === next ? 28 : 10) + 'px'; bar.style.background = i === next ? '#8E2A26' : '#CFC7BC'; d.setAttribute('aria-current', i === next ? 'true' : 'false'); });
  }

  function hidden(btn, name) {
    var box = btn.parentNode;
    var h = box.querySelector('input[type=hidden][name="' + name + '"]');
    if (!h) { h = doc.createElement('input'); h.type = 'hidden'; h.name = name; box.appendChild(h); }
    return h;
  }
  var LIMITS = { traits: 5 };
  var EXCLUSIVE = { 'Nothing planned': 1, 'Not sure': 1 };
  function paintChip(b, on) {
    b.setAttribute('aria-pressed', on ? 'true' : 'false');
    b.style.background = on ? '#1E1E1E' : '#ffffff'; b.style.color = on ? '#ffffff' : '#1E1E1E'; b.style.borderColor = on ? '#1E1E1E' : '#CFC7BC';
  }
  function chip(b, key, multi, opt) {
    var form = b.closest('form');
    var all = form.querySelectorAll('[data-on^="chip:' + key + ':"]');
    var on = b.getAttribute('aria-pressed') === 'true';
    if (!multi) all.forEach(function (o) { paintChip(o, false); });
    else if (!on && LIMITS[key]) {
      var count = 0; all.forEach(function (o) { if (o.getAttribute('aria-pressed') === 'true') count++; });
      if (count >= LIMITS[key]) return;
    }
    paintChip(b, !on);
    // "Nothing planned" / "Not sure" can't be combined with other answers
    if (multi && !on) {
      var excl = EXCLUSIVE[b.textContent.trim()];
      all.forEach(function (o) { if (o !== b && (excl || EXCLUSIVE[o.textContent.trim()])) paintChip(o, false); });
    }
    var vals = []; all.forEach(function (o) { if (o.getAttribute('aria-pressed') === 'true') vals.push(o.textContent.trim()); });
    hidden(b, key).value = vals.join(', ');
  }
  function scale(b, key, n) {
    var form = b.closest('form');
    form.querySelectorAll('[data-on^="scale:' + key + ':"]').forEach(function (o, i) {
      var on = i + 1 === n;
      o.setAttribute('aria-pressed', on ? 'true' : 'false');
      o.style.background = on ? '#A42C35' : '#ffffff'; o.style.color = on ? '#ffffff' : '#1E1E1E'; o.style.borderColor = on ? '#A42C35' : '#E4DED5';
    });
    hidden(b, key).value = String(n);
  }

  /* ---------- forms ---------- */
  var KINDS = {
    'Request portfolio access': { kind: 'portfolio', ok: 'Thank you. Your request is with me, and your private portfolio link will follow shortly.' },
    'Get the guide': { kind: 'guide', ok: 'Thank you. I’ll send the guide to your inbox shortly.' },
    'Send a message': { kind: 'message', ok: 'Thank you. Your message is with me, and I’ll be in touch soon.' },
    'Discovery brief': { kind: 'discovery', next: 'thanks.html' }
  };
  function collect(form) {
    var data = {};
    form.querySelectorAll('input[name], textarea[name]').forEach(function (f) {
      var v = f.type === 'checkbox' ? (f.checked ? 'yes' : 'no') : f.value.trim();
      if (data[f.name] && v) data[f.name] += ' | ' + v; else if (!data[f.name]) data[f.name] = v;
    });
    return data;
  }
  function message(form, btn, text, cls) {
    var m = form.querySelector('.form-msg');
    if (!m) { m = doc.createElement('p'); m.className = 'form-msg'; m.setAttribute('role', 'status'); btn.parentNode.insertBefore(m, btn.nextSibling); }
    m.className = 'form-msg ' + (cls || ''); m.textContent = text;
    return m;
  }
  doc.querySelectorAll('form').forEach(function (form) {
    var cfg = KINDS[form.getAttribute('aria-label')];
    if (!cfg) return;
    form.setAttribute('novalidate', '');
    var btn = Array.prototype.filter.call(form.querySelectorAll('button[type=button]'), function (b) { return !b.hasAttribute('data-on') && !b.getAttribute('aria-label'); }).pop();
    if (!btn) return;
    function submit(e) {
      if (e) e.preventDefault();
      var data = collect(form), bad = [];
      form.querySelectorAll('.field-err').forEach(function (f) { f.classList.remove('field-err'); });
      ['name', 'email'].forEach(function (k) {
        var f = form.querySelector('[name="' + k + '"]');
        var okv = k === 'email' ? /^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(data[k] || '') : !!data[k];
        if (f && !okv) { f.classList.add('field-err'); bad.push(f); }
      });
      if (bad.length) { message(form, btn, bad.length === 1 && bad[0].name === 'email' ? 'Please enter a valid email address.' : 'Please add your name and a valid email address.', 'err'); bad[0].focus(); return; }
      btn.disabled = true; btn.style.opacity = '0.6';
      var send = window.ppSubmit ? window.ppSubmit(cfg.kind, data, form) : Promise.resolve();
      send.then(function () {
        if (cfg.next) { location.href = cfg.next; return; }
        btn.style.display = 'none';
        var m = message(form, btn, cfg.ok, 'form-ok');
        form.querySelectorAll('input:not([type=hidden]), textarea').forEach(function (f) { if (f.type === 'checkbox') f.checked = false; else f.value = ''; });
        m.focus && m.setAttribute('tabindex', '-1');
      }).catch(function () {
        btn.disabled = false; btn.style.opacity = '';
        message(form, btn, 'Sorry, something went wrong. Please try again, or email paulpacey@gmail.com.', 'err');
      });
    }
    btn.addEventListener('click', submit);
    form.addEventListener('submit', submit);
  });
})();
