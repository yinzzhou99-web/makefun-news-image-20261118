#!/usr/bin/env python3
"""news-image-20261118: draws a newspaper front page summing up the
world news of Wednesday 18 November 2026 and writes it to
/output/entry.png. Stdlib + Pillow only, no network, fully deterministic.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = "/output/entry.png"
FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)
SERIF = lambda s: font("DejaVuSerif.ttf", s)
SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)
SANS = lambda s: font("DejaVuSans.ttf", s)

INK = (18, 18, 18)
RED = (178, 24, 24)
GREY = (90, 90, 90)
RULE = (40, 40, 40)
PAPER = (252, 250, 244)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns list of lines that fit max_w."""
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
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


def hrule(draw, y, x0=36, x1=988, width=3):
    draw.line([(x0, y), (x1, y)], fill=RULE, width=width)


def draw_burst(draw, cx, cy, r1, r2, fill, n=12):
    """Starburst polygon: alternating outer/inner radius points."""
    import math
    pts = []
    for i in range(n * 2):
        r = r1 if i % 2 == 0 else r2
        a = math.pi * i / n - math.pi / 2
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    draw.polygon(pts, fill=fill)


def illustration(draw, x0, y0, x1, y1):
    """Flat drawn scene: Gulf night sky, island, explosion, jets, sea."""
    draw.rectangle([x0, y0, x1, y1], fill=(16, 34, 64))
    # stars
    for sx, sy in [(0.12, 0.15), (0.3, 0.08), (0.55, 0.18), (0.78, 0.1),
                   (0.9, 0.25), (0.22, 0.3), (0.66, 0.3), (0.45, 0.06)]:
        px, py = x0 + int(sx * (x1 - x0)), y0 + int(sy * (y1 - y0))
        draw.ellipse([px - 2, py - 2, px + 2, py + 2], fill=(255, 255, 255))
    # sea
    sea_y = y0 + int(0.68 * (y1 - y0))
    draw.rectangle([x0, sea_y, x1, y1], fill=(24, 68, 110))
    for k, wy in enumerate([0.74, 0.82, 0.9]):
        yy = y0 + int(wy * (y1 - y0))
        for wx in range(0, x1 - x0 - 40, 46):
            draw.arc([x0 + wx, yy - 6, x0 + wx + 36, yy + 10],
                     start=180, end=360, fill=(180, 210, 235), width=3)
    # island silhouette
    ix0, ix1 = x0 + 20, x1 - 90
    draw.polygon([(ix0, sea_y), (ix0 + 40, sea_y - 34), (ix0 + 110, sea_y - 52),
                  (ix0 + 180, sea_y - 26), (ix1, sea_y), (ix1, sea_y + 4),
                  (ix0, sea_y + 4)], fill=(38, 52, 40))
    # missile site: small towers on the island
    for tx in (ix0 + 55, ix0 + 95, ix0 + 135):
        draw.rectangle([tx, sea_y - 66, tx + 8, sea_y - 40], fill=(70, 70, 70))
        draw.ellipse([tx - 3, sea_y - 72, tx + 11, sea_y - 60], fill=(70, 70, 70))
    # explosion burst above the island
    bx, by = x0 + int(0.55 * (x1 - x0)), y0 + int(0.34 * (y1 - y0))
    draw_burst(draw, bx, by, 64, 30, (255, 122, 26))
    draw_burst(draw, bx, by, 44, 20, (255, 196, 0))
    draw_burst(draw, bx, by, 22, 10, (255, 240, 180))
    # two jets (simple triangles) in the sky
    for jx, jy in [(x0 + 30, y0 + 42), (x0 + 90, y0 + 24)]:
        draw.polygon([(jx, jy), (jx + 34, jy + 8), (jx, jy + 16)],
                     fill=(200, 205, 210))
        draw.line([(jx, jy + 8), (jx - 16, jy + 8)], fill=(200, 205, 210),
                  width=2)
    # smoke plume
    draw.ellipse([bx - 46, by - 96, bx - 6, by - 56], fill=(120, 120, 120))
    draw.ellipse([bx - 30, by - 116, bx + 6, by - 76], fill=(150, 150, 150))
    # caption bar
    draw.rectangle([x0, y1 - 30, x1, y1], fill=(0, 0, 0))
    cap = "Qeshm Island, Iran"
    draw.text((x0 + 10, y1 - 25), cap, font=SANS(15), fill=(255, 255, 255))


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead ----
    d.text((W // 2, 26), "THE WORLD TODAY", font=SERIF_B(76),
           fill=INK, anchor="ma")
    hrule(d, 118, width=4)
    d.text((36, 128), "WEDNESDAY, 18 NOVEMBER 2026", font=SANS_B(21),
           fill=INK)
    d.text((988, 128), "WORLD NEWS IN ONE IMAGE", font=SANS_B(21),
           fill=RED, anchor="ra")
    hrule(d, 162, width=2)

    # ---- lead story ----
    y = 182
    d.text((36, y), "GULF CRISIS", font=SANS_B(24), fill=RED)
    y += 34
    lead_lines = wrap(d, "US strikes Iranian missile site as Gulf drones fly",
                      SERIF_B(56), 580)
    assert len(lead_lines) <= 3, "lead headline overflow"
    ly = y
    for ln in lead_lines:
        d.text((36, ly), ln, font=SERIF_B(56), fill=INK)
        ly += 64
    sub = ("US jets hit a Revolutionary Guard launch site on Qeshm Island "
           "after Iran fired drones at a US radar base in Bahrain — "
           "its third attack there in under a week. Kuwait's air defences "
           "also shot down drones overnight.")
    sub_lines = wrap(d, sub, SERIF(23), 560)
    assert len(sub_lines) <= 5, "lead subhead overflow"
    draw_lines(d, sub_lines, SERIF(23), 36, ly + 8, INK, 30)
    illustration(d, 640, 182, 988, 560)

    # ---- secondary stories: 2 x 2 grid ----
    hrule(d, 592, width=3)
    stories = [
        ("UKRAINE", "Kerch Bridge hit again",
         "Ukraine hit the bridge to Crimea for a second day; part of "
         "its road span fell."),
        ("DIPLOMACY", "Trump, Xi and Putin to meet",
         "The three leaders meet in Shenzhen on Thursday as the "
         "APEC summit opens."),
        ("HEALTH", "Ebola in DR Congo doubles",
         "Cases pass 11,000 with 5,400 deaths in three months, "
         "the UN says."),
        ("DISASTER", "19 die in Russian plane crash",
         "A military transport plane came down in Kemerovo, Siberia; "
         "no survivors."),
    ]
    col_w, col_x = 462, [36, 526]
    row_y = [606, 786]
    for i, (kick, head, body) in enumerate(stories):
        x = col_x[i % 2]
        yy = row_y[i // 2]
        d.text((x, yy), kick, font=SANS_B(20), fill=RED)
        head_lines = wrap(d, head, SERIF_B(34), col_w)
        assert len(head_lines) <= 2, "headline overflow: " + head
        yy = draw_lines(d, head_lines, SERIF_B(34), x, yy + 28, INK, 40)
        body_lines = wrap(d, body, SERIF(21), col_w)
        assert len(body_lines) <= 2, "body overflow: " + head
        draw_lines(d, body_lines, SERIF(21), x, yy + 6, INK, 26)
        if i % 2 == 0:
            d.line([(506, yy - 6), (506, yy + 96)], fill=(200, 200, 200),
                   width=1)

    # ---- footer ----
    hrule(d, 972, width=2)
    d.text((36, 982), "Sources: Reuters · BBC · Al Jazeera · AP — compiled 18 Nov 2026",
           font=SANS(15), fill=GREY)
    d.text((988, 982), "THE WORLD TODAY", font=SANS_B(15), fill=GREY,
           anchor="ra")

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    img.save(OUT, format="PNG")


if __name__ == "__main__":
    main()
