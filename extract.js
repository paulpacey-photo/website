// Runs inside each page. Collects visible marketing text with its rendered size and position.
() => {
  const SKIP = 'nav,footer,[role=navigation],[role=contentinfo],[aria-hidden="true"],script,style,noscript,svg,select,option,button,dialog,[role=dialog],[role=menu],[role=menubar],' +
    '[class*="cookie" i],[id*="cookie" i],[class*="consent" i],[id*="consent" i],[class*="gdpr" i],' +
    '[class*="footer" i],[id*="footer" i],[class*="breadcrumb" i],a[class*="skip" i],[class*="megamenu" i],[class*="mega-menu" i]';
  const SKIPS = SKIP.split(',');
  const why = {};
  const vh = window.innerHeight;
  const blocks = new Map();
  const order = [];
  const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
  while (walker.nextNode()) {
    const node = walker.currentNode;
    const txt = node.textContent.replace(/\s+/g, ' ').trim();
    if (txt.length < 2) continue;
    const el = node.parentElement;
    if (!el) continue;
    const hit = el.closest(SKIP);
    if (hit) {
      const sel = SKIPS.find(q => { try { return hit.matches(q); } catch (e) { return false; } }) || '?';
      const k = sel + ' @' + hit.tagName.toLowerCase() + '.' + String(hit.className || '').slice(0, 40) + '#' + (hit.id || '');
      why[k] = (why[k] || 0) + txt.length;
      continue;
    }
    const cs = getComputedStyle(el);
    if (cs.display === 'none' || cs.visibility === 'hidden' || parseFloat(cs.opacity) === 0) continue;
    const r = el.getBoundingClientRect();
    if (r.width < 1 || r.height < 1) continue;
    // group by the nearest block-level ancestor so inline spans join their sentence
    let blk = el;
    while (blk && blk !== document.body && getComputedStyle(blk).display.startsWith('inline')) blk = blk.parentElement;
    if (!blk) continue;
    const fs = parseFloat(cs.fontSize);
    const top = r.top + window.scrollY;
    if (!blocks.has(blk)) { blocks.set(blk, { parts: [], fs: 0, top, tag: blk.tagName.toLowerCase() }); order.push(blk); }
    const b = blocks.get(blk);
    b.parts.push(txt);
    b.fs = Math.max(b.fs, fs);
    b.top = Math.min(b.top, top);
  }
  const out = [];
  const seen = new Set();
  for (const blk of order) {
    const b = blocks.get(blk);
    const text = b.parts.join(' ').replace(/\s+/g, ' ').trim();
    if (text.length < 3 || seen.has(text)) continue;
    seen.add(text);
    const inHeader = !!blk.closest('header');
    out.push([Math.round(b.fs * 10) / 10, b.tag, Math.round(b.top), b.top < vh ? 1 : 0, inHeader ? 1 : 0, text.slice(0, 1500)]);
  }
  // candidate links about mission / values / why choose us
  const RX = /((?<![a-z])mission|vision|values|ethos|philosoph|guiding|purpose|why[- ]?(choose|us|[a-z]+)|about|welcome|who[- ]we[- ]are|our[- ]school|our[- ]story|principal|head'?s?[- ]welcome)/i;
  const links = [];
  for (const a of document.querySelectorAll('a[href]')) {
    const href = a.href.split('#')[0];
    const label = (a.textContent || '').replace(/\s+/g, ' ').trim().slice(0, 80);
    if (!/^https?:/.test(href) || /\.(pdf|jpg|png|docx?)$/i.test(href)) continue;
    if (RX.test(label) || RX.test(href)) links.push([href, label]);
  }
  const skipped = Object.entries(why).sort((a, b) => b[1] - a[1]).slice(0, 8);
  return { url: location.href, title: document.title, lang: document.documentElement.lang || '', vh, blocks: out, links: links.slice(0, 80), skipped,
           sample: out.length ? '' : (document.body.innerText || '').slice(0, 600) };
}
