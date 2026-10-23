"""Turn the collected page text into vocabulary statistics.

Prominence weight of a text block = its font size relative to the page's body text size
(capped at 5x), times 1.5 if it is on the first screen. A word's prominence index is the
average weight of its appearances; reach is how many sites use it at all.
"""
import json, glob, re, os, statistics, collections, unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))

STOP = set("""a about above across after again against all almost along already also although always am among an and another any anyone anything
are around as at away back be became because become becomes been before being below best better between beyond both bring brings but by can cannot
could day days did do does doing done down during each either else enough even ever every everyone everything far few find first for found from
further get gets give given gives go going good got great had has have having he her here hers him his how however i if in inside into is it its
itself just keep know known last least less let like made make makes making many may me more most much must my near need needs new next no not
now of off often on once one only onto or other others our ours ourselves out over own part per perhaps place put rather really right same see
seen set several she should show shows since so some something sometimes still such take takes taking than that the their theirs them themselves
then there these they thing things this those though through throughout thus to today together too toward towards two under until up upon us use
used using very via want was way ways we well were what whatever when where whether which while who whole whom whose why will with within without
would yet you your yours yourself also each read more learn click view explore discover find visit apply enquire inquire contact join
""".split())

# Words that describe what a school is rather than how it sells itself
GENERIC = set("""school schools student students pupil pupils child children kid kids young people person parent parents family families teacher teachers
staff faculty class classes classroom classrooms grade grades year years age aged ages campus campuses programme programmes program programs
curriculum curricula course courses subject subjects lesson lessons education educational educate educator educators academic academics learning
learn learner learners study studies primary secondary early elementary middle high upper lower junior senior nursery kindergarten reception sixth
form college university universities ib diploma ap igcse gcse baccalaureate international bilingual english french german spanish language languages
admission admissions apply application fees fee boarding day week weeks term terms open event events news calendar home page website
team head director principal leadership alumni world global life time also more we're""".split())

SUPERLATIVES = set("""excellence excellent outstanding exceptional exceptionally world-class leading leader premier premium top finest best unrivalled
unrivaled unparalleled unmatched extraordinary remarkable superb renowned prestigious elite highest unique distinctive incredible amazing
first-class high-quality award-winning""".split())

# Multi-word ideas kept intact (matched before single words); value = canonical label
PHRASES = {
    r'global citizen\w*': 'global citizens', r'life-?long learn\w*': 'lifelong learners', r'love of learning': 'love of learning',
    r'whole[- ]child': 'whole child', r'holistic\w*': 'holistic', r'(student|child|learner)[- ]cent(er|re)d': 'student-centred',
    r'21st[- ]century': '21st-century', r'critical think\w*': 'critical thinking', r'growth mindset': 'growth mindset',
    r'sense of belonging': 'belonging', r'well[- ]?being': 'wellbeing', r'inquiry[- ]based|enquiry[- ]based|inquiry|enquiry': 'inquiry',
    r'world[- ]class': 'world-class', r'high[- ]quality': 'high-quality', r'award[- ]winning': 'award-winning', r'first[- ]class': 'first-class',
    r'future[- ]ready|ready for the future|prepared for the future': 'future-ready', r'real[- ]world': 'real-world',
    r'international[- ]minded\w*': 'international-mindedness', r'personali[sz]ed': 'personalised', r'tailor[- ]made|tailored': 'tailored',
    r'home away from home': 'home away from home', r'full potential|reach their potential|fulfil(l)? their potential': 'potential',
    r'state[- ]of[- ]the[- ]art': 'state-of-the-art', r'cutting[- ]edge': 'cutting-edge', r'safe and (happy|nurturing|supportive)': 'safe',
    r'make a (positive )?difference': 'make a difference', r'positive impact': 'impact', r'social purpose': 'social purpose',
    r'growth': 'growth',
}

# Fold word variants into one idea
LEMMA = {}
for canon, forms in {
    'inclusive': 'inclusive inclusion inclusivity include', 'diverse': 'diverse diversity', 'innovative': 'innovative innovation innovate innovating innovations innovators innovator',
    'creative': 'creative creativity create creating creators', 'curious': 'curious curiosity', 'empower': 'empower empowering empowered empowers empowerment',
    'nurturing': 'nurture nurturing nurtured nurtures', 'caring': 'caring care cares', 'collaborative': 'collaborative collaboration collaborate collaborating',
    'compassionate': 'compassion compassionate', 'respect': 'respect respectful respected', 'resilient': 'resilient resilience', 'confident': 'confident confidence',
    'rigorous': 'rigorous rigour rigor', 'challenging': 'challenge challenging challenges challenged', 'supportive': 'support supportive supporting supported supports',
    'inspire': 'inspire inspiring inspired inspires inspiration inspirational', 'passion': 'passion passionate passions', 'thrive': 'thrive thriving thrives',
    'flourish': 'flourish flourishing', 'excellence': 'excellence excellent excel excels excelling', 'leading': 'leading leader leaders', 'leadership': 'leadership lead leads',
    'responsible': 'responsible responsibility', 'kind': 'kind kindness', 'happy': 'happy happiness', 'safe': 'safe safety safeguarding secure',
    'sustainable': 'sustainable sustainability', 'independent': 'independent independence independently', 'balanced': 'balanced balance',
    'opportunity': 'opportunity opportunities', 'potential': 'potential', 'success': 'success successful succeed succeeding', 'values': 'values value valued',
    'unique': 'unique uniquely uniqueness', 'individual': 'individual individuals individuality individually', 'engage': 'engage engaging engaged engagement',
    'explore': 'exploration exploring', 'discovery': 'discovery', 'growth': 'grow growing grows', 'welcoming': 'welcoming', 'welcome': 'welcome welcomes welcomed',
    'connected': 'connected connection connections connect', 'ambitious': 'ambition ambitious ambitions', 'character': 'character',
    'integrity': 'integrity', 'authentic': 'authentic authenticity', 'joy': 'joy joyful', 'purpose': 'purpose purposeful', 'impact': 'impact impactful',
    'exceptional': 'exceptional exceptionally', 'personalised': 'personalised personalized personalisation', 'personal': 'personal', 'future': 'future futures',
    'world': 'worlds', 'experience': 'experience experiences experiential', 'skills': 'skill skills', 'tradition': 'tradition traditions traditional',
    'heritage': 'heritage', 'family': 'family-like', 'belonging': 'belong belonging belongs', 'agency': 'agency', 'mindful': 'mindful mindfulness',
    'reflective': 'reflective reflection reflect', 'principled': 'principled principles', 'open-minded': 'open-minded open-mindedness',
    'excellent': 'excellent', 'outstanding': 'outstanding', 'renowned': 'renowned', 'prestigious': 'prestigious',
}.items():
    for f in forms.split():
        LEMMA[f] = canon
LEMMA['excellent'] = 'excellence'

NOISE = re.compile(r'^[\d\W_]+$|\d{1,2}:\d{2}|©|cookie', re.I)


def norm(t):
    t = unicodedata.normalize('NFKC', t).replace('’', "'").replace('‘', "'").replace('–', '-').replace('—', '-').lower()
    return t


def tokens(text):
    t = norm(text)
    found = []
    for rx, canon in PHRASES.items():
        def rep(m, canon=canon):
            found.append(canon)
            return ' '
        t = re.sub(r'\b(?:' + rx + r')\b', rep, t)
    for w in re.findall(r"[^\W\d_][^\W\d_'-]*(?:['-][^\W\d_]+)*", t):
        w = w.strip("'-")
        if w.endswith("'s"): w = w[:-2]
        if len(w) < 3 or w in STOP: continue
        if w in LEMMA: w = LEMMA[w]
        elif w.endswith('ies') and len(w) > 5: w = w[:-3] + 'y'
        elif w.endswith('s') and not w.endswith('ss') and len(w) > 4 and w[:-1] in LEMMA: w = LEMMA[w[:-1]]
        found.append(w)
    return found


def site_blocks(rec):
    """Unique text blocks across a site's pages, each with its prominence weight."""
    best = {}
    for p in rec['pages']:
        blocks = [b for b in p['blocks'] if not NOISE.search(b[5]) and sum(c.isalpha() for c in b[5]) >= 0.6 * len(b[5])]
        long_ = [(b[0], len(b[5])) for b in blocks if len(b[5]) >= 80]
        if long_:
            sizes = sorted(s for s, n in long_ for _ in range(max(1, n // 50)))
            base = sizes[len(sizes) // 2]
        else:
            base = 16.0
        base = max(base, 12.0)
        for fs, tag, top, fold, header, text in blocks:
            w = min(max(fs / base, 1.0), 5.0) * (1.5 if fold else 1.0)
            key = norm(text)
            if key not in best or w > best[key][0]:
                best[key] = (w, text, fs, base, fold, p['role'])
    return list(best.values())


def load():
    recs = []
    for f in sorted(glob.glob(os.path.join(os.environ.get('DATA', HERE), 'results', '*.json'))):
        recs.append(json.load(open(f)))
    return recs


def own_words(site):
    from urllib.parse import urlparse
    t = norm(site['name'] + ' ' + urlparse(site['url']).netloc + ' ' + urlparse(site['url']).path + ' ' + site['country'])
    return set(re.findall(r"[^\W\d_]+", t))


def site_profile(rec):
    """Per site: for each term, total weight, max weight, appearances, whether in a headline (weight>=2) or first screen."""
    own = own_words(rec['site'])
    prof = collections.defaultdict(lambda: {'w': 0.0, 'max': 0.0, 'n': 0, 'headline': 0, 'fold': 0})
    total = 0.0
    for w, text, fs, base, fold, role in site_blocks(rec):
        for t in tokens(text):
            if t in GENERIC or t in own: continue
            d = prof[t]
            d['w'] += w; d['max'] = max(d['max'], w); d['n'] += 1
            if w >= 2.0: d['headline'] = 1
            if fold: d['fold'] = 1
            total += w
    return prof, total


if __name__ == '__main__':
    recs = load()
    for r in recs:
        prof, total = site_profile(r)
        top = sorted(prof.items(), key=lambda kv: -kv[1]['w'])[:15]
        print(r['site']['name'], f'{total:.0f}', ', '.join(f"{k} {v['w']:.1f}" for k, v in top))
