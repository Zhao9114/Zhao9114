"""Shared content and SVG helpers for the README themes."""
from __future__ import annotations

import random
import textwrap
from pathlib import Path
from xml.sax.saxutils import escape

from fonts import font_face

ROOT = Path(__file__).resolve().parent.parent

# ------------------------------------------------------------------ content

NAME = "Zheng Yao Wong"
ROLE = "Full-stack developer"
ORIGIN = "Malaysia → Arlington, TX"
TAGLINE = "CS senior at UT Arlington. I like building things people actually use."
STATUS = "currently teaching an app to watch sparring footage"

NOW = [
    ("Studying", "Senior CS at UT Arlington, May 2027"),
    ("Working", "Web Developer at UTA's Office of IT"),
    ("Building", "Combat Capture, ML for sparring"),
    ("Looking for", "Summer 2027 SWE internships"),
]

PORTFOLIO = "https://zhengyaoportfolio.vercel.app"
NAV = [
    ("Portfolio", f"{PORTFOLIO}/recruiter"),
    ("Projects", f"{PORTFOLIO}/recruiter/projects"),
    ("Research", f"{PORTFOLIO}/recruiter/research"),
    ("Resume", f"{PORTFOLIO}/recruiter/resume"),
    ("LinkedIn", "https://www.linkedin.com/in/zheng-yao-wong/"),
    ("Email", "mailto:zhengyaowong.cs@gmail.com"),
]

PROJECTS = [
    dict(
        slug="finvantage",
        bounty="1,500,000,000",
        name="FinVantage",
        kind="Hackathon · 2026",
        award="PNC Track Winner, HackUTD",
        desc="AI finance copilot that pulls every account into one place and warns you before you spend. Every figure is computed in code, not by the model.",
        tech=["Next.js", "Hono", "MongoDB", "Plaid", "Gemini"],
        url="https://github.com/ashzaeen/FinVantage",
    ),
    dict(
        slug="draftly",
        bounty="800,000,000",
        name="Draftly",
        kind="Class project · 2026",
        award=None,
        desc="Resume builder where every section is a draggable block: five templates, saved versions tied to a job tracker, and an ATS check scored in code.",
        tech=["React", "TypeScript", "dnd-kit", "Supabase", "Claude"],
        url="https://github.com/Zhao9114/CSE3311_resumeBuilder",
    ),
    dict(
        slug="bacteria",
        bounty="650,000,000",
        name="Bacteria Annotator",
        kind="Research · UTA lab",
        award=None,
        desc="Researchers outline bacteria cells and get measurements that match the lab's neural network, so human and model results line up.",
        tech=["TypeScript", "Canvas 2D", "Supabase", "WebCodecs"],
        url="https://github.com/Zhao9114/bacteria_annotation",
    ),
    dict(
        slug="furever",
        bounty="320,000,000",
        name="Furever Home",
        kind="Hackathon · 2024",
        award="Best Use of MongoDB Atlas, HackUTA 6",
        desc="Swipe-based adoption app that matches people with adoptable shelter dogs, built in a weekend.",
        tech=["Next.js", "Flask", "MongoDB", "OpenAI"],
        url="https://github.com/kztJames01/hackUTA",
    ),
]

# ------------------------------------------------------------------ helpers


def wrap(text: str, width: int) -> list[str]:
    return textwrap.wrap(text, width)


def esc(s: str) -> str:
    return escape(s)


def svg(w: int, h: int, body: str, fonts: list[tuple[str, str]], css: str, label: str) -> str:
    chars = "".join(sorted(set(body))) + "0123456789"
    faces = "".join(font_face(k, fam, chars) for k, fam in fonts)
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" '
        f'role="img" aria-label="{esc(label)}">\n<defs><style>{faces}{css}'
        "@media (prefers-reduced-motion:reduce){*{animation:none!important}}"
        f"</style></defs>\n{body}\n</svg>"
    )


def write(theme: str, name: str, content: str) -> None:
    out = ROOT / "assets" / theme
    out.mkdir(parents=True, exist_ok=True)
    (out / f"{name}.svg").write_text(content, encoding="utf-8")


def emblem(ink: str, hole: str, accent: str | None = None) -> str:
    """Original flag mark: a skull written as a self-closing tag, <skull />. Centered on 0,0, ~90 wide."""
    accent = accent or ink
    return f"""<g>
  <path d="M-30,-14 L-44,0 L-30,14" fill="none" stroke="{accent}" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/>
  <path d="M28,16 L36,-16" fill="none" stroke="{accent}" stroke-width="6" stroke-linecap="round"/>
  <path d="M38,-14 L52,0 L38,14" fill="none" stroke="{accent}" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/>
  <ellipse cx="0" cy="-5" rx="19" ry="18" fill="{ink}"/>
  <rect x="-11" y="5" width="22" height="13" rx="4" fill="{ink}"/>
  <circle cx="-7.5" cy="-5" r="5.4" fill="{hole}"/>
  <circle cx="7.5" cy="-5" r="5.4" fill="{hole}"/>
  <path d="M0,2 L-3,7 L3,7 Z" fill="{hole}"/>
  <path d="M-5,11 V17 M0,11 V17 M5,11 V17" stroke="{hole}" stroke-width="1.6"/>
</g>"""


def stars(n: int, w: int, h: int, seed: int = 3) -> str:
    rnd = random.Random(seed)
    out = []
    for _ in range(n):
        x, y = rnd.uniform(0, w), rnd.uniform(0, h)
        r = rnd.choice([0.6, 0.8, 1.0, 1.3, 1.7])
        d = rnd.uniform(0, 4)
        out.append(
            f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r}" fill="#fff" class="tw" style="animation-delay:{d:.1f}s"/>'
        )
    return "".join(out)


def wave_path(y: float, amp: float, length: float, width: float, bottom: float) -> str:
    """Closed wave shape from x=0 to x=width, filled down to `bottom`."""
    d = f"M0,{y}"
    x = 0.0
    while x < width:
        d += f" q{length / 4},{-amp} {length / 2},0 q{length / 4},{amp} {length / 2},0"
        x += length
    return d + f" L{x},{bottom} L0,{bottom} Z"
