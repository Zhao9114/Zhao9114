"""Embed subset web fonts into SVGs as base64 @font-face rules.

SVGs shown through <img> on GitHub cannot load outside files, so every font
has to live inside the SVG itself. Subsetting to the characters actually used
keeps each file small.
"""
import base64
import io
from pathlib import Path

from fontTools import subset
from fontTools.ttLib import TTFont

FONT_DIR = Path(__file__).resolve().parent.parent / "assets" / "fonts"


def font_face(key: str, family: str, text: str | None = None) -> str:
    """Return an @font-face rule for assets/fonts/<key>.woff2.

    If text is given the font is cut down to just those characters.
    """
    path = FONT_DIR / f"{key}.woff2"
    if text:
        font = TTFont(path)
        opts = subset.Options()
        opts.flavor = "woff2"
        sub = subset.Subsetter(opts)
        sub.populate(text=text + " ")
        sub.subset(font)
        buf = io.BytesIO()
        font.flavor = "woff2"
        font.save(buf)
        data = buf.getvalue()
    else:
        data = path.read_bytes()
    b64 = base64.b64encode(data).decode()
    return (
        f"@font-face{{font-family:'{family}';"
        f"src:url(data:font/woff2;base64,{b64}) format('woff2');}}"
    )
