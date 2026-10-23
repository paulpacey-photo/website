"""Compute the study's statistics and write them to JSON for the spreadsheet."""
import json, collections, itertools, statistics
import analyze as A

# Words that make a claim about a school's character, values or promise (the "buzzwords")
BUZZ = """community creative supportive inspire opportunity success challenging growth future diverse passion inclusive thrive collaborative
caring journey nurturing respect confident innovative individual connected responsible curious independent empower global citizens
purpose impact potential compassionate vibrant safe reflective wellbeing sustainable lifelong belonging critical thinking inquiry principled
rigorous resilient character ambitious love of learning engage holistic whole child student-centred personalised tailored welcoming kind
integrity joy flourish empathy balanced open-minded future-ready 21st-century real-world international-mindedness agency authentic
excellence""".replace('global citizens', 'global_citizens').replace('critical thinking', 'critical_thinking').replace(
    'love of learning', 'love_of_learning').replace('whole child', 'whole_child').split()
BUZZ = {w.replace('_', ' ') for w in BUZZ} - {'excellence'}
SUPER = {'excellence', 'leading', 'unique', 'world-class', 'exceptional', 'outstanding', 'top', 'highest', 'best', 'premier', 'renowned',
         'prestigious', 'extraordinary', 'remarkable', 'finest', 'unrivalled', 'unparalleled', 'award-winning', 'first-class', 'high-quality',
         'state-of-the-art', 'cutting-edge', 'superb', 'elite', 'exceptionally'}

recs = A.load()
ok = [r for r in recs if sum(len(b[5]) for p in r['pages'] for b in p['blocks']) >= 1500]
skipped = [{'name': r['site']['name'], 'reason': 'Bot-verification wall; text could not be read' if 'Copenhagen' in r['site']['name']
            else 'Page text sits in panels the reader could not open; too little text to analyse'} for r in recs if r not in ok]
N = len(ok)

profiles = {}
for r in ok:
    profiles[r['site']['id']] = A.site_profile(r)

def stats(terms):
    rows = []
    for t in terms:
        users = [(sid, p[0][t]) for sid, p in profiles.items() if t in p[0]]
        if not users: continue
        n_use = sum(d['n'] for _, d in users); w_sum = sum(d['w'] for _, d in users)
        rows.append({'term': t, 'sites': len(users), 'share': len(users) / N, 'uses': n_use,
                     'prominence': w_sum / n_use, 'headline_sites': sum(d['headline'] for _, d in users),
                     'first_screen_sites': sum(d['fold'] for _, d in users),
                     'weighted_total': w_sum})
    return rows

buzz = sorted(stats(BUZZ), key=lambda r: (-r['sites'], -r['weighted_total']))
top20 = buzz[:20]
# prominence-weighted ranking of the same 20 words: average weighted presence per site
for r in top20:
    r['impact_score'] = r['weighted_total'] / N
for i, r in enumerate(sorted(top20, key=lambda r: -r['impact_score']), 1):
    r['prominence_rank'] = i
for i, r in enumerate(top20, 1):
    r['reach_rank'] = i
superl = sorted(stats(SUPER), key=lambda r: (-r['sites'], -r['weighted_total']))

top20_set = {r['term'] for r in top20}
per_site = []
for r in ok:
    sid = r['site']['id']; prof, total = profiles[sid]
    mine = sorted([(t, d['w']) for t, d in prof.items() if t in BUZZ], key=lambda x: -x[1])
    top10 = [t for t, _ in mine[:10]]
    sup_w = sum(d['w'] for t, d in prof.items() if t in SUPER)
    buzz_w = sum(d['w'] for t, d in prof.items() if t in BUZZ)
    per_site.append({'id': sid, 'name': r['site']['name'], 'type': r['site']['type'], 'region': r['site']['region'],
                     'curriculum': r['site']['curriculum'], 'ownership': r['site']['ownership'], 'client': r['site']['client'],
                     'pages': len(r['pages']), 'top20_used': sum(1 for t in top20_set if t in prof),
                     'top10_buzz': top10, 'top10_in_top20': sum(1 for t in top10 if t in top20_set),
                     'superlatives_used': sorted(t for t in prof if t in SUPER),
                     'superlative_share': sup_w / (sup_w + buzz_w) if (sup_w + buzz_w) else 0,
                     'urls': [p['url'] for p in r['pages']]})

# how alike are vocabularies? Jaccard of each site's buzzword set
sets = {s['id']: {t for t in profiles[s['id']][0] if t in BUZZ} for s in per_site}
def jac(a, b): return len(a & b) / len(a | b) if a | b else 0
schools = [s for s in per_site if s['type'] == 'School']
pairs = [jac(sets[a['id']], sets[b['id']]) for a, b in itertools.combinations(schools, 2)]
groups = {}
for gname, key in [('Nord Anglia Education', 'Nord Anglia'), ('Dulwich', 'Dulwich')]:
    gsite = next((s for s in per_site if s['name'].startswith(gname)), None)
    members = [s for s in per_site if s['type'] == 'School' and (key in s['name'] or (key == 'Nord Anglia' and s['ownership'] == 'Group' and 'Nord Anglia' in (s.get('note') or '')))]
    groups[gname] = {'group_site': gsite['name'] if gsite else None, 'members': [m['name'] for m in members]}
nae_ids = [s['id'] for s in per_site if s['name'] in ('International College Spain', 'La Côte International School Aubonne', 'Collège du Léman',
           'Collège Champittet', 'Nord Anglia International School Dublin', 'Nord Anglia International School Rotterdam (formerly AIS Rotterdam)')]
nae_pairs = [jac(sets[a], sets[b]) for a, b in itertools.combinations(nae_ids, 2)]
other_ids = [s['id'] for s in schools if s['id'] not in nae_ids]
other_pairs = [jac(sets[a], sets[b]) for a, b in itertools.combinations(other_ids, 2)]

by_region = {}
for reg in ['Europe', 'Middle East', 'Asia', 'Africa', 'Americas', 'Global']:
    ids = [s['id'] for s in per_site if s['region'] == reg]
    c = collections.Counter(t for i in ids for t in sets[i])
    by_region[reg] = {'sites': len(ids), 'top': [(t, n) for t, n in c.most_common(8)]}

summary = {
    'sites_read': N, 'sites_total': len(recs), 'pages_read': sum(len(r['pages']) for r in ok),
    'avg_top20_used': statistics.mean(s['top20_used'] for s in per_site),
    'min_top20_used': min(s['top20_used'] for s in per_site),
    'avg_top10_in_top20': statistics.mean(s['top10_in_top20'] for s in per_site),
    'sites_with_superlative': sum(1 for s in per_site if s['superlatives_used']),
    'avg_superlative_share': statistics.mean(s['superlative_share'] for s in per_site),
    'avg_pair_similarity_schools': statistics.mean(pairs),
    'avg_pair_similarity_nae': statistics.mean(nae_pairs) if nae_pairs else None,
    'avg_pair_similarity_non_nae': statistics.mean(other_pairs),
    'sites_using_5plus_of_top10': sum(1 for s in per_site if sum(1 for r in top20[:10] if r['term'] in sets[s['id']]) >= 5),
}
all_terms = sorted(stats({t for p, _ in profiles.values() for t in p}), key=lambda r: -r['sites'])[:200]
json.dump({'summary': summary, 'top20': top20, 'buzz': buzz, 'superlatives': superl, 'per_site': per_site, 'by_region': by_region,
           'skipped': skipped, 'all_terms': all_terms, 'buzz_list': sorted(BUZZ), 'super_list': sorted(SUPER)},
          open('study_results.json', 'w'), indent=1, ensure_ascii=False)
print(json.dumps(summary, indent=1))
for r in top20: print(f"{r['reach_rank']:2d} {r['term']:18s} {r['sites']:2d}/{N} prom {r['prominence']:.2f} head {r['headline_sites']:2d} impact {r['impact_score']:.2f} prank {r['prominence_rank']}")
print('SUPER', [(r['term'], r['sites'], round(r['prominence'], 2)) for r in superl[:10]])
