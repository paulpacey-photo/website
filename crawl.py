"""Read each school site in a real browser and save its marketing text with rendered sizes.

Reads sites.json and run.json ({"only": [ids]} to limit the run, or {} for all).
Writes results/<id>.json. Commits progress every few sites when COMMIT=1.
"""
import json, os, re, subprocess, time, traceback
from urllib.parse import urlparse
from playwright.sync_api import sync_playwright

HERE = os.path.dirname(os.path.abspath(__file__))
EXTRACT = open(os.path.join(HERE, 'extract.js')).read()
SITES = json.load(open(os.path.join(HERE, 'sites.json')))
RUN = json.load(open(os.path.join(HERE, 'run.json')))
OUT = os.path.join(HERE, 'results')
os.makedirs(OUT, exist_ok=True)
UA = ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) '
      'Chrome/130.0.0.0 Safari/537.36')

PRIORITY = [
    (r'(?<![a-z])mission|vision|values|ethos|philosoph|guiding|purpose', 3),
    (r'why[- ]?(choose|us)|why-', 2),
    (r'about|welcome|who[- ]we[- ]are|our[- ]school|our[- ]story', 1),
]


def score(href, label):
    s = 0
    for rx, w in PRIORITY:
        if re.search(rx, label, re.I): s = max(s, w + 0.5)
        if re.search(rx, href, re.I): s = max(s, w)
    if s:
        depth = len([x for x in urlparse(href).path.split('/') if x])
        s -= 0.4 * max(0, depth - 2)
    return s


def same_site(base, href):
    b, h = urlparse(base), urlparse(href)
    bh, hh = b.netloc.replace('www.', ''), h.netloc.replace('www.', '')
    if bh != hh: return False
    prefix = b.path.rstrip('/')
    # schools hosted under a group domain (e.g. nordangliaeducation.com/ics-madrid) stay inside their own path
    if prefix and not h.path.startswith(prefix): return False
    return True


def read(page, url):
    page.goto(url, wait_until='domcontentloaded', timeout=45000)
    try:
        page.wait_for_load_state('networkidle', timeout=12000)
    except Exception:
        pass
    # scroll through the page so lazy sections render, then return to the top
    h = page.evaluate('document.body.scrollHeight')
    for y in range(0, min(h, 20000), 800):
        page.evaluate(f'window.scrollTo(0, {y})'); time.sleep(0.15)
    page.evaluate('window.scrollTo(0, 0)'); time.sleep(1.2)
    return page.evaluate(EXTRACT)


def commit(msg):
    if os.environ.get('COMMIT') != '1': return
    subprocess.run(['git', 'add', 'results'], cwd=HERE)
    r = subprocess.run(['git', 'commit', '-q', '-m', msg], cwd=HERE)
    if r.returncode == 0:
        subprocess.run(['git', 'push', '-q', 'origin', 'HEAD:language-study'], cwd=HERE)


def main():
    only = set(RUN.get('only') or [])
    todo = [s for s in SITES if not only or s['id'] in only]
    with sync_playwright() as p:
        browser = p.chromium.launch()
        ctx = browser.new_context(viewport={'width': 1440, 'height': 900}, user_agent=UA, locale='en-GB')
        for i, s in enumerate(todo, 1):
            rec = {'site': s, 'pages': [], 'errors': [], 'fetched': time.strftime('%Y-%m-%d %H:%M UTC', time.gmtime())}
            page = ctx.new_page()
            try:
                home = read(page, s['url'])
                home['role'] = 'home'
                rec['pages'].append(home)
                cands = {}
                for href, label in home['links']:
                    if href.rstrip('/') == home['url'].rstrip('/') or not same_site(home['url'] if urlparse(s['url']).path in ('', '/') else s['url'], href):
                        continue
                    sc = score(href, label)
                    if sc > 0.5 and sc > cands.get(href, (0, ''))[0]:
                        cands[href] = (sc, label)
                picked = sorted(cands.items(), key=lambda kv: (-kv[1][0], len(kv[0])))[:2]
                for href, (sc, label) in picked:
                    try:
                        sub = read(page, href)
                        sub['role'] = 'sub'; sub['link_label'] = label; sub['link_score'] = sc
                        rec['pages'].append(sub)
                    except Exception as e:
                        rec['errors'].append(f'{href}: {e!r}'[:300])
            except Exception as e:
                rec['errors'].append(f"{s['url']}: {e!r}"[:300])
            finally:
                page.close()
            json.dump(rec, open(os.path.join(OUT, s['id'] + '.json'), 'w'), ensure_ascii=False)
            print(i, s['id'], len(rec['pages']), 'pages', len(rec['errors']), 'errors', flush=True)
            if i % 8 == 0:
                commit(f'results: {i}/{len(todo)}')
        browser.close()
    open(os.path.join(OUT, '_done.txt'), 'w').write(f'{len(todo)} sites at {time.strftime("%Y-%m-%d %H:%M UTC", time.gmtime())}\n')
    commit(f'results: done ({len(todo)})')


if __name__ == '__main__':
    main()
