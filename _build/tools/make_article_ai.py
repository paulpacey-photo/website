"""Generate Article boards (desktop + mobile) for the AI article, in the same layout as
make_article.py (The Uncomfortable Truth), with extra block types for lists, a
numbered question set, a three-column guide and a sources list.

Usage: SPLIT_D=.. SPLIT_M=.. python3 make_article_ai.py OUTDIR
"""
import re, sys, os

SRC = '/home/claude/website/_build/project/'
OUT = sys.argv[1]
NAME = 'Article-AI'

SERIF = "'Newsreader', Georgia, serif"
RED, INK, BODY, MUTED, CREAM, STONE = '#A42C35', '#1E1E1E', '#2E2B28', '#6B665F', '#F6F2EC', '#E4DED5'

COVER = '/_blob/06cc3238b6ccd5de9b96e8d61a8a0377'   # zipline rider in the forest
BAND = {
    1: '/_blob/c70a6e49c666b7d98f849d327aa8ab61',   # mother hugging toddler in playground
    2: '/_blob/66216121c1359b55a182e351621e6b38',   # climbing wall
}
PORTRAIT = '/_blob/5cbcad31e477110391127e9cf157361c'
SIGNATURE = '/_blob/ed31b870cf6c1f8e89f4233c4fee7b09'

TITLE_HTML = 'AI in International School Marketing: <i>The Good, the Bad and the Ugly</i>'
DEK = 'Why schools are right to be wary of AI, why they’re wrong to give up on it, and how to tell the difference.'
READ = '9 min read'


def A(href, text):
    return (f'<a href="{href}" target="_blank" rel="noopener" style="color: inherit; text-decoration: underline; '
            f'text-decoration-color: {RED}; text-decoration-thickness: 1px; text-underline-offset: 3px">{text}</a>')


# ---- content -----------------------------------------------------------------------
# ('lead', t) ('p', t) ('h', t) ('h3', t) ('list', [(bold, text)]) ('qs', [q]) ('guide', cols)
# ('band', n, quote) ('pull', quote) ('final', t) ('sources', note, [(label, url)])
B = []
P = lambda t: B.append(('p', t))
H = lambda t: B.append(('h', t))
H3 = lambda t: B.append(('h3', t))
L = lambda items: B.append(('list', items))

B.append(('lead', 'When I first started using AI in my editing, it felt like a gift. Cables snaking across a classroom floor, a trash bin in the corner of an otherwise perfect frame, a horizontal image that needed to work as a vertical story: problems that once cost me hours disappeared in seconds.'))
P('Then I discovered video generation, and excitement turned into something closer to euphoria. A school could hire me for a photo shoot and walk away with a brand video campaign as well, built from the same images, in the same style, in a fraction of the time and at a fraction of the cost. Still images could move. Stories could have music. For the first time, I could offer far more than a set of photographs.')
P('Then came the fear. If a school could train an AI on my style, why would it ever need to hire me again?')
P('Today, I’m seeing something I didn’t expect: more and more schools are stepping back from AI content altogether. Part of me finds that reassuring. But a bigger part of me is disappointed, because in the rush to avoid the risks, schools are throwing the baby out with the bathwater.')
P('AI is neither the threat nor the miracle it first appeared to be. Used in the wrong places, it undermines the very thing school marketing exists to prove. Used in the right ones, it still has real magic to offer. This article is about telling the difference.')

H('The good: what AI already does well')
P('Start with the unglamorous wins, because they’re real.')
L([
    ('Cleaning up the frame.', 'Cables, bins, parked cars and outdated signage, gone in seconds.'),
    ('Reformatting.', 'Extending a background so a horizontal image works as a vertical story or a wide web banner.'),
    ('Protecting privacy.', 'Removing or obscuring a student in the background whose family hasn’t given consent. Here, AI solves a consent problem instead of creating one.'),
    ('Restoring the archive.', 'Bringing faded photographs back to life for an anniversary or a heritage page.'),
    ('Planning.', 'Mocking up a concept so a leadership team can approve an idea before a single frame is shot.'),
    ('Managing the library.', 'Tagging, captions and alt text that make hundreds of images searchable by theme, season or year group.'),
    ('Showing what doesn’t exist yet.', 'A clearly labeled “artist’s impression” of a new building.'),
])
P('None of these change what a real moment looked like. They save time and money, and nobody is misled.')
P('Then there’s motion. When I first animated a set of my own school photographs and set them to music, the emotion already in those images seemed to deepen. A glance lingered a moment longer; a laugh had room to breathe. The motion was generated, but the feeling was already in the photograph; the movement and the music simply amplified it. I stand by the emotional honesty of every clip.')
P('That’s the magic I don’t want schools to lose. It’s also where things get complicated.')

H('The bad: the line I didn’t see')
P('The moment I understood what was really at stake came from a client I’d worked with for more than a decade. I’d spent days on a sample reel that brought some of my favorite images from their shoot to life, and I was proud of it. I still am. I sent it expecting delight.')
P('What came back was concern, and they were right to raise it. I had been thinking like a creative. They were thinking like guardians. Those weren’t just my images; they were their students, now moving in ways no parent had agreed to, in a video the school hadn’t asked for. However beautiful the result, I had stepped over a line I hadn’t known was there.')
P('That’s the part of AI that rarely makes the headlines. The technology was never the problem. Consent was.')
B.append(('band', 1, 'I had been thinking like a creative. They were thinking <i>like guardians.</i>'))
H3('What the rules now say')
P('The law has caught up faster than most of us expected. Here’s where things stand as of October 2026. It’s a general overview, not legal advice, so check anything specific with your data protection officer or legal team.')
L([
    ('Labeling is now mandatory in the EU.', 'Since August 2, 2026, the EU AI Act has required anyone who publishes a “deepfake” to disclose that it was generated or manipulated by AI (' + A('https://www.legalithm.com/en/blog/eu-ai-act-what-applies-2-august-2026', 'Legalithm') + ').'),
    ('“Deepfake” means more than you think.', 'It isn’t limited to face swaps. It covers realistic AI-made or AI-altered images, audio or video that resemble real people, places or events and could pass as authentic (' + A('https://www.dglaw.com/eu-ai-act-guidance-expands-ai-disclosure-rules-for-advertisers-and-pr-teams/', 'Davis+Gilbert') + '). Animating a real photograph of a real student falls squarely inside it.'),
    ('Advertising gets little relief.', 'There’s a lighter regime for evidently artistic works, but the European Commission’s guidelines treat it as very narrow for advertising (' + A('https://www.twobirds.com/en/insights/2026/european-commission-adopts-final-guidelines-on-ai-act-article-50-transparency-obligations-first-impr', 'Bird &amp; Bird') + ').'),
    ('Your photo consent probably doesn’t cover it.', 'Most consent forms cover photographing students and using the images in marketing. Animating a child’s likeness with AI is a different use, and it needs consent that names it. Data protection authorities around the world have made clear that realistic AI images of identifiable people, especially children, are personal data (' + A('https://www.grcreport.com/post/global-regulators-draw-a-line-on-ai-deepfakes-as-privacy-risks-escalate', 'GRC Report') + ').'),
    ('Enforcement is national and complaint-driven.', 'Each EU country enforces the labeling rules, with fines of up to €15 million or 3% of turnover (' + A('https://www.aiactblog.nl/en/posts/article-50-enforcement-fines-ai-act-2026', 'Responsible AI Platform') + '). Early enforcement has been slow, but anyone can complain: a parent, a competitor, a journalist.'),
    ('Outside the EU, details differ.', 'Switzerland has decided against a specific deepfake law (' + A('https://www.swissinfo.ch/eng/ai-governance/switzerland-rejects-deepfake-regulation/89277391', 'Swissinfo') + '), and the UK isn’t covered by the EU Act. Data protection rules on children’s images apply everywhere.'),
])
H3('The label problem')
P('Which brings me back to my reel. I’d stand by it today. Because I made it before the new rules took effect, it doesn’t legally need a label. But if I made the same reel now, it would, and I know how that label would be read: fake. To me, the reel shows real children, real feeling and real moments, only in motion. A label tells you how something was made, not whether it’s true to what happened.')
B.append(('pull', 'A label tells you how something was made, not whether it’s true to what happened.'))
P('To be clear about what that reel did and didn’t do: I didn’t invent a single smile, and no student does anything they weren’t already doing in the photograph. The AI extended moments that really happened; it didn’t create new ones. But the motion itself was still generated. The exact turn of a head, or the way a laugh unfolds over two seconds, is the AI’s best interpretation, not a recording. I understand why a parent seeing their child move in a way no camera captured, in a video they never agreed to, might feel differently than I do. That gap between how the maker sees it and how a parent might is exactly why the label exists.')

H('The ugly: the authenticity contradiction')
P('Every school I’ve worked with says some version of the same thing: we value authenticity. Our community is real. Come and see for yourself. So here’s the question every school should ask before publishing AI imagery: how can you say you value authenticity, then present your school with images that aren’t real?')
L([
    ('Invented students.', 'On LinkedIn, I followed a long discussion about an AI tool marketed to schools that “anonymizes” students by replacing their faces with generated ones. Commenters were appalled that the results looked like idealized “poster children.” Every shoot involves casting; we photograph the students who shine in front of a camera, and there’s nothing wrong with that. But choosing real students who photograph well is very different from replacing them with students who don’t exist. The first shows your community at its best. The second shows a community you don’t have.'),
    ('The label undermines the proof.', 'Parents look at your photos for evidence of what life at your school is really like. An “AI-generated” label tells them that what they’re looking at isn’t evidence.'),
    ('Everything starts to look the same.', 'AI learns from what already exists, so it drifts toward the average. Schools already struggle to stand apart; generated imagery makes it harder.'),
    ('The safeguarding climate.', 'Parents are hearing about school photos being taken from websites and manipulated with AI (' + A('https://techround.co.uk/artificial-intelligence/ai-deepfakes-are-forcing-schools-to-rethink-child-protection/', 'TechRound') + '). In that climate, “we used AI on your child’s photo” is a hard sentence to say, however good your intentions.'),
])

H('Keeping the magic')
P('The answer isn’t to abandon AI. It’s to move it.')
P('Behind the camera, everything in “the good” list above is still open to you. Those uses save time, protect students and mislead no one.')
P('In front of the camera, one of the most exciting opportunities sits where the rules are kindest: content that is obviously not real. Picture a Primary student learning about the Stone Age who drifts into a daydream and finds herself in a prehistoric cave. Or a lesson on the planets that ends with a student standing on Mars. Nobody thinks it actually happened, so it isn’t pretending to be real. What it shows is true: what a great lesson does to a child’s imagination. And it would cut straight through the sea of identical corridor-and-classroom content most schools publish.')
B.append(('band', 2, 'The fantasy is the hook.<br>The <i>real story</i> is the payoff.'))
P('To do it well:')
L([
    ('Keep the child real; let AI build the world.', 'Film the real student and the real wonder, then place them in an AI-generated environment. The child’s face and emotion are never synthesized. You’ll still need parental consent for the use, and should check with your legal team whether a label applies, but you’re on far firmer ground.'),
    ('Bookend it with reality.', 'Start in the real classroom, drift into the daydream, and come back to the real lesson. The fantasy is the hook; your school is the payoff.'),
    ('Move early.', 'Before long, AI fantasy sequences will be everywhere. Most schools plan marketing a year at a time, and consent and approvals take time, so the schools that start now have a window of a cycle or two before it becomes the new generic.'),
])

H('A simple test before you use AI')
P('Before any AI touches an image, ask three questions:')
B.append(('qs', [
    'Is a real child’s likeness being generated or altered?',
    'Would a parent feel misled if they knew how it was made?',
    'If it needs a label, would the label hurt the message?',
]))
P('If the answer to any of them is yes, stop and think again.')
B.append(('guide', [
    ('Generally safe', ['Cleanup and retouching', 'Reformatting for different placements', 'Removing students without consent', 'Archive restoration, planning visuals, library management']),
    ('Think twice', ['Motion added to scenery or buildings', 'A real student placed in an openly imaginative world', 'Labeled renders of facilities not yet built']),
    ('Avoid', ['Animating identifiable students without specific consent', 'AI-generated “students” who don’t exist', 'Replacing real faces with generated ones']),
]))

H('The fear, answered')
P('Do I still worry that AI could reproduce my work? Less than I did. If it can’t imitate the look today, it probably will one day. But a look was never what schools were paying for. They were paying for proof: real children, at a real school, in moments that actually happened. AI can imitate a style. It can’t attend your school.')
B.append(('final', 'That’s the irony. The more convincing AI becomes, the more valuable the real thing becomes. Use AI to clear the cables, plan the shoot and dream up the trip to Mars. But when a parent looks at your website and asks, “Is this really what it’s like?”, <i>make sure the answer is yes.</i>'))
B.append(('sources', 'Legal information current as of October 2026.', [
    ('Legalithm: The EU AI Act on August 2, 2026', 'https://www.legalithm.com/en/blog/eu-ai-act-what-applies-2-august-2026'),
    ('Davis+Gilbert: EU AI Act guidance for advertisers', 'https://www.dglaw.com/eu-ai-act-guidance-expands-ai-disclosure-rules-for-advertisers-and-pr-teams/'),
    ('Bird &amp; Bird: Final Article 50 guidelines', 'https://www.twobirds.com/en/insights/2026/european-commission-adopts-final-guidelines-on-ai-act-article-50-transparency-obligations-first-impr'),
    ('GRC Report: Global regulators on AI deepfakes', 'https://www.grcreport.com/post/global-regulators-draw-a-line-on-ai-deepfakes-as-privacy-risks-escalate'),
    ('Responsible AI Platform: Article 50 enforcement and fines', 'https://www.aiactblog.nl/en/posts/article-50-enforcement-fines-ai-act-2026'),
    ('Swissinfo: Switzerland rejects deepfake regulation', 'https://www.swissinfo.ch/eng/ai-governance/switzerland-rejects-deepfake-regulation/89277391'),
    ('TechRound: AI deepfakes and child protection in schools', 'https://techround.co.uk/artificial-intelligence/ai-deepfakes-are-forcing-schools-to-rethink-child-protection/'),
]))


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
<div data-parallax="0.18" style="position: relative; height: {ch}px; overflow: hidden; background: #D8D0C4"><img data-parallax-layer="1" src="{COVER}" alt="" style="position: absolute; left: 0; top: -10%; width: 100%; height: 120%; object-fit: cover; object-position: 40% 30%; display: block"></div>
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
                f'<li style="position: relative; margin-top: {16 if m else 20}px; padding-left: {22 if m else 28}px"><span aria-hidden="true" style="position: absolute; left: 0; top: {15 if m else 17}px; width: {10 if m else 12}px; height: 1px; background: {RED}"></span><strong style="font-weight: 600; color: {INK}">{b}</strong> {x}</li>'
                for b, x in blk[1])
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
        elif k == 'band':
            n, q = blk[1], blk[2]
            h = 460 if m else 620
            body.append(f'<div data-parallax="0.28" style="position: relative; margin-top: {56 if m else 96}px; margin-bottom: {16 if m else 24}px; height: {h}px; overflow: hidden; background: #1E1E1E"><img data-parallax-layer="1" src="{BAND[n]}" alt="" style="position: absolute; left: 0; top: -18%; width: 100%; height: 136%; object-fit: cover; display: block"><div style="position: absolute; inset: 0; background: rgba(20,20,20,0.58)"></div><div data-reveal="1" style="position: relative; box-sizing: border-box; height: 100%; padding: {"0 28px" if m else "0 160px"}; display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center"><span aria-hidden="true" style="font-family: {SERIF}; font-size: {80 if m else 120}px; line-height: 0.6; height: {34 if m else 52}px; color: #CF5C65">“</span><blockquote style="margin: {18 if m else 26}px 0 0 0; max-width: 980px; font-family: {SERIF}; font-weight: 400; font-size: {30 if m else 54}px; line-height: 1.16; color: #ffffff">{q}</blockquote></div></div>')
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
