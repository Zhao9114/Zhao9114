"""Theme 2: NIGHT VOYAGE, Grand Line edition. Deep navy sea, moonlight and gold, One Piece motifs."""
from common import *  # noqa: F403

THEME = "voyage"
NAVY, NAVY2, CARD = "#0a1628", "#0d2440", "#0e1d35"
GOLD, FOAM, MUTED, TEAL, RED = "#f4c95d", "#e8dcc0", "#8aa4c4", "#1f8a8a", "#e5484d"
STRAW, STRAW_D, HATBAND = "#f2cf63", "#b98d24", "#d7262e"
FONTS = [("pirata", "Pirata"), ("inter", "Inter"), ("inter-bold", "InterB"), ("fira", "Fira")]
POSTER_FONTS = FONTS + [("fell", "Fell")]  # wanted-poster lettering, only embedded where used


def straw_hat(line: str = "#1a1206") -> str:
    """Straw hat sized to sit on common.emblem()'s skull (centered on 0,0)."""
    return f"""<g>
  <path d="M-17,-17 Q-18,-42 0,-43 Q18,-42 17,-17 Z" fill="{STRAW}" stroke="{line}" stroke-width="1.6"/>
  <path d="M-17.6,-25 Q0,-29 17.6,-25 L17.3,-18 Q0,-22 -17.3,-18 Z" fill="{HATBAND}"/>
  <ellipse cx="0" cy="-16" rx="33" ry="7.5" fill="{STRAW}" stroke="{line}" stroke-width="1.6"/>
  <path d="M-24,-15 Q0,-12 24,-15" fill="none" stroke="{STRAW_D}" stroke-width="1.2"/>
</g>"""


def jolly(ink: str, hole: str, accent: str | None = None, line: str = "#1a1206") -> str:
    """The <skull /> code mark wearing a straw hat."""
    return f"<g>{emblem(ink, hole, accent)}{straw_hat(line)}</g>"


def berry(x: float, y: float, size: float = 20, fill: str = GOLD) -> str:
    """Berry sign: a B with two vertical strokes through it."""
    k = size / 20
    return (
        f'<text x="{x}" y="{y}" font-size="{size}" style="font-family:Fell,serif;fill:{fill}">B</text>'
        f'<path d="M{x + 4.2 * k:.1f},{y - 17 * k:.1f} V{y + 3.5 * k:.1f} M{x + 8.4 * k:.1f},{y - 17 * k:.1f} V{y + 3.5 * k:.1f}" stroke="{fill}" stroke-width="{1.4 * k:.1f}"/>'
    )

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
  <path d="M-22,-70 L-46,-66 L-22,-58 Z" fill="#111" stroke="{FOAM}" stroke-opacity=".5" stroke-width=".8" class="flap"/>
  <g transform="translate(-27 -40) scale(.3)">{jolly('#1a1206', '#f3ead6', line='#1a1206')}</g>
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
    # next island on the horizon, and the Log Pose locked onto it
    lighthouse = f"""
<g transform="translate(940 300)">
  <path d="M-60,4 Q-44,-22 -14,-26 Q-4,-48 14,-44 Q30,-40 34,-22 Q52,-14 62,6 Z" fill="#0b1a2c"/>
  <path d="M10,-44 Q4,-62 12,-70 M14,-44 Q22,-60 30,-62" fill="none" stroke="#0b1a2c" stroke-width="3" stroke-linecap="round"/>
  <circle cx="-8" cy="-12" r="2" fill="#ffd27a" class="tw"/><circle cx="20" cy="-8" r="2" fill="#ffd27a" class="tw" style="animation-delay:1.3s"/>
</g>
<g transform="translate(905 104)">
  <circle r="70" fill="url(#lpglow)"/>
  <rect x="-40" y="22" width="80" height="18" rx="7" fill="#5a3a1e" stroke="{GOLD}" stroke-opacity=".6" stroke-width="1.4"/>
  <path d="M-30,31 h60" stroke="{GOLD}" stroke-opacity=".35" stroke-dasharray="3 4"/>
  <rect x="-16" y="16" width="32" height="10" rx="3" fill="#b8862a" stroke="#3b220f" stroke-width="1.4"/>
  <circle r="32" fill="url(#glass)" stroke="{GOLD}" stroke-opacity=".75" stroke-width="2"/>
  <g class="needle"><path d="M0,-24 L4.5,0 L0,24 L-4.5,0 Z" fill="{RED}"/><path d="M4.5,0 L0,24 L-4.5,0 Z" fill="{FOAM}"/></g>
  <circle r="3" fill="{GOLD}"/>
  <ellipse cx="-12" cy="-15" rx="9" ry="4.5" fill="#fff" opacity=".35" transform="rotate(-35 -12 -15)"/>
  <text y="60" text-anchor="middle" class="sans b muted" font-size="10" letter-spacing="2.5">LOG POSE</text>
</g>"""
    tag = wrap(TAGLINE, 52)
    body = f"""
<defs>
  <linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#050b18"/><stop offset=".75" stop-color="{NAVY2}"/></linearGradient>
  <radialGradient id="glow"><stop offset="0" stop-color="#f6e7b8" stop-opacity=".45"/><stop offset="1" stop-color="#f6e7b8" stop-opacity="0"/></radialGradient>
  <radialGradient id="glass" cx=".4" cy=".35"><stop offset="0" stop-color="#bfe9ff" stop-opacity=".55"/><stop offset="1" stop-color="#1c4f7c" stop-opacity=".85"/></radialGradient>
  <radialGradient id="lpglow"><stop offset="0" stop-color="#9fe7ff" stop-opacity=".22"/><stop offset="1" stop-color="#9fe7ff" stop-opacity="0"/></radialGradient>
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
<text x="60" y="94" class="sans b muted" font-size="13" letter-spacing="3">GRAND LINE ROOKIE</text>
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
.needle{{animation:nd 6s ease-in-out infinite}}
@keyframes nd{{0%,100%{{transform:rotate(-30deg)}}22%{{transform:rotate(70deg)}}38%{{transform:rotate(150deg)}}50%{{transform:rotate(186deg)}}62%,90%{{transform:rotate(170deg)}}}}
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
<text x="300" y="46" class="sans b muted" font-size="12" letter-spacing="3">CURRENT ARC · NOW BUILDING</text>
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


def sea_king() -> str:
    """Divider strip: a Sea King rises out of the water, snaps its jaws and sinks while fish flee."""
    W, H = 1000, 120
    SK, FIN, BELLY = "#2b6b73", "#c0504d", "#9fe0d4"
    bubbles = "".join(
        f'<circle cx="{x}" cy="0" r="{r}" fill="none" stroke="#9fe7ff" stroke-opacity=".7" class="bub" style="animation-delay:{d}s"/>'
        for x, r, d in ((-40, 2.4, 0), (-18, 3, .5), (8, 2, 1.1), (-110, 2.2, .3), (-74, 2.6, .9), (30, 2.2, 1.6))
    )
    hump = lambda x0, x1, h: (  # noqa: E731
        f'<path d="M{x0},8 Q{(x0 + x1) / 2},{-h} {x1},8 Z" fill="{SK}"/>'
        + "".join(
            f'<path d="M{x0 + (x1 - x0) * t - 4:.0f},{-h * 0.48 * (1 - (2 * t - 1) ** 2) + 2:.0f} l4,-11 l4,11 z" fill="{FIN}"/>'
            for t in (0.3, 0.5, 0.7)
        )
    )
    body = f"""<defs><clipPath id="c"><rect width="{W}" height="{H}" rx="16"/></clipPath>
  <linearGradient id="bg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#071226"/><stop offset="1" stop-color="{NAVY2}"/></linearGradient></defs>
<g clip-path="url(#c)">
  <rect width="{W}" height="{H}" fill="url(#bg)"/>
  {stars(24, W, 60, seed=5)}
  <g transform="translate(300 100)"><g class="sk">
    <g class="coil">{hump(-182, -122, 74)}{hump(-112, -62, 60)}</g>
    <g class="head">
      <path d="M-14,-58 L-32,-80 L-4,-66 Z M2,-70 L-8,-92 L14,-72 Z M18,-73 L16,-94 L30,-71 Z" fill="{FIN}"/>
      <path d="M-34,12 Q-40,-36 -14,-58 Q8,-76 44,-70 Q70,-64 84,-50 Q90,-42 82,-38 L56,-40 Q70,-32 68,-24 Q50,-20 36,-28 Q24,-16 22,12 Z" fill="{SK}"/>
      <path d="M-22,8 Q-28,-28 -4,-50" fill="none" stroke="{BELLY}" stroke-opacity=".45" stroke-width="2.4" stroke-dasharray="5 4"/>
      <path d="M60,-40 l3,5 l3,-5 Z M68,-40 l3,5 l3,-5 Z M76,-39 l2.5,4 l2.5,-4 Z M46,-27 l3,-5 l3,5 Z M56,-25 l3,-5 l3,5 Z" fill="#f3ead6"/>
      <circle cx="44" cy="-57" r="5" fill="{GOLD}" class="eye"/><rect x="43" y="-61" width="2" height="8" rx="1" fill="#0a1628"/>
    </g>
    <g transform="translate(0 -4)">{bubbles}</g>
  </g></g>
  <g transform="translate(680 92)"><g class="fish"><path d="M0,0 Q10,-8 20,0 Q10,8 0,0 Z M20,0 L28,-6 L28,6 Z" fill="{GOLD}"/></g></g>
  <g transform="translate(720 96)"><g class="fish" style="animation-delay:.35s"><path d="M0,0 Q8,-6 16,0 Q8,6 0,0 Z M16,0 L22,-5 L22,5 Z" fill="#7fd6d6"/></g></g>
  <path d="{wave_path(86, 6, 250, 1500, H)}" fill="#123a63" class="wv" style="animation-duration:10s"/>
  <path d="{wave_path(98, 7, 250, 1500, H)}" fill="#16477a" class="wv" style="animation-duration:7s"/>
  <path d="{wave_path(98, 7, 250, 1500, H)}" fill="none" stroke="#5ff3e0" stroke-opacity=".35" class="wv" style="animation-duration:7s"/>
</g>
<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="16" fill="none" stroke="{GOLD}" stroke-opacity=".2"/>"""
    css = BASE_CSS + """
.wv{animation:dr linear infinite}@keyframes dr{to{transform:translateX(-250px)}}
.sk{animation:sk 9s ease-in-out infinite}
@keyframes sk{0%,100%{transform:translateY(96px)}28%,64%{transform:translateY(0)}}
.coil{animation:co 9s ease-in-out infinite}@keyframes co{0%,100%{transform:translateY(20px)}40%{transform:translateY(-3px)}55%{transform:translateY(4px)}}
.head{transform-origin:0 10px;animation:hd 9s ease-in-out infinite}
@keyframes hd{0%,30%{transform:rotate(0)}38%{transform:rotate(-7deg)}44%{transform:rotate(3deg)}50%{transform:rotate(-5deg)}58%,100%{transform:rotate(0)}}
.eye{animation:ey 9s ease-in-out infinite}@keyframes ey{0%,30%,62%,100%{fill:#f4c95d}40%,52%{fill:#ffe9a8}}
.bub{opacity:0;animation:bb 3s ease-out infinite}
@keyframes bb{0%{transform:translateY(0);opacity:0}20%{opacity:1}100%{transform:translateY(-34px);opacity:0}}
.fish{animation:fi 5s ease-in-out infinite;transform-box:fill-box;transform-origin:center}
@keyframes fi{0%,55%{transform:translate(0,30px) rotate(-50deg)}68%{transform:translate(40px,-40px) rotate(0)}80%{transform:translate(80px,30px) rotate(50deg)}100%{transform:translate(80px,30px) rotate(50deg)}}
"""
    return svg(W, H, body, FONTS, css, "A Sea King rising out of the water")


def den_den_mushi() -> str:
    """Contact card: a Den Den Mushi ringing on a rock, receiver rattling."""
    W, H = 1000, 180
    SKIN, SKIN_D, SHELL, SHELL_L = "#e2a77c", "#a8714c", "#f3ead6", "#b8a37f"
    rings = "".join(
        f'<path d="M{8 + k * 9},{-10 - k * 6} q{6 + k * 3},{10 + k * 6} 0,{20 + k * 12}" fill="none" stroke="{GOLD}" stroke-width="2.4" stroke-linecap="round" class="ring" style="animation-delay:{k * 0.18:.2f}s"/>'
        for k in range(3)
    )
    body = f"""<defs><clipPath id="c"><rect width="{W}" height="{H}" rx="16"/></clipPath></defs>
<g clip-path="url(#c)">
  <rect width="{W}" height="{H}" fill="{CARD}"/>
  {stars(30, W, 90, seed=8)}
  <path d="M60,150 Q80,116 130,112 Q200,104 250,118 Q290,128 300,150 Z" fill="#0b1a2c"/>
  <g transform="translate(150 116)"><g class="ddm">
    <path d="M-66,8 Q-72,-4 -52,-6 L30,-6 Q40,-8 42,-22 L44,-48 Q46,-60 58,-60 Q70,-60 70,-48 L68,-20 Q66,2 50,8 Z" fill="{SKIN}" stroke="{SKIN_D}" stroke-width="1.6"/>
    <path d="M52,-58 L46,-80 M64,-58 L70,-80" stroke="{SKIN}" stroke-width="4.5" stroke-linecap="round"/>
    <g class="eyes"><circle cx="46" cy="-82" r="5.5" fill="#fff" stroke="{SKIN_D}" stroke-width="1.2"/><circle cx="70" cy="-82" r="5.5" fill="#fff" stroke="{SKIN_D}" stroke-width="1.2"/>
      <circle cx="47" cy="-82" r="2.6" fill="#0a1628"/><circle cx="71" cy="-82" r="2.6" fill="#0a1628"/></g>
    <path d="M52,-36 Q58,-30 64,-36" fill="none" stroke="#5a3320" stroke-width="2" stroke-linecap="round" class="mouth"/>
    <circle cx="-14" cy="-32" r="32" fill="{SHELL}" stroke="{SHELL_L}" stroke-width="2"/>
    <path d="M-14,-32 q8,-2 8,6 q0,12 -14,12 q-18,0 -18,-18 q0,-24 26,-24 q30,0 30,28" fill="none" stroke="{SHELL_L}" stroke-width="2.2"/>
    <circle cx="-30" cy="-22" r="7" fill="{GOLD}" stroke="#b8862a" stroke-width="1.2"/>
    <circle cx="-30" cy="-26" r="1.2" fill="#0a1628"/><circle cx="-26" cy="-22" r="1.2" fill="#0a1628"/><circle cx="-30" cy="-18" r="1.2" fill="#0a1628"/><circle cx="-34" cy="-22" r="1.2" fill="#0a1628"/>
    <path d="M-48,-56 q-10,6 -4,12 q6,6 -2,12 q-6,6 2,10" fill="none" stroke="#1d1d1d" stroke-width="1.8"/>
    <g class="rcv">
      <path d="M-40,-68 Q-14,-84 12,-68" fill="none" stroke="#1d1d1d" stroke-width="7" stroke-linecap="round"/>
      <path d="M-40,-68 Q-14,-84 12,-68" fill="none" stroke="{GOLD}" stroke-opacity=".35" stroke-width="1"/>
      <rect x="-52" y="-72" width="20" height="11" rx="5" fill="#1d1d1d" stroke="{GOLD}" stroke-opacity=".5"/>
      <rect x="4" y="-72" width="20" height="11" rx="5" fill="#1d1d1d" stroke="{GOLD}" stroke-opacity=".5"/>
    </g>
    <g transform="translate(76 -50)">{rings}</g>
  </g></g>
  <text x="196" y="22" class="pir ringtxt" font-size="15">puru puru puru...</text>
  <path d="{wave_path(130, 7, 250, 1500, H)}" fill="#123a63" class="wv" style="animation-duration:9s"/>
  <path d="{wave_path(146, 8, 250, 1500, H)}" fill="#16477a" class="wv" style="animation-duration:6s"/>
  <path d="{wave_path(146, 8, 250, 1500, H)}" fill="none" stroke="#5ff3e0" stroke-opacity=".35" class="wv" style="animation-duration:6s"/>
</g>
<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="16" fill="none" stroke="{GOLD}" stroke-opacity=".25"/>
<text x="340" y="48" class="sans b muted" font-size="12" letter-spacing="3">SEND A MESSAGE</text>
<text x="340" y="86" class="pir" font-size="34">Ring the Den Den Mushi</text>
<text x="340" y="112" class="sans" font-size="15">zhengyaowong.cs@gmail.com  \u00b7  open to Summer 2027 SWE internships</text>
<g transform="translate({W - 200} 30)"><rect width="160" height="40" rx="20" fill="{GOLD}"/>
  <text x="80" y="25" text-anchor="middle" class="sans b" font-size="13" letter-spacing="1.5" style="fill:#0a1628">EMAIL ME \u2192</text></g>"""
    css = BASE_CSS + """
.wv{animation:dr linear infinite}@keyframes dr{to{transform:translateX(-250px)}}
.rcv{transform-box:fill-box;transform-origin:center bottom;animation:rc 2.4s ease-in-out infinite}
@keyframes rc{0%,8%,16%,24%,32%{transform:translateY(0) rotate(0)}4%,20%{transform:translateY(-4px) rotate(-4deg)}12%,28%{transform:translateY(-4px) rotate(4deg)}40%,100%{transform:translateY(0) rotate(0)}}
.ring{opacity:0;animation:rg 2.4s ease-out infinite}
@keyframes rg{0%{opacity:0}6%{opacity:1}36%{opacity:0}100%{opacity:0}}
.ringtxt{animation:rt 2.4s ease-in-out infinite}@keyframes rt{0%,40%{opacity:.95}60%,100%{opacity:.25}}
.eyes{transform-box:fill-box;transform-origin:center bottom;animation:ew 4.8s ease-in-out infinite}
@keyframes ew{0%,40%,100%{transform:scaleY(1)}44%{transform:scaleY(.1)}48%{transform:scaleY(1)}}
.ddm{animation:dd 2.4s ease-in-out infinite}@keyframes dd{0%,100%{transform:translateY(0)}50%{transform:translateY(1.5px)}}
"""
    return svg(W, H, body, FONTS, css, "Den Den Mushi: zhengyaowong.cs@gmail.com")


def nav(label: str) -> str:
    W, H = 150, 46
    body = f"""<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="23" fill="{CARD}" stroke="{GOLD}" stroke-opacity=".55" stroke-width="1.4"/>
<g transform="translate(23 33) scale(.3)">{straw_hat()}</g>
<text x="{W / 2 + 8}" y="28" text-anchor="middle" class="sans b gold" font-size="13" letter-spacing="1.6">{esc(label.upper())}</text>"""
    return svg(W, H, body, FONTS, BASE_CSS, label)


def header(num: str, title: str, sub: str) -> str:
    W, H = 1000, 86
    tw = 40 + len(title) * 17
    body = f"""<defs><linearGradient id="ln" x1="0" x2="1"><stop offset="0" stop-color="{GOLD}" stop-opacity=".7"/><stop offset="1" stop-color="{GOLD}" stop-opacity="0"/></linearGradient></defs>
<text x="40" y="28" class="sans b muted" font-size="12" letter-spacing="3">{esc(num)}  ·  {esc(sub.upper())}</text>
<g transform="translate(50 70) scale(.62)"><g class="tilt">{straw_hat()}</g></g>
<text x="80" y="68" class="pir" font-size="36">{esc(title)}</text>
<rect x="{80 + tw}" y="56" width="{W - 120 - tw}" height="1.5" fill="url(#ln)"/>"""
    css = BASE_CSS + ".tilt{transform-origin:0 -16px;animation:tl 5s ease-in-out infinite}@keyframes tl{0%,100%{transform:rotate(-8deg)}50%{transform:rotate(6deg)}}"
    return svg(W, H, body, FONTS, css, title)


def about() -> str:
    W, H = 1000, 352
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
        ("dream", '"King of the Devs"'),
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
<rect x="112" y="{92 + 10 * 22 + 4}" width="9" height="16" fill="{GOLD}" class="blink"/>
<g transform="translate(820 214) scale(2.4)" opacity=".12">{jolly(GOLD, '#0b1a30', line='#0b1a30')}</g>"""
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
<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="16" fill="url(#cg)" stroke="{GOLD}" stroke-opacity=".35"/>
<rect x="8" y="8" width="{W - 16}" height="{H - 16}" rx="11" fill="none" stroke="{GOLD}" stroke-opacity=".14"/>
<g transform="translate({W - 74} 120) rotate(12) scale(.5)" opacity=".1">{jolly(GOLD, CARD, line=CARD)}</g>
<text x="28" y="40" font-size="19" letter-spacing="7" style="font-family:Fell,serif;fill:{GOLD}">WANTED</text>
<text x="{W - 28}" y="38" text-anchor="end" class="sans b muted" font-size="10.5" letter-spacing="2">{esc(p['kind'].upper())}</text>
<text x="28" y="76" class="pir" font-size="34">{esc(p['name'])}</text>
{award}
{''.join(f'<text x="28" y="{y0 + i * 21}" class="sans" font-size="14">{esc(l)}</text>' for i, l in enumerate(desc))}
{tags}
{berry(28, 252)}<text x="44" y="252" font-size="20" style="font-family:Fell,serif;fill:{GOLD}">{esc(p['bounty'])} -</text>
<text x="{W - 28}" y="250" text-anchor="end" class="sans b gold" font-size="12" letter-spacing="1.5">SET SAIL →</text>"""
    return svg(W, H, body, POSTER_FONTS, BASE_CSS, p["name"])


def footer() -> str:
    W, H = 1000, 150
    body = f"""<defs><clipPath id="c"><rect width="{W}" height="{H}" rx="16"/></clipPath></defs>
<g clip-path="url(#c)">
  <rect width="{W}" height="{H}" fill="{NAVY}"/>
  {stars(30, W, 70, seed=11)}
  <path d="{wave_path(112, 8, 250, 1500, H)}" fill="#0f2f52" class="wv" style="animation-duration:12s"/>
  <path d="{wave_path(126, 9, 250, 1500, H)}" fill="#16477a" class="wv" style="animation-duration:8s"/>
</g>
<text x="500" y="56" text-anchor="middle" class="pir" font-size="30">The One Piece is real!</text>
<text x="500" y="84" text-anchor="middle" class="sans muted" font-size="13">zhengyaowong.cs@gmail.com  ·  zhengyaoportfolio.vercel.app</text>"""
    css = BASE_CSS + ".wv{animation:dr linear infinite}@keyframes dr{to{transform:translateX(-250px)}}"
    return svg(W, H, body, FONTS, css, "Footer")


HEADERS = {
    "projects": ("01", "Bounties", "things I've built and shipped"),
    "stack": ("02", "Devil Fruits", "what I build with"),
    "log": ("03", "Log Pose", "the last twelve months"),
}


def build() -> None:
    write(THEME, "hero", hero())
    write(THEME, "about", about())
    write(THEME, "footer", footer())
    write(THEME, "chest", chest())
    write(THEME, "sea-king", sea_king())
    write(THEME, "den-den-mushi", den_den_mushi())
    for label, _ in NAV:
        write(THEME, f"nav-{label.lower()}", nav(label))
    for key, (n, t, s) in HEADERS.items():
        write(THEME, f"h-{key}", header(n, t, s))
    for p in PROJECTS:
        write(THEME, f"card-{p['slug']}", card(p))
