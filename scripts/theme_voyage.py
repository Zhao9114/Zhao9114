"""Theme 2: NIGHT VOYAGE. Deep navy sea, moonlight and gold."""
from common import *  # noqa: F403

THEME = "voyage"
NAVY, NAVY2, CARD = "#0a1628", "#0d2440", "#0e1d35"
GOLD, FOAM, MUTED, TEAL, RED = "#f4c95d", "#e8dcc0", "#8aa4c4", "#1f8a8a", "#e5484d"
FONTS = [("pirata", "Pirata"), ("inter", "Inter"), ("inter-bold", "InterB"), ("fira", "Fira")]

BASE_CSS = f"""
.pir{{font-family:Pirata,serif;fill:{GOLD}}}
.sans{{font-family:Inter,system-ui,sans-serif;fill:{FOAM}}}
.b{{font-family:InterB,system-ui,sans-serif}}
.mono{{font-family:Fira,monospace}}
.muted{{fill:{MUTED}}}
.gold{{fill:{GOLD}}}
.tw{{animation:tw 3.5s ease-in-out infinite}}@keyframes tw{{0%,100%{{opacity:.25}}50%{{opacity:1}}}}
"""

SHIP = f"""
<g>
  <path d="M-62,10 L66,10 L52,36 Q0,44 -50,36 Z" fill="#4a2c16" stroke="{GOLD}" stroke-width="1.6"/>
  <path d="M-58,18 L60,18" stroke="{GOLD}" stroke-opacity=".5"/>
  <circle cx="-30" cy="26" r="2.4" fill="{GOLD}"/><circle cx="-8" cy="27" r="2.4" fill="{GOLD}"/><circle cx="14" cy="27" r="2.4" fill="{GOLD}"/><circle cx="36" cy="26" r="2.4" fill="{GOLD}"/>
  <line x1="-22" y1="10" x2="-22" y2="-70" stroke="{FOAM}" stroke-width="2.4"/>
  <line x1="18" y1="10" x2="18" y2="-56" stroke="{FOAM}" stroke-width="2.2"/>
  <path d="M-22,-64 Q6,-44 -22,-22 Z" fill="#f3ead6"/>
  <path d="M-22,-20 Q10,-6 -22,6 Z" fill="#e9dcc0"/>
  <path d="M18,-50 Q40,-34 18,-16 Z" fill="#f3ead6"/>
  <path d="M18,-14 Q42,-4 18,8 Z" fill="#e9dcc0"/>
  <path d="M66,10 L92,-6" stroke="{FOAM}" stroke-width="1.6"/>
  <path d="M-22,-70 L-44,-64 L-22,-58 Z" fill="{RED}" class="flap"/>
  <g transform="translate(-26 -44) scale(.32)">{emblem('#3b2a1a', '#f3ead6')}</g>
  <circle cx="60" cy="2" r="3" fill="#ffd27a"/><circle cx="60" cy="2" r="9" fill="#ffd27a" opacity=".25" class="tw"/>
</g>"""


def hero() -> str:
    W, H = 1000, 400
    MX, MY = 610, 82
    waves = ""
    for i, (y, amp, color, dur) in enumerate([(300, 9, "#0f2f52", 14), (322, 11, "#123a63", 10), (350, 13, "#16477a", 7)]):
        waves += f'<path d="{wave_path(y, amp, 250, 1500, H + 10)}" fill="{color}" class="wv" style="animation-duration:{dur}s"/>'
        waves += f'<path d="{wave_path(y, amp, 250, 1500, H + 10)}" fill="none" stroke="#5ff3e0" stroke-width="1.4" stroke-opacity=".35" class="wv glow" style="animation-duration:{dur}s;animation-delay:-{i}s"/>'
        if i == 1:
            waves += f'<g transform="translate(760 300)"><g class="bob">{SHIP}</g></g>'
    shimmer = "".join(
        f'<rect x="{MX - 18 + (k % 3) * 8 - k * 2}" y="{304 + k * 9}" width="{36 - k * 3}" height="2" rx="1" fill="#f6e7b8" class="tw" style="animation-delay:{k * 0.4:.1f}s"/>'
        for k in range(8)
    )
    import random as _r
    rnd = _r.Random(21)
    sparks = "".join(
        f'<circle cx="{rnd.uniform(20, 980):.0f}" cy="{rnd.uniform(330, 395):.0f}" r="{rnd.choice([1.2, 1.6, 2])}" fill="#7dfbe8" class="tw" style="animation-delay:{rnd.uniform(0, 4):.1f}s"/>'
        for _ in range(26)
    )
    shooting = "".join(
        f'<g class="shoot" style="animation-delay:{d}s;animation-duration:{dur}s"><line x1="{x}" y1="{y}" x2="{x + 90}" y2="{y - 34}" stroke="url(#trail)" stroke-width="2" stroke-linecap="round"/></g>'
        for x, y, d, dur in ((380, 70, 0, 7), (700, 40, 3.5, 9), (180, 130, 6, 11))
    )
    lighthouse = f"""
<g transform="translate(940 300)">
  <path d="M-46,4 Q-30,-14 0,-16 Q34,-14 50,6 Z" fill="#0b1a2c"/>
  <g class="beam"><polygon points="0,-104 -340,-150 -340,-58" fill="url(#beam)"/></g>
  <path d="M-12,-14 L-8,-96 L8,-96 L12,-14 Z" fill="#e8dcc0"/>
  <path d="M-11,-40 L11,-40 L10,-56 L-10,-56 Z M-9,-72 L9,-72 L8.5,-86 L-8.5,-86 Z" fill="{RED}"/>
  <rect x="-10" y="-112" width="20" height="16" rx="2" fill="#ffd27a" class="lamp"/>
  <path d="M-13,-112 L0,-124 L13,-112 Z" fill="#1d2f47"/>
</g>"""
    tag = wrap(TAGLINE, 52)
    body = f"""
<defs>
  <linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#050b18"/><stop offset=".75" stop-color="{NAVY2}"/></linearGradient>
  <radialGradient id="glow"><stop offset="0" stop-color="#f6e7b8" stop-opacity=".45"/><stop offset="1" stop-color="#f6e7b8" stop-opacity="0"/></radialGradient>
  <linearGradient id="beam" x1="1" y1="0" x2="0" y2="0"><stop offset="0" stop-color="#ffe9a8" stop-opacity=".55"/><stop offset="1" stop-color="#ffe9a8" stop-opacity="0"/></linearGradient>
  <linearGradient id="trail" x1="1" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
  <filter id="soft"><feGaussianBlur stdDeviation="7"/></filter>
  <clipPath id="c"><rect width="{W}" height="{H}" rx="16"/></clipPath>
</defs>
<g clip-path="url(#c)">
  <rect width="{W}" height="{H}" fill="url(#sky)"/>
  {stars(80, W, 260)}
  {shooting}
  <circle cx="{MX}" cy="{MY}" r="100" fill="url(#glow)"/>
  <circle cx="{MX}" cy="{MY}" r="32" fill="#f6e7b8"/>
  <circle cx="{MX - 11}" cy="{MY - 7}" r="6" fill="#e6d29a" opacity=".6"/><circle cx="{MX + 10}" cy="{MY + 11}" r="4.5" fill="#e6d29a" opacity=".6"/>
  {lighthouse}
  {waves}
  {shimmer}
  {sparks}
</g>
<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="16" fill="none" stroke="{GOLD}" stroke-opacity=".25"/>
<text x="60" y="94" class="sans b muted" font-size="13" letter-spacing="3">AHOY, I'M</text>
<text x="60" y="152" class="pir" font-size="66" filter="url(#soft)" opacity=".55">{esc(NAME)}</text>
<text x="60" y="152" class="pir" font-size="66">{esc(NAME)}</text>
<text x="62" y="186" class="sans" font-size="17">{esc(ROLE)}  \u00b7  {esc(ORIGIN)}</text>
{''.join(f'<text x="62" y="{218 + i * 22}" class="sans muted" font-size="15">{esc(l)}</text>' for i, l in enumerate(tag))}
<text x="62" y="276" class="mono gold" font-size="14">&gt; {esc(PRINCIPLE.lower())}</text>
<rect x="{62 + 6 + (len(PRINCIPLE) + 2) * 8.43:.0f}" y="264" width="8" height="15" fill="{GOLD}" class="blink"/>
"""
    css = BASE_CSS + f"""
.wv{{animation:dr linear infinite}}@keyframes dr{{to{{transform:translateX(-250px)}}}}
.glow{{animation-name:dr,gl}}@keyframes gl{{0%,100%{{stroke-opacity:.15}}50%{{stroke-opacity:.6}}}}
.bob{{animation:bob 5s ease-in-out infinite;transform-origin:0 20px}}
@keyframes bob{{0%,100%{{transform:translateY(0) rotate(-2.5deg)}}50%{{transform:translateY(7px) rotate(2.5deg)}}}}
.flap{{transform-box:fill-box;transform-origin:right center;animation:fl 1s ease-in-out infinite alternate}}@keyframes fl{{to{{transform:scaleX(.75)}}}}
.blink{{animation:bl 1s steps(1) infinite}}@keyframes bl{{50%{{opacity:0}}}}
.shoot{{opacity:0;animation:sh linear infinite}}
@keyframes sh{{0%{{opacity:0;transform:translate(0,0)}}3%{{opacity:1}}12%{{opacity:0;transform:translate(-160px,60px)}}100%{{opacity:0;transform:translate(-160px,60px)}}}}
.beam{{transform-origin:0 -104px;animation:bm 6s ease-in-out infinite alternate}}@keyframes bm{{from{{transform:rotate(-14deg)}}to{{transform:rotate(16deg)}}}}
.lamp{{animation:lp 2s ease-in-out infinite}}@keyframes lp{{50%{{fill:#fff4cf}}}}
"""
    return svg(W, H, body, FONTS, css, f"{NAME}, {ROLE}")


def chest() -> str:
    """'Now building' card: a treasure chest that keeps opening, plus the current project."""
    W, H = 1000, 190
    coins = "".join(
        f'<circle cx="{cx}" cy="{cy}" r="7" fill="{GOLD}" stroke="#b8862a" class="coin" style="animation-delay:{d}s"/>'
        for cx, cy, d in ((-22, -6, 0), (-6, -12, .2), (10, -8, .4), (24, -4, .6), (2, -2, .1))
    )
    sparkles = "".join(
        f'<path d="M{x},{y} l2,-7 l2,7 l7,2 l-7,2 l-2,7 l-2,-7 l-7,-2 z" fill="#fff1bf" class="spk" style="animation-delay:{d}s"/>'
        for x, y, d in ((-40, -50, 0), (30, -62, .7), (50, -30, 1.3), (-10, -76, 1.9))
    )
    x, pills = 300, ""
    for t in ("Flutter", "TensorFlow Lite", "FFmpeg", "SQLite"):
        w = 18 + len(t) * 7.2
        pills += f'<rect x="{x}" y="136" width="{w:.0f}" height="24" rx="12" fill="{TEAL}" fill-opacity=".22"/><text x="{x + w / 2:.0f}" y="152" text-anchor="middle" class="sans b" font-size="11" style="fill:#7fd6d6">{t}</text>'
        x += w + 7
    body = f"""<defs>
  <pattern id="stripe" width="16" height="16" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">
    <rect width="8" height="16" fill="{GOLD}" fill-opacity=".9"/><rect x="8" width="8" height="16" fill="{GOLD}" fill-opacity=".6"/></pattern>
  <radialGradient id="cg"><stop offset="0" stop-color="#ffd27a" stop-opacity=".5"/><stop offset="1" stop-color="#ffd27a" stop-opacity="0"/></radialGradient>
</defs>
<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="16" fill="{CARD}" stroke="{GOLD}" stroke-opacity=".22"/>
<g transform="translate(150 118)">
  <circle cx="0" cy="-20" r="80" fill="url(#cg)" class="halo"/>
  {coins}
  <rect x="-48" y="-4" width="96" height="46" rx="6" fill="#6b3f1d" stroke="#3b220f" stroke-width="2"/>
  <rect x="-48" y="10" width="96" height="6" fill="#b8862a"/>
  <rect x="-8" y="4" width="16" height="18" rx="3" fill="{GOLD}" stroke="#b8862a"/>
  <g class="lid"><path d="M-50,-4 L50,-4 L50,-20 Q0,-46 -50,-20 Z" fill="#7d4a22" stroke="#3b220f" stroke-width="2"/>
    <path d="M-50,-12 Q0,-38 50,-12" fill="none" stroke="#b8862a" stroke-width="4"/></g>
  {sparkles}
</g>
<text x="300" y="46" class="sans b muted" font-size="12" letter-spacing="3">NOW BUILDING</text>
<text x="300" y="84" class="pir" font-size="36">Combat Capture</text>
<text x="300" y="112" class="sans" font-size="14">Flutter app that uses on-device ML to spot sparring rounds and clip them automatically.</text>
{pills}
<text x="{W - 40}" y="46" text-anchor="end" class="sans b gold" font-size="11" letter-spacing="2">IN DEVELOPMENT</text>
<rect x="{W - 240}" y="58" width="200" height="10" rx="5" fill="#12233c"/>
<clipPath id="bc"><rect x="{W - 240}" y="58" width="128" height="10" rx="5"/></clipPath>
<g clip-path="url(#bc)"><rect x="{W - 272}" y="58" width="170" height="10" fill="url(#stripe)" class="bar"/></g>"""
    css = BASE_CSS + """
.lid{transform-origin:50px -4px;animation:lid 4s ease-in-out infinite}
@keyframes lid{0%,15%,85%,100%{transform:rotate(0)}35%,65%{transform:rotate(28deg)}}
.coin{transform-box:fill-box;transform-origin:center;animation:cn 4s ease-in-out infinite}
@keyframes cn{0%,25%,80%,100%{transform:translateY(14px);opacity:0}40%,65%{transform:translateY(-10px);opacity:1}}
.spk{transform-box:fill-box;transform-origin:center;animation:sk 2.4s ease-in-out infinite}
@keyframes sk{0%,100%{transform:scale(0);opacity:0}50%{transform:scale(1);opacity:1}}
.halo{animation:ha 4s ease-in-out infinite}@keyframes ha{0%,20%,85%,100%{opacity:.2}45%,65%{opacity:1}}
.bar{animation:br 1s linear infinite}@keyframes br{to{transform:translateX(22.6px)}}
"""
    return svg(W, H, body, FONTS, css, "Now building: Combat Capture")


def whale() -> str:
    """Divider strip: a whale surfaces and spouts while a fish jumps."""
    W, H = 1000, 120
    drops = "".join(
        f'<circle cx="0" cy="0" r="{r}" fill="#9fe7ff" class="drop" style="--dx:{dx}px;--dy:{dy}px;animation-delay:{d}s"/>'
        for dx, dy, r, d in ((-26, -30, 2.4, 0), (-14, -46, 3, .05), (0, -56, 3.4, .1), (14, -46, 3, .05), (26, -30, 2.4, 0), (-7, -38, 2, .15), (8, -40, 2, .15))
    )
    body = f"""<defs><clipPath id="c"><rect width="{W}" height="{H}" rx="16"/></clipPath>
  <linearGradient id="bg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#071226"/><stop offset="1" stop-color="{NAVY2}"/></linearGradient></defs>
<g clip-path="url(#c)">
  <rect width="{W}" height="{H}" fill="url(#bg)"/>
  {stars(24, W, 60, seed=5)}
  <g transform="translate(300 84)"><g class="whale">
    <path d="M-80,10 Q-70,-26 -10,-28 Q50,-30 72,-6 Q86,4 96,-14 L104,-24 Q104,-2 92,12 Q60,18 -80,10 Z" fill="#2a5684"/>
    <path d="M-70,6 Q-10,14 70,4" fill="none" stroke="#9fc4e8" stroke-opacity=".5" stroke-width="2"/>
    <circle cx="-50" cy="-8" r="3" fill="#0a1628"/>
    <g transform="translate(-34 -26)">{drops}</g>
  </g></g>
  <g transform="translate(700 92)"><g class="fish"><path d="M0,0 Q10,-8 20,0 Q10,8 0,0 Z M20,0 L28,-6 L28,6 Z" fill="{GOLD}"/></g></g>
  <path d="{wave_path(86, 6, 250, 1500, H)}" fill="#123a63" class="wv" style="animation-duration:10s"/>
  <path d="{wave_path(98, 7, 250, 1500, H)}" fill="#16477a" class="wv" style="animation-duration:7s"/>
  <path d="{wave_path(98, 7, 250, 1500, H)}" fill="none" stroke="#5ff3e0" stroke-opacity=".35" class="wv" style="animation-duration:7s"/>
</g>
<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="16" fill="none" stroke="{GOLD}" stroke-opacity=".2"/>"""
    css = BASE_CSS + """
.wv{animation:dr linear infinite}@keyframes dr{to{transform:translateX(-250px)}}
.whale{animation:wh 8s ease-in-out infinite}
@keyframes wh{0%,100%{transform:translateY(46px)}30%,60%{transform:translateY(0)}}
.drop{opacity:0;animation:sp 8s ease-out infinite}
@keyframes sp{0%,32%{transform:translate(0,0);opacity:0}36%{opacity:1}46%{transform:translate(var(--dx),var(--dy));opacity:1}56%,100%{transform:translate(calc(var(--dx)*1.6),-6px);opacity:0}}
.fish{animation:fi 5s ease-in-out infinite;transform-box:fill-box;transform-origin:center}
@keyframes fi{0%,55%{transform:translate(0,30px) rotate(-50deg)}68%{transform:translate(40px,-40px) rotate(0)}80%{transform:translate(80px,30px) rotate(50deg)}100%{transform:translate(80px,30px) rotate(50deg)}}
"""
    return svg(W, H, body, FONTS, css, "Divider")


def bottle() -> str:
    """Contact card: a message in a bottle bobbing on the waves."""
    W, H = 1000, 180
    body = f"""<defs><clipPath id="c"><rect width="{W}" height="{H}" rx="16"/></clipPath></defs>
<g clip-path="url(#c)">
  <rect width="{W}" height="{H}" fill="{CARD}"/>
  {stars(30, W, 90, seed=8)}
  <g transform="translate(170 118)"><g class="bot">
    <path d="M-60,-14 Q-62,-30 -40,-30 L30,-30 Q44,-30 50,-20 L72,-16 L72,-2 L50,2 Q44,12 30,12 L-40,12 Q-62,12 -60,-4 Z" fill="#5fb3a4" fill-opacity=".35" stroke="#9fe0d4" stroke-width="2"/>
    <rect x="72" y="-17" width="12" height="16" rx="2" fill="#8a5a33"/>
    <rect x="-34" y="-20" width="58" height="22" rx="4" fill="#f3ead6" transform="rotate(-6)"/>
    <path d="M-28,-14 h40 M-28,-8 h32" stroke="#b8a37f" stroke-width="1.5" transform="rotate(-6)"/>
    <path d="M-50,-24 Q-30,-28 -10,-26" stroke="#fff" stroke-opacity=".5" stroke-width="2" fill="none"/>
  </g></g>
  <path d="{wave_path(130, 7, 250, 1500, H)}" fill="#123a63" class="wv" style="animation-duration:9s"/>
  <path d="{wave_path(146, 8, 250, 1500, H)}" fill="#16477a" class="wv" style="animation-duration:6s"/>
  <path d="{wave_path(146, 8, 250, 1500, H)}" fill="none" stroke="#5ff3e0" stroke-opacity=".35" class="wv" style="animation-duration:6s"/>
</g>
<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="16" fill="none" stroke="{GOLD}" stroke-opacity=".25"/>
<text x="340" y="48" class="sans b muted" font-size="12" letter-spacing="3">SEND A MESSAGE</text>
<text x="340" y="86" class="pir" font-size="34">Message in a bottle</text>
<text x="340" y="112" class="sans" font-size="15">zhengyaowong.cs@gmail.com  \u00b7  open to Summer 2027 SWE internships</text>
<g transform="translate({W - 200} 30)"><rect width="160" height="40" rx="20" fill="{GOLD}"/>
  <text x="80" y="25" text-anchor="middle" class="sans b" font-size="13" letter-spacing="1.5" style="fill:#0a1628">WRITE ME \u2192</text></g>"""
    css = BASE_CSS + """
.wv{animation:dr linear infinite}@keyframes dr{to{transform:translateX(-250px)}}
.bot{animation:bt 4s ease-in-out infinite}
@keyframes bt{0%,100%{transform:translate(0,0) rotate(-6deg)}50%{transform:translate(10px,8px) rotate(5deg)}}
"""
    return svg(W, H, body, FONTS, css, "Message in a bottle: zhengyaowong.cs@gmail.com")


def nav(label: str) -> str:
    W, H = 150, 46
    body = f"""<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="23" fill="{CARD}" stroke="{GOLD}" stroke-opacity=".55" stroke-width="1.4"/>
<path d="M22,17 l5,6 l-5,6 l-5,-6 z" fill="{GOLD}"/>
<text x="{W / 2 + 8}" y="28" text-anchor="middle" class="sans b gold" font-size="13" letter-spacing="1.6">{esc(label.upper())}</text>"""
    return svg(W, H, body, FONTS, BASE_CSS, label)


def header(num: str, title: str, sub: str) -> str:
    W, H = 1000, 86
    tw = 40 + len(title) * 17
    body = f"""<defs><linearGradient id="ln" x1="0" x2="1"><stop offset="0" stop-color="{GOLD}" stop-opacity=".7"/><stop offset="1" stop-color="{GOLD}" stop-opacity="0"/></linearGradient></defs>
<text x="40" y="28" class="sans b muted" font-size="12" letter-spacing="3">{esc(num)}  ·  {esc(sub.upper())}</text>
<path d="M50,52 l4,-12 l4,12 l12,4 l-12,4 l-4,12 l-4,-12 l-12,-4 z" fill="{GOLD}" class="spin"/>
<text x="80" y="68" class="pir" font-size="36">{esc(title)}</text>
<rect x="{80 + tw}" y="56" width="{W - 120 - tw}" height="1.5" fill="url(#ln)"/>"""
    css = BASE_CSS + ".spin{transform-box:fill-box;transform-origin:center;animation:sp 12s linear infinite}@keyframes sp{to{transform:rotate(360deg)}}"
    return svg(W, H, body, FONTS, css, title)


def about() -> str:
    W, H = 1000, 330
    K, KEY, STR, P = "#c792ea", "#8fc6ff", GOLD, MUTED
    rows = [
        ("name", '"Zheng Yao Wong"'),
        ("role", '"Full-stack developer"'),
        ("route", '["Malaysia", "Arlington, TX"]'),
        ("crew", '"UT Arlington, CS \'27"'),
        ("aboard", '"UTA Office of IT"'),
        ("building", '"Combat Capture"'),
        ("seeking", '"Summer 2027 SWE internship"'),
        ("rule", '"own every line before it ships"'),
    ]
    lines = [f'<tspan fill="{K}">const</tspan> <tspan fill="{FOAM}">captain</tspan> <tspan fill="{P}">= {{</tspan>']
    for k, v in rows:
        lines.append(f'  <tspan fill="{KEY}">{k}</tspan><tspan fill="{P}">:</tspan> <tspan fill="{STR}">{esc(v)}</tspan><tspan fill="{P}">,</tspan>')
    lines.append(f'<tspan fill="{P}">}};</tspan>')
    code = "".join(
        f'<text x="64" y="{92 + i * 22}" class="mono" font-size="15" xml:space="preserve"><tspan fill="#3d5878">{i + 1:>2}</tspan>   {l}</text>'
        for i, l in enumerate(lines)
    )
    body = f"""<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="16" fill="#0b1a30" stroke="{GOLD}" stroke-opacity=".22"/>
<rect x="1" y="1" width="{W - 2}" height="44" rx="16" fill="#0f2240"/><rect x="1" y="30" width="{W - 2}" height="15" fill="#0f2240"/>
<circle cx="28" cy="23" r="6" fill="{RED}"/><circle cx="48" cy="23" r="6" fill="{GOLD}"/><circle cx="68" cy="23" r="6" fill="{TEAL}"/>
<text x="500" y="28" text-anchor="middle" class="mono muted" font-size="13">captain.ts</text>
{code}
<rect x="112" y="{92 + 9 * 22 + 4}" width="9" height="16" fill="{GOLD}" class="blink"/>
<g transform="translate(820 190) scale(2.4)" opacity=".1">{emblem(GOLD, '#0b1a30')}</g>"""
    css = BASE_CSS + ".blink{animation:bl 1s steps(1) infinite}@keyframes bl{50%{opacity:0}}"
    return svg(W, H, body, FONTS, css, "About")


def card(p: dict) -> str:
    W, H = 490, 270
    desc = wrap(p["desc"], 58)
    x, tags = 28, ""
    for t in p["tech"]:
        w = 18 + len(t) * 7.2
        tags += f'<rect x="{x}" y="196" width="{w:.0f}" height="24" rx="12" fill="{TEAL}" fill-opacity=".22"/><text x="{x + w / 2:.0f}" y="212" text-anchor="middle" class="sans b" font-size="11" style="fill:#7fd6d6">{esc(t)}</text>'
        x += w + 7
    award = (
        f'<text x="28" y="98" class="sans b gold" font-size="12" letter-spacing=".5">★ {esc(p["award"].upper())}</text>'
        if p["award"]
        else ""
    )
    y0 = 124 if p["award"] else 108
    body = f"""<defs><linearGradient id="cg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#112645"/><stop offset="1" stop-color="{CARD}"/></linearGradient></defs>
<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="16" fill="url(#cg)" stroke="{GOLD}" stroke-opacity=".22"/>
<text x="28" y="40" class="sans b muted" font-size="11" letter-spacing="2.2">{esc(p['kind'].upper())}</text>
<text x="28" y="76" class="pir" font-size="34">{esc(p['name'])}</text>
{award}
{''.join(f'<text x="28" y="{y0 + i * 21}" class="sans" font-size="14">{esc(l)}</text>' for i, l in enumerate(desc))}
{tags}
<text x="{W - 28}" y="248" text-anchor="end" class="sans b gold" font-size="12" letter-spacing="1.5">SET SAIL →</text>"""
    return svg(W, H, body, FONTS, BASE_CSS, p["name"])


def footer() -> str:
    W, H = 1000, 150
    body = f"""<defs><clipPath id="c"><rect width="{W}" height="{H}" rx="16"/></clipPath></defs>
<g clip-path="url(#c)">
  <rect width="{W}" height="{H}" fill="{NAVY}"/>
  {stars(30, W, 70, seed=11)}
  <path d="{wave_path(112, 8, 250, 1500, H)}" fill="#0f2f52" class="wv" style="animation-duration:12s"/>
  <path d="{wave_path(126, 9, 250, 1500, H)}" fill="#16477a" class="wv" style="animation-duration:8s"/>
</g>
<text x="500" y="56" text-anchor="middle" class="pir" font-size="30">Fair winds and following seas</text>
<text x="500" y="84" text-anchor="middle" class="sans muted" font-size="13">zhengyaowong.cs@gmail.com  ·  zhengyaoportfolio.vercel.app</text>"""
    css = BASE_CSS + ".wv{animation:dr linear infinite}@keyframes dr{to{transform:translateX(-250px)}}"
    return svg(W, H, body, FONTS, css, "Footer")


HEADERS = {
    "projects": ("01", "Voyages", "things I've built and shipped"),
    "stack": ("02", "Cargo Hold", "what I build with"),
    "log": ("03", "Ship's Log", "the last twelve months"),
}


def build() -> None:
    write(THEME, "hero", hero())
    write(THEME, "about", about())
    write(THEME, "footer", footer())
    write(THEME, "chest", chest())
    write(THEME, "whale", whale())
    write(THEME, "bottle", bottle())
    for label, _ in NAV:
        write(THEME, f"nav-{label.lower()}", nav(label))
    for key, (n, t, s) in HEADERS.items():
        write(THEME, f"h-{key}", header(n, t, s))
    for p in PROJECTS:
        write(THEME, f"card-{p['slug']}", card(p))
