/* Sends website form entries to Wix Forms (site 894e01bd…). */
(function () {
  'use strict';
  var CLIENT_ID = '611e9bad-e7ad-4c82-9df6-b53aa23748c2';
  var FORMS = {
    portfolio: '05e484ee-a54c-4d81-a7da-aec8c9b1289e',
    guide: '6d929b76-342b-4279-beec-51a096172ecb',
    message: '7e8e7bf6-5020-4350-b64d-757ef84daf28',
    discovery: '33571af6-1726-43ac-b93f-1bcf1771d205'
  };
  var API = 'https://www.wixapis.com';
  var KEY = 'pp-visitor';

  function token() {
    try {
      var s = JSON.parse(localStorage.getItem(KEY) || 'null');
      if (s && s.exp > Date.now() + 60000) return Promise.resolve(s.at);
    } catch (e) {}
    return fetch(API + '/oauth2/token', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ clientId: CLIENT_ID, grantType: 'anonymous' })
    }).then(function (r) {
      if (!r.ok) throw new Error('token ' + r.status);
      return r.json();
    }).then(function (j) {
      try { localStorage.setItem(KEY, JSON.stringify({ at: j.access_token, exp: Date.now() + (j.expires_in || 3600) * 1000 })); } catch (e) {}
      return j.access_token;
    });
  }

  function questionFor(el) {
    var n = el.parentNode;
    while (n && n.tagName !== 'FORM') {
      var first = n.firstElementChild;
      if (first && first.tagName === 'P' && first !== el) return first.textContent.trim();
      n = n.parentNode;
    }
    return el.getAttribute('placeholder') || el.name;
  }

  var CONTACT = { name: 1, email: 1, school: 1, role: 1, 'yourschool-org': 1, 'if-part-of-one-optional': 1 };
  function discoveryAnswers(form) {
    var blocks = [], byQ = {}, order = [];
    form.querySelectorAll('input[name], textarea[name]').forEach(function (el) {
      if (CONTACT[el.name] || el.type === 'checkbox') return;
      var v = (el.value || '').trim();
      if (!v) return;
      var q = questionFor(el);
      if (!byQ[q]) { byQ[q] = []; order.push(q); }
      byQ[q].push(v);
    });
    order.forEach(function (q, i) { blocks.push((i + 1) + '. ' + q + '\n' + byQ[q].join('\n')); });
    return blocks.join('\n\n');
  }

  function clean(o) {
    var out = {};
    Object.keys(o).forEach(function (k) { if (o[k] !== '' && o[k] != null) out[k] = o[k]; });
    return out;
  }

  function uploadImages(t, form) {
    var files = (form && form._ppFiles) || [];
    if (!files.length) return Promise.resolve();
    return Promise.all(files.map(function (f) {
      return fetch(API + '/form-submission-service/v4/submissions/media-upload-url', {
        method: 'POST', headers: { 'Content-Type': 'application/json', Authorization: t },
        body: JSON.stringify({ formId: FORMS.discovery, filename: f.name, mimeType: f.type })
      }).then(function (r) { if (!r.ok) throw new Error('upload url ' + r.status); return r.json(); })
        .then(function (j) {
          var u = j.uploadUrl;
          return fetch(u + (u.indexOf('?') < 0 ? '?' : '&') + 'filename=' + encodeURIComponent(f.name), { method: 'PUT', headers: { 'Content-Type': f.type }, body: f });
        }).then(function (r) { if (!r.ok) throw new Error('upload ' + r.status); return r.json(); })
        .then(function (j) { return j.file && j.file.url; });
    })).then(function (urls) {
      var store = form.querySelector('input[name="images"]');
      if (store) store.value = urls.filter(Boolean).join('\n');
    });
  }

  window.ppSubmit = function (kind, d, form) {
    if (kind === 'discovery' && form && form._ppFiles && form._ppFiles.length) {
      return token().then(function (t) { return uploadImages(t, form); }).then(function () { return send(kind, d, form); });
    }
    return send(kind, d, form);
  };
  function send(kind, d, form) {
    var v;
    if (kind === 'portfolio' || kind === 'message') v = { name: d.name, school: d.school, role: d.role, email: d.email, message: d.message };
    else if (kind === 'guide') v = { name: d.name, school: d.school, email: d.email, newsletter: d.newsletter === 'yes' };
    else if (kind === 'discovery') v = { name: d.name, role: d.role, school: d.school, email: d.email, website: d['yourschool-org'], school_group: d['if-part-of-one-optional'], answers: discoveryAnswers(form).slice(0, 20000) };
    var body = JSON.stringify({ submission: { formId: FORMS[kind], submissions: clean(v) } });
    return token().then(function (t) {
      return fetch(API + '/form-submission-service/v4/submissions', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', Authorization: t },
        body: body
      });
    }).then(function (r) {
      if (!r.ok) return r.text().then(function (t) { throw new Error('submit ' + r.status + ' ' + t.slice(0, 300)); });
      return r.json();
    });
  }
})();
