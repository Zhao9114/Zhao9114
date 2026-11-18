"""Render a GitHub contribution calendar as themed SVG widgets.

Styles
  map    parchment treasure map, dashed route through your busiest stretches, X on your best day
  beach  daytime version of sea: shallow water rising into sandy islands
  sea    night sea chart, quiet days are deep water, busy days rise into gold islands, a ship sails across
  manga  halftone panel, every day is an ink dot sized by how much you shipped

Usage
  python scripts/contrib.py --user Zhao9114 --out dist            # real data (needs GITHUB_TOKEN)
  python scripts/contrib.py --sample --out dist                    # made-up data for previews
  python scripts/contrib.py --user Zhao9114 --style sea --out dist
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import math
import os
import random
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from xml.sax.saxutils import escape

from fonts import font_face

# ----------------------------------------------------------------- data


@dataclass
class Day:
    date: dt.date
    count: int
    level: int = 0


def fetch_calendar(user: str, token: str) -> list[list[Day]]:
    query = """
    query($login: String!) {
      user(login: $login) {
        contributionsCollection {
          contributionCalendar {
            weeks { contributionDays { date contributionCount } }
          }
        }
      }
    }"""
    body = json.dumps({"query": query, "variables": {"login": user}}).encode()
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=body,
        headers={"Authorization": f"bearer {token}", "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        payload = json.load(resp)
    if "errors" in payload:
        raise SystemExit(f"GitHub API error: {payload['errors']}")
    weeks = payload["data"]["user"]["contributionsCollection"]["contributionCalendar"]["weeks"]
    return [
        [Day(dt.date.fromisoformat(d["date"]), d["contributionCount"]) for d in w["contributionDays"]]
        for w in weeks
    ]


def sample_calendar(end: dt.date | None = None, seed: int = 9114) -> list[list[Day]]:
    """Plausible fake year for previews: weekday rhythm, a busy summer, hackathon spikes."""
    rng = random.Random(seed)
    end = end or dt.date.today()
    start = end - dt.timedelta(days=364)
    start -= dt.timedelta(days=(start.weekday() + 1) % 7)  # back up to Sunday
    weeks, week = [], []
    d = start
    while d <= end:
        weekend = d.weekday() >= 5
        p = 0.36 if weekend else 0.58
        if d.month in (6, 7, 8):
            p += 0.18
        if d.month in (12,) and d.day > 15:
            p -= 0.3
        count = 0
        if rng.random() < p:
            count = max(1, int(rng.expovariate(1 / 3.2)))
            if d.month in (6, 7) and rng.random() < 0.2:
                count += rng.randint(5, 10)
        if d.month == 11 and d.year == end.year and 7 <= d.day <= 16:  # hackathon season
            count = rng.randint(9, 26)
        week.append(Day(d, count))
        if len(week) == 7:
            weeks.append(week)
            week = []
        d += dt.timedelta(days=1)
    if week:
        weeks.append(week)
    return weeks


def assign_levels(weeks: list[list[Day]]) -> None:
    nonzero = sorted(d.count for w in weeks for d in w if d.count)
    if not nonzero:
        return
    q = [nonzero[int(len(nonzero) * f)] for f in (0.25, 0.5, 0.75)]
    for w in weeks:
        for d in w:
            d.level = 0 if d.count == 0 else 1 + sum(d.count > t for t in q)


@dataclass
class Stats:
    total: int
    longest: int
    current: int
    best: Day


def stats(weeks: list[list[Day]]) -> Stats:
    days = [d for w in weeks for d in w]
    longest = run = 0
    for d in days:
        run = run + 1 if d.count else 0
        longest = max(longest, run)
    current = 0
    for i, d in enumerate(reversed(days)):
        if d.count:
            current += 1
        elif i == 0:  # today can still be empty without breaking the streak
            continue
        else:
            break
    best = max(days, key=lambda d: (d.count, d.date))
    return Stats(sum(d.count for d in days), longest, current, best)


def fmt_day(d: dt.date) -> str:
    return f"{d.strftime('%b')} {d.day}"


def month_labels(weeks: list[list[Day]]) -> list[tuple[int, str]]:
    out, last = [], None
    for i, w in enumerate(weeks):
        m = w[0].date.month
        if m != last:
            if i < len(weeks) - 2:
                out.append((i, w[0].date.strftime("%b")))
            last = m
    if len(out) > 1 and out[1][0] - out[0][0] < 3:  # partial first month would overlap
        out.pop(0)
    return out


def row_of(d: Day) -> int:
    return (d.date.weekday() + 1) % 7  # Sunday = 0, like GitHub


def catmull_rom(points: list[tuple[float, float]]) -> str:
    if len(points) < 2:
        return ""
    p = [points[0]] + points + [points[-1]]
    path = f"M{p[1][0]:.1f},{p[1][1]:.1f}"
    for i in range(1, len(p) - 2):
        x0, y0 = p[i - 1]
        x1, y1 = p[i]
        x2, y2 = p[i + 1]
        x3, y3 = p[i + 2]
        c1 = (x1 + (x2 - x0) / 6, y1 + (y2 - y0) / 6)
        c2 = (x2 - (x3 - x1) / 6, y2 - (y3 - y1) / 6)
        path += f" C{c1[0]:.1f},{c1[1]:.1f} {c2[0]:.1f},{c2[1]:.1f} {x2:.1f},{y2:.1f}"
    return path


ASCII = "".join(chr(c) for c in range(32, 127))

# ----------------------------------------------------------------- style: treasure map


def render_map(weeks: list[list[Day]], s: Stats) -> str:
    W, H = 1000, 300
    pitch, cell = 16.5, 13
    x0, y0 = 62 + (53 - len(weeks)) * pitch / 2, 104
    ink, red = "#3b2a1a", "#a4282b"
    alpha = [0, 0.22, 0.45, 0.68, 0.92]

    def center(i: int, d: Day) -> tuple[float, float]:
        return x0 + i * pitch + cell / 2, y0 + row_of(d) * pitch + cell / 2

    cells = []
    for i, w in enumerate(weeks):
        for d in w:
            x, y = x0 + i * pitch, y0 + row_of(d) * pitch
            if d.level == 0:
                cells.append(
                    f'<rect x="{x:.1f}" y="{y:.1f}" width="{cell}" height="{cell}" rx="2" '
                    f'fill="{ink}" fill-opacity=".06" stroke="{ink}" stroke-opacity=".18" stroke-width=".8"/>'
                )
            else:
                cells.append(
                    f'<rect x="{x:.1f}" y="{y:.1f}" width="{cell}" height="{cell}" rx="2" '
                    f'fill="{ink}" fill-opacity="{alpha[d.level]}"><title>{d.count} on {fmt_day(d.date)}</title></rect>'
                )

    # route: busiest day in each of 8 stretches of the year, joined into a smooth path
    n = 8
    chunk = max(1, math.ceil(len(weeks) / n))
    pts = []
    for c in range(0, len(weeks), chunk):
        best = max(
            ((i, d) for i in range(c, min(c + chunk, len(weeks))) for d in weeks[i]),
            key=lambda t: t[1].count,
        )
        if best[1].count:
            pts.append(center(*best))
    bi = next(i for i, w in enumerate(weeks) if s.best in w)
    bx, by = center(bi, s.best)
    pts = [p for p in pts if abs(p[0] - bx) > 1 or abs(p[1] - by) > 1]
    pts.append((bx, by))
    pts.sort()
    route = catmull_rom(pts)
    waypoints = "".join(
        f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3" fill="#f1e3c3" stroke="{red}" stroke-width="1.6"/>'
        for x, y in pts
        if (x, y) != (bx, by)
    )

    months = "".join(
        f'<text x="{x0 + i * pitch:.1f}" y="{y0 - 10}" class="lbl">{m}</text>' for i, m in month_labels(weeks)
    )
    days = "".join(
        f'<text x="{x0 - 10:.1f}" y="{y0 + r * pitch + 10:.1f}" class="lbl" text-anchor="end">{t}</text>'
        for r, t in ((1, "Mon"), (3, "Wed"), (5, "Fri"))
    )
    legend_x = W - 210
    legend = f'<text x="{legend_x - 8}" y="269" class="lbl" text-anchor="end">calm</text>' + "".join(
        f'<rect x="{legend_x + k * 16}" y="259" width="12" height="12" rx="2" fill="{ink}" '
        f'fill-opacity="{alpha[k] if k else 0.06}" stroke="{ink}" stroke-opacity="{0.18 if k == 0 else 0}"/>'
        for k in range(5)
    ) + f'<text x="{legend_x + 84}" y="269" class="lbl">stormy</text>'

    stats_line = (
        f"{s.total:,} contributions   ·   longest voyage {s.longest} days   ·   "
        f"X marks {fmt_day(s.best.date)} ({s.best.count})"
    )

    compass = f"""
    <g transform="translate(925 58)" class="spin">
      <circle r="30" fill="none" stroke="{ink}" stroke-opacity=".5"/>
      <circle r="24" fill="none" stroke="{ink}" stroke-opacity=".3" stroke-dasharray="2 3"/>
      <polygon points="0,-28 5,0 0,28 -5,0" fill="{ink}" fill-opacity=".85"/>
      <polygon points="-28,0 0,5 28,0 0,-5" fill="{ink}" fill-opacity=".45"/>
      <polygon points="0,-28 5,0 0,0" fill="{red}"/>
    </g>
    <text x="925" y="20" class="lbl" text-anchor="middle" font-size="12">N</text>"""

    css = (
        font_face("pirata", "Pirata", ASCII)
        + font_face("fell", "Fell", ASCII)
        + f"""
    .t{{font-family:Pirata,serif;font-size:32px;fill:{ink}}}
    .lbl{{font-family:Fell,Georgia,serif;font-size:11px;fill:{ink};fill-opacity:.75}}
    .st{{font-family:Fell,Georgia,serif;font-size:15px;fill:{ink}}}
    .route{{stroke-dasharray:7 6;animation:march 1.4s linear infinite}}
    @keyframes march{{to{{stroke-dashoffset:-26}}}}
    .ring{{transform-box:fill-box;transform-origin:center;animation:ping 2.4s ease-out infinite}}
    @keyframes ping{{0%{{transform:scale(.6);opacity:.9}}100%{{transform:scale(2.4);opacity:0}}}}
    .spin{{animation:sway 6s ease-in-out infinite}}
    @keyframes sway{{0%,100%{{transform:translate(925px,58px) rotate(-6deg)}}50%{{transform:translate(925px,58px) rotate(6deg)}}}}
    @media (prefers-reduced-motion:reduce){{.route,.ring,.spin{{animation:none}}}}
    """
    )

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="Contribution chart: {s.total} contributions in the last year">
  <defs>
    <style>{css}</style>
    <filter id="paper"><feTurbulence type="fractalNoise" baseFrequency=".9" numOctaves="3" seed="4"/>
      <feColorMatrix values="0 0 0 0 .23  0 0 0 0 .16  0 0 0 0 .1  0 0 0 .09 0"/></filter>
    <radialGradient id="burn" cx="50%" cy="50%" r="75%"><stop offset=".6" stop-color="#000" stop-opacity="0"/>
      <stop offset="1" stop-color="#5a3a1a" stop-opacity=".45"/></radialGradient>
  </defs>
  <rect width="{W}" height="{H}" rx="14" fill="#f1e3c3"/>
  <rect width="{W}" height="{H}" rx="14" filter="url(#paper)"/>
  <rect width="{W}" height="{H}" rx="14" fill="url(#burn)"/>
  <rect x="10" y="10" width="{W - 20}" height="{H - 20}" rx="8" fill="none" stroke="{ink}" stroke-opacity=".35" stroke-dasharray="1 4"/>
  <text x="40" y="58" class="t">The Year's Chart</text>
  <text x="42" y="80" class="lbl" font-size="13">a record of every day at sea, drawn fresh each morning</text>
  {compass}
  {months}{days}
  {''.join(cells)}
  <path d="{route}" fill="none" stroke="{red}" stroke-width="2.2" stroke-linecap="round" class="route"/>
  {waypoints}
  <circle cx="{bx:.1f}" cy="{by:.1f}" r="8" fill="none" stroke="{red}" stroke-width="1.5" class="ring"/>
  <g stroke="{red}" stroke-width="3.2" stroke-linecap="round">
    <line x1="{bx - 7:.1f}" y1="{by - 7:.1f}" x2="{bx + 7:.1f}" y2="{by + 7:.1f}"/>
    <line x1="{bx + 7:.1f}" y1="{by - 7:.1f}" x2="{bx - 7:.1f}" y2="{by + 7:.1f}"/>
  </g>
  <line x1="40" y1="236" x2="{W - 40}" y2="236" stroke="{ink}" stroke-opacity=".25"/>
  <text x="40" y="270" class="st">{escape(stats_line)}</text>
  {legend}
</svg>"""


# ----------------------------------------------------------------- style: night sea chart


SHIP_T = """
<g>
  <path d="M-17,4 L17,4 L12,12 L-12,12 Z" fill="#7a4a24" stroke="{hull_line}" stroke-width="1"/>
  <line x1="-3" y1="4" x2="-3" y2="-20" stroke="{pole}" stroke-width="1.4"/>
  <line x1="7" y1="4" x2="7" y2="-13" stroke="{pole}" stroke-width="1.2"/>
  <path d="M-3,-18 Q8,-11 -3,-2 Z" fill="#f3ead6"/>
  <path d="M7,-12 Q14,-7 7,1 Z" fill="#f3ead6"/>
  <path d="M-3,-20 L-12,-17 L-3,-15 Z" fill="#e5484d"/>
</g>"""


NIGHT = dict(
    bg=("#0a1628", "#0d2440"), title="#f4c95d", label="#8aa4c4", wave="#8fc6ff", wave_op=".08",
    cells=["#12233c", "#14506a", "#1f8a8a", "#d9b26a", "#f4c95d"], glint="#fff1bf", frame="#f4c95d",
    pole="#e8dcc0", hull_line="#f4c95d", low="DEEP", high="ISLANDS",
)
DAY = dict(
    bg=("#e4f6fb", "#fff6e3"), title="#0f3550", label="#5a7d94", wave="#1fa8c9", wave_op=".16",
    cells=["#d3ecf2", "#8fd6e6", "#2fb4cf", "#f1c97e", "#f59e3d"], glint="#ffd27a", frame="#1fa8c9",
    pole="#5b3a1f", hull_line="#4a2c16", low="WATER", high="ISLANDS",
)


def render_sea(weeks: list[list[Day]], s: Stats, pal: dict = NIGHT) -> str:
    SHIP = SHIP_T.replace("{hull_line}", pal["hull_line"]).replace("{pole}", pal["pole"])
    W, H = 1000, 356
    pitch, cell = 16.5, 13
    x0, y0 = 62 + (53 - len(weeks)) * pitch / 2, 136
    colors = pal["cells"]

    cells = []
    for i, w in enumerate(weeks):
        for d in w:
            x, y = x0 + i * pitch, y0 + row_of(d) * pitch
            cls = ' class="g"' if d.level == 4 else ""
            delay = f' style="animation-delay:{(i * 97) % 3000}ms"' if d.level == 4 else ""
            tip = f"<title>{d.count} on {fmt_day(d.date)}</title>" if d.count else ""
            cells.append(
                f'<rect x="{x:.1f}" y="{y:.1f}" width="{cell}" height="{cell}" rx="3" fill="{colors[d.level]}"{cls}{delay}>{tip}</rect>'
            )

    bi = next(i for i, w in enumerate(weeks) if s.best in w)
    fx, fy = x0 + bi * pitch + cell / 2, y0 + row_of(s.best) * pitch
    flag = (
        f'<line x1="{fx:.1f}" y1="{fy + 4:.1f}" x2="{fx:.1f}" y2="{fy - 16:.1f}" stroke="{pal['pole']}" stroke-width="1.3"/>'
        f'<path d="M{fx:.1f},{fy - 16:.1f} l11,4 l-11,4 z" fill="#e5484d" class="flap"/>'
    )

    months = "".join(
        f'<text x="{x0 + i * pitch:.1f}" y="{y0 - 10}" class="lbl">{m}</text>' for i, m in month_labels(weeks)
    )
    days = "".join(
        f'<text x="{x0 - 10:.1f}" y="{y0 + r * pitch + 10:.1f}" class="lbl" text-anchor="end">{t}</text>'
        for r, t in ((1, "Mon"), (3, "Wed"), (5, "Fri"))
    )

    lane = "M-30,92 " + " ".join(
        f"Q{-30 + k * 60 + 30},{86 if k % 2 else 98} {-30 + (k + 1) * 60},92" for k in range(18)
    )
    waves = "".join(
        f'<path d="M-200,{y} ' + " ".join(f"q25,-6 50,0 q25,6 50,0" for _ in range(28)) + f'" class="wv" style="animation-duration:{d}s"/>'
        for y, d in ((40, 26), (96, 34), (250, 30), (318, 38))
    )

    tiles = [
        (f"{s.total:,}", "contributions"),
        (f"{s.longest}d", "longest voyage"),
        (f"{s.current}d", "current streak"),
        (fmt_day(s.best.date), f"best day · {s.best.count}"),
    ]
    tile_svg = "".join(
        f'<text x="{60 + k * 190}" y="318" class="big">{escape(v)}</text>'
        f'<text x="{60 + k * 190}" y="338" class="cap">{escape(c.upper())}</text>'
        for k, (v, c) in enumerate(tiles)
    )
    lx = W - 220
    legend = (
        f'<text x="{lx - 8}" y="324" class="cap" text-anchor="end">{pal['low']}</text>'
        + "".join(f'<rect x="{lx + k * 16}" y="314" width="12" height="12" rx="3" fill="{c}"/>' for k, c in enumerate(colors))
        + f'<text x="{lx + 86}" y="324" class="cap">{pal['high']}</text>'
    )

    css = (
        font_face("pirata", "Pirata", ASCII)
        + font_face("inter", "Inter", ASCII)
        + f"""
    .t{{font-family:Pirata,serif;font-size:32px;fill:{pal['title']}}}
    .lbl{{font-family:Inter,system-ui,sans-serif;font-size:10.5px;fill:{pal['label']}}}
    .big{{font-family:Pirata,serif;font-size:26px;fill:{pal['title']}}}
    .cap{{font-family:Inter,system-ui,sans-serif;font-size:10px;letter-spacing:1.4px;fill:{pal['label']}}}
    .wv{{fill:none;stroke:{pal['wave']};stroke-opacity:{pal['wave_op']};stroke-width:1.2;animation:drift linear infinite}}
    @keyframes drift{{to{{transform:translateX(100px)}}}}
    .g{{animation:glint 3s ease-in-out infinite}}
    @keyframes glint{{0%,100%{{fill:{colors[4]}}}50%{{fill:{pal['glint']}}}}}
    .flap{{transform-box:fill-box;transform-origin:left center;animation:flap 1.2s ease-in-out infinite alternate}}
    @keyframes flap{{to{{transform:scaleX(.7)}}}}
    @media (prefers-reduced-motion:reduce){{.wv,.g,.flap{{animation:none}}}}
    """
    )

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="Sea chart of {s.total} contributions in the last year">
  <defs>
    <style>{css}</style>
    <linearGradient id="sea" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{pal['bg'][0]}"/><stop offset="1" stop-color="{pal['bg'][1]}"/></linearGradient>
    <clipPath id="frame"><rect width="{W}" height="{H}" rx="14"/></clipPath>
  </defs>
  <g clip-path="url(#frame)">
    <rect width="{W}" height="{H}" fill="url(#sea)"/>
    {waves}
  </g>
  <rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="14" fill="none" stroke="{pal['frame']}" stroke-opacity=".3"/>
  <text x="40" y="50" class="t">Sea Chart</text>
  <text x="{W - 40}" y="46" class="cap" text-anchor="end">LAST 12 MONTHS · UPDATED DAILY</text>
  <path d="{lane}" fill="none" stroke="{pal['wave']}" stroke-opacity=".3" stroke-dasharray="2 6"/>
  <g>{SHIP}<animateMotion dur="26s" repeatCount="indefinite" rotate="auto" path="{lane}"/></g>
  {months}{days}
  {''.join(cells)}
  {flag}
  <line x1="40" y1="280" x2="{W - 40}" y2="280" stroke="{pal['frame']}" stroke-opacity=".2"/>
  {tile_svg}
  {legend}
</svg>"""


# ----------------------------------------------------------------- style: manga halftone


def render_manga(weeks: list[list[Day]], s: Stats) -> str:
    W, H = 1000, 340
    pitch = 16.5
    x0, y0 = 62 + (53 - len(weeks)) * pitch / 2 + 6, 124
    radius = [1.4, 3.1, 4.5, 5.9, 7.4]
    ink, red, paper = "#111111", "#e63946", "#f7f4ec"

    bi = next(i for i, w in enumerate(weeks) if s.best in w)
    dots = []
    for i, w in enumerate(weeks):
        for d in w:
            cx, cy = x0 + i * pitch, y0 + row_of(d) * pitch
            fill = red if d is s.best else (ink if d.level else "#bdb6a6")
            tip = f"<title>{d.count} on {fmt_day(d.date)}</title>" if d.count else ""
            dots.append(
                f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{radius[d.level] + (1 if d is s.best else 0)}" fill="{fill}" '
                f'class="p" style="animation-delay:{i * 26}ms">{tip}</circle>'
            )

    bx, by = x0 + bi * pitch, y0 + row_of(s.best) * pitch
    spikes = []
    for k in range(24):
        a = k * math.pi / 12
        r = 19 if k % 2 == 0 else 11
        spikes.append(f"{bx + r * math.cos(a):.1f},{by + r * math.sin(a):.1f}")
    burst = f'<polygon points="{" ".join(spikes)}" fill="{paper}" stroke="{red}" stroke-width="2" class="pulse"/>'

    months = "".join(
        f'<text x="{x0 + i * pitch - 6:.1f}" y="{y0 - 16}" class="lbl">{m.upper()}</text>' for i, m in month_labels(weeks)
    )

    # speed lines in the top right corner
    lines = []
    rnd = random.Random(7)
    for k in range(26):
        a = math.radians(200 + k * 2.6)
        r1, r2 = 110 + rnd.random() * 40, 330
        cx, cy = W + 40, -60
        lines.append(
            f'<line x1="{cx + r1 * math.cos(a):.1f}" y1="{cy - r1 * math.sin(a):.1f}" '
            f'x2="{cx + r2 * math.cos(a):.1f}" y2="{cy - r2 * math.sin(a):.1f}" stroke="{ink}" stroke-width="{0.6 + rnd.random() * 1.6:.1f}"/>'
        )

    css = (
        font_face("bangers", "Bangers", ASCII)
        + font_face("inter-bold", "InterB", ASCII)
        + f"""
    .h{{font-family:Bangers,Impact,sans-serif;font-size:34px;letter-spacing:1.5px;fill:{ink}}}
    .cap{{font-family:Bangers,Impact,sans-serif;font-size:22px;letter-spacing:1.5px;fill:{paper}}}
    .lbl{{font-family:InterB,system-ui,sans-serif;font-size:9.5px;letter-spacing:1px;fill:{ink}}}
    .say{{font-family:Bangers,Impact,sans-serif;font-size:20px;letter-spacing:1px;fill:{ink}}}
    .p{{transform-box:fill-box;transform-origin:center;animation:wave 7s ease-in-out infinite}}
    @keyframes wave{{0%,10%,100%{{transform:scale(1)}}5%{{transform:scale(1.45)}}}}
    .pulse{{transform-box:fill-box;transform-origin:center;animation:thump 1.6s ease-in-out infinite}}
    @keyframes thump{{0%,100%{{transform:scale(1) rotate(0)}}50%{{transform:scale(1.15) rotate(8deg)}}}}
    @media (prefers-reduced-motion:reduce){{.p,.pulse{{animation:none}}}}
    """
    )

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="Training arc: {s.total} contributions in the last year">
  <defs>
    <style>{css}</style>
    <pattern id="tone" width="7" height="7" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">
      <circle cx="3.5" cy="3.5" r="1.3" fill="{ink}" fill-opacity=".22"/></pattern>
    <clipPath id="panel"><rect x="12" y="12" width="{W - 24}" height="{H - 24}"/></clipPath>
    <clipPath id="corner"><rect x="640" y="12" width="{W - 652}" height="82"/></clipPath>
  </defs>
  <rect width="{W}" height="{H}" fill="{paper}"/>
  <g clip-path="url(#corner)">{''.join(lines)}</g>
  <g clip-path="url(#panel)">
    <rect x="12" y="250" width="{W - 24}" height="80" fill="url(#tone)"/></g>
  <rect x="12" y="12" width="{W - 24}" height="{H - 24}" fill="none" stroke="{ink}" stroke-width="4"/>
  <g transform="rotate(-2 120 46)">
    <rect x="30" y="26" width="196" height="40" fill="{ink}"/>
    <text x="44" y="56" class="cap">TRAINING ARC</text>
  </g>
  <text x="248" y="58" class="h">{s.total:,} CONTRIBUTIONS THIS YEAR!</text>
  {months}
  {burst}
  {''.join(dots)}
  <g transform="translate(36 262)">
    <rect width="260" height="50" fill="{paper}" stroke="{ink}" stroke-width="3"/>
    <text x="14" y="33" class="say">BEST DAY: {escape(fmt_day(s.best.date).upper())} · {s.best.count}</text>
  </g>
  <g transform="translate({W - 330} 252)">
    <path d="M10,34 C10,8 290,8 290,34 C290,60 120,62 70,58 L36,76 L48,54 C22,50 10,44 10,34 Z" fill="#fff" stroke="{ink}" stroke-width="3"/>
    <text x="150" y="42" class="say" text-anchor="middle">LONGEST STREAK: {s.longest} DAYS!</text>
  </g>
</svg>"""


# ----------------------------------------------------------------- main

def render_beach(weeks: list[list[Day]], s: Stats) -> str:
    return render_sea(weeks, s, DAY)


RENDERERS = {"map": render_map, "sea": render_sea, "beach": render_beach, "manga": render_manga}


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--user", default=os.environ.get("GITHUB_USER"))
    ap.add_argument("--style", choices=[*RENDERERS, "all"], default="all")
    ap.add_argument("--out", default="dist")
    ap.add_argument("--sample", action="store_true", help="use made-up data instead of the API")
    args = ap.parse_args()

    if args.sample:
        weeks = sample_calendar()
    else:
        token = os.environ.get("GITHUB_TOKEN")
        if not (args.user and token):
            raise SystemExit("need --user and GITHUB_TOKEN (or pass --sample)")
        weeks = fetch_calendar(args.user, token)

    assign_levels(weeks)
    s = stats(weeks)
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    for name in RENDERERS if args.style == "all" else [args.style]:
        (out / f"contrib-{name}.svg").write_text(RENDERERS[name](weeks, s), encoding="utf-8")
        print(f"wrote {out / f'contrib-{name}.svg'}")


if __name__ == "__main__":
    main()
