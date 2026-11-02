"""Generate Article boards (desktop + mobile) for the AI agents article (Found, Chosen, Kept), in the same layout as
make_article.py (The Uncomfortable Truth), with extra block types for lists, a
numbered question set, a three-column guide and a sources list.

Usage: SPLIT_D=.. SPLIT_M=.. python3 make_article_ai.py OUTDIR
"""
import re, sys, os

SRC = '/home/claude/website/_build/project/'
OUT = sys.argv[1]
NAME = 'Article-Agents'

SERIF = "'Newsreader', Georgia, serif"
RED, INK, BODY, MUTED, CREAM, STONE = '#A42C35', '#1E1E1E', '#2E2B28', '#6B665F', '#F6F2EC', '#E4DED5'

COVER = '/_blob/f4cd2ccde04eadc8b2a29e6b23be876b'   # hand moving a chess piece (Paul's own photo)
COVER_POS = '50% 38%'
PH_BG = '#E4DED5'
BANDCAP = {}
BANDPOS = {}
BAND = {
    1: '/_blob/c70a6e49c666b7d98f849d327aa8ab61',   # mother hugging toddler in playground
    2: '/_blob/200e93fbf198579bd5ca3425ced56bb7',   # AI-generated: girl reading with dragon (knight trial: ddf72efe0dc45416368c00d7bf81b8da)
}
PORTRAIT = '/_blob/5cbcad31e477110391127e9cf157361c'
SIGNATURE = '/_blob/ed31b870cf6c1f8e89f4233c4fee7b09'

TITLE_HTML = 'Found, Chosen, Kept: <i>Where AI Agents Belong in School Marketing</i>'
DEK = 'The eight new hires your marketing team doesn’t need to interview.'
READ = '8 min read'


def A(href, text):
    return (f'<a href="{href}" target="_blank" rel="noopener" style="color: inherit; text-decoration: underline; '
            f'text-decoration-color: {RED}; text-decoration-thickness: 1px; text-underline-offset: 3px">{text}</a>')


# ---- content -----------------------------------------------------------------------
# ('lead', t) ('p', t) ('h', t) ('h3', t) ('list', [(bold, text)]) ('stages', cols) ('ph', caption)
# ('final', t)
B = []
P = lambda t: B.append(('p', t))
H = lambda t: B.append(('h', t))
H3 = lambda t: B.append(('h3', t))
L = lambda items: B.append(('list', items))
WHY = lambda t: P(f'<strong style="font-weight: 600; color: {INK}">Why it matters:</strong> {t}')

B.append(('lead', 'If I ran marketing at an international school today, I’d set up eight AI agents, organized around the three moments that decide enrollment: being found, being chosen, and keeping families.'))
P('For 15 years I’ve worked inside school marketing campaigns, across more than 200 shoots in over 30 countries. The pattern I see everywhere isn’t a lack of talent or ideas. It’s a lack of time. Small marketing teams carry admissions events, newsletters, social media, the website, agency briefs and the head’s latest request, all at once. The work that would make the biggest difference is usually the work nobody has time for.')
P('That’s exactly where AI agents earn their place. An agent is simply an AI assistant given one standing job: it watches, gathers, drafts and reminds, so your team can spend its time on the things only people can do. None of the eight below replaces anyone. Each one gives a busy team back a few hours a week, and between them they close the gaps where families are quietly lost.')
B.append(('stages', [
    ('Being found', 'Can families find you?', ['1. Search and AI visibility', '2. Competitor and market watch']),
    ('Being chosen', 'Do they choose you?', ['3. Enquiry follow-up', '4. Admissions funnel analyst', '5. Story finder', '6. Content repurposing']),
    ('Keeping families', 'Do they stay?', ['7. Reviews and reputation', '8. Retention signals']),
]))

H('Being found')
P('Before a family can choose you, they have to find you, and the way they search is changing fast.')
H3('1. The search and AI visibility agent')
P('More and more parents now ask an AI assistant “What’s the best international school in Zurich for a 10-year-old?” instead of typing a search into Google. The answer they get depends on what the AI can find and trust about your school.')
P('This agent checks how your school appears in Google results and in AI answers. It makes sure your key facts (curriculum, ages, fees, location, accreditation) are consistent across your website and the school directories parents use. It flags pages that search engines can’t read well, and suggests the questions your website should answer but doesn’t.')
WHY('a school that doesn’t show up in the answer never makes the shortlist, however good it is.')
H3('2. The competitor and market watch agent')
P('Most marketing teams know their direct competitors. Few have time to watch them closely.')
P('This agent keeps an eye on the schools you compete with: new campuses, fee changes, new programs, campaigns, and how their messaging is shifting. It also watches the market around you, such as a multinational announcing a new regional office, or an embassy expanding. Those are families arriving next year. Once a month it sends a short briefing: what changed, and what it might mean for you.')
WHY('positioning only works relative to the schools beside you. If everyone claims the same things, you need to know before you say them too.')

H('Being chosen')
P('Once a family has found you, the decision usually comes down to two things: how they’re treated, and whether they believe what they see.')
H3('3. The enquiry follow-up agent')
P('Most schools already put real people and real care into this stage, and rightly so. A relocating family often enquires at three or four schools in the same week, and the school that replies quickly, personally and warmly starts with a real advantage. The challenge is rarely effort. It’s timing: enquiries peak at weekends, during open days and from families in other time zones, exactly when even a well-staffed team can’t reply at once.')
P('This agent doesn’t replace your admissions team; it makes sure no family waits for them. It drafts a personal reply to every enquiry within the hour, in the family’s own language, answering their actual questions and suggesting tour dates. It keeps track of families who have gone quiet, with a gentle follow-up ready. A member of the admissions team reads and sends every message, so the personal touch your team already gives stays exactly where it is.')
WHY('every family lost at this stage cost the whole marketing budget to reach.')
H3('4. The admissions funnel analyst')
P('Admissions teams track a great deal, but the information usually lives in several places at once: the enquiry form, the admissions system, spreadsheets, email, and the notes in people’s heads. Pulling it together into one clear picture takes hours few teams have.')
P('This agent does that work continuously. It follows each stage of the journey, from enquiry to tour, application, offer and enrollment, and shows where families drop out, which sources bring the families who actually enroll, and how this year compares with last. It turns “we need more enquiries” into a sharper question, such as “we’re losing families between the tour and the application, so why?”')
WHY('you can’t fix what you can’t see, and the cheapest new families are often the ones you’re already losing.')
H3('5. The story finder')
P('This is the agent closest to my own work. Every school produces remarkable stories every single day: a science project that went somewhere unexpected, a student who found her voice in drama, a teacher who turned a field trip into a lesson nobody will forget. Most never reach the marketing team.')
B.append(('img', '/_blob/1e8e7e78be9304821096f7d053d698e2', 'Teachers, parents and young students walking hand in hand along a leafy school path', 'A moment like this rarely makes it to the marketing team.'))
P('This agent gathers them from where they already live: newsletters, teacher posts, the school calendar, class blogs. It flags the moments worth telling, and builds a content calendar from them. It also knows what’s coming up, so the moments worth capturing on camera are planned for, not discovered afterwards.')
WHY('parents don’t choose a school because of its claims. They choose it because of the moments that make those claims believable.')
H3('6. The content repurposing agent')
P('A good story deserves more than one outing. This agent takes one strong story and drafts the versions each channel needs: a newsletter item, two or three social posts, a website update, a line for the admissions email. Everything is written in your school’s voice, and your team edits before anything goes out.')
WHY('it multiplies the value of every story, without multiplying the team’s workload.')

H('Keeping families')
P('Enrollment doesn’t end on the first day of school. Your current families are your most trusted marketing channel, and the families you keep never have to be won again.')
H3('7. The reviews and reputation agent')
P('What parents say about you online now carries as much weight as anything you say yourself. This agent watches your Google reviews, parent forums and expat community groups. It drafts thoughtful replies to reviews for your team to approve, and flags any concern early, before a single unhappy post becomes a thread everyone reads.')
WHY('relocating families trust other parents more than any brochure. You want to know what they’re hearing.')
H3('8. The retention signals agent')
P('Families rarely leave without warning. The signs are usually there: lower scores in a parent survey, a re-enrollment form that hasn’t come back, a sibling’s application that quietly stalls. The trouble is that these signals sit in different places, seen by different people.')
P('This agent brings them together and gives your team a short list of families who may need a personal conversation. What happens next stays human: a call from the right teacher or the head, at the right time.')
WHY('keeping a family costs far less than finding a new one, and a family that stays becomes your best advocate.')

H('Three lines I wouldn’t cross')
P('Agents make a small team far more capable. They also make it easier to cut corners that matter. Schools hold something more precious than most businesses do: the trust of families with their children. So I’d hold three firm lines.')
B.append(('img', '/_blob/ce47ad2c99d5145d480f0d9da495d8c6', 'A smiling student looks up from his work in class', 'Real students, in a real classroom. Parents can tell the difference.'))
L([
    ('Keep children’s data out of it.', 'Student names, photos, records and anything that identifies a child stay out of AI tools unless your data protection set-up is watertight, and your data protection lead has signed it off. Most of these agents don’t need student data at all.'),
    ('A person sends every message to a family.', 'Agents draft; people decide. One clumsy automated email, with the wrong name or the wrong tone at the wrong moment, can undo years of goodwill.'),
    ('No AI-generated “students.”', 'It’s tempting to fill a gap in your image library with a generated picture. Don’t. Parents are choosing a real community, and the moment they suspect your pictures aren’t real, they start to wonder what else isn’t. In an age of AI imagery, authenticity is your strongest asset.'),
])

H('Where to start')
P('Don’t build all eight at once. Start where your team is stretched thinnest, prove it works, then add the next.')
P('In my experience, admissions is usually the best-resourced part of a school’s marketing effort. The gaps tend to sit around it: the stories that never get told, the AI answers nobody is checking, and the families who quietly drift away. That’s where I’d begin:')
L([
    ('1. The story finder.', 'It feeds every channel you have, and every campaign you’ll run.'),
    ('2. Search and AI visibility.', 'It decides whether families find you at all, and almost nobody is watching it yet.'),
    ('3. Retention signals.', 'It protects the families you’ve already won.'),
])
P('The rest can follow as your team gets comfortable working alongside them.')
B.append(('final', 'Technology won’t make a school worth choosing. That part is already there, in your classrooms, every day. What agents can do is give your team the time to find it, tell it well and make sure the right families see it. You don’t need to manufacture a story. <i>Just hold up a mirror to the magic that’s already there.</i>'))


# ---- rendering (same styles as make_article.py) ------------------------------------
def shell(name):
    s = open(SRC + name).read()
    head = s[:s.index('<!-- 2 INTRO -->')]
    tail = s[s.index('<!-- 9 FOOTER -->'):]
    return head, tail


def eyebrow(text, m, color=MUTED):
    w = 24 if m else 32
    return (f'<div style="display: flex; align-items: center; gap: 16px"><span style="width: {w}px; height: 1px; background: {RED}"></span>'
            f'<span style="font-size: {11 if m else 12}px; font-weight: 600; letter-spacing: 0.22em; text-transform: uppercase; color: {color}">{text}</span></div>')


def render(m):
    col = 'padding: 0 24px' if m else 'width: 680px; margin: 0 auto'
    wide = 'padding: 0 24px' if m else 'width: 920px; margin: 0 auto'
    fs, lh = (19, 1.7) if m else (21, 1.72)
    out = []
    out.append(f'''<!-- 2 TITLE -->
<section data-article="1" style="box-sizing: border-box; padding: {'56px 24px 44px 24px' if m else '112px 80px 72px 80px'}; background: {CREAM}"><div style="{'' if m else 'max-width: 1040px'}">{eyebrow('Article · ' + READ, m)}<h1 style="margin: {22 if m else 30}px 0 0 0; font-family: {SERIF}; font-weight: 400; font-size: {40 if m else 76}px; line-height: 1.04; letter-spacing: -0.01em; color: {INK}">{TITLE_HTML}</h1><p style="margin: {20 if m else 28}px 0 0 0; max-width: 760px; font-family: {SERIF}; font-style: italic; font-size: {20 if m else 25}px; line-height: 1.45; color: #3d3a36">{DEK}</p><div style="margin-top: {28 if m else 40}px; display: flex; align-items: center; gap: 14px"><img src="{PORTRAIT}" alt="" style="width: 44px; height: 44px; border-radius: 50%; object-fit: cover; display: block"><div style="display: flex; flex-direction: column; gap: 2px"><span style="font-size: 15px; font-weight: 500; color: {INK}">Paul Pacey</span><span style="font-size: 13px; color: {MUTED}">Photographer to international schools · Prague</span></div></div></div></section>
''')
    ch = 300 if m else 620
    out.append(f'''<!-- 3 COVER -->
<div data-parallax="0.18" style="position: relative; height: {ch}px; overflow: hidden; background: {PH_BG}">{'' if COVER is None else f'<img data-parallax-layer="1" src="{COVER}" alt="A student’s hand moving a chess piece mid-game" style="position: absolute; left: 0; top: -10%; width: 100%; height: 120%; object-fit: cover; object-position: {COVER_POS}; display: block">'}</div>
''')
    body = []
    for blk in B:
        k = blk[0]
        if k == 'lead':
            t = blk[1]
            body.append(f'<p data-reveal="1" style="{col}; box-sizing: border-box; margin-top: {48 if m else 88}px; margin-bottom: 0; font-family: {SERIF}; font-size: {fs + 2}px; line-height: {lh}; color: {BODY}"><span style="float: left; font-family: {SERIF}; font-weight: 400; font-size: {74 if m else 96}px; line-height: 0.82; padding: {8 if m else 10}px 12px 0 0; color: {RED}">{t[0]}</span>{t[1:]}</p>')
        elif k == 'p':
            body.append(f'<p style="{col}; box-sizing: border-box; margin-top: {20 if m else 26}px; margin-bottom: 0; font-family: {SERIF}; font-size: {fs}px; line-height: {lh}; color: {BODY}">{blk[1]}</p>')
        elif k == 'h':
            body.append(f'<div data-reveal="1" style="{col}; box-sizing: border-box; margin-top: {52 if m else 76}px"><span style="display: block; width: 40px; height: 2px; background: {RED}"></span><h2 style="margin: {18 if m else 22}px 0 0 0; font-family: {SERIF}; font-weight: 400; font-size: {30 if m else 40}px; line-height: 1.12; color: {INK}">{blk[1]}</h2></div>')
        elif k == 'h3':
            body.append(f'<h3 data-reveal="1" style="{col}; box-sizing: border-box; margin-top: {40 if m else 56}px; margin-bottom: 0; font-size: {11 if m else 12}px; font-weight: 600; letter-spacing: 0.22em; text-transform: uppercase; color: {RED}">{blk[1]}</h3>')
        elif k == 'list':
            items = ''.join(
                f'<li style="position: relative; margin-top: {16 if m else 20}px; padding-left: {22 if m else 28}px">{(f'<span aria-hidden="true" style="position: absolute; left: 0; top: {3 if m else 4}px; font-family: {SERIF}; font-size: {26 if m else 30}px; line-height: 1; color: {RED}">*</span>' if it[2:] == ('*',) else f'<span aria-hidden="true" style="position: absolute; left: 0; top: {15 if m else 17}px; width: {10 if m else 12}px; height: 1px; background: {RED}"></span>')}<strong style="font-weight: 600; color: {INK}">{it[0]}</strong> {it[1]}</li>'
                for it in blk[1])
            body.append(f'<ul style="{col}; box-sizing: border-box; list-style: none; margin-top: {6 if m else 8}px; margin-bottom: 0; font-family: {SERIF}; font-size: {fs}px; line-height: {lh}; color: {BODY}">{items}</ul>')
        elif k == 'qs':
            items = ''.join(
                f'<div data-reveal="1" style="display: grid; grid-template-columns: {"56px" if m else "110px"} minmax(0, 1fr); align-items: baseline; padding: {22 if m else 30}px 0; border-top: 1px solid {STONE}"><span style="font-family: {SERIF}; font-weight: 300; font-size: {48 if m else 72}px; line-height: 0.85; color: {RED}">0{i + 1}</span><p style="margin: 0; font-family: {SERIF}; font-size: {23 if m else 30}px; line-height: 1.3; color: {INK}">{q}</p></div>'
                for i, q in enumerate(blk[1]))
            body.append(f'<div style="{wide}; box-sizing: border-box; margin-top: {24 if m else 36}px; border-bottom: 1px solid {STONE}">{items}</div>')
        elif k == 'guide':
            cols = ''.join(
                f'<div style="box-sizing: border-box; padding: {"22px 22px 24px 22px" if m else "30px 30px 34px 30px"}; background: {CREAM if i < 2 else "#F3E7E5"}; border-top: 3px solid {[INK, MUTED, RED][i]}"><span style="display: block; font-size: 11px; font-weight: 600; letter-spacing: 0.22em; text-transform: uppercase; color: {[INK, MUTED, RED][i]}">{title}</span><ul style="list-style: none; margin: {12 if m else 16}px 0 0 0; padding: 0">'
                + ''.join(f'<li style="margin-top: 10px; font-family: {SERIF}; font-size: {17 if m else 18}px; line-height: 1.45; color: {BODY}">{x}</li>' for x in items)
                + '</ul></div>'
                for i, (title, items) in enumerate(blk[1]))
            body.append(f'<div data-reveal="1" style="{wide}; box-sizing: border-box; margin-top: {28 if m else 40}px; display: grid; grid-template-columns: {"1fr" if m else "repeat(3, minmax(0, 1fr))"}; gap: {14 if m else 20}px">{cols}</div>')
        elif k == 'stages':
            cols = ''.join(
                f'<div style="box-sizing: border-box; padding: {"22px 22px 24px 22px" if m else "28px 28px 32px 28px"}; background: {CREAM}; border-top: 3px solid {RED}"><span style="display: block; font-size: 11px; font-weight: 600; letter-spacing: 0.22em; text-transform: uppercase; color: {RED}">{title}</span><p style="margin: 8px 0 0 0; font-family: {SERIF}; font-style: italic; font-size: {17 if m else 18}px; line-height: 1.4; color: {MUTED}">{q}</p><ul style="list-style: none; margin: {12 if m else 16}px 0 0 0; padding: {12 if m else 16}px 0 0 0; border-top: 1px solid {STONE}">'
                + ''.join(f'<li style="margin-top: 8px; font-family: {SERIF}; font-size: {17 if m else 18}px; line-height: 1.45; color: {INK}">{x}</li>' for x in items)
                + '</ul></div>'
                for i, (title, q, items) in enumerate(blk[1]))
            body.append(f'<div data-reveal="1" style="{wide}; box-sizing: border-box; margin-top: {32 if m else 48}px; display: grid; grid-template-columns: {"1fr" if m else "repeat(3, minmax(0, 1fr))"}; gap: {14 if m else 20}px">{cols}</div>')
        elif k == 'img':
            _, src, alt, cap = blk
            capt = (f'<figcaption style="margin-top: 12px; font-size: {13 if m else 14}px; line-height: 1.5; color: {MUTED}">{cap}</figcaption>') if cap else ''
            mm = '; margin-left: 0; margin-right: 0' if m else ''
            body.append(f'<figure data-reveal="1" style="{wide}; box-sizing: border-box; margin-top: {32 if m else 48}px; margin-bottom: 0{mm}"><img src="{src}" alt="{alt}" style="display: block; width: 100%; aspect-ratio: 3 / 2; object-fit: cover"></figure>'.replace('</figure>', capt + '</figure>'))
        elif k == 'ph':
            cap = blk[1]
            capt = (f'<figcaption style="margin-top: 12px; font-size: {13 if m else 14}px; line-height: 1.5; color: {MUTED}">{cap}</figcaption>') if cap else ''
            mm = '; margin-left: 0; margin-right: 0' if m else ''
            body.append(f'<figure style="{wide}; box-sizing: border-box; margin-top: {32 if m else 48}px; margin-bottom: 0{mm}"><div style="width: 100%; aspect-ratio: 3 / 2; background: {PH_BG}"></div>{capt}</figure>')
        elif k == 'band':
            n, q = blk[1], blk[2]
            h = 460 if m else 620
            body.append(f'<div data-parallax="0.28" style="position: relative; margin-top: {56 if m else 96}px; margin-bottom: {16 if m else 24}px; height: {h}px; overflow: hidden; background: #1E1E1E"><img data-parallax-layer="1" src="{BAND[n]}" alt="" style="position: absolute; left: 0; top: -18%; width: 100%; height: 136%; object-fit: cover; object-position: {BANDPOS.get(n, 'center')}; display: block"><div style="position: absolute; inset: 0; background: rgba(20,20,20,0.58)"></div>{('<span style="position: absolute; right: ' + ('16px' if m else '24px') + '; bottom: 12px; z-index: 2; font-family: Jost, sans-serif; font-size: 10px; letter-spacing: 0.14em; text-transform: uppercase; color: rgba(255,255,255,0.72)">' + BANDCAP[n] + '</span>') if n in BANDCAP else ''}<div data-reveal="1" style="position: relative; box-sizing: border-box; height: 100%; padding: {"0 28px" if m else "0 160px"}; display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center"><span aria-hidden="true" style="font-family: {SERIF}; font-size: {80 if m else 120}px; line-height: 0.6; height: {34 if m else 52}px; color: #CF5C65">“</span><blockquote style="margin: {18 if m else 26}px 0 0 0; max-width: 980px; font-family: {SERIF}; font-weight: 400; font-size: {30 if m else 54}px; line-height: 1.16; color: #ffffff">{q}</blockquote></div></div>')
        elif k == 'video':
            _, src, poster, orig, vw, vh, alt, cap = blk
            btn = f'font-family: inherit; font-size: {11 if m else 12}px; font-weight: 600; letter-spacing: 0.16em; text-transform: uppercase; padding: {"9px 14px" if m else "10px 18px"}; border: 1px solid {INK}; cursor: pointer; -webkit-tap-highlight-color: transparent'
            toggle = (f'<div role="group" aria-label="Compare the original photo with the animated version" style="display: flex; margin-bottom: 12px">'
                      f'<button type="button" data-show="photo" aria-pressed="false" style="{btn}; background: transparent; color: {INK}">Original photo</button>'
                      f'<button type="button" data-show="video" aria-pressed="true" style="{btn}; margin-left: -1px; background: {INK}; color: #FFFFFF">Animated with AI</button></div>') if orig else ''
            photo = (f'<img data-compare-photo="1" src="{orig}" alt="The original photograph" loading="lazy" style="position: absolute; inset: 0; display: block; width: 100%; height: 100%; object-fit: cover; opacity: 0; transition: opacity 0.35s ease; pointer-events: none">') if orig else ''
            body.append(f'<figure data-reveal="1"{" data-compare=\"1\"" if orig else ""} style="{col}; box-sizing: border-box; margin-top: {36 if m else 52}px; margin-bottom: 0{"; margin-left: 0; margin-right: 0" if m else ""}">{toggle}'
                        f'<div style="position: relative; width: 100%; aspect-ratio: {vw} / {vh}; background: #E8E2D8; overflow: hidden">'
                        f'<video data-autovideo="1" muted loop playsinline preload="none" poster="{poster}" aria-label="{alt}" style="position: absolute; inset: 0; display: block; width: 100%; height: 100%; object-fit: cover"><source data-src="{src}" type="video/mp4"></video>{photo}</div>'
                        f'<figcaption style="margin-top: 12px; font-size: {13 if m else 14}px; line-height: 1.5; color: {MUTED}">{cap}</figcaption></figure>')
        elif k == 'pull':
            body.append(f'<blockquote data-reveal="1" style="{wide}; box-sizing: border-box; margin-top: {40 if m else 64}px; margin-bottom: {8 if m else 16}px; {"margin-left: 24px; margin-right: 24px; padding: 6px 0 6px 20px" if m else "padding: 8px 0 8px 40px"}; border-left: 3px solid {RED}; font-family: {SERIF}; font-weight: 400; font-size: {27 if m else 40}px; line-height: 1.22; color: {RED}">{blk[1]}</blockquote>')
        elif k == 'final':
            body.append(f'<div data-reveal="1" style="{col}; box-sizing: border-box; margin-top: {48 if m else 72}px; padding-top: {32 if m else 44}px; border-top: 1px solid {INK}"><p style="margin: 0; font-family: {SERIF}; font-size: {24 if m else 32}px; line-height: 1.38; color: {INK}">{blk[1]}</p><img src="{SIGNATURE}" alt="Paul Pacey" style="display: block; margin-top: {24 if m else 32}px; margin-left: auto; width: {260 if m else 380}px; height: {98 if m else 143}px"></div>')
        elif k == 'sources':
            note, items = blk[1], blk[2]
            lis = ''.join(f'<li style="margin-top: 8px">{A(u, t)}</li>' for t, u in items)
            body.append(f'<div style="{col}; box-sizing: border-box; margin-top: {48 if m else 64}px; padding-top: {24 if m else 28}px; border-top: 1px solid {STONE}"><span style="display: block; font-size: 11px; font-weight: 600; letter-spacing: 0.22em; text-transform: uppercase; color: {MUTED}">Sources</span><p style="margin: 8px 0 0 0; font-size: 14px; line-height: 1.6; color: {MUTED}">{note} This article is a general overview, not legal advice.</p><ul style="list-style: none; margin: 6px 0 0 0; padding: 0; font-size: 14px; line-height: 1.55; color: #3d3a36">{lis}</ul></div>')
    top = ''.join(out)
    bottom = f'''<!-- 5 AUTHOR -->
<section style="box-sizing: border-box; padding: {'0 24px 64px 24px' if m else '0 80px 120px 80px'}"><div style="{'' if m else 'width: 920px; margin: 0 auto;'} box-sizing: border-box; padding: {'28px 24px' if m else '40px 48px'}; background: {CREAM}; display: flex; {'flex-direction: column; gap: 18px' if m else 'align-items: center; gap: 36px'}"><img src="{PORTRAIT}" alt="Paul Pacey" style="width: {84 if m else 120}px; height: {84 if m else 120}px; border-radius: 50%; object-fit: cover; display: block; flex: none"><div><span style="display: block; font-size: 11px; font-weight: 600; letter-spacing: 0.22em; text-transform: uppercase; color: {RED}">About the author</span><p style="margin: 10px 0 0 0; font-family: {SERIF}; font-size: {19 if m else 21}px; line-height: 1.5; color: {INK}">Paul Pacey has photographed more than 200 campaigns for international schools in over 30 countries. He works with marketing teams to find, and show, what makes each school unmistakably itself.</p><div style="margin-top: 20px; display: flex; {'flex-direction: column; align-items: flex-start; gap: 14px' if m else 'align-items: center; gap: 32px'}"><a href="#discovery" style="display: inline-flex; align-items: center; height: {54 if m else 56}px; padding: 0 28px; background: {RED}; color: #ffffff; font-size: 12px; font-weight: 500; letter-spacing: 0.18em; text-transform: uppercase">Start your discovery brief</a><a href="#articles" style="display: inline-flex; align-items: center; gap: 10px; padding: 10px 0 4px 0; font-size: 12px; font-weight: 500; letter-spacing: 0.16em; text-transform: uppercase; color: {INK}; border-bottom: 1px solid {INK}">More articles <span aria-hidden="true">→</span></a></div></div></div></section>
'''
    return top, body, bottom


def art(blocks, m, last):
    pb = ('64px' if m else '120px') if last else '0'
    return '<!-- BODY -->\n<article style="box-sizing: border-box; padding-bottom: ' + pb + '">' + '\n'.join(blocks) + '</article>\n'


SPLIT = {False: [int(x) for x in os.environ.get('SPLIT_D', '23').split(',')], True: [int(x) for x in os.environ.get('SPLIT_M', '20,38').split(',')]}
os.makedirs(OUT, exist_ok=True)
for src, m in [('Resources.dc.html', False), ('Resources-Mobile.dc.html', True)]:
    head, tail = shell(src)
    helmet_head = head[:head.index('<!-- 1 HEADER -->')]
    w = 390 if m else 1440
    top, blocks, bottom = render(m)
    cuts = [0] + SPLIT[m] + [len(blocks)]
    parts = [blocks[cuts[i]:cuts[i + 1]] for i in range(len(cuts) - 1)]
    for pi, part in enumerate(parts):
        last = pi == len(parts) - 1
        suffix = ('-Mobile' if m else '') + ('' if pi == 0 else f'-{pi + 1}')
        name = NAME + suffix + '.dc.html'
        h = 7900
        hd = head if pi == 0 else helmet_head
        hd = hd.replace('Resources · ', 'Article · ')
        hd = re.sub(r'<div style="width: %dpx; height: \d+px;' % w, f'<div style="width: {w}px; height: {h}px;', hd)
        tl = tail if last else tail[tail.index('</div>\n</x-dc>'):]
        tl = re.sub(r'"\$preview":\{"width":%d,"height":\d+\}' % w, f'"$preview":{{"width":{w},"height":{h}}}', tl)
        content = (top if pi == 0 else '') + art(part, m, last) + (bottom if last else '')
        open(os.path.join(OUT, name), 'w').write(hd + content + tl)
        print(name, len(part))
print('blocks', len(B))
