"""Generate Article boards (desktop + mobile) for one long-form article from the Resources shell.

Usage: python3 make_article.py OUTDIR [desktopH] [mobileH]
"""
import re, sys, os, html

SRC = '/home/claude/website/_build/project/'
OUT = sys.argv[1]
NAME = 'Article-Uncomfortable-Truth'

SERIF = "'Newsreader', Georgia, serif"
RED, INK, BODY, MUTED, CREAM, STONE = '#A42C35', '#1E1E1E', '#2E2B28', '#6B665F', '#F6F2EC', '#E4DED5'

# Photos already used on the site, behind the pull-quote bands
BAND = {
    1: '/_blob/3b6f8b437059cf0da2f78b39690bed98',   # children laughing
    2: '/_blob/4e3a9d8ee137f04633bf6a310ed9f2ea',   # teacher and student
    3: '/_blob/9c30d14da3ed8313b4c30ba054b72f70',   # student concentrating
}
PORTRAIT = '/_blob/34f01390389b25089aa6720dc5b4f8f5'
SIGNATURE = '/_blob/ed31b870cf6c1f8e89f4233c4fee7b09'

TITLE = 'The Uncomfortable Truth About International School Marketing'
DEK = 'What remains when you strip the carefully worded mission statements away, and where a school’s real distinctiveness has been living all along.'
READ = '9 min read'

# ---- content: a list of blocks -------------------------------------------------
# ('p', text) ('h', heading) ('spec', text, [words]) ('band', n, quote) ('pull', quote)
# ('three', [(title, text), ...]) ('lead', text) ('final', text)
B = []
P = lambda t: B.append(('p', t))
H = lambda t: B.append(('h', t))

B.append(('lead', 'I’ve spent more than a decade on the creative front line of international schools. I’ve been in their corridors before the first bell, in their science labs and music rooms, on their playing fields in the last light of the afternoon. Through more campaigns and countries than I can count, I have developed a strong instinct about what makes one school feel different from another, and very little of it has to do with what schools say about themselves.'))
P('I’ve always been able to feel those differences, but never able to objectively quantify them. Until recently.')
H('An experiment in subtraction')
P('For some time now, I’ve been developing software designed to read a school’s website in a way that consolidates and prioritizes its positioning pillars into actionable words that would translate visually. Think of it as both a marketing audit and an action plan, used to better serve my clients.')
P('Beyond analyzing visual content (an article for another day), the software crawls a site and scores its language by prominence, measuring word frequency, visual scale and page placement. Then it does what a prospective parent rarely has time to do: it strips away the superlative, ‘fluffy’ vocabulary to reveal what lies beneath.')
P('By fluffy, I mean the words every institution reaches for when it wants to sound impressive: <i>exceptional, world-class, outstanding, excellent, limitless.</i> These words aren’t lies. Most of the schools using them are, in fact, very good. But they carry no real information. A parent can’t learn anything about a school from being told it is exceptional, because every school they are considering says the same.')
P('Once those words are gone, what remains should be the school’s real self-description, the words it has chosen to define its true character.')
P('I ran the tool on five schools with no connection to each other. Different cities, different ownership, different histories, catering to different families walking through the gates each morning.')
P('Well, their core language was almost indistinguishable. If the following sounds familiar, you’ll know what I’m talking about:')
B.append(('spec', 'In our welcoming, safe, and community-oriented environment, we provide a holistic and rigorous education that is both innovative and challenging. We empower a diverse and inclusive student body through a caring and nurturing culture, preparing global citizens to thrive in the future.',
          ['welcoming', 'safe', 'community-oriented', 'holistic', 'rigorous', 'innovative', 'challenging', 'empower', 'diverse', 'inclusive', 'caring', 'nurturing', 'global citizens', 'thrive']))
P('The vast majority of what each school presented as its distinctive character appeared, in nearly the same words, on the others’ sites. If you’d swapped their vocabularies overnight, I doubt any of their communities would have noticed.')
P('School after school, the pattern held everywhere I looked.')
H('This is not a failure')
P('The easy response to this finding is cynicism: schools are lazy, marketing is empty, it’s all the same brochure. I want to resist that, because I think it’s wrong, and because I’ve worked with enough school marketing teams to know how thoughtful and hardworking they generally are.')
P('What I found isn’t a failure of marketing. It’s what marketing looks like in a mature category that has been optimized to resonate with prospective families.')
P('When a market becomes sophisticated, when every serious participant understands its audience well, the messaging converges. Everyone learns what the discerning customer values, and everyone tells the truth about offering it. International school parents want their children to be safe, known and cared for. They want academic challenge. They want a genuinely international outlook. They want an environment where difference is welcomed rather than tolerated. Good schools provide these things, so good schools say so.')
B.append(('band', 1, 'The words are shared because the values are shared. And the values are shared <i>because they’re right.</i>'))
P('That’s the uncomfortable part. Not that schools are saying false things, but that they are all saying true things, the same true things, to the same careful parent, who is reading five or six of these websites in a single evening and finding them blurring together.')
P('The implication is quiet but significant: positioning no longer lives in the words we use. A school cannot out-word its competitors, because there are no better words left. “Caring” has no more distinctive synonym. Refining the adjectives, commissioning another round of brand language, debating whether “nurturing” or “supportive” sounds warmer: this work has a very low ceiling. It can make a school’s language clearer. It cannot make it different.')
B.append(('pull', 'A school cannot out-word its competitors, because there are no better words left.'))
P('So where does the difference go?')
H('Three places distinctiveness actually lives')
P('Looking closely at the data, and at the schools behind it, I see three places where genuine differentiation survives. None of them is in the dictionary.')
B.append(('three', [
    ('Emphasis', 'Two schools may use identical words, but they rarely assign them identical weight. One leads with academic rigor and places pastoral care lower down the page; another opens with belonging and lets examination results follow. The vocabulary is shared; the hierarchy is not.'),
    ('The non-transferable fact', 'Some statements cannot be copied onto another school’s website, because they are only true of one school. A named forty-five-year history with the IB. A partnership with a particular institution. The specific history of its founding and the explicit reason it exists. A concrete, structured commitment that parents can see and hold the school to. “We are a caring global community” could be pasted onto almost any international school’s homepage tomorrow and be true there too. A specific history cannot. These facts are the evidence behind the shared claims, and they are often underplayed, tucked into an “About Us” page while the generic adjectives take the hero banner.'),
    ('Execution', 'The third, and the one I know best, is execution: how a school actually looks, sounds and behaves when it is seen. In my world, that means the photography.'),
]))
H('What I’ve never done on a shoot')
P('Here is something that may surprise the marketing teams I work with. In all my years and hundreds of shoots, I have never once consulted a brand pyramid or a written photo brief on the day itself.')
P('I read them beforehand, of course. I respect the thinking that goes into them, and they help me understand what a school hopes to communicate. But on the day, they stay in the bag.')
P('This isn’t carelessness. It comes from something I learned early and have relearned on every shoot since: a school reveals its true spirit in front of the camera regardless of its mission statement. The real moments (the actions, interactions and reactions that make a parent stop scrolling) are as obvious as they are fleeting. A teacher leaning in to a student who has just understood something. Two children from different continents laughing at a joke neither could have explained in the other’s language. A coach’s hand on a shoulder after a missed shot.')
P('These moments last a second, sometimes less. If, in that second, I am consciously checking what I see against a brand pillar (Is this ‘nurturing’? Is this ‘rigorous’?), it’s already gone. Any attempt to recreate a second, performed version comes across as forced, which a parent can always sense.')
B.append(('band', 2, 'I don’t illustrate the mission statement. I watch, and I trust that what the school actually is <i>will show up.</i>'))
H('Photography as a mirror')
P('What the language experiment clarified for me is why that trust has always worked.')
P('If every school uses the same words, the words cannot do the distinguishing. Something else has to. And photography, done honestly, is one of the few forms of marketing that cannot simply assert a claim. It can only show what was there.')
P('That makes it something closer to a mirror than a tool. A school can write “caring” on its homepage, and it will be believed about as much as every other school that writes it. But when a camera is present for a full day, moving through classrooms and corridors without a script, the images become a test of whether what the school says and what the school does line up. When they do, the photographs carry a conviction no copy can manufacture. When they don’t, when a school’s language is warm but its interactions are guarded, or its words celebrate curiosity but its classrooms are silent rows, the camera tends to notice that too.')
P('This is why I’ve come to think of honest school photography not as decoration for a brand but as evidence for it. Parents, whether they articulate it or not, read images this way. They are looking past the words for proof.')
B.append(('band', 3, 'Not decoration for a brand, but <i>evidence for it.</i>'))
H('On making every school look the same')
P('There is a critique I’ve heard, and I think it deserves a serious answer. It goes like this: if one photographer brings the same style to many different schools (the same light, the same eye, the same approach), doesn’t that make the schools all look alike? Isn’t that the visual equivalent of the shared vocabulary?')
P('I understand the concern. But I think it has the logic backwards.')
P('Consider what a consistent style actually does. If I changed my lens, my lighting and my way of seeing for every school, each set of images would differ, but you would never know why. Was it the school, or was it me? The variation would be mine, and it would tell you nothing about the institution.')
P('When the lens stays constant, the variable that remains is the school itself. How its teachers stand with its students. How its children occupy their space. What the energy of a corridor feels like before the morning bell. How openly the parent community presents itself to someone watching honestly. Those differences are real, and they are exactly what a consistent approach allows to surface.')
B.append(('pull', 'A consistent style isn’t what makes schools look the same; it’s what makes it possible to see how different they are.'))
P('The differentiator isn’t how I make a school look. It’s how the school actually conducts itself in front of the mirror I hold up to it.')
H('What this means for schools')
P('None of this is an argument against brand strategy, careful copywriting, or the teams who produce them. Clear language matters. Shared values should be stated well. But I think schools would benefit from being honest with themselves about where that work’s returns run out.')
P('If your positioning rests on an eloquently crafted mission statement, you are competing on the one ground where everyone has already arrived at the same place. The more productive questions lie elsewhere. What do you choose to lead with, and does that reflect what you actually prioritize? Which facts about your school are true of no one else, and are they visible, or hidden three clicks deep? And when someone watches your community honestly for a day, does what they see confirm what you’ve written?')
P('That last question is the hardest, and the most valuable. It can’t be answered in a brand workshop. It can only be answered by looking.')
B.append(('final', 'After all my years behind the camera, the most useful thing I’ve learned about international school marketing is that the schools that stand out aren’t always the ones with the best mission statement. They are the ones whose words turn out to be true <i>when you look.</i>'))


# ---- rendering ----------------------------------------------------------------
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
    # title block
    out.append(f'''<!-- 2 TITLE -->
<section data-article="1" style="box-sizing: border-box; padding: {'56px 24px 44px 24px' if m else '112px 80px 72px 80px'}; background: {CREAM}"><div style="{'' if m else 'max-width: 1040px'}">{eyebrow('Article · ' + READ, m)}<h1 style="margin: {22 if m else 30}px 0 0 0; font-family: {SERIF}; font-weight: 400; font-size: {40 if m else 76}px; line-height: 1.04; letter-spacing: -0.01em; color: {INK}">The Uncomfortable Truth About <i>International School Marketing</i></h1><p style="margin: {20 if m else 28}px 0 0 0; max-width: 760px; font-family: {SERIF}; font-style: italic; font-size: {20 if m else 25}px; line-height: 1.45; color: #3d3a36">{DEK}</p><div style="margin-top: {28 if m else 40}px; display: flex; align-items: center; gap: 14px"><img src="{PORTRAIT}" alt="" style="width: 44px; height: 44px; border-radius: 50%; object-fit: cover; display: block"><div style="display: flex; flex-direction: column; gap: 2px"><span style="font-size: 15px; font-weight: 500; color: {INK}">Paul Pacey</span><span style="font-size: 13px; color: {MUTED}">Photographer to international schools · Prague</span></div></div></div></section>
''')
    # cover (placeholder) with parallax
    ch = 300 if m else 620
    out.append(f'''<!-- 3 COVER -->
<div data-parallax="0.18" style="position: relative; height: {ch}px; overflow: hidden; background: #D8D0C4"><div data-parallax-layer="1" style="position: absolute; left: 0; right: 0; top: -12%; height: 124%; background: linear-gradient(160deg, #E4DED5 0%, #CFC7BC 55%, #B9B0A4 100%); display: flex; align-items: center; justify-content: center"><span style="font-size: 11px; font-weight: 600; letter-spacing: 0.22em; text-transform: uppercase; color: {MUTED}; background: rgba(255,255,255,0.7); padding: 10px 14px">Cover image · placeholder</span></div></div>
''')
    body = []
    first_p = True
    for blk in B:
        k = blk[0]
        if k == 'lead':
            t = blk[1]
            cap = t[0]
            body.append(f'<p data-reveal="1" style="{col}; box-sizing: border-box; margin-top: {48 if m else 88}px; margin-bottom: 0; font-family: {SERIF}; font-size: {fs + 2}px; line-height: {lh}; color: {BODY}"><span style="float: left; font-family: {SERIF}; font-weight: 400; font-size: {74 if m else 96}px; line-height: 0.82; padding: {8 if m else 10}px 12px 0 0; color: {RED}">{cap}</span>{t[1:]}</p>')
        elif k == 'p':
            body.append(f'<p style="{col}; box-sizing: border-box; margin-top: {20 if m else 26}px; margin-bottom: 0; font-family: {SERIF}; font-size: {fs}px; line-height: {lh}; color: {BODY}">{blk[1]}</p>')
        elif k == 'h':
            body.append(f'<div data-reveal="1" style="{col}; box-sizing: border-box; margin-top: {52 if m else 76}px"><span style="display: block; width: 40px; height: 2px; background: {RED}"></span><h2 style="margin: {18 if m else 22}px 0 0 0; font-family: {SERIF}; font-weight: 400; font-size: {30 if m else 40}px; line-height: 1.12; color: {INK}">{blk[1]}</h2></div>')
        elif k == 'spec':
            t, words = blk[1], blk[2]
            for i, w in enumerate(sorted(words, key=len, reverse=True)):
                pass
            def mark(mm, _c=[0]):
                _c[0] += 1
                return f'<mark data-hl="{_c[0]}" style="background-color: transparent; color: inherit; padding: 0 2px">{mm.group(0)}</mark>'
            pat = re.compile(r'\b(' + '|'.join(re.escape(w) for w in sorted(words, key=len, reverse=True)) + r')\b')
            t2 = pat.sub(mark, t)
            body.append(f'<figure data-reveal="1" data-spec="1" style="{wide}; box-sizing: border-box; margin-top: {32 if m else 44}px; margin-bottom: 0; {"margin-left: 24px; margin-right: 24px; padding: 28px 22px" if m else "padding: 48px 56px"}; background: {CREAM}; border-left: 3px solid {RED}"><span style="display: block; font-size: {10 if m else 11}px; font-weight: 600; letter-spacing: 0.22em; text-transform: uppercase; color: {RED}">Sound familiar?</span><blockquote style="margin: {14 if m else 18}px 0 0 0; font-family: {SERIF}; font-style: italic; font-size: {21 if m else 28}px; line-height: 1.5; color: {INK}">“{t2}”</blockquote><figcaption style="margin-top: {14 if m else 18}px; font-size: 13px; line-height: 1.5; color: {MUTED}">The shared vocabulary of five unconnected schools, once the superlatives are stripped away.</figcaption></figure>')
        elif k == 'band':
            n, q = blk[1], blk[2]
            h = 460 if m else 620
            body.append(f'<div data-parallax="0.28" style="position: relative; margin-top: {56 if m else 96}px; height: {h}px; overflow: hidden; background: #1E1E1E"><img data-parallax-layer="1" src="{BAND[n]}" alt="" style="position: absolute; left: 0; top: -18%; width: 100%; height: 136%; object-fit: cover; display: block"><div style="position: absolute; inset: 0; background: rgba(20,20,20,0.58)"></div><div data-reveal="1" style="position: relative; box-sizing: border-box; height: 100%; padding: {"0 28px" if m else "0 160px"}; display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center"><span aria-hidden="true" style="font-family: {SERIF}; font-size: {80 if m else 120}px; line-height: 0.6; height: {34 if m else 52}px; color: #CF5C65">“</span><blockquote style="margin: {18 if m else 26}px 0 0 0; max-width: 980px; font-family: {SERIF}; font-weight: 400; font-size: {30 if m else 54}px; line-height: 1.16; color: #ffffff">{q}</blockquote></div></div>')
        elif k == 'pull':
            body.append(f'<blockquote data-reveal="1" style="{wide}; box-sizing: border-box; margin-top: {40 if m else 64}px; margin-bottom: {8 if m else 16}px; {"margin-left: 24px; margin-right: 24px; padding: 6px 0 6px 20px" if m else "padding: 8px 0 8px 40px"}; border-left: 3px solid {RED}; font-family: {SERIF}; font-weight: 400; font-size: {27 if m else 40}px; line-height: 1.22; color: {RED}">{blk[1]}</blockquote>')
        elif k == 'three':
            items = ''.join(
                f'<div data-reveal="1" style="display: {"block" if m else "grid"}; {"" if m else "grid-template-columns: 180px minmax(0, 1fr); column-gap: 40px;"} padding: {28 if m else 40}px 0; border-top: 1px solid {STONE}"><span style="display: block; font-family: {SERIF}; font-weight: 300; font-size: {64 if m else 96}px; line-height: 0.85; color: {RED}">0{i + 1}</span><div style="margin-top: {14 if m else 0}px"><h3 style="margin: 0; font-family: {SERIF}; font-weight: 400; font-size: {24 if m else 30}px; line-height: 1.2; color: {INK}">{t}</h3><p style="margin: 12px 0 0 0; font-family: {SERIF}; font-size: {fs}px; line-height: {lh}; color: {BODY}">{x}</p></div></div>'
                for i, (t, x) in enumerate(blk[1]))
            body.append(f'<div style="{wide}; box-sizing: border-box; margin-top: {28 if m else 40}px; border-bottom: 1px solid {STONE}">{items}</div>')
        elif k == 'final':
            body.append(f'<div data-reveal="1" style="{col}; box-sizing: border-box; margin-top: {48 if m else 72}px; padding-top: {32 if m else 44}px; border-top: 1px solid {INK}"><p style="margin: 0; font-family: {SERIF}; font-size: {24 if m else 32}px; line-height: 1.38; color: {INK}">{blk[1]}</p><img src="{SIGNATURE}" alt="Paul Pacey" style="display: block; margin-top: {24 if m else 32}px; width: {200 if m else 260}px; height: {76 if m else 98}px"></div>')
    top = ''.join(out); out = []
    # author + CTA
    out.append(f'''<!-- 5 AUTHOR -->
<section style="box-sizing: border-box; padding: {'0 24px 64px 24px' if m else '0 80px 120px 80px'}"><div style="{'' if m else 'width: 920px; margin: 0 auto;'} box-sizing: border-box; padding: {'28px 24px' if m else '40px 48px'}; background: {CREAM}; display: flex; {'flex-direction: column; gap: 18px' if m else 'align-items: center; gap: 36px'}"><img src="{PORTRAIT}" alt="Paul Pacey" style="width: {84 if m else 120}px; height: {84 if m else 120}px; border-radius: 50%; object-fit: cover; display: block; flex: none"><div><span style="display: block; font-size: 11px; font-weight: 600; letter-spacing: 0.22em; text-transform: uppercase; color: {RED}">About the author</span><p style="margin: 10px 0 0 0; font-family: {SERIF}; font-size: {19 if m else 21}px; line-height: 1.5; color: {INK}">Paul Pacey has photographed more than 200 campaigns for international schools in over 30 countries. He works with marketing teams to find, and show, what makes each school unmistakably itself.</p><div style="margin-top: 20px; display: flex; {'flex-direction: column; align-items: flex-start; gap: 14px' if m else 'align-items: center; gap: 32px'}"><a href="#discovery" style="display: inline-flex; align-items: center; height: {54 if m else 56}px; padding: 0 28px; background: {RED}; color: #ffffff; font-size: 12px; font-weight: 500; letter-spacing: 0.18em; text-transform: uppercase">Start your discovery brief</a><a href="#articles" style="display: inline-flex; align-items: center; gap: 10px; padding: 10px 0 4px 0; font-size: 12px; font-weight: 500; letter-spacing: 0.16em; text-transform: uppercase; color: {INK}; border-bottom: 1px solid {INK}">More articles <span aria-hidden="true">→</span></a></div></div></div></section>
''')
    return top, body, ''.join(out)


def art(blocks, m, last):
    pb = ('64px' if m else '120px') if last else '0'
    return '<!-- BODY -->\n<article style="box-sizing: border-box; padding-bottom: ' + pb + '">' + '\n'.join(blocks) + '</article>\n'


SPLIT = {False: [int(x) for x in os.environ.get('SPLIT_D', '28').split(',')], True: [int(x) for x in os.environ.get('SPLIT_M', '19,36').split(',')]}
HEIGHTS = {}
for spec in sys.argv[2:]:
    k, v = spec.split('=')
    HEIGHTS[k] = int(v)
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
        h = HEIGHTS.get(name, 7900)
        if pi == 0:
            hd = head
        else:
            hd = helmet_head
        hd = hd.replace('Resources · ', 'Article · ')
        hd = re.sub(r'<div style="width: %dpx; height: \d+px;' % w, f'<div style="width: {w}px; height: {h}px;', hd)
        tl = tail if last else tail[tail.index('</div>\n</x-dc>'):]
        tl = re.sub(r'"\$preview":\{"width":%d,"height":\d+\}' % w, f'"$preview":{{"width":{w},"height":{h}}}', tl)
        content = (top if pi == 0 else '') + art(part, m, last) + (bottom if last else '')
        open(os.path.join(OUT, name), 'w').write(hd + content + tl)
        print(name, h, len(part))
