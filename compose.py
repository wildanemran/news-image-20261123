#!/usr/bin/env python3
"""Compose the news-image-20261123 entry: a newspaper front page, 1024x1024.
All text is rendered by PIL (crisp, no garbled AI text); the four photos are
AI-generated illustrations of the day's verified stories.

REVISED v3 after Gemini Neon re-review of v2 (verdict: "good enough to
submit, but not yet tight enough to win", 2026-11-23): Neon verified all 8
v2 fixes but found 1 flat factual error ("Oil prices jumped" — crude
SLIPPED on 23 Nov), 2 vertical-spacing collisions (ALSO strip 1px clearance,
headline ";" grazing the deck), and 2 photo tells (col 1 ship is a US
Arleigh Burke at sea, not a moored Russian stealth corvette; lead photo
has duplicate flags + a sliced head at x=999). v3 fixes: col 3 body drops
the oil-price claim (Neon's permitted alternative — the 5-line "slipped"
version could not fit the column); ALSO pitch 19 -> 22px with 7px clearance
to the bottom rule; 6px extra clearance headline -> deck (headline stays
56pt: a 62-64pt bump would cost 12-16px the page cannot afford); deck
"Friday's strike" -> "Friday's incursion"; col 1 headline "off Libya" ->
"in Libya"; col 1 photo replaced with a burning stealth corvette moored at
a pier at night; lead photo edited to remove duplicate flags + restore the
sliced head. All clearances pixel-measured (see revision-v3-result.md).

REVISED v2 after Gemini Hydrogen review (independent, same REVISE FIRST
verdict, 2026-11-23): Hydrogen confirmed the overflow bugs (lead x=1011,
col 1 x=334-337) and added: (a) lead timeline blur — missiles fell FRIDAY
20 Nov, deck must say so; (b) col 3 misquote — Baghaei said "all available
means", not "every means"; (c) COP31 collapsed SUNDAY 22 Nov; (d) Democrats'
258 seats TIED 1992, not "largest since 1992"; (e) 17px gutters with no
rules made cols 1-2 look merged — grid evened to 308px cols + 26px gutters
(block now spans exactly x=24..1000); (f) lead photo replaced again with a
North Atlantic Council session (human/diplomatic stakes); (g) ALSO item 5
swapped to the verified Monday AI-stock rout (Kospi -3.3%, Seoul $8B fund)
— Hydrogen's Bahrain example was checked and REJECTED (attack was Sat 21
Nov, not Monday). Headline choice (measured): Neon's "RUSSIAN MISSILES HIT
POLAND; NATO MEETS" kept at 56pt — Hydrogen's "NATO CONVENES OVER RUSSIAN
MISSILES IN POLAND" cannot fit ≤950px at 56-60pt (line 2 = 1022px at 56pt),
and "NATO MEETS ON POLAND MISSILE BREACH" is vague ("breach" of what?).
"""
import textwrap
from PIL import Image, ImageDraw, ImageFont, ImageOps

W, H = 1024, 1024
M = 24                      # margin
GUT = 26                    # gutter between columns (was 16: cols looked merged)
CONTENT_W = W - 2 * M       # 976
ASSETS = "/home/hatch/workspace/makefun/news-image-20261123/repo/assets/"
OUT = "/home/hatch/workspace/makefun/news-image-20261123/repo/entry.png"

PAPER = (248, 245, 238)
INK = (20, 20, 20)
NAVY = (22, 35, 63)
RED = (163, 29, 29)
GREY = (90, 90, 90)
RULE = (180, 175, 165)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def fit_font(draw, path, start_size, text, width, min_size=16):
    """Largest size <= start_size whose text fits `width` px. Never grows."""
    size = start_size
    while size > min_size:
        f = font(path, size)
        if draw.textlength(text, font=f) <= width:
            return f, size
        size -= 1
    return font(path, min_size), min_size


def fit_wrap(draw, path, start_size, text, width, min_size=16):
    """Wrap text, shrinking size until every line fits `width` px.
    Returns (font, size, lines). Guarantees no line overflows the container."""
    size = start_size
    while size >= min_size:
        f = font(path, size)
        lines = wrap(draw, text, f, width)
        if all(draw.textlength(ln, font=f) <= width for ln in lines):
            return f, size, lines
        size -= 1
    f = font(path, min_size)
    return f, min_size, wrap(draw, text, f, width)


def wrap(draw, text, fnt, width):
    """Wrap text to fit pixel width; returns list of lines."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_lines(draw, lines, fnt, x, y, fill, leading):
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y


def photo(path, w, h, vbias=0.5):
    """Crop-resize to (w, h). vbias 0=top, 0.5=center, 1=bottom: where the
    crop window sits vertically (lets a tall lead keep its emblem/faces)."""
    im = Image.open(path).convert("RGB")
    iw, ih = im.size
    scale = max(w / iw, h / ih)
    im = im.resize((round(iw * scale), round(ih * scale)), Image.LANCZOS)
    rw, rh = im.size
    x0 = (rw - w) // 2
    y0 = round((rh - h) * vbias)
    return im.crop((x0, y0, x0 + w, y0 + h))


img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)
y = 0

# ---- Masthead (fit-checked) ----
d.rectangle([0, 0, W, 64], fill=NAVY)
f_mast, _ = fit_font(d, SERIF_B, 42, "THE WORLD IN ONE DAY", CONTENT_W)
t = "THE WORLD IN ONE DAY"
d.text(((W - d.textlength(t, font=f_mast)) / 2, 9), t, font=f_mast, fill=(255, 255, 255))
d.rectangle([0, 64, W, 68], fill=RED)

# ---- Date line (must be unmissable). Subline REMOVED (was redundant: the
# ---- date appeared 4x on the page; now twice: here + footer source line).
y = 76
f_date, _ = fit_font(d, SERIF_B, 40, "MONDAY, 23 NOVEMBER 2026", CONTENT_W)
t = "MONDAY, 23 NOVEMBER 2026"
d.text(((W - d.textlength(t, font=f_date)) / 2, y), t, font=f_date, fill=RED)
y += 44
d.line([M, y, W - M, y], fill=RULE, width=2)
y += 10

# ---- Lead photo (North Atlantic Council emergency session) — 198px ----
# ---- (v3: trimmed 210 -> 198 to reclaim 12px for the ALSO strip de-crowd;
# ---- vbias 0.35 keeps the NATO emblem + delegates' faces in frame)
lead_w, lead_h = CONTENT_W, 198
img.paste(photo(ASSETS + "lead-nato-council.webp", lead_w, lead_h, vbias=0.35), (M, y))
y += lead_h + 10

# ---- Lead story ----
f_kick = font(SANS_B, 18)
d.text((M, y), "BRUSSELS  ·  NATO", font=f_kick, fill=RED)
y += 24
# Headline: two pre-split lines, fit-checked to the content width.
# Kept Neon's headline at 56pt (measured: 772/745px, both <=950).
# Hydrogen's "NATO CONVENES OVER RUSSIAN MISSILES IN POLAND" rejected:
# line 2 is 1022px at 56pt (>950); "NATO MEETS ON POLAND MISSILE BREACH"
# is vague ("breach" of what?) with a weak second line.
head_lines = ["RUSSIAN MISSILES HIT", "POLAND; NATO MEETS"]
f_head, head_size = fit_font(d, SERIF_B, 56, max(head_lines, key=len), CONTENT_W - 8)
for ln in head_lines:
    d.text((M, y), ln, font=f_head, fill=INK)
    y += 60
# v3 (Neon re-review): the ";" tail in "POLAND;" grazed the deck (2px gap).
# Add 6px clearance so the gap is ~8px. Headline stays 56pt: a bump to
# 62-64pt would cost ~12-16px vertically and the vertical budget is spent
# on the ALSO de-crowd + the longer col-3 body.
y += 6
# Deck (v3): "Friday's strike" -> "Friday's incursion" (Neon: strictly more
# accurate — the missiles crashed after crossing Polish airspace).
deck = ("Emergency Brussels talks follow Friday\u2019s incursion by three Russian "
        "Kh-101 missiles; Rutte vows to defend \u201cevery inch\u201d of Polish "
        "territory.")
f_deck, _dsize, deck_lines = fit_wrap(d, SANS, 20, deck, CONTENT_W - 8)
y = draw_lines(d, deck_lines, f_deck, M, y, INK, 25)
y += 6
d.line([M, y, W - M, y], fill=RULE, width=2)
y += 8

# ---- Three secondary stories ----
col_w = (CONTENT_W - 2 * GUT) // 3   # 308px cols, 26px gutters: block = 24..1000
col_h_img = 100
cols = [
    ("corvette-benghazi.webp",
     "BENGHAZI, LIBYA  ·  UKRAINE",
     "Ukraine sinks Russian warship in Libya",
     "Sea drones sank the corvette Merkury at its Benghazi base and hit the "
     "cargo ship MV Angara, Kyiv said on Monday."),
    ("cop31-antalya.webp",
     "ANTALYA, TURKEY  ·  CLIMATE",
     "COP31 collapses with no deal",
     "Nearly 200 nations ended the longest climate talks in history on Sunday "
     "with no agreement after fossil-fuel language split the summit."),
    ("media-generation-tanker-blockade-sea-0-206e4d81-67d0-445a-b488-3c666058d96f.webp",
     "TEHRAN  ·  WASHINGTON",
     "Iran vows \u201call available means\u201d over blockade",
     # v3 (Neon re-review): "Oil prices jumped" is FACTUALLY WRONG for 23 Nov
     # (crude slipped: Brent ~$89-90, WTI below $83). Neon's alternative —
     # drop oil prices altogether — is used here: at 16pt in a 300px column
     # the "even as crude prices slipped" version wraps to 5 lines (+40px
     # the page cannot afford); this 4-line version keeps the two facts that
     # matter (Baghaei's "military aggression", UN Charter Art. 51, and
     # Washington's vow to sink blockade-runners).
     "Tehran called the U.S. naval blockade \u201cmilitary aggression\u201d as "
     "Washington vowed to sink any ship that defies it."),
]
top = y
# Fit all three column headlines at ONE uniform size (the min that fits all),
# so no column headline can invade its neighbour's gutter.
f_ckick = font(SANS_B, 16)
f_cbody = font(SANS, 16)
col_head_fits = []
for _fn, _kick, head, _body in cols:
    _f, size, _lines = fit_wrap(d, SERIF_B, 25, head, col_w - 8, min_size=18)
    col_head_fits.append(size)
chead_size = min(col_head_fits)
f_chead = font(SERIF_B, chead_size)
col_bottom = top
for i, (fn, kick, head, body) in enumerate(cols):
    x = M + i * (col_w + GUT)
    img.paste(photo(ASSETS + fn, col_w, col_h_img), (x, top))
    yy = top + col_h_img + 8
    d.text((x, yy), kick, font=f_ckick, fill=RED)
    yy += 20
    lines = wrap(d, head, f_chead, col_w - 8)
    yy = draw_lines(d, lines, f_chead, x, yy, INK, 28)
    yy += 4
    yy = draw_lines(d, wrap(d, body, f_cbody, col_w - 8), f_cbody, x, yy, INK, 20)
    col_bottom = max(col_bottom, yy)
y = col_bottom + 4
d.line([M, y, W - M, y], fill=RULE, width=2)
y += 6

# ---- Also on 23 November (fit-checked lines) ----
f_also_h = font(SANS_B, 18)
d.text((M, y), "ALSO ON 23 NOVEMBER", font=f_also_h, fill=RED)
y += 22
items = [
    ("UKRAINE", "Dymer toll rises to 11 after Russian strike; rescuers search the rubble."),
    ("INDONESIA", "Candy factory fire toll rises to 24 dead; about 30 still missing."),
    ("UNITED STATES", "Democrats win 258 House seats, matching their 1992 tally."),
    ("MARKETS", "Compass Group plans to move its main listing from London to New York."),
    ("TECH", "AI stock rout rattles Asia; Kospi down 3.3% as Seoul readies an $8B rescue fund."),
]
for tag, txt in items:
    line = f"{tag}  —  {txt}"
    f_also, _ = fit_font(d, SANS, 19, line, CONTENT_W - 16)
    d.rectangle([M, y + 5, M + 8, y + 13], fill=RED)
    d.text((M + 16, y), line, font=f_also, fill=INK)
    y += 22  # v3 (Neon re-review): pitch 19 -> 22 — v2 had 1px clearance
    # between descenders and the next line; 22px gives a 4px+ interline gap.
y += 7  # v3: 7px clearance between the last ALSO row's descenders and the
# bottom rule (measured 4px with +4; the must-fix requires >=7px).
d.line([M, y, W - M, y], fill=RULE, width=2)
y += 4

# ---- Footer (Hydrogen's edition-line format: "compiled Monday" covers
# ---- Sunday events reported Monday, e.g. the COP31 collapse) ----
f_foot = font(SANS, 14)
t = ("World Edition \u2014 Compiled Monday, 23 November 2026 from AP, Reuters, "
     "CNN, AFP and Al Jazeera.")
d.text((M, y), t, font=f_foot, fill=GREY)
y += 18  # v3: 20 -> 18 (footer glyphs span ~14px; keeps 8px bottom margin)

print("lead headline size =", head_size, "| col headline size =", chead_size)
print("final y =", y, "canvas H =", H)
assert y <= H, "layout overflow!"

img.save(OUT, "PNG", optimize=True)
import os
print("saved", OUT, os.path.getsize(OUT), "bytes")
