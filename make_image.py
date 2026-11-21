# make_image.py — renders the 20 November 2026 world-news front page to entry.png
# Author: Hermes Agent session for make.fun bounty news-image-20261120.
# Deterministic: same bytes on every run. Pillow is build-time only; the shipped
# entry program (main.ts) just copies the rendered PNG.
# Rev 2: every string is measured and auto-fitted to its box (rev 1 clipped the
# right column); summit icon redrawn as three flags; ticker moved inside frame.
from PIL import Image, ImageDraw, ImageFont
import os, math

W = H = 1024
PAPER = (247, 243, 232)
INK = (22, 22, 28)
RED = (172, 32, 32)
MUTED = (92, 90, 82)
BLUE = (28, 78, 156)
GOLD = (196, 152, 40)

F = "C:/Windows/Fonts/"
def font(name, size):
    return ImageFont.truetype(F + name, size)

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

def fit(text, maxw, base, minsize=17, bold=True):
    name = "arialbd.ttf" if bold else "arial.ttf"
    size = base
    while size > minsize and d.textlength(text, font=font(name, size)) > maxw:
        size -= 1
    return font(name, size)

def center(text, y, f, fill=INK):
    w = d.textlength(text, font=f)
    d.text(((W - w) / 2, y), text, font=f, fill=fill)

def rule(y, w=3, x0=40, x1=984, fill=INK):
    d.rectangle([x0, y, x1, y + w - 1], fill=fill)

# ---------- masthead ----------
d.rectangle([16, 16, W - 17, H - 17], outline=INK, width=3)
center("THE WORLD TODAY", 30, font("timesbd.ttf", 74))
rule(112, 2)
center("FRIDAY · 20 NOVEMBER 2026 · THE DAY'S WORLD NEWS IN ONE IMAGE", 122, font("arial.ttf", 26), MUTED)
rule(156, 4)

# ---------- lead story: Trump–Xi–Putin summit ----------
d.rectangle([40, 172, 152, 204], fill=RED)
d.text((50, 176), "LEAD", font=font("arialbd.ttf", 20), fill=PAPER)
d.text((170, 176), "SHENZHEN · APEC SIDELINES", font=font("arialbd.ttf", 20), fill=MUTED)
lead = "TRUMP, XI & PUTIN HOLD FIRST-EVER"
d.text((40, 214), lead, font=fit(lead, 760, 44, 30), fill=INK)
lead2 = "THREE-WAY SUMMIT"
d.text((40, 264), lead2, font=fit(lead2, 760, 44, 30), fill=INK)
sub1 = '"Declaration toward Peace": nuclear-risk talks, UN reform,'
sub2 = "petroleum pledge · Trump touts history, offers few results"
d.text((40, 320), sub1, font=fit(sub1, 760, 26, 20, bold=False), fill=MUTED)
d.text((40, 352), sub2, font=fit(sub2, 760, 26, 20, bold=False), fill=MUTED)

def summit_icon(x, y, s):
    # three national flags on poles above a shared table
    for i, kind in enumerate(["us", "cn", "ru"]):
        px = x + s * (0.12 + 0.30 * i)
        d.line([px, y + s * 0.08, px, y + s * 0.72], fill=INK, width=4)
        fx, fy, fw, fh = px + 2, y + s * 0.10, s * 0.24, s * 0.17
        if kind == "us":
            d.rectangle([fx, fy, fx + fw, fy + fh], fill=(240, 240, 240), outline=INK, width=1)
            for k in range(3):
                d.rectangle([fx, fy + fh * (0.2 + 0.28 * k), fx + fw, fy + fh * (0.32 + 0.28 * k)], fill=RED)
            d.rectangle([fx, fy, fx + fw * 0.45, fy + fh * 0.5], fill=BLUE)
        elif kind == "cn":
            d.rectangle([fx, fy, fx + fw, fy + fh], fill=RED, outline=INK, width=1)
            d.ellipse([fx + fw * 0.12, fy + fh * 0.18, fx + fw * 0.30, fy + fh * 0.42], fill=GOLD)
        else:
            for k, c in enumerate([(240, 240, 240), BLUE, RED]):
                d.rectangle([fx, fy + fh * k / 3, fx + fw, fy + fh * (k + 1) / 3], fill=c)
            d.rectangle([fx, fy, fx + fw, fy + fh], outline=INK, width=1)
    d.rectangle([x + s * 0.05, y + s * 0.74, x + s * 0.95, y + s * 0.84], fill=INK)
summit_icon(820, 212, 160)
rule(392, 3)

# ---------- six story cards ----------
def chart_icon(x, y, s):
    d.line([x + s*0.1, y + s*0.85, x + s*0.9, y + s*0.85], fill=INK, width=4)
    d.line([x + s*0.1, y + s*0.85, x + s*0.1, y + s*0.1], fill=INK, width=4)
    pts = [(x + s*0.18, y + s*0.65), (x + s*0.40, y + s*0.50), (x + s*0.58, y + s*0.58), (x + s*0.85, y + s*0.18)]
    d.line(pts, fill=RED, width=6)
    d.polygon([(x + s*0.85, y + s*0.18), (x + s*0.70, y + s*0.20), (x + s*0.82, y + s*0.34)], fill=RED)

def kyiv_icon(x, y, s):
    d.rectangle([x + s*0.2, y + s*0.3, x + s*0.55, y + s*0.85], outline=INK, width=5)
    for wy in (0.4, 0.55, 0.7):
        d.rectangle([x + s*0.28, y + s*wy, x + s*0.36, y + s*(wy + 0.07)], fill=INK)
    d.polygon([(x + s*0.62, y + s*0.1), (x + s*0.52, y + s*0.45), (x + s*0.66, y + s*0.45), (x + s*0.56, y + s*0.85), (x + s*0.85, y + s*0.38), (x + s*0.70, y + s*0.38), (x + s*0.80, y + s*0.1)], fill=GOLD)

def euuk_icon(x, y, s):
    d.ellipse([x + s*0.08, y + s*0.15, x + s*0.62, y + s*0.69], outline=BLUE, width=5)
    for k in range(8):
        a = math.tau * k / 8
        cx = x + s*0.35 + s*0.20*math.cos(a); cy = y + s*0.42 + s*0.20*math.sin(a)
        d.ellipse([cx-2, cy-2, cx+2, cy+2], fill=GOLD)
    d.rectangle([x + s*0.55, y + s*0.45, x + s*0.92, y + s*0.80], outline=RED, width=5)
    d.line([x + s*0.55, y + s*0.62, x + s*0.92, y + s*0.62], fill=RED, width=4)
    d.line([x + s*0.73, y + s*0.45, x + s*0.73, y + s*0.80], fill=RED, width=4)

def gamepad_icon(x, y, s):
    d.rounded_rectangle([x + s*0.08, y + s*0.3, x + s*0.92, y + s*0.72], radius=s*0.18, outline=INK, width=5)
    d.line([x + s*0.22, y + s*0.44, x + s*0.22, y + s*0.58], fill=INK, width=5)
    d.line([x + s*0.15, y + s*0.51, x + s*0.29, y + s*0.51], fill=INK, width=5)
    d.ellipse([x + s*0.66, y + s*0.42, x + s*0.74, y + s*0.50], fill=RED)
    d.ellipse([x + s*0.78, y + s*0.52, x + s*0.86, y + s*0.60], fill=BLUE)

def pew_icon(x, y, s):
    d.arc([x + s*0.10, y + s*0.15, x + s*0.60, y + s*0.75], 60, 300, fill=INK, width=6)
    d.ellipse([x + s*0.34, y + s*0.22, x + s*0.44, y + s*0.32], fill=GOLD)
    d.line([x + s*0.74, y + s*0.18, x + s*0.74, y + s*0.80], fill=BLUE, width=6)
    d.line([x + s*0.58, y + s*0.36, x + s*0.90, y + s*0.36], fill=BLUE, width=6)

def arctic_icon(x, y, s):
    # snowflake: three crossed spokes with branch ticks — Arctic security
    cx, cy = x + s * 0.5, y + s * 0.45
    for k in range(3):
        a = math.pi * k / 3
        dx, dy = math.cos(a) * s * 0.34, math.sin(a) * s * 0.34
        d.line([cx - dx, cy - dy, cx + dx, cy + dy], fill=BLUE, width=5)
        for sgn in (-1, 1):
            bx, by = cx + dx * 0.6 * sgn, cy + dy * 0.6 * sgn
            a2 = a + math.pi / 3
            d.line([bx, by, bx + math.cos(a2) * s * 0.12, by + math.sin(a2) * s * 0.12], fill=BLUE, width=4)
            d.line([bx, by, bx - math.cos(a2) * s * 0.12, by - math.sin(a2) * s * 0.12], fill=BLUE, width=4)
    d.line([x + s * 0.15, y + s * 0.88, x + s * 0.85, y + s * 0.88], fill=INK, width=4)

CARDS = [
    (chart_icon, "ANTHROPIC'S RECORD IPO",
     ["ANT opens +34% · $81.3B raised", "near $2T value · Dow -1,100 pts"]),
    (kyiv_icon, "KYIV CRIPPLED BY STRIKES",
     ["3 dead, bridges hit, power out", "Ukraine hits Luhansk: 3 dead"]),
    (euuk_icon, "UK & EU RESET TIES",
     ["Burnham–Costa–von der Leyen", "youth mobility plan floated"]),
    (gamepad_icon, "GTA 6 BREAKS RECORDS",
     ["$3.79B day one · 32.5M preorders", "Metacritic 99 · all-time record"]),
    (pew_icon, "PEW: FAITH SHIFT 2035",
     ["Islam to pass Christianity by 2035", "Pew: 3.1 vs 2.5 births per woman"]),
    (arctic_icon, "ARCTIC SECURITY DEAL",
     ["Denmark OKs bigger US military", "presence in Greenland · NATO buildup"]),
]

cw, ch, gx, gy = 482, 168, 20, 12
x0, y0 = 40, 408
for i, (icon, head, facts) in enumerate(CARDS):
    cx = x0 + (i % 2) * (cw + gx)
    cy = y0 + (i // 2) * (ch + gy)
    d.rectangle([cx, cy, cx + cw, cy + ch], outline=(200, 194, 178), width=2)
    icon(cx + 12, cy + 34, 92)
    tx = cx + 116
    tw = cw - 116 - 14
    d.text((tx, cy + 18), head, font=fit(head, tw, 32, 19), fill=INK)
    for j, line in enumerate(facts):
        d.text((tx, cy + 66 + j * 32), line, font=fit(line, tw, 22, 16, bold=False), fill=MUTED)

# ---------- bottom ticker ----------
rule(944, 3)
d.text((40, 952), "ALSO TODAY:", font=font("arialbd.ttf", 24), fill=RED)
t1 = "Italy general strike over wages · NYC moves to close Rikers jail"
t2 = "EU troops drill in Poland for Ukraine · Fiona the hippo dies at Cincinnati Zoo"
d.text((218, 952), t1, font=fit(t1, 766, 24, 17), fill=INK)
d.text((218, 980), t2, font=fit(t2, 766, 22, 16, bold=False), fill=MUTED)

img.save("entry.png", optimize=True)
print("entry.png written:", os.path.getsize("entry.png"), "bytes", img.size)
