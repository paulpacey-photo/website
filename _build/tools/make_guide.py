"""Generate Guide.dc.html (desktop) and Guide-Mobile.dc.html from the Resources boards' shell."""
import re, sys, os

SRC = '/home/claude/website/_build/project/'
OUT = sys.argv[1]
HD = {'Guide.dc.html': int(sys.argv[2]) if len(sys.argv) > 2 else 9000,
      'Guide-Mobile.dc.html': int(sys.argv[3]) if len(sys.argv) > 3 else 12000}
PHOTO = '/_blob/0b79078a4c4e5f35c4f1f27a0e989e24'
PDF = 'planning-your-photo-campaign.pdf'

STEPS = [
    ('Ready.', '01', 'We align on goals, scope and price', 'It starts with listening, before anything is planned.',
     ['<b>Discovery brief:</b> your school, in your words', '<b>Website audit:</b> how closely your site reflects it',
      '<b>Discovery report:</b> what we heard, and where to focus', 'A clear scope, goals and price'], None),
    ('Ready.', '02', 'We lock in the dates and make it official', 'Once we agree on the plan, we commit to it together.',
     ['Dates agreed around your calendar and my availability', 'Contract signed', '50% deposit paid on signing'], None),
    ('Set.', '03', 'I design your list of activities', 'Your goals, turned into real moments we can photograph.',
     ['Tailor-made activities, built around your pillars and goals', 'Options for every age group',
      'Ready-to-send templates for teacher communications', 'A scheduling template to keep it simple'], None),
    ('Set.', '04', 'Your teachers tell us what’s already happening', 'The best activities are often the ones already planned.',
     ['The school shares the activity list with teachers', 'Teachers flag what’s already in their plans',
      'About one week for first responses'], None),
    ('Set.', '05', 'We find the gaps and close them', 'Every goal and every age group, covered.',
     ['We cross-reference what we have against your goals', 'We invite select teachers to fill any gaps', 'About one week'], None),
    ('Set.', '06', 'We finalize the schedule and prepare the school', 'Everyone knows what’s happening, and when.',
     ['Final schedule confirmed with every teacher', 'A reassuring, informative email to parents',
      'The non-media student list checked and up to date'], None),
    ('Shine.', '07', 'We shoot, and stay flexible', 'The plan puts us in the right place. Then we follow what’s real.',
     ['One to three days on location (two is typical)', 'Room to seize unplanned opportunities',
      'A school liaison: guide, second set of eyes and safeguarding support', 'Help with logistics and non-media students'], None),
    ('Shine.', '08', 'I deliver your final edit', None,
     ['A final edit sized to your shoot', 'My top images flagged for you', 'Enough assets to meet your media needs for two years'],
     [('~300', 'Per two-day shoot'), ('72h', 'Or as agreed'), ('2 yrs', 'Of campaign assets')]),
    ('Shine.', '09', 'We look back together', 'A campaign isn’t finished at delivery.',
     ['A follow-up call to assess the campaign’s success', 'What worked, and what we’d refine next time', 'Your honest feedback'], None),
]
PHASES = [
    ('Ready.', 'Align, agree and commit', ['01', '02'], False),
    ('Set.', 'Design, gather, close the gaps, prepare', ['03', '04', '05', '06'], False),
    ('Shine.', 'Shoot, deliver, look back', ['07', '08', '09'], True),
]
SHORT = {'01': 'Align goals, scope, price', '02': 'Lock dates, sign', '03': 'Design activities', '04': 'Teachers respond',
         '05': 'Close the gaps', '06': 'Finalize and prepare', '07': 'Shoot, stay flexible', '08': 'Deliver the edit',
         '09': 'Look back together'}

SERIF = "font-family: 'Newsreader', Georgia, serif"
LABEL = "font-size: {fs}px; font-weight: 600; letter-spacing: 0.22em; text-transform: uppercase"


def shell(name):
    s = open(SRC + name).read()
    head = s[:s.index('<!-- 2 INTRO -->')]
    cta_i = s.index('<!-- 5 CTA -->')
    tail = s[s.index('<!-- 9 FOOTER -->'):]
    return head, tail


def eyebrow(text, m, color='#6B665F', rule='#A42C35'):
    w = 24 if m else 32
    return (f'<div style="display: flex; align-items: center; gap: 16px"><span style="width: {w}px; height: 1px; background: {rule}"></span>'
            f'<span style="{LABEL.format(fs=11 if m else 12)}; color: {color}">{text}</span></div>')


def btn_primary(m, label='Download the PDF'):
    pad = '0 26px' if m else '0 32px'
    h = 54 if m else 56
    disp = 'display: flex; justify-content: center' if m else 'display: inline-flex'
    return (f'<a href="{PDF}" target="_blank" rel="noopener" style="{disp}; align-items: center; gap: 12px; height: {h}px; padding: {pad}; '
            f'background: #A42C35; color: #ffffff; font-size: 12px; font-weight: 500; letter-spacing: 0.18em; text-transform: uppercase">'
            f'{label} <span aria-hidden="true">↓</span></a>')


def hero(m):
    if m:
        return f'''<!-- 2 HERO -->
<section style="position: relative; background: #1E1E1E; color: #F6F2EC">
<div style="position: relative; height: 300px; overflow: hidden"><img src="{PHOTO}" alt="A primary student building a structure from spaghetti and gumdrops" style="position: absolute; left: 0; top: 0; width: 100%; height: 100%; object-fit: cover; object-position: 78% 40%; display: block"></div>
<div style="box-sizing: border-box; padding: 40px 24px 52px 24px">{eyebrow('Planning guide', True, '#E8848B', '#E8848B')}<h1 style="margin: 22px 0 0 0; {SERIF}; font-weight: 400; font-size: 46px; line-height: 1.03; letter-spacing: -0.01em; color: #F6F2EC"><span style="display: block">Planning Your</span><span style="display: block; font-style: italic">Photo Campaign</span></h1><p style="margin: 20px 0 0 0; font-size: 17px; line-height: 1.65; color: #E4DED5">A nine-step framework, from discovery brief to final edit.</p><div style="margin-top: 30px">{btn_primary(True)}</div><p style="margin: 14px 0 0 0; font-size: 13px; color: #CFC7BC; text-align: center">13 pages · PDF</p></div>
</section>
'''
    return f'''<!-- 2 HERO -->
<section style="position: relative; height: 640px; overflow: hidden; background: #1E1E1E; color: #F6F2EC">
<img src="{PHOTO}" alt="A primary student building a structure from spaghetti and gumdrops" style="position: absolute; left: 0; top: 0; width: 100%; height: 100%; object-fit: cover; object-position: 100% 35%; display: block">
<div style="position: absolute; left: 0; top: 0; width: 900px; height: 100%; background: linear-gradient(90deg, rgba(20,24,22,0.78) 0%, rgba(20,24,22,0.5) 60%, rgba(20,24,22,0) 100%)"></div>
<div style="position: relative; box-sizing: border-box; height: 100%; padding: 0 80px; display: flex; flex-direction: column; justify-content: center; width: 760px">{eyebrow('Planning guide', False, '#E8848B', '#E8848B')}<h1 style="margin: 30px 0 0 0; {SERIF}; font-weight: 400; font-size: 80px; line-height: 1.03; letter-spacing: -0.01em; color: #F6F2EC"><span style="display: block">Planning Your</span><span style="display: block; font-style: italic">Photo Campaign</span></h1><p style="margin: 24px 0 0 0; font-size: 19px; line-height: 1.7; color: #E4DED5; max-width: 520px">A nine-step framework, from discovery brief to final edit. Read it here, or download the PDF to share with your team.</p><div style="margin-top: 36px; display: flex; align-items: center; gap: 24px">{btn_primary(False)}<span style="font-size: 13px; letter-spacing: 0.06em; color: #CFC7BC">13 pages · PDF</span></div></div>
</section>
'''


def quote(m):
    pad = '56px 24px 60px 24px' if m else '120px 80px 120px 80px'
    qs, hs, ps = (110, 36, 17) if m else (180, 64, 20)
    qh = 52 if m else 80
    return f'''<!-- 3 QUOTE -->
<section style="box-sizing: border-box; padding: {pad}; background: #F6F2EC"><div style="max-width: 1040px"><p style="margin: 0; {SERIF}; font-size: {qs}px; line-height: 0.6; height: {qh}px; color: #A42C35" aria-hidden="true">“</p><h2 style="margin: 0; {SERIF}; font-weight: 400; font-size: {hs}px; line-height: 1.1; color: #1E1E1E">A good plan makes room for the moments <i>you can’t plan for.</i></h2><p style="margin: {20 if m else 28}px 0 0 0; font-size: {ps}px; line-height: 1.65; color: #3d3a36; max-width: 720px">We plan every detail so that, on the day, the camera can follow what’s real. Here is how the nine steps fit together.</p></div></section>
'''


def glance(m):
    cards = []
    for name, desc, nums, dark in PHASES:
        bg, fg, num, sub = ('#1E1E1E', '#F6F2EC', '#CF5C65', '#CFC7BC') if dark else ('#F6F2EC', '#1E1E1E', '#A42C35', '#6B665F')
        it = 'font-style: italic; ' if dark else ''
        items = ''.join(f'<li style="font-size: {16 if m else 17}px; line-height: 1.45; color: {fg}"><span style="color: {num}">{n}</span>&nbsp; {SHORT[n]}</li>' for n in nums)
        flex = '' if m else f'flex: {len(nums)} 1 0; '
        cards.append(f'<div style="{flex}min-width: 0; box-sizing: border-box; padding: {28 if m else 36}px; background: {bg}; display: flex; flex-direction: column; gap: 18px"><div><h3 style="margin: 0; {SERIF}; font-weight: 400; {it}font-size: {34 if m else 40}px; line-height: 1.1; color: {fg}">{name}</h3><p style="margin: 6px 0 0 0; font-size: 14px; line-height: 1.5; color: {sub}">{desc}</p></div><ul style="margin: 0; padding: 0; list-style: none; display: flex; flex-direction: column; gap: 10px">{items}</ul></div>')
    dirn = 'flex-direction: column; gap: 16px' if m else 'gap: 20px; align-items: stretch'
    pad = '56px 24px 24px 24px' if m else '112px 80px 40px 80px'
    hs = 34 if m else 52
    return f'''<!-- 4 AT A GLANCE -->
<section id="at-a-glance" style="box-sizing: border-box; padding: {pad}">{eyebrow('At a glance', m)}<h2 style="margin: {20 if m else 28}px 0 0 0; {SERIF}; font-weight: 400; font-size: {hs}px; line-height: 1.08; color: #1E1E1E">Nine steps, three phases, <i>one shared plan.</i></h2><div style="margin-top: {28 if m else 48}px; display: flex; {dirn}">{''.join(cards)}</div></section>
'''


def step(s, m, dark):
    phase, n, title, lead, bullets, stats = s
    fg, num, lead_c, li_c, line = (('#F6F2EC', '#CF5C65', '#CFC7BC', '#F6F2EC', 'rgba(246,242,236,0.16)') if dark
                                   else ('#1E1E1E', '#A42C35', '#6B665F', '#3d3a36', '#E4DED5'))
    lis = ''.join(f'<li style="padding-left: 4px">{b}</li>' for b in bullets)
    ul = f'<ul style="margin: {18 if m else 22}px 0 0 0; padding-left: 20px; font-size: {16 if m else 17}px; line-height: 1.7; color: {li_c}">{lis}</ul>'
    lead_html = f'<p style="margin: 12px 0 0 0; {SERIF}; font-style: italic; font-size: {20 if m else 22}px; line-height: 1.4; color: {lead_c}">{lead}</p>' if lead else ''
    stats_html = ''
    if stats:
        cells = ''.join(f'<div style="display: flex; flex-direction: column; gap: 6px; min-width: 0"><span style="{SERIF}; font-weight: 300; font-size: {40 if m else 56}px; line-height: 1; color: {num}">{v}</span><span style="font-size: {10 if m else 11}px; font-weight: 600; letter-spacing: 0.18em; text-transform: uppercase; color: {lead_c}">{k}</span></div>' for v, k in stats)
        stats_html = f'<div style="margin-top: 22px; display: flex; gap: {20 if m else 56}px">{cells}</div>'
    ital = 'font-style: italic; ' if dark else ''
    if m:
        return (f'<article id="step-{n}" style="box-sizing: border-box; padding: 36px 0; border-top: 1px solid {line}">'
                f'<div style="display: flex; align-items: baseline; gap: 14px"><span style="{SERIF}; font-weight: 300; font-size: 64px; line-height: 0.9; color: {num}">{n}</span>'
                f'<span style="{LABEL.format(fs=11)}; {ital}color: {num}">{phase}</span></div>'
                f'<h3 style="margin: 18px 0 0 0; {SERIF}; font-weight: 400; font-size: 28px; line-height: 1.15; color: {fg}">{title}</h3>{lead_html}{stats_html}{ul}</article>')
    return (f'<article id="step-{n}" style="box-sizing: border-box; padding: 56px 0; border-top: 1px solid {line}; display: grid; grid-template-columns: 260px minmax(0, 1fr); column-gap: 64px">'
            f'<div><span style="display: block; {SERIF}; font-weight: 300; font-size: 128px; line-height: 0.85; color: {num}">{n}</span></div>'
            f'<div style="max-width: 760px"><h3 style="margin: 4px 0 0 0; {SERIF}; font-weight: 400; font-size: 40px; line-height: 1.12; color: {fg}">{title}</h3>{lead_html}{stats_html}{ul}</div></article>')


def phases(m):
    out = []
    for i, (name, desc, nums, dark) in enumerate(PHASES):
        bg = '#1E1E1E' if dark else ('#ffffff' if i % 2 == 0 else '#F6F2EC')
        fg = '#F6F2EC' if dark else '#1E1E1E'
        sub = '#CFC7BC' if dark else '#6B665F'
        ec = '#E8848B' if dark else '#6B665F'
        rule = '#E8848B' if dark else '#A42C35'
        it = 'font-style: italic; ' if dark else ''
        steps = ''.join(step(s, m, dark) for s in STEPS if s[1] in nums)
        pad = '52px 24px 20px 24px' if m else '104px 80px 64px 80px'
        out.append(f'''<!-- PHASE {name} -->
<section id="{name.lower().strip('.')}" style="box-sizing: border-box; padding: {pad}; background: {bg}; color: {fg}">{eyebrow(f'Phase {i + 1} of 3', m, ec, rule)}<h2 style="margin: {18 if m else 24}px 0 0 0; {SERIF}; font-weight: 400; {it}font-size: {46 if m else 72}px; line-height: 1.03; color: {fg}">{name}</h2><p style="margin: 10px 0 0 0; font-size: {16 if m else 18}px; line-height: 1.6; color: {sub}">{desc}</p><div style="margin-top: {28 if m else 40}px">{steps}</div></section>
''')
    return ''.join(out)


def cta(m):
    if m:
        return f'''<!-- 5 CTA -->
<section style="box-sizing: border-box; padding: 64px 24px 56px 24px; background: #21262A; color: #ffffff"><h2 style="margin: 0; {SERIF}; font-weight: 400; font-size: 36px; line-height: 1.1; color: #ffffff"><span style="display: block">Ready to plan</span><span style="display: block; font-style: italic">yours?</span></h2><p style="margin: 16px 0 0 0; font-size: 16px; line-height: 1.65; color: #D3D7DA">It all starts with the discovery brief: your school, in your words. It takes about ten minutes.</p><a href="#discovery" style="margin-top: 28px; display: flex; align-items: center; justify-content: center; height: 54px; background: #A42C35; color: #ffffff; font-size: 12px; font-weight: 500; letter-spacing: 0.18em; text-transform: uppercase">Start your discovery brief</a><div style="margin-top: 20px; text-align: center"><a href="{PDF}" target="_blank" rel="noopener" style="display: inline-flex; align-items: center; gap: 10px; padding: 6px 0 4px 0; font-size: 12px; font-weight: 500; letter-spacing: 0.16em; text-transform: uppercase; color: #ffffff; border-bottom: 1px solid rgba(255,255,255,0.6)">Download the PDF <span aria-hidden="true">↓</span></a></div><p style="margin: 40px 0 0 0; font-size: 12px; line-height: 1.6; color: #A9B0B5">© 2026 Paul Pacey. This framework and all material in this guide are the intellectual property of Paul Pacey. Please do not copy, reproduce or distribute any part of it without written permission.</p></section>
'''
    return f'''<!-- 5 CTA -->
<section style="box-sizing: border-box; padding: 104px 80px 72px 80px; background: #21262A; color: #ffffff"><div style="display: grid; grid-template-columns: minmax(0, 1fr) auto; column-gap: 80px; align-items: center"><div><h2 style="margin: 0; {SERIF}; font-weight: 400; font-size: 52px; line-height: 1.08; color: #ffffff"><span style="display: block">Ready to plan</span><span style="display: block; font-style: italic">yours?</span></h2><p style="margin: 20px 0 0 0; max-width: 560px; font-size: 17px; line-height: 1.7; color: #D3D7DA">It all starts with the discovery brief: your school, in your words. It takes about ten minutes.</p></div><div style="display: flex; flex-direction: column; align-items: flex-start; gap: 18px"><a href="#discovery" style="display: inline-flex; align-items: center; height: 56px; padding: 0 32px; background: #A42C35; color: #ffffff; font-size: 12px; font-weight: 500; letter-spacing: 0.18em; text-transform: uppercase">Start your discovery brief</a><a href="{PDF}" target="_blank" rel="noopener" style="display: inline-flex; align-items: center; gap: 10px; padding: 6px 0 4px 0; font-size: 12px; font-weight: 500; letter-spacing: 0.16em; text-transform: uppercase; color: #ffffff; border-bottom: 1px solid rgba(255,255,255,0.6)">Download the PDF <span aria-hidden="true">↓</span></a></div></div><p style="margin: 72px 0 0 0; max-width: 900px; font-size: 12px; line-height: 1.6; color: #A9B0B5">© 2026 Paul Pacey. This framework and all material in this guide are the intellectual property of Paul Pacey. Please do not copy, reproduce or distribute any part of it without written permission.</p></section>
'''


for name, src, m in [('Guide.dc.html', 'Resources.dc.html', False), ('Guide-Mobile.dc.html', 'Resources-Mobile.dc.html', True)]:
    head, tail = shell(src)
    head = head.replace('Resources · ', 'Planning guide · ')
    w = 390 if m else 1440
    h = HD[name]
    head = re.sub(r'<div style="width: %dpx; height: \d+px;' % w, f'<div style="width: {w}px; height: {h}px;', head)
    tail = re.sub(r'"\$preview":\{"width":%d,"height":\d+\}' % w, f'"$preview":{{"width":{w},"height":{h}}}', tail)
    body = hero(m) + quote(m) + glance(m) + phases(m) + cta(m)
    os.makedirs(OUT, exist_ok=True)
    open(os.path.join(OUT, name), 'w').write(head + body + tail)
    print(name, h)
