"""Build the live site from the canvas boards.

Each page holds the desktop layout (1440 wide) and the mobile layout (390 wide).
site.js shows the right one for the screen and scales it to fit.
"""
import re, os, json, glob, shutil, html
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, 'project')
ASSETS = os.path.join(HERE, 'assets')
OUT = os.path.join(HERE, 'dist')
CAL = 'https://calendly.com/paulpacey/30min'
DOMAIN = 'https://paulpacey.photography'

PAGES = [
    # slug, file, desktop boards, mobile boards, title, description
    ('index', 'index.html', ['Main', 'Main-2'], ['Mobile', 'Mobile-2'],
     'Paul Pacey | Marketing Photography for International Schools',
     'Marketing photography and visual brand strategy for international schools. 200+ campaigns in 30+ countries.'),
    ('services', 'services.html', ['Services'], ['Services-Mobile', 'Services-Mobile-2'],
     'Services | Paul Pacey',
     'Campaign photography, image audits, partnerships and training for international school marketing teams.'),
    ('resources', 'resources.html', ['Resources'], ['Resources-Mobile'],
     'Resources | Paul Pacey',
     'Free guides and essays for international school marketing teams, drawn from 200+ campaigns.'),
    ('contact', 'contact.html', ['Contact'], ['Contact-Mobile'],
     'Contact | Paul Pacey',
     'Start a project, request private portfolio access, or ask a question.'),
    ('discovery', 'discovery.html', ['Discovery'], ['Discovery-Mobile'],
     'Discovery brief | Paul Pacey',
     'Tell me about your school in ten minutes. Your answers shape our first conversation.'),
    ('thanks', 'thanks.html', ['Thanks'], ['Thanks-Mobile'],
     'Thank you | Paul Pacey', 'Your discovery brief has been received.'),
    ('planning-guide', 'planning-guide.html', ['Guide'], ['Guide-Mobile'],
     'Planning Your Photo Campaign | Paul Pacey',
     'A free nine-step framework for planning a school marketing photo campaign, from discovery brief to final edit.'),
    ('privacy', 'privacy.html', ['Privacy'], ['Privacy-Mobile'],
     'Privacy policy | Paul Pacey', 'How Paul Pacey Photography handles your personal data.'),
]

# where each placeholder link goes when its target is not on the current page
GLOBAL = {
    'home': 'index.html', 'top': 'index.html', 'services': 'services.html',
    'resources': 'resources.html', 'portfolio': 'index.html#portfolio',
    'contact': 'contact.html', 'discovery': 'discovery.html', 'privacy': 'privacy.html',
    'planning': 'resources.html#planning', 'process': 'index.html#process',
    'faq': 'services.html#faq', 'audit-tool': 'resources.html#articles',
    'essay': 'resources.html#articles', 'lessons': 'resources.html#articles',
    'guide-download': 'index.html#resources',      # the guide sign-up form
    'planning-guide': 'planning-guide.html',
    'essay-read': 'resources.html#articles',          # TODO: essay page
    'call': 'services.html#call',
}
NAV = {'home': 'index.html', 'top': 'index.html', 'services': 'services.html',
       'resources': 'resources.html', 'portfolio': 'index.html#portfolio', 'contact': 'contact.html'}
ALWAYS = {'contact', 'home'}  # never treated as in-page anchors

# ---------------------------------------------------------------- assets
def build_assets():
    os.makedirs(os.path.join(OUT, 'img'), exist_ok=True)
    m = {}
    for p in glob.glob(os.path.join(ASSETS, '*')):
        bid, ext = os.path.splitext(os.path.basename(p))
        if ext == '.svg':
            name = bid + '.svg'; shutil.copy(p, os.path.join(OUT, 'img', name))
        elif bid == 'c5aa90e6520ebdd69fd4caa29326c030':
            name = 'share-image.jpg'; Image.open(p).convert('RGB').save(os.path.join(OUT, name), quality=88)
            m[bid] = name; continue
        else:
            im = Image.open(p)
            if ext == '.webp' and im.width <= 2880:
                shutil.copy(p, os.path.join(OUT, 'img', bid + '.webp')); m[bid] = 'img/' + bid + '.webp'; continue
            if im.mode not in ('RGB', 'RGBA'): im = im.convert('RGB')
            if im.width > 2880: im = im.resize((2880, round(im.height * 2880 / im.width)), Image.LANCZOS)
            name = bid + '.webp'
            q = 82
            im.save(os.path.join(OUT, 'img', name), 'WEBP', quality=q, method=6)
            if ext == '.webp' and os.path.getsize(os.path.join(OUT, 'img', name)) > os.path.getsize(p):
                shutil.copy(p, os.path.join(OUT, 'img', name))
        m[bid] = 'img/' + name
    return m

# ---------------------------------------------------------------- template rendering
TOK = re.compile(r'<sc-(for|if)\b([^>]*)>|</sc-(for|if)>')

def lookup(ctx, expr):
    expr = expr.strip()
    if expr in ('true', 'false'): return expr == 'true'
    cur = ctx
    for part in expr.split('.'):
        cur = cur[part] if isinstance(cur, dict) else getattr(cur, part)
    return cur

def parse(s, i=0, end_tag=None):
    """Return (nodes, index). nodes: str | ('for'|'if', attrs, children)."""
    nodes = []
    while True:
        m = TOK.search(s, i)
        if not m:
            nodes.append(s[i:]); return nodes, len(s)
        nodes.append(s[i:m.start()])
        if m.group(3):
            return nodes, m.end()
        kind, attrs = m.group(1), m.group(2)
        children, j = parse(s, m.end(), kind)
        nodes.append((kind, attrs, children))
        i = j

def attr(attrs, name):
    m = re.search(name + r'="\{\{([^}]+)\}\}"', attrs)
    return m.group(1) if m else None

def render(nodes, ctx):
    out = []
    for n in nodes:
        if isinstance(n, str):
            out.append(re.sub(r'\{\{([^}]+)\}\}', lambda m: html.escape(str(lookup(ctx, m.group(1))), quote=True) if not isinstance(lookup(ctx, m.group(1)), bool) else str(lookup(ctx, m.group(1))).lower(), n))
        elif n[0] == 'for':
            lst = lookup(ctx, attr(n[1], 'list')); name = re.search(r'as="([^"]+)"', n[1]).group(1)
            for item in lst:
                c = dict(ctx); c[name] = item
                out.append(render(n[2], c))
        else:
            v = lookup(ctx, attr(n[1], 'value'))
            if v == 'SLIDE':
                pass
            if isinstance(v, dict):  # slide wrapper
                out.append(v['open'] + render(n[2], ctx) + '</div>')
            elif v:
                out.append(render(n[2], ctx))
    return ''.join(out)

def expand(body, ctx):
    body = re.sub(r'onClick="\{\{([^}]+)\}\}"', r'data-on="{{\1}}"', body)
    nodes, _ = parse(body)
    return render(nodes, ctx)

def testimonial_ctx(script):
    T = json.loads(re.search(r'const TESTIMONIALS = (\[.*?\]);\n', script, re.S).group(1))
    items = []
    for i, q in enumerate(T):
        items.append(dict(q, idx=i,
            active={'open': f'<div class="tslide" data-i="{i}"' + ('' if i == 0 else ' hidden') + '>'},
            go=f'go:{i}', dotW=28 if i == 0 else 10, dotBg='#8E2A26' if i == 0 else '#CFC7BC',
            label=f'Show testimonial {i + 1}'))
    return {'testimonials': items, 'prevT': 'prev', 'nextT': 'next', 'showLabels': False}

def discovery_ctx(script):
    G = json.loads(re.search(r'const GROUPS = (\{.*?\});\n', script, re.S).group(1))
    ctx = {}
    for k, (opts, multi) in G.items():
        ctx[k] = [dict(label=o, pressed='false', bg='#ffffff', fg='#1E1E1E', bd='#CFC7BC',
                       toggle=f'chip:{k}:{"m" if multi else "s"}:{o}') for o in opts]
    for k in ('compete', 'visual'):
        ctx[k] = [dict(num=n, label=f'{k} {n} of 10', pressed='false', bg='#ffffff', fg='#1E1E1E',
                       bd='#E4DED5', pick=f'scale:{k}:{n}') for n in range(1, 11)]
    return ctx

# ---------------------------------------------------------------- CSS scoping
def split_rules(css):
    """Top-level rules: list of (prelude, body)."""
    out, i, n = [], 0, len(css)
    while i < n:
        j = css.find('{', i)
        if j < 0: break
        prelude = css[i:j].strip()
        depth, k = 1, j + 1
        while depth and k < n:
            if css[k] == '{': depth += 1
            elif css[k] == '}': depth -= 1
            k += 1
        out.append((prelude, css[j + 1:k - 1])); i = k
    return out

def scope_css(css, scope, suffix):
    frames = re.findall(r'@keyframes\s+([\w-]+)', css)
    def ren(text):
        for f in frames: text = re.sub(r'\b' + f + r'\b', f + suffix, text)
        return text
    out, glob_ = [], []
    for pre, body in split_rules(css):
        if pre.startswith('@keyframes'):
            out.append(ren(pre) + '{' + body + '}')
        elif pre.startswith('@media'):
            inner = ''.join(scope_rule(p, b, scope, ren) for p, b in split_rules(body))
            out.append(pre + '{' + inner + '}')
        elif re.match(r'^(body|html)\b', pre):
            glob_.append(pre + '{' + body + '}')
        else:
            out.append(scope_rule(pre, body, scope, ren))
    return ''.join(out), ''.join(glob_)

def scope_rule(pre, body, scope, ren):
    sels = [scope + ' ' + s.strip() for s in pre.split(',')]
    return ','.join(sels) + '{' + ren(body) + '}'

# ---------------------------------------------------------------- links
def rewrite_links(s, page_ids):
    def fix(seg, nav):
        def rep(m):
            t = m.group(1)
            if nav and t in NAV: return f'href="{NAV[t]}"'
            if t in page_ids and t not in ALWAYS: return m.group(0)
            if t in GLOBAL: return f'href="{GLOBAL[t]}"'
            return m.group(0)
        return re.sub(r'href="#([^"]*)"', rep, seg)
    parts = re.split(r'(<header\b.*?</header>)', s, flags=re.S)
    return ''.join(fix(p, p.startswith('<header')) for p in parts)

def prefix_ids(s, ids):
    for i in ids:
        s = s.replace(f'id="{i}"', f'id="m-{i}"').replace(f'for="{i}"', f'for="m-{i}"').replace(f'href="#{i}"', f'href="#m-{i}"')
    return s

# ---------------------------------------------------------------- forms: give every field a name
SLUG = lambda t: re.sub(r'[^a-z0-9]+', '-', t.lower()).strip('-')[:40]
def name_fields(body):
    seen = {}
    def rep(m):
        tag = m.group(0)
        if ' name="' in tag or 'type="checkbox"' in tag and 'name=' in tag: return tag
        ph = re.search(r'placeholder="([^"]*)"', tag)
        idm = re.search(r'id="([^"]*)"', tag)
        if 'type="checkbox"' in tag: n = 'newsletter'
        elif ph:
            p = ph.group(1).lower()
            n = {'your name': 'name', 'your full name': 'name', 'school name': 'school', 'name@school.org': 'email',
                 'e.g. director of marketing': 'role', 'hi paul,': 'message'}.get(p, SLUG(ph.group(1)))
        else: n = idm.group(1) if idm else 'field'
        return tag.replace('<' + m.group(1), '<' + m.group(1) + f' name="{n}"', 1)
    return re.sub(r'<(input|textarea)\b[^>]*>', rep, body)

# ---------------------------------------------------------------- page assembly
AUTO_HEIGHT = {'Discovery', 'Discovery-Mobile'}

def board(name):
    s = open(os.path.join(SRC, name + '.dc.html')).read()
    helmet = re.search(r'<helmet>(.*?)</helmet>', s, re.S).group(1)
    css = re.search(r'<style>(.*?)</style>', helmet, re.S).group(1)
    start = s.index('<div style="width: ', s.index('</helmet>'))
    end = s.rindex('</x-dc>')
    body = s[start:end].rstrip()
    # pages whose content can grow or shrink (e.g. reveal-on-select fields) size to their content
    if name in AUTO_HEIGHT:
        body = re.sub(r'^(<div style="width: \d+px; )height: \d+px;', r'\1height: auto;', body, count=1)
    script = re.search(r'<script type="text/x-dc"[^>]*>(.*?)</script>', s, re.S).group(1)
    if 'TESTIMONIALS' in script and '{{testimonials}}' in body: body = expand(body, testimonial_ctx(script))
    elif 'const GROUPS' in script: body = expand(body, discovery_ctx(script))
    elif '<sc-' in body or '{{' in body: body = expand(body, {'showLabels': False})
    return css, body

def build():
    if os.path.exists(OUT): shutil.rmtree(OUT)
    os.makedirs(OUT)
    amap = build_assets()
    seen, shared = set(), []
    order = ['Main', 'Mobile'] + [b for p in PAGES for b in p[2] + p[3] if b not in ('Main', 'Mobile')]
    for b in order:
        css = board(b)[0]
        mob = 'Mobile' in b
        scoped = scope_css(css, '.v-m' if mob else '.v-d', '-m' if mob else '-d')[0]
        for pre, body in split_rules(scoped):
            key = pre + ('{' + body + '}' if pre.startswith('@media') else '')
            if key in seen:
                continue
            seen.add(key)
            shared.append(pre + '{' + body + '}')
    open(os.path.join(OUT, 'pages.css'), 'w').write(''.join(shared))
    for f in ('site.css', 'site.js', 'wix.js'): shutil.copy(os.path.join(HERE, f), OUT)
    for p in glob.glob(os.path.join(HERE, 'static', '*')): shutil.copy(p, OUT)  # files served as-is (e.g. PDFs)
    built = {}
    for slug, fname, dboards, mboards, title, desc in PAGES:
        d = [board(b) for b in dboards]; m = [board(b) for b in mboards]
        dbody = '\n'.join(b for _, b in d); mbody = '\n'.join(b for _, b in m)
        ids = set(re.findall(r'\sid="([^"]+)"', dbody)) | set(re.findall(r'\sid="([^"]+)"', mbody))
        dbody = rewrite_links(dbody, ids); mbody = rewrite_links(mbody, ids)
        mbody = prefix_ids(mbody, sorted(set(re.findall(r'\sid="([^"]+)"', mbody)), key=len, reverse=True))
        dbody = name_fields(dbody); mbody = name_fields(mbody)
        dcss, gcss = scope_css(d[0][0], '.v-d', '-d')
        mcss, _ = scope_css(m[0][0], '.v-m', '-m')
        extra = ''.join(scope_css(c, '.v-d', '-d')[0] for c, _ in d[1:] if c != d[0][0]) + \
                ''.join(scope_css(c, '.v-m', '-m')[0] for c, _ in m[1:] if c != m[0][0])
        page = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<link rel="canonical" href="{DOMAIN}/{'' if slug == 'index' else fname}">
<meta property="og:type" content="website">
<meta property="og:url" content="{DOMAIN}/{'' if slug == 'index' else fname}">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:image" content="{SHARE}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="627">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" type="image/svg+xml" href="img/260b764977aed2393c6045ade5a04036.svg">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Jost:wght@400;500;600&amp;family=Newsreader:ital,opsz,wght@0,6..72,300..700;1,6..72,300..700&amp;display=swap">
<link rel="stylesheet" href="site.css">
<link rel="stylesheet" href="pages.css">
<link rel="stylesheet" href="styles.css">
<script>{open(os.path.join(HERE, 'fit.js')).read()}</script>
</head>
<body data-page="{slug}">
<div class="v-d" id="layout-d">
{dbody}
</div>
<div class="v-m" id="layout-m">
{mbody}
</div>
{MENU}
<script src="wix.js" defer></script>
<script src="site.js" defer></script>
</body>
</html>
'''
        for bid, path in amap.items():
            page = page.replace('/_blob/' + bid, MEDIA.get(bid, path))
        page = re.sub(r'<!--.*?-->', '', page, flags=re.S)
        assert '/_blob/' not in page, (slug, re.findall(r'/_blob/\w+', page)[:3])
        assert '{{' not in page and '<sc-' not in page, slug
        page = page.replace('href="https://calendly.com', 'href="https://calendly.com')
        built[fname] = page
    # move repeated inline styles into one shared stylesheet
    reg = {}
    def cls(m):
        st = re.sub(r'\s*([:;])\s*', r'\1', m.group(1)).strip().rstrip(';')
        if st not in reg: reg[st] = 's' + format(len(reg), 'x')
        return f'data-s="{reg[st]}"'
    for fname, page in built.items():
        head, body = page.split('<body', 1)
        body = re.sub(r'style="([^"]*)"', cls, body)
        # merge data-s into class attribute
        def merge(m):
            tag = m.group(0)
            ds = re.search(r' data-s="([^"]+)"', tag)
            if not ds: return tag
            tag = tag.replace(ds.group(0), '')
            if ' class="' in tag: return tag.replace(' class="', f' class="{ds.group(1)} ', 1)
            return tag[:-1].rstrip('/') + f' class="{ds.group(1)}"' + ('/>' if tag.endswith('/>') else '>') if False else re.sub(r'^(<[\w-]+)', lambda t: t.group(1) + f' class="{ds.group(1)}"', tag)
        body = re.sub(r'<[a-zA-Z][\w-]*\b[^>]*\bdata-s="[^"]+"[^>]*>', merge, body)
        open(os.path.join(OUT, fname), 'w').write(head + '<body' + body)
    css = ''.join(f'.{c}.{c}.{c}{{{st}}}' for st, c in reg.items())
    open(os.path.join(OUT, 'styles.css'), 'w').write(css)
    print('built', sorted(os.listdir(OUT)), len(reg), 'styles')

MEDIA = json.load(open(os.path.join(HERE, 'media.json'))) if os.path.exists(os.path.join(HERE, 'media.json')) else {}
SHARE = MEDIA.get('share', DOMAIN + '/share-image.jpg')

MENU = '''<div class="menu" id="menu" hidden>
<div class="menu-top"><a href="index.html" class="menu-logo" aria-label="Paul Pacey — home"><img src="img/260b764977aed2393c6045ade5a04036.svg" alt="" width="30" height="42"></a>
<button type="button" class="menu-close" aria-label="Close menu"><svg width="20" height="20" viewBox="0 0 20 20" fill="none" stroke="#1E1E1E" stroke-width="1.4" aria-hidden="true"><path d="M2 2l16 16M18 2L2 18"/></svg></button></div>
<nav aria-label="Main" class="menu-nav">
<a href="index.html">Home</a><a href="services.html">Services</a><a href="resources.html">Resources</a><a href="index.html#portfolio">Private portfolio</a><a href="contact.html">Contact</a>
</nav>
<div class="menu-foot"><a href="discovery.html" class="menu-cta">Start your discovery brief</a>
<a href="mailto:paulpacey@gmail.com">paulpacey@gmail.com</a><a href="tel:+420776182699">+420 776 182 699</a></div>
</div>'''

def bust_cache():
    """Add a content fingerprint to each stylesheet/script link so browsers never mix old and new files."""
    import hashlib
    tags = {}
    for f in ('site.css', 'pages.css', 'styles.css', 'site.js', 'wix.js'):
        tags[f] = hashlib.md5(open(os.path.join(OUT, f), 'rb').read()).hexdigest()[:10]
    for p in glob.glob(os.path.join(OUT, '*.html')):
        s = open(p).read()
        for f, h in tags.items():
            s = s.replace(f'href="{f}"', f'href="{f}?v={h}"').replace(f'src="{f}"', f'src="{f}?v={h}"')
        open(p, 'w').write(s)


if __name__ == '__main__':
    build()
    bust_cache()
