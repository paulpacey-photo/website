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
    syncOther(form, key);
    hidden(b, key).value = vals.join(', ');
  }
  // "Something else" fields are hidden until that option is selected
  function syncOther(form, key) {
    var on = false;
    form.querySelectorAll('[data-on^="chip:' + key + ':"]').forEach(function (o) {
      if (o.textContent.trim() === 'Something else' && o.getAttribute('aria-pressed') === 'true') on = true;
    });
    form.querySelectorAll('[data-other="' + key + '"]').forEach(function (inp) {
      var was = !inp.hidden;
      inp.hidden = !on;
      if (!on) inp.value = '';
      else if (!was) inp.focus();
    });
  }
  doc.querySelectorAll('[data-other]').forEach(function (inp) { inp.hidden = true; });
  function scale(b, key, n) {
    var form = b.closest('form');
    form.querySelectorAll('[data-on^="scale:' + key + ':"]').forEach(function (o, i) {
      var on = i + 1 === n;
      o.setAttribute('aria-pressed', on ? 'true' : 'false');
      o.style.background = on ? '#A42C35' : '#ffffff'; o.style.color = on ? '#ffffff' : '#1E1E1E'; o.style.borderColor = on ? '#A42C35' : '#E4DED5';
    });
    hidden(b, key).value = String(n);
  }

  /* ---------- article effects: reveal, parallax, reading progress ---------- */
  if (doc.documentElement.classList.contains('fx')) {
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } });
    }, { rootMargin: '0px 0px -12% 0px', threshold: 0.12 });
    doc.querySelectorAll('[data-reveal]').forEach(function (el) { io.observe(el); });
    var layers = Array.prototype.slice.call(doc.querySelectorAll('[data-parallax]'));
    var bar = null;
    if (doc.querySelector('[data-article]')) { bar = doc.createElement('div'); bar.className = 'read-progress'; doc.body.appendChild(bar); }
    var ticking = false;
    function frame() {
      ticking = false;
      var vh = window.innerHeight;
      layers.forEach(function (box) {
        var r = box.getBoundingClientRect();
        if (!r.height || r.bottom < -200 || r.top > vh + 200) return;
        var k = parseFloat(box.getAttribute('data-parallax')) || 0.2;
        var z = parseFloat(getComputedStyle(doc.documentElement).getPropertyValue('--z')) || 1;
        var off = ((r.top + r.height / 2) - vh / 2) * -k / z;
        var l = box.querySelector('[data-parallax-layer]');
        if (l) l.style.transform = 'translate3d(0,' + off.toFixed(1) + 'px,0)';
      });
      if (bar) {
        var h = doc.documentElement.scrollHeight - vh;
        bar.style.transform = 'scaleX(' + (h > 0 ? Math.min(1, window.scrollY / h) : 0) + ')';
      }
    }
    function onScroll() { if (!ticking) { ticking = true; requestAnimationFrame(frame); } }
    window.addEventListener('scroll', onScroll, { passive: true });
    window.addEventListener('resize', onScroll);
    frame();
  }

  /* ---------- image upload (Discovery brief, question 14) ---------- */
  var MAX_FILES = 10, MAX_MB = 10, OK_TYPES = ['image/jpeg', 'image/png', 'image/webp'];
  Array.prototype.forEach.call(doc.querySelectorAll('form span'), function (sp) {
    if (sp.firstChild && sp.firstChild.nodeType === 3 && sp.firstChild.nodeValue.indexOf('Drop images here') === 0) setupUpload(sp.parentNode);
  });
  function setupUpload(box) {
    var form = box.closest('form');
    form._ppFiles = form._ppFiles || [];
    var input = doc.createElement('input');
    input.type = 'file'; input.multiple = true; input.accept = 'image/jpeg,image/png,image/webp'; input.hidden = true;
    box.appendChild(input);
    var store = doc.createElement('input'); store.type = 'hidden'; store.name = 'images'; box.parentNode.appendChild(store);
    var list = doc.createElement('ul'); list.className = 'up-list'; box.parentNode.insertBefore(list, box.nextSibling);
    var note = doc.createElement('p'); note.className = 'up-note'; note.setAttribute('role', 'status'); list.parentNode.insertBefore(note, list.nextSibling);
    box.setAttribute('role', 'button'); box.setAttribute('tabindex', '0'); box.setAttribute('aria-label', 'Add images, optional. JPG or PNG, up to 10 files');
    box.classList.add('up-box');
    box.addEventListener('click', function (e) { if (e.target !== input) input.click(); });
    box.addEventListener('keydown', function (e) { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); input.click(); } });
    ['dragenter', 'dragover'].forEach(function (t) { box.addEventListener(t, function (e) { e.preventDefault(); box.classList.add('up-over'); }); });
    ['dragleave', 'drop'].forEach(function (t) { box.addEventListener(t, function (e) { e.preventDefault(); box.classList.remove('up-over'); }); });
    box.addEventListener('drop', function (e) { add(e.dataTransfer.files); });
    input.addEventListener('change', function () { add(input.files); input.value = ''; });
    function add(files) {
      var skipped = [];
      Array.prototype.forEach.call(files, function (f) {
        if (OK_TYPES.indexOf(f.type) < 0) skipped.push(f.name + ' (not a JPG or PNG)');
        else if (f.size > MAX_MB * 1024 * 1024) skipped.push(f.name + ' (over ' + MAX_MB + ' MB)');
        else if (form._ppFiles.length >= MAX_FILES) skipped.push(f.name + ' (limit of ' + MAX_FILES + ' files)');
        else form._ppFiles.push(f);
      });
      note.textContent = skipped.length ? 'Not added: ' + skipped.join(', ') + '.' : '';
      render();
    }
    function render() {
      list.innerHTML = '';
      form._ppFiles.forEach(function (f, i) {
        var li = doc.createElement('li');
        var name = doc.createElement('span'); name.textContent = f.name;
        var rm = doc.createElement('button'); rm.type = 'button'; rm.className = 'up-rm'; rm.textContent = '×';
        rm.setAttribute('aria-label', 'Remove ' + f.name);
        rm.addEventListener('click', function () { form._ppFiles.splice(i, 1); note.textContent = ''; render(); });
        li.appendChild(name); li.appendChild(rm); list.appendChild(li);
      });
    }
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
      if (form._ppFiles && form._ppFiles.length) message(form, btn, 'Uploading your images…', '');
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

/* ---------- landing page: 3D word cloud (replaces the flat image when motion is welcome) ---------- */
(function () {
  var imgs = document.querySelectorAll('img[data-cloud3d]');
  if (!imgs.length) return;
  var ok = !(window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches) &&
    window.CSS && CSS.supports('transform-style', 'preserve-3d') && CSS.supports('mix-blend-mode', 'multiply');
  if (!ok) return;   // the original flat image stays

  // Bubbles measured from the original artwork on a 1000-unit grid. d = depth (0 front … 1 back), o = opacity.
  var B = [
    {t:'Global<br>Citizen', x:640,y:150,w:380,h:320,s:180,d:1.00,c:'#cfdbe0',o:.55,tail:'tr'},
    {t:'Community',         x:270,y:760,w:690,h:230,s:180,d:0.95,c:'#e6dccd',o:.6, tail:'tl'},
    {t:'Innovative',        x:560,y:590,w:430,h:115,s:122,d:0.92,c:'#c9d0d8',o:.55,tail:'tr'},
    {t:'Individual<br>Approach',x:20,y:455,w:285,h:185,s:74,d:0.88,c:'#e2c9be',o:.65,tail:'tl'},
    {t:'Limitless',         x:40, y:245,w:200,h:100,s:76, d:0.55,c:'#8ea6b5',o:.92,tail:'tl'},
    {t:'Lifelong',          x:160,y:320,w:215,h:125,s:96, d:0.5, c:'#c9ad86',o:.92,tail:'tr'},
    {t:'Full<br>Potential', x:170,y:25, w:175,h:180,s:66, d:0.45,c:'#5f5664',o:.9, tail:'tl'},
    {t:'Unique',            x:485,y:5,  w:165,h:115,s:86, d:0.45,c:'#7a9fb2',o:.92,tail:'tl'},
    {t:'Caring',            x:290,y:510,w:265,h:180,s:140,d:0.35,c:'#7e9eae',o:.9, tail:'tl'},
    {t:'Diverse',           x:400,y:340,w:215,h:140,s:96, d:0.3, c:'#5a2832',o:.92,tail:'tl'},
    {t:'Rigorous',          x:55, y:695,w:275,h:180,s:122,d:0.18,c:'#3c5f79',o:.92,tail:'tr'},
    {t:'Whole<br>Child',    x:700,y:-10,w:300,h:260,s:124,d:0.15,c:'#5a2b33',o:.95,tail:'tr'},
    {t:'Empowered',         x:585,y:440,w:415,h:160,s:124,d:0.12,c:'#2c4b66',o:.93,tail:'tr'},
    {t:'Inclusive',         x:315,y:120,w:360,h:220,s:176,d:0.08,c:'#a8303b',o:.93,tail:'tr'},
    {t:'Holistic',          x:515,y:640,w:455,h:260,s:204,d:0.0, c:'#a3232d',o:.95,tail:'tr'}
  ];
  // Ghost words: faint white words on their own plane, visible only where they pass over colour
  var G = [
    {t:'Inclusive Global',x:300,y:130,s:150},{t:'Diverse',x:330,y:300,s:110},{t:'Lifelong',x:150,y:300,s:80},
    {t:'Empowered',x:600,y:400,s:120},{t:'Caring',x:230,y:500,s:120},{t:'Holistic',x:520,y:600,s:150},
    {t:'Rigorous',x:40,y:690,s:110},{t:'Innovative',x:500,y:540,s:110},{t:'Community',x:250,y:720,s:150},
    {t:'Individual',x:20,y:430,s:90},{t:'Leadership',x:650,y:20,s:120},{t:'Potential',x:150,y:40,s:70}
  ];
  // Paul's settings: front words slower, depth 95%, tilt 19°, ghost words 19%, soft focus off
  var ST = {sign: 1, depth: .95, tilt: 19, ghost: .19};
  var P = 1500, OX = 250, OY = 500;

  function build(img) {
    var mode = img.getAttribute('data-cloud3d');          // 'd' desktop (wide artwork) or 'm' phone (square crop)
    var wrap = document.createElement('div');
    wrap.className = img.className + ' cloud3d';
    img.parentNode.insertBefore(wrap, img); wrap.appendChild(img);
    img.className = 'cloud3d-flat';
    wrap.setAttribute('role', 'img'); wrap.setAttribute('aria-label', img.alt);
    var stage = document.createElement('div'); stage.className = 'cloud3d-stage'; stage.setAttribute('aria-hidden', 'true');
    wrap.appendChild(stage);
    var bEls = [], lEls = [], gEls = [];
    B.forEach(function (b, i) {
      var e = document.createElement('div'); e.className = 'c3-bub ' + b.tail;
      e.style.cssText = 'width:' + b.w + 'px;height:' + b.h + 'px;z-index:' + (10 + 2 * i) + ';opacity:' + b.o + ';--c:' + b.c;
      e.innerHTML = '<div class="c3-box"></div>'; stage.appendChild(e); bEls.push(e);
      var l = document.createElement('div'); l.className = 'c3-lab';
      l.style.cssText = 'width:' + b.w + 'px;height:' + b.h + 'px;z-index:' + (11 + 2 * i) + (b.d > 0.8 ? ';opacity:.85' : '');
      l.innerHTML = '<div class="c3-w" style="font-size:' + b.s + 'px">' + b.t + '</div>'; stage.appendChild(l); lEls.push(l);
    });
    G.forEach(function (g) {
      var e = document.createElement('div'); e.className = 'c3-ghost'; e.style.cssText = 'font-size:' + g.s + 'px;opacity:' + ST.ghost;
      e.textContent = g.t; stage.appendChild(e); gEls.push(e);
    });
    var E = {depth: ST.depth, tilt: ST.tilt}, size = 1000;
    function fit() {
      var w = wrap.offsetWidth, h = wrap.offsetHeight;
      if (mode === 'd') { size = w * 1396 / 2576; stage.style.left = (w - size) + 'px'; stage.style.top = '0px'; }
      else { size = Math.min(w, h); stage.style.left = (w - size) + 'px'; stage.style.top = ((h - size) / 2) + 'px'; }
      stage.style.transform = 'scale(' + (size / 1000) + ')';
      var m = size < 600 ? 0.6 : 1; E.depth = ST.depth * m; E.tilt = ST.tilt * m;
    }
    function fitWords() {
      B.forEach(function (b, i) {
        var w = lEls[i].firstChild; w.style.fontSize = b.s + 'px'; w.style.transform = 'none';
        var f = Math.min(1, (b.w * 0.84) / w.scrollWidth);
        w.style.fontSize = (b.s * f).toFixed(1) + 'px'; w.style.transform = 'scaleY(' + Math.min(1.45, 1 / f).toFixed(3) + ')';
      });
    }
    function settle(p) { var a = Math.abs(p), q = Math.max(0, a - 0.05); return (p < 0 ? -1 : 1) * (q * q / (q + 0.08)); }
    function place(el, x, y, w, h, d, dy) {
      var z = (0.3 - d) * 360 * E.depth, k = (P - z) / P;
      var bx = OX + (x + w / 2 - OX) * k, by = OY + (y + h / 2 - OY) * k;
      el.style.transform = 'translate3d(' + (bx - w / 2).toFixed(1) + 'px,' + (by - h / 2 + dy).toFixed(1) + 'px,' + z.toFixed(0) + 'px) scale(' + k.toFixed(4) + ') rotateY(' + (-E.tilt) + 'deg)';
    }
    function frame() {
      var r = stage.getBoundingClientRect(), vh = window.innerHeight;
      if (!r.height || r.bottom < -300 || r.top > vh + 300) return;
      stage.style.perspectiveOrigin = '25% ' + ((vh / 2 - r.top) / (r.height / 1000)).toFixed(1) + 'px';
      var p = settle(((r.top + r.height / 2) - vh / 2) / vh);
      B.forEach(function (b, i) {
        var dy = -p * ST.sign * (1 - 1.8 * b.d) * 110 * E.depth;
        place(bEls[i], b.x, b.y, b.w, b.h, b.d, dy); place(lEls[i], b.x, b.y, b.w, b.h, b.d, dy);
      });
      G.forEach(function (g, i) {
        place(gEls[i], g.x, g.y, gEls[i].offsetWidth, gEls[i].offsetHeight, 1.35, -p * ST.sign * (1 - 1.8 * 1.35) * 110 * E.depth);
      });
    }
    wrap.classList.add('live');
    fit(); fitWords(); frame();
    if (document.fonts) document.fonts.ready.then(function () { fitWords(); frame(); });
    return {fit: fit, frame: frame};
  }

  var clouds = Array.prototype.map.call(imgs, build);
  var ticking = false;
  function on() { if (!ticking) { ticking = true; requestAnimationFrame(function () { ticking = false; clouds.forEach(function (c) { c.frame(); }); }); } }
  window.addEventListener('scroll', on, {passive: true});
  window.addEventListener('resize', function () { clouds.forEach(function (c) { c.fit(); }); on(); });
})();

/* ---------- moving light: card shadows swing as the page scrolls, as if the light crosses the room ---------- */
(function () {
  if (!document.documentElement.classList.contains('fx')) return;
  var cards = Array.prototype.slice.call(document.querySelectorAll('[data-light]'));
  if (!cards.length) return;
  var spec = cards.map(function (el) {
    var a = el.getAttribute('data-light').split('|');
    var m = a[0] === 'm';
    return {el: el, a1: a[1], a2: a[2], y1: m ? 18 : 22, b1: m ? 36 : 44, s1: m ? -12 : -14, y2: m ? 30 : 40, b2: m ? 54 : 70, s2: m ? -18 : -22, reach: m ? 50 : 100, on: false};
  });
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (es) { es.forEach(function (e) { spec.forEach(function (c) { if (c.el === e.target) c.on = e.isIntersecting; }); }); on(); }, {rootMargin: '120px 0px'});
    spec.forEach(function (c) { io.observe(c.el); });
  } else spec.forEach(function (c) { c.on = true; });
  function frame() {
    var vh = window.innerHeight;
    spec.forEach(function (c) {
      if (!c.on) return;
      var r = c.el.getBoundingClientRect(); if (!r.height) return;
      var p = Math.max(-1, Math.min(1, ((r.top + r.height / 2) - vh / 2) / (vh / 2)));
      var sx = p * c.reach;      // low on screen: light from the left, shadow falls right; high: the reverse
      c.el.style.boxShadow = '0 2px 6px rgba(30,30,30,0.06), ' + (sx * 0.45).toFixed(1) + 'px ' + c.y1 + 'px ' + c.b1 + 'px ' + c.s1 + 'px rgba(30,30,30,' + c.a1 + '), ' +
        sx.toFixed(1) + 'px ' + c.y2 + 'px ' + c.b2 + 'px ' + c.s2 + 'px rgba(30,30,30,' + c.a2 + ')';
    });
  }
  var ticking = false;
  function on() { if (!ticking) { ticking = true; requestAnimationFrame(function () { ticking = false; frame(); }); } }
  window.addEventListener('scroll', on, {passive: true});
  window.addEventListener('resize', on);
  frame();
})();
