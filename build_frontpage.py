#!/usr/bin/env python3
"""Build the front page for news-image-20261119 (v3 rebuild, winner template).

Total rewrite of the v2 text-only page, following the stable winner
template seen in 15/15 top-5 images across news-18/19/20:
  cream paper + navy band, giant serif date, coloured region bar,
  "THE DAY IN NUMBERS" strip, 3 illustrated hero cards, 10 illustrated
  medium cards, dotted world map "WHERE IT HAPPENED" with numbered pins,
  numbered ALSO list 14-36, DATE CHECK box, per-story sources.

All 13 illustrations are flat vector shapes drawn in code (PIL) — no
photographs, no AI images. Deterministic: fixed fonts, fixed layout,
no clock, no network, no randomness. Two runs produce byte-identical
PNG. Output entry.png is committed to the repo; main.ts copies it to
/output/entry.png.

Every story carries event_date + source in stories.json. The iron rule:
event date is when the event HAPPENED, never the article date. Stories
first reported on 18 Nov (EU EUR45bn loan, Van Gogh $190.4m, Libya
seizure, Voyager 1, CMA Awards, Pew study) are NOT news here — they are
listed in the DATE CHECK box as deliberately excluded.

Fonts: OFL faces bundled with the canvas-design skill
  (~/workspace/custom-skills/canvas-design/canvas-fonts/).
"""

import json
import math
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
MARGIN = 30
CW = W - 2 * MARGIN  # 964

FONT_DIR = os.path.expanduser(
    "~/workspace/custom-skills/canvas-design/canvas-fonts"
)

# Palette: cream paper, ink, navy, ONE accent red, muted region colours.
PAPER = (247, 242, 231)
PANEL = (252, 249, 242)
PANEL2 = (240, 234, 220)
INK = (22, 22, 22)
NAVY = (27, 42, 74)
RED = (178, 34, 22)
GOLD = (176, 141, 87)
GREY = (96, 94, 88)
HAIRLINE = (205, 198, 184)
TEAL = (31, 111, 107)
GREEN = (74, 124, 58)
PURPLE = (106, 76, 147)
ORANGE = (214, 110, 44)
SKY = (58, 90, 140)
SKIN = (232, 190, 160)
DARKGREEN = (16, 60, 48)

REGION_COLORS = {
    "EUROPE": NAVY,
    "ASIA": RED,
    "AMERICAS": TEAL,
    "MIDDLE EAST": GOLD,
    "AFRICA": GREEN,
    "OCEANIA": PURPLE,
    "GLOBAL": (90, 88, 84),
}

HERE = os.path.dirname(os.path.abspath(__file__))
_FONTS = {}


def font(name, size):
    key = (name, size)
    if key not in _FONTS:
        _FONTS[key] = ImageFont.truetype(os.path.join(FONT_DIR, name), size)
    return _FONTS[key]


def wrap(text, fnt, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if fnt.getlength(trial) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_tracked(dr, x, y, text, fnt, fill, tracking=3):
    cx = x
    for ch in text:
        dr.text((cx, y), ch, font=fnt, fill=fill)
        cx += int(fnt.getlength(ch)) + tracking
    return cx


def tracked_width(text, fnt, tracking=3):
    return sum(int(fnt.getlength(ch)) + tracking for ch in text) - tracking


def center_tracked(dr, cx, y, text, fnt, fill, tracking=3):
    w = tracked_width(text, fnt, tracking)
    draw_tracked(dr, cx - w // 2, y, text, fnt, fill, tracking)


def rule(dr, x0, x1, y, fill=HAIRLINE, width=1):
    dr.line([(x0, y), (x1, y)], fill=fill, width=width)


def fit_one(text, fnt, max_w):
    """Shorten with an ellipsis until it fits one line."""
    while fnt.getlength(text) > max_w and len(text) > 10:
        text = text[:-5].rstrip() + "…"
    return text


# ---------------------------------------------------------------------------
# Illustrations — flat vector, drawn in code. One per feature card.
# Each takes (dr, x, y, w, h) and fills its own background.
# ---------------------------------------------------------------------------

def _flag_us(dr, x, y, w, h):
    for i in range(7):
        dr.rectangle([x, y + i * h / 7, x + w, y + (i + 1) * h / 7],
                     fill=RED if i % 2 == 0 else (250, 250, 250))
    dr.rectangle([x, y, x + w * 0.42, y + h * 4 / 7], fill=NAVY)
    for r in range(2):
        for c in range(3):
            dr.ellipse([x + 3 + c * w * 0.11, y + 3 + r * h * 0.2,
                        x + 6 + c * w * 0.11, y + 6 + r * h * 0.2],
                       fill=(255, 255, 255))


def _flag_cn(dr, x, y, w, h):
    dr.rectangle([x, y, x + w, y + h], fill=RED)
    dr.ellipse([x + w * 0.12, y + h * 0.18, x + w * 0.32, y + h * 0.5],
               fill=(255, 220, 60))
    for cx, cy in [(0.55, 0.25), (0.68, 0.38), (0.68, 0.58), (0.55, 0.68)]:
        dr.ellipse([x + w * cx - 2, y + h * cy - 2, x + w * cx + 2,
                    y + h * cy + 2], fill=(255, 220, 60))


def _flag_ru(dr, x, y, w, h):
    dr.rectangle([x, y, x + w, y + h / 3], fill=(250, 250, 250))
    dr.rectangle([x, y + h / 3, x + w, y + 2 * h / 3], fill=SKY)
    dr.rectangle([x, y + 2 * h / 3, x + w, y + h], fill=RED)


def _flag_de(dr, x, y, w, h):
    dr.rectangle([x, y, x + w, y + h / 3], fill=INK)
    dr.rectangle([x, y + h / 3, x + w, y + 2 * h / 3], fill=RED)
    dr.rectangle([x, y + 2 * h / 3, x + w, y + h], fill=(255, 206, 0))


def art_summit(dr, x, y, w, h):
    """Three leaders at a round table, three flags behind them."""
    dr.rectangle([x, y, x + w, y + h], fill=NAVY)
    dr.rectangle([x, y + h * 0.62, x + w, y + h], fill=(214, 110, 44))
    sun_r = 14
    dr.ellipse([x + w - 34 - sun_r, y + 10, x + w - 34 + sun_r, y + 10 + 2 * sun_r],
               fill=(255, 200, 90))
    # Flags on poles.
    for i, fl in enumerate((_flag_us, _flag_cn, _flag_ru)):
        fx = x + w * (0.14 + i * 0.33)
        dr.line([(fx, y + 8), (fx, y + h * 0.52)], fill=(240, 240, 240), width=2)
        fl(dr, fx + 1, y + 8, 34, 22)
    # Three seated figures: head + shoulders.
    for i, col in enumerate((NAVY, RED, (60, 60, 60))):
        cx = x + w * (0.2 + i * 0.3)
        dr.ellipse([cx - 13, y + h * 0.5, cx + 13, y + h * 0.5 + 26], fill=SKIN)
        dr.pieslice([cx - 24, y + h * 0.66, cx + 24, y + h * 0.66 + 44],
                    180, 360, fill=col)
    # Round table + name plates.
    dr.ellipse([x + w * 0.08, y + h * 0.72, x + w * 0.92, y + h * 0.98],
               fill=(240, 235, 220))
    fnt = font("IBMPlexMono-Bold.ttf", 9)
    for i, name in enumerate(("TRUMP", "XI", "PUTIN")):
        nx = x + w * (0.2 + i * 0.3)
        tw = fnt.getlength(name) + 8
        dr.rectangle([nx - tw / 2, y + h * 0.78, nx + tw / 2, y + h * 0.78 + 13],
                     fill=(255, 255, 255))
        dr.text((nx - fnt.getlength(name) / 2, y + h * 0.78 + 2), name,
                font=fnt, fill=INK)


def art_gta(dr, x, y, w, h):
    """Vice City sunset: purple sky, orange sun, skyline, pink car."""
    dr.rectangle([x, y, x + w, y + h * 0.55], fill=(88, 48, 118))
    dr.rectangle([x, y + h * 0.55, x + w, y + h], fill=(214, 110, 44))
    dr.ellipse([x + w * 0.62, y + 8, x + w * 0.62 + 44, y + 52], fill=(255, 170, 80))
    # Skyline.
    base = y + h - 26
    for ox, tw, th in [(8, 22, 30), (36, 16, 44), (58, 26, 26), (90, 18, 52),
                       (114, 24, 34), (144, 16, 48), (166, 26, 30),
                       (198, 18, 44), (222, 24, 28), (250, 20, 40),
                       (276, 22, 32)]:
        dr.rectangle([x + ox, base - th, x + ox + tw, base], fill=(40, 20, 60))
    dr.rectangle([x, base, x + w, base + 2], fill=(40, 20, 60))
    # Pink convertible + wheels.
    dr.rounded_rectangle([x + 96, y + h - 24, x + 210, y + h - 8],
                         radius=5, fill=(255, 80, 160))
    dr.rounded_rectangle([x + 118, y + h - 34, x + 182, y + h - 22],
                         radius=4, fill=(255, 120, 190))
    for wx in (112, 186):
        dr.ellipse([x + wx, y + h - 10, x + wx + 12, y + h + 2], fill=INK)
    # Palm.
    dr.line([(x + 24, y + h - 8), (x + 30, y + h - 52)], fill=(20, 60, 30), width=3)
    for dx, dy in [(-16, -8), (16, -10), (-10, -16), (10, -18)]:
        dr.arc([x + 30 + dx - 8, y + h - 62 + dy, x + 30 + dx + 14,
                y + h - 44 + dy], 180, 360, fill=(20, 90, 40), width=3)
    fnt = font("IBMPlexMono-Bold.ttf", 10)
    dr.text((x + 10, y + 8), "VICE CITY", font=fnt, fill=(255, 255, 255))


def art_ipo(dr, x, y, w, h):
    """Nasdaq chart: rising candlesticks, big $81.3BN."""
    dr.rectangle([x, y, x + w, y + h], fill=DARKGREEN)
    candles = [(0.08, 0.62, 0.14), (0.24, 0.5, 0.16), (0.4, 0.56, 0.12),
               (0.56, 0.38, 0.18), (0.72, 0.3, 0.2)]
    base = y + h - 34
    for fx, top, ch in candles:
        cx = x + w * fx
        cw = 16
        dr.line([(cx + cw / 2, y + h * top - 8), (cx + cw / 2, base + 6)],
                fill=(255, 255, 255), width=2)
        dr.rectangle([cx, y + h * top, cx + cw, y + h * top + h * ch],
                     fill=(60, 200, 130))
    fnt_big = font("InstrumentSans-Bold.ttf", 30)
    dr.text((x + 12, y + 6), "$81.3BN", font=fnt_big, fill=(255, 255, 255))
    fnt = font("IBMPlexMono-Bold.ttf", 10)
    dr.text((x + 12, y + h - 26), "IPO PRICE $83  ·  TICKER ANT",
            font=fnt, fill=(255, 220, 90))


def art_icj(dr, x, y, w, h):
    """The Hague courthouse + scales of justice + 9–6."""
    dr.rectangle([x, y, x + w, y + h], fill=PANEL2)
    # Courthouse left, scaled to the 52px medium illustration height.
    cx, cy = x + 30, y + 6
    dr.polygon([(cx - 22, cy + 12), (cx + 22, cy + 12), (cx, cy)],
               fill=NAVY)
    for i in range(3):
        dr.rectangle([cx - 18 + i * 15, cy + 14, cx - 13 + i * 15, cy + 30],
                     fill=NAVY)
    dr.rectangle([cx - 24, cy + 30, cx + 24, cy + 33], fill=NAVY)
    # Scales right.
    sx = x + w - 48
    dr.line([(sx, y + 6), (sx, y + 34)], fill=INK, width=3)
    dr.line([(sx - 17, y + 11), (sx + 17, y + 11)], fill=INK, width=3)
    dr.polygon([(sx - 22, y + 21), (sx - 12, y + 21), (sx - 17, y + 13)],
               fill=GOLD)
    dr.polygon([(sx + 12, y + 21), (sx + 22, y + 21), (sx + 17, y + 13)],
               fill=GOLD)
    dr.ellipse([sx - 3, y + 3, sx + 3, y + 9], fill=GOLD)
    fnt = font("InstrumentSans-Bold.ttf", 18)
    dr.text((x + w - 52, y + h - 24), "9–6", font=fnt, fill=RED)


def art_cop(dr, x, y, w, h):
    """Globe + thermometer + 'FOSSIL FUELS' struck through + CUT stamp."""
    dr.rectangle([x, y, x + w, y + h], fill=(210, 222, 228))
    # Globe.
    gx, gy, gr = x + 34, y + h / 2 + 2, 26
    dr.ellipse([gx - gr, gy - gr, gx + gr, gy + gr], fill=(70, 130, 180))
    dr.ellipse([gx - 16, gy - 18, gx - 2, gy - 6], fill=GREEN)
    dr.ellipse([gx + 2, gy + 4, gx + 18, gy + 18], fill=GREEN)
    dr.ellipse([gx - 6, gy + 8, gx + 8, gy + 16], fill=GREEN)
    # Thermometer.
    tx = x + w - 34
    dr.rounded_rectangle([tx - 5, y + 10, tx + 5, y + h - 18], radius=5,
                         fill=(255, 255, 255))
    dr.ellipse([tx - 9, y + h - 26, tx + 9, y + h - 8], fill=RED)
    dr.rectangle([tx - 2, y + h - 30, tx + 2, y + h - 14], fill=RED)
    # Struck-through text + CUT stamp.
    fnt = font("IBMPlexMono-Bold.ttf", 10)
    label = "FOSSIL FUELS"
    lx = x + w - 96
    dr.text((lx, y + h - 26), label, font=fnt, fill=INK)
    dr.line([(lx - 2, y + h - 20), (lx + fnt.getlength(label) + 2, y + h - 20)],
            fill=RED, width=3)
    dr.rectangle([x + 8, y + 8, x + 46, y + 26], outline=RED, width=2)
    dr.text((x + 13, y + 11), "CUT", font=fnt, fill=RED)


def art_cyclone(dr, x, y, w, h):
    """Spiral storm + rain + 200,000 evacuated."""
    dr.rectangle([x, y, x + w, y + h], fill=(226, 232, 236))
    cx, cy = x + 44, y + h / 2
    for r in (26, 19, 12, 6):
        dr.arc([cx - r, cy - r, cx + r, cy + r], 20, 300, fill=TEAL, width=3)
    for i in range(4):
        rx = x + w - 46 + i * 10
        dr.line([(rx, y + 10 + i * 3), (rx - 4, y + 22 + i * 3)], fill=SKY,
                width=2)
    fnt = font("InstrumentSans-Bold.ttf", 18)
    dr.text((x + w - 92, y + h - 26), "200,000", font=fnt, fill=NAVY)


def art_exam(dr, x, y, w, h):
    """Exam desk: paper, pencil, no-phone sign, 551,864."""
    dr.rectangle([x, y, x + w, y + h], fill=(238, 232, 216))
    dr.rectangle([x + 12, y + 34, x + w - 12, y + h - 6], fill=(150, 100, 50))
    dr.rectangle([x + 26, y + 8, x + 96, y + 40], fill=(255, 255, 255))
    for i in range(3):
        dr.line([(x + 32, y + 16 + i * 8), (x + 90, y + 16 + i * 8)],
                fill=HAIRLINE, width=1)
    # Pencil.
    dr.polygon([(x + 108, y + 12), (x + 158, y + 12), (x + 158, y + 18),
                (x + 108, y + 18)], fill=(255, 206, 0))
    dr.polygon([(x + 158, y + 12), (x + 166, y + 15), (x + 158, y + 18)],
               fill=INK)
    # No-phone circle-slash.
    px, py = x + w - 30, y + 16
    dr.ellipse([px - 11, py - 11, px + 11, py + 11], outline=RED, width=3)
    dr.line([(px - 8, py + 8), (px + 8, py - 8)], fill=RED, width=3)
    fnt = font("InstrumentSans-Bold.ttf", 16)
    dr.text((x + 12, y + h - 24), "551,864", font=fnt, fill=INK)


def art_flood(dr, x, y, w, h):
    """House in floodwater, rain, 15 IN."""
    dr.rectangle([x, y, x + w, y + h], fill=(200, 220, 228))
    for i in range(5):
        rx = x + 14 + i * 30
        dr.line([(rx, y + 8), (rx - 5, y + 20)], fill=SKY, width=2)
    hx, hy = x + 62, y + 30
    dr.rectangle([hx - 26, hy, hx + 26, hy + 22], fill=(250, 250, 250))
    dr.polygon([(hx - 32, hy), (hx + 32, hy), (hx, hy - 16)], fill=RED)
    dr.rectangle([hx - 6, hy + 10, hx + 6, hy + 22], fill=NAVY)
    for i, wy in enumerate((y + h - 16, y + h - 10)):
        for k in range(4):
            dr.arc([x + 10 + k * 44, wy - 4, x + 30 + k * 44, wy + 6],
                   180, 360, fill=TEAL, width=2)
    fnt = font("InstrumentSans-Bold.ttf", 18)
    dr.text((x + w - 62, y + h - 26), "15 IN", font=fnt, fill=NAVY)


def art_strike(dr, x, y, w, h):
    """PARO NACIONAL banner + crowd."""
    dr.rectangle([x, y, x + w, y + h], fill=(240, 228, 200))
    dr.rectangle([x + 10, y + 8, x + w - 10, y + 32], fill=(255, 255, 255),
                 outline=RED, width=2)
    fnt = font("InstrumentSans-Bold.ttf", 13)
    label = "PARO NACIONAL"
    dr.text((x + (w - fnt.getlength(label)) / 2, y + 13), label, font=fnt,
            fill=RED)
    for i in range(7):
        cx = x + 16 + i * 24
        dr.ellipse([cx - 6, y + 30, cx + 6, y + 42], fill=SKIN)
        dr.pieslice([cx - 10, y + 40, cx + 10, y + 40 + 14], 180, 360,
                    fill=NAVY if i % 2 == 0 else TEAL)


def art_riyadh(dr, x, y, w, h):
    """Riyadh towers + missile streak + ALL-CLEAR check."""
    dr.rectangle([x, y, x + w, y + h], fill=(240, 200, 150))
    base = y + h - 8
    dr.rectangle([x + 14, base - 34, x + 34, base], fill=(90, 60, 40))
    dr.rectangle([x + 42, base - 44, x + 64, base], fill=(90, 60, 40))
    dr.ellipse([x + 46, base - 54, x + 60, base - 40], fill=(240, 200, 150))
    dr.rectangle([x + 72, base - 28, x + 92, base], fill=(90, 60, 40))
    # Missile streak.
    dr.line([(x + w - 70, y + 8), (x + w - 20, y + 30)], fill=(255, 255, 255),
            width=3)
    dr.ellipse([x + w - 24, y + 26, x + w - 16, y + 34], fill=RED)
    # Green all-clear check.
    gx, gy = x + w - 26, y + h - 22
    dr.ellipse([gx - 11, gy - 11, gx + 11, gy + 11], fill=GREEN)
    dr.line([(gx - 6, gy), (gx - 1, gy + 5), (gx + 7, gy - 5)], fill=(255, 255, 255),
            width=3)
    fnt = font("IBMPlexMono-Bold.ttf", 9)
    dr.text((x + 8, y + 8), "ALL-CLEAR", font=fnt, fill=(255, 255, 255))


def art_jobs(dr, x, y, w, h):
    """Rising jobless bars + 4.9%."""
    dr.rectangle([x, y, x + w, y + h], fill=PANEL2)
    base = y + h - 10
    heights = (10, 16, 22, 30)
    for i, bh in enumerate(heights):
        bx = x + 14 + i * 22
        dr.rectangle([bx, base - bh, bx + 14, base],
                     fill=RED if i == 3 else NAVY)
    dr.line([(x + 8, base), (x + w - 8, base)], fill=INK, width=2)
    fnt = font("InstrumentSans-Bold.ttf", 20)
    dr.text((x + w - 66, y + 8), "4.9%", font=fnt, fill=RED)


def art_moscow(dr, x, y, w, h):
    """Kremlin tower crossed out + German flag."""
    dr.rectangle([x, y, x + w, y + h], fill=(232, 226, 210))
    tx, ty = x + 40, y + 10
    dr.rectangle([tx - 12, ty + 18, tx + 12, ty + 44], fill=RED)
    dr.ellipse([tx - 12, ty + 6, tx + 12, ty + 26], fill=GOLD)
    dr.polygon([(tx - 12, ty + 18), (tx + 12, ty + 18), (tx, ty + 2)],
               fill=GOLD)
    # Red X over the tower.
    dr.line([(tx - 20, ty), (tx + 20, ty + 52)], fill=RED, width=4)
    dr.line([(tx + 20, ty), (tx - 20, ty + 52)], fill=RED, width=4)
    _flag_de(dr, x + w - 62, y + 12, 46, 28)
    fnt = font("IBMPlexMono-Bold.ttf", 9)
    dr.text((x + w - 62, y + h - 26), "NEUTRAL", font=fnt, fill=INK)
    dr.text((x + w - 62, y + h - 16), "GROUND", font=fnt, fill=INK)


def art_iea(dr, x, y, w, h):
    """Oil drop + down arrow + HORMUZ ½."""
    dr.rectangle([x, y, x + w, y + h], fill=(226, 232, 236))
    dx, dy = x + 40, y + 30
    dr.polygon([(dx, dy - 18), (dx - 14, dy + 2), (dx + 14, dy + 2)],
               fill=INK)
    dr.ellipse([dx - 14, dy - 2, dx + 14, dy + 22], fill=INK)
    dr.line([(x + w - 40, y + 8), (x + w - 40, y + 34)], fill=RED, width=4)
    dr.polygon([(x + w - 48, y + 26), (x + w - 32, y + 26), (x + w - 40, y + 38)],
               fill=RED)
    fnt = font("InstrumentSans-Bold.ttf", 15)
    dr.text((x + 10, y + h - 24), "HORMUZ 1/2", font=fnt, fill=NAVY)


ARTS = {
    "summit": art_summit, "gta": art_gta, "ipo": art_ipo, "icj": art_icj,
    "cop": art_cop, "cyclone": art_cyclone, "exam": art_exam,
    "flood": art_flood, "strike": art_strike, "riyadh": art_riyadh,
    "jobs": art_jobs, "moscow": art_moscow, "iea": art_iea,
}


# ---------------------------------------------------------------------------
# World map — dotted grid, continents as ellipses in lon/lat space.
# ---------------------------------------------------------------------------

CONTINENTS = [
    (-100, 50, 52, 20),   # North America
    (-42, 74, 10, 5),     # Greenland
    (-60, -12, 20, 26),   # South America
    (12, 53, 20, 9),      # Europe
    (18, 3, 20, 28),      # Africa
    (95, 50, 55, 20),     # Asia
    (115, 0, 20, 10),     # SE Asia / Indonesia
    (138, 38, 6, 8),      # Japan
    (134, -25, 16, 9),    # Australia
]


def _on_land(lon, lat):
    for clon, clat, rx, ry in CONTINENTS:
        if ((lon - clon) / rx) ** 2 + ((lat - clat) / ry) ** 2 <= 1:
            return True
    return False


def draw_map(dr, stories, x, y, w, h):
    """Dotted world map with numbered red pins for the 13 feature stories."""
    f_title = font("IBMPlexMono-Bold.ttf", 11)
    dr.text((x, y), "WHERE IT HAPPENED", font=f_title, fill=INK)
    rule(dr, x + 150, x + w, y + 7, fill=INK, width=1)
    mx, my, mw, mh = x, y + 20, w, h - 20
    # Dots.
    lon = -180.0
    while lon < 180:
        lat = 78.0
        while lat > -58:
            if _on_land(lon, lat):
                px = mx + (lon + 180) / 360 * mw
                py = my + (78 - lat) / 136 * mh
                dr.ellipse([px - 1.6, py - 1.6, px + 1.6, py + 1.6],
                           fill=(120, 128, 142))
            lat -= 6.5
        lon += 7.0
    # Pins.
    f_pin = font("IBMPlexMono-Bold.ttf", 8)
    for st in stories:
        px = mx + (st["lon"] + 180) / 360 * mw
        py = my + (78 - st["lat"]) / 136 * mh
        dx = st.get("pin_dx", 0)
        dy = st.get("pin_dy", 0)
        qx, qy = px + dx, py + dy
        if dx or dy:
            dr.line([(px, py), (qx, qy)], fill=RED, width=1)
        dr.ellipse([px - 2, py - 2, px + 2, py + 2], fill=RED)
        dr.ellipse([qx - 7, qy - 7, qx + 7, qy + 7], fill=RED)
        num = str(st["n"])
        dr.text((qx - f_pin.getlength(num) / 2, qy - 5), num, font=f_pin,
                fill=(255, 255, 255))


# ---------------------------------------------------------------------------
# Page sections.
# ---------------------------------------------------------------------------

def draw_region_bar(dr, regions, x, y, w, h):
    """Equal-width coloured segments, name + count per region."""
    order = sorted(regions, key=lambda r: -regions[r])
    seg = w / len(order)
    fnt = font("IBMPlexMono-Bold.ttf", 11)
    for i, name in enumerate(order):
        sx = x + i * seg
        dr.rectangle([sx, y, sx + seg - 1, y + h],
                     fill=REGION_COLORS[name])
        label = f"{name} {regions[name]}"
        tw = fnt.getlength(label)
        dr.text((sx + (seg - tw) / 2, y + (h - 13) / 2), label, font=fnt,
                fill=(255, 255, 255))


def draw_numbers(dr, numbers, x, y, w, h):
    """THE DAY IN NUMBERS: big value + small label per cell."""
    f_val = font("InstrumentSans-Bold.ttf", 26)
    f_lab = font("IBMPlexMono-Bold.ttf", 9)
    cell = w / len(numbers)
    for i, item in enumerate(numbers):
        cx = x + i * cell
        val = item["value"]
        vw = f_val.getlength(val)
        dr.text((cx + (cell - vw) / 2, y), val, font=f_val, fill=RED)
        lab = item["label"]
        lw = f_lab.getlength(lab)
        dr.text((cx + (cell - lw) / 2, y + 30), lab, font=f_lab, fill=GREY)
        if i:
            dr.line([(cx, y + 2), (cx, y + h - 4)], fill=HAIRLINE, width=1)


def draw_hero(dr, st, x, y, w, h):
    dr.rectangle([x, y, x + w, y + h], fill=PANEL, outline=HAIRLINE, width=1)
    ARTS[st["art"]](dr, x + 1, y + 1, w - 2, 104)
    ty = y + 110
    f_kick = font("IBMPlexMono-Bold.ttf", 10)
    kick = f"{st['n']} · {st['region']} · {st['kicker']}"
    dr.text((x + 10, ty), kick, font=f_kick, fill=RED)
    f_head = font("CrimsonPro-Bold.ttf", 19)
    lines = wrap(st["headline"], f_head, w - 20)[:2]
    ly = ty + 16
    for ln in lines:
        dr.text((x + 10, ly), ln, font=f_head, fill=INK)
        ly += 21
    f_deck = font("InstrumentSans-Regular.ttf", 12)
    dlines = wrap(st["deck"], f_deck, w - 20)[:2]
    for ln in dlines:
        dr.text((x + 10, ly + 2), ln, font=f_deck, fill=GREY)
        ly += 14
    f_src = font("IBMPlexMono-Regular.ttf", 8)
    src = "SOURCES: " + " · ".join(st["sources"]).upper()
    dr.text((x + 10, y + h - 14), src, font=f_src, fill=GREY)


def draw_medium(dr, st, x, y, w, h):
    dr.rectangle([x, y, x + w, y + h], fill=PANEL, outline=HAIRLINE, width=1)
    ARTS[st["art"]](dr, x + 1, y + 1, w - 2, 52)
    ty = y + 58
    f_kick = font("IBMPlexMono-Bold.ttf", 8)
    kick = f"{st['n']} · {st['region']}"
    dr.text((x + 8, ty), kick, font=f_kick, fill=RED)
    f_head = font("InstrumentSans-Bold.ttf", 12)
    lines = wrap(st["headline"], f_head, w - 16)
    max_head = 3 if len(lines) <= 2 else 2
    lines = lines[:max_head]
    ly = ty + 11
    for ln in lines:
        dr.text((x + 8, ly), ln, font=f_head, fill=INK)
        ly += 14
    f_deck = font("InstrumentSans-Regular.ttf", 10)
    max_deck = 2 if len(lines) <= 2 else 1
    dlines = wrap(st["deck"], f_deck, w - 16)[:max_deck]
    for ln in dlines:
        dr.text((x + 8, ly + 1), ln, font=f_deck, fill=GREY)
        ly += 12
    f_src = font("IBMPlexMono-Regular.ttf", 8)
    src = " · ".join(st["sources"]).upper()
    dr.text((x + 8, y + h - 12), src, font=f_src, fill=GREY)


def draw_also(dr, items, x, y, col_w, rows):
    """Two-column numbered brief list, 14-36."""
    f_title = font("IBMPlexMono-Bold.ttf", 11)
    dr.text((x, y), "ALSO ON THURSDAY — 23 MORE STORIES", font=f_title,
            fill=INK)
    rule(dr, x + 262, x + col_w * 2 + 16, y + 7, fill=INK, width=1)
    fnt = font("InstrumentSans-Regular.ttf", 11)
    f_bold = font("InstrumentSans-Bold.ttf", 11)
    for idx, it in enumerate(items):
        col = idx % 2
        row = idx // 2
        cx = x + col * (col_w + 16)
        cy = y + 20 + row * 15
        num = f"{it['n']}"
        dr.text((cx, cy), num, font=f_bold, fill=RED)
        nw = f_bold.getlength(num) + 4
        city = it["city"] + ": "
        dr.text((cx + nw, cy), city, font=f_bold, fill=INK)
        cw = f_bold.getlength(city)
        text = fit_one(it["headline"], fnt, col_w - nw - cw)
        dr.text((cx + nw + cw, cy), text, font=fnt, fill=INK)
    return y + 20 + rows * 15


def draw_datecheck(dr, dc, x, y, w, h):
    dr.rectangle([x, y, x + w, y + h], fill=(250, 238, 232),
                 outline=RED, width=2)
    f_title = font("IBMPlexMono-Bold.ttf", 11)
    dr.text((x + 10, y + 5), "DATE CHECK — LEFT OUT ON PURPOSE", font=f_title,
            fill=RED)
    fnt = font("InstrumentSans-Regular.ttf", 10)
    line1 = "Left out — happened on another day: " + "  ·  ".join(dc["excluded"])
    line1 = fit_one(line1, fnt, w - 20)
    dr.text((x + 10, y + 19), line1, font=fnt, fill=INK)
    line2 = "Not yet: " + dc["notyet"] + ".  Every story above is dated 19 November 2026."
    line2 = fit_one(line2, fnt, w - 20)
    dr.text((x + 10, y + 32), line2, font=fnt, fill=INK)


def build(stories, out_path):
    img = Image.new("RGB", (W, H), PAPER)
    dr = ImageDraw.Draw(img)

    # --- Masthead: small red name, giant serif date, red italic deck ---
    f_eye = font("IBMPlexMono-Bold.ttf", 13)
    center_tracked(dr, W // 2, 12, stories["masthead"], f_eye, RED, tracking=4)
    f_date = font("Gloock-Regular.ttf", 42)
    date = stories["date"]
    dw = f_date.getlength(date)
    dr.text(((W - dw) / 2, 30), date, font=f_date, fill=INK)
    f_deck = font("CrimsonPro-Italic.ttf", 16)
    deck = stories["deck"]
    dw2 = f_deck.getlength(deck)
    dr.text(((W - dw2) / 2, 86), deck, font=f_deck, fill=RED)
    rule(dr, MARGIN, W - MARGIN, 110, fill=NAVY, width=3)

    # --- Region bar ---
    draw_region_bar(dr, stories["regions"], MARGIN, 118, CW, 24)

    # --- The day in numbers ---
    f_sec = font("IBMPlexMono-Bold.ttf", 11)
    dr.text((MARGIN, 150), "THE DAY IN NUMBERS", font=f_sec, fill=INK)
    rule(dr, MARGIN + 132, W - MARGIN, 157, fill=INK, width=1)
    draw_numbers(dr, stories["numbers"], MARGIN, 166, CW, 42)

    # --- 3 hero cards ---
    hero_y, hero_h, hero_w, hero_gap = 216, 220, 308, 20
    for i, st in enumerate(stories["heroes"]):
        draw_hero(dr, st, MARGIN + i * (hero_w + hero_gap), hero_y, hero_w,
                  hero_h)

    # --- 10 medium cards, 5 x 2 ---
    med_y, med_h, med_w, med_gap = 444, 136, 182, 13
    for i, st in enumerate(stories["medium"]):
        col, row = i % 5, i // 5
        draw_medium(dr, st, MARGIN + col * (med_w + med_gap),
                    med_y + row * (med_h + 10), med_w, med_h)

    # --- Map + ALSO list ---
    map_y = 734
    draw_map(dr, stories["heroes"] + stories["medium"], MARGIN, map_y, 352,
             198)
    also_y = draw_also(dr, stories["also"], MARGIN + 368, map_y, 290, 12)

    # --- DATE CHECK ---
    dc_y = 938
    draw_datecheck(dr, stories["datecheck"], MARGIN, dc_y, CW, 46)

    # --- Footer ---
    f_foot = font("IBMPlexMono-Regular.ttf", 10)
    total = 3 + len(stories["medium"]) + len(stories["also"])
    foot = (f"{total} STORIES  ·  7 REGIONS  ·  {stories['promise']}")
    fw = f_foot.getlength(foot)
    rule(dr, MARGIN, W - MARGIN, 992, fill=HAIRLINE)
    dr.text(((W - fw) / 2, 998), foot, font=f_foot, fill=GREY)
    src = stories["sources_footer"]
    sw = f_foot.getlength(src)
    dr.text(((W - sw) / 2, 1010), src, font=f_foot, fill=GREY)

    img.save(out_path, "PNG", optimize=True, compress_level=9)
    print(f"saved {out_path}  {os.path.getsize(out_path)} bytes  "
          f"also-end-y={also_y} (canvas {H})")
    return also_y


def main():
    with open(os.path.join(HERE, "stories.json"), encoding="utf-8") as fh:
        stories = json.load(fh)
    out = os.path.join(HERE, "entry.png")
    build(stories, out)


if __name__ == "__main__":
    main()
