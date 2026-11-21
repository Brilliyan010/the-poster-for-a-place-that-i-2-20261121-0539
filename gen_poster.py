#!/usr/bin/env python3
"""LUMARIS — The Poster for a Place That Isn't There.

Draws a vintage flat-style travel poster (1024x1024 PNG) with PIL:
twin suns setting over a calm lagoon, a striped lighthouse on a rocky
isle, one small sailboat, and the invented place name set in large type.

Deterministic: fixed seed, no network, no time input. Rendered at 2048
and downscaled to 1024 for anti-aliasing.
"""
import math
import random
from PIL import Image, ImageDraw, ImageFilter, ImageFont

S = 2                      # supersample factor
W = H = 1024 * S           # working canvas 2048
OUT = "entry.png"

SERIF_BLACK = "/usr/share/fonts/truetype/noto/NotoSerifDisplay-Black.ttf"
SANS_CONDB = "/usr/share/fonts/truetype/noto/NotoSansDisplay-CondensedBold.ttf"

CREAM = (247, 238, 220)
CREAM_SOFT = (255, 243, 220)
GOLD = (255, 217, 138)
INK = (30, 37, 71)

rng = random.Random(20261121)


def lerp(a, b, t):
    return tuple(round(a[i] + (b[i] - a[i]) * t) for i in range(3))


def vgrad(img, box, stops):
    """Vertical gradient over box (x0, y0, x1, y1); stops = [(pos, rgb)]."""
    x0, y0, x1, y1 = box
    d = ImageDraw.Draw(img)
    span = y1 - y0
    for y in range(y0, y1):
        t = (y - y0) / max(span - 1, 1)
        for i in range(len(stops) - 1):
            p0, c0 = stops[i]
            p1, c1 = stops[i + 1]
            if p0 <= t <= p1:
                f = 0.0 if p1 == p0 else (t - p0) / (p1 - p0)
                d.line([(x0, y), (x1, y)], fill=lerp(c0, c1, f))
                break


def glow(base, cx, cy, r, color, alpha, blur):
    """Soft radial glow: blurred filled circle composited onto base."""
    layer = Image.new("RGBA", base.size, (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)
    ld.ellipse([cx - r, cy - r, cx + r, cy + r], fill=color + (alpha,))
    layer = layer.filter(ImageFilter.GaussianBlur(blur))
    base.alpha_composite(layer)


def ridge(draw, y_base, peaks, color):
    """Jagged mountain silhouette: peaks = [(x, y), ...] along the top."""
    pts = [(0, y_base)] + peaks + [(W, y_base)]
    draw.polygon(pts, fill=color)


def main():
    img = Image.new("RGB", (W, H), (20, 25, 50))
    d = ImageDraw.Draw(img, "RGBA")

    horizon = int(H * 0.575)  # 1178

    # ---- sky ----
    vgrad(img, (0, 0, W, horizon), [
        (0.00, (30, 37, 71)),    # deep indigo
        (0.32, (87, 72, 122)),   # violet
        (0.58, (168, 90, 99)),   # rose
        (0.80, (224, 138, 82)),  # coral
        (1.00, (247, 180, 92)),  # gold horizon
    ])

    # ---- clouds: soft horizontal bands ----
    cloud_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    cd = ImageDraw.Draw(cloud_layer)
    for (cx, cy, rw, rh, a) in [
        (420, 300, 330, 26, 34), (760, 350, 260, 20, 26),
        (1500, 300, 380, 28, 30), (1180, 470, 300, 22, 24),
        (300, 760, 300, 24, 30), (1650, 700, 340, 26, 26),
        (950, 950, 420, 26, 28),
    ]:
        cd.ellipse([cx - rw, cy - rh, cx + rw, cy + rh], fill=(255, 226, 196, a))
    cloud_layer = cloud_layer.filter(ImageFilter.GaussianBlur(18))
    img.paste(Image.alpha_composite(img.convert("RGBA"), cloud_layer).convert("RGB"), (0, 0))
    d = ImageDraw.Draw(img, "RGBA")

    # ---- twin suns (the place's identity: the sun rises twice) ----
    img_rgba = img.convert("RGBA")
    glow(img_rgba, 800, 640, 300, (255, 190, 90), 90, 90)
    glow(img_rgba, 1290, 540, 210, (255, 220, 150), 80, 70)
    img = img_rgba.convert("RGB")
    d = ImageDraw.Draw(img, "RGBA")
    # big sun
    d.ellipse([800 - 150, 640 - 150, 800 + 150, 640 + 150], fill=(255, 227, 161))
    d.ellipse([800 - 118, 640 - 118, 800 + 118, 640 + 118], fill=(255, 236, 190))
    # small sun
    d.ellipse([1290 - 95, 540 - 95, 1290 + 95, 540 + 95], fill=(255, 237, 190))
    d.ellipse([1290 - 70, 540 - 70, 1290 + 70, 540 + 70], fill=(255, 244, 214))

    # ---- distant ridges ----
    ridge(d, horizon, [(0, 1080), (180, 1010), (380, 1075), (560, 990),
                       (760, 1060), (980, 1000), (1240, 1070), (1500, 995),
                       (1750, 1065), (2048, 1020)], (91, 58, 94))
    ridge(d, horizon, [(0, 1130), (240, 1085), (520, 1135), (900, 1080),
                       (1300, 1130), (1700, 1075), (2048, 1120)], (70, 48, 78))

    # ---- sea ----
    vgrad(img, (0, horizon, W, H), [
        (0.00, (27, 74, 90)),    # teal, lit by sunset
        (0.45, (18, 56, 70)),
        (1.00, (12, 40, 51)),    # deep teal
    ])
    d = ImageDraw.Draw(img, "RGBA")
    d.line([(0, horizon), (W, horizon)], fill=(255, 200, 120, 90), width=3)

    # sun paths: shimmering gold dashes under each sun
    for (sx, spread, top, n, base_a) in [(800, 260, horizon + 30, 90, 150),
                                         (1290, 170, horizon + 30, 60, 110)]:
        for _ in range(n):
            y = rng.randint(top, H - 60)
            depth = (y - horizon) / (H - horizon)
            w_half = spread * (0.35 + 0.65 * depth)
            x = sx + rng.uniform(-w_half, w_half)
            ln = rng.uniform(18, 70) * (0.5 + depth)
            a = int(base_a * (0.35 + 0.65 * depth) * rng.uniform(0.5, 1.0))
            d.line([(x - ln, y), (x + ln, y)], fill=(255, 205, 120, a), width=4)

    # ---- rocky isle + lighthouse (right of centre) ----
    isle = [(1150, 1560), (1210, 1420), (1300, 1360), (1420, 1330),
            (1560, 1345), (1660, 1400), (1720, 1560)]
    d.polygon(isle, fill=(28, 42, 51))
    d.line([(1210, 1420), (1300, 1360), (1420, 1330), (1560, 1345), (1660, 1400)],
           fill=(64, 92, 104), width=5)

    # light beams from the lamp (drawn first, behind the tower)
    beam = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    bd = ImageDraw.Draw(beam)
    lamp = (1410, 1062)
    bd.polygon([lamp, (700, 1180), (700, 1330)], fill=(255, 220, 140, 70))
    bd.polygon([lamp, (2048, 1150), (2048, 1290)], fill=(255, 220, 140, 52))
    beam = beam.filter(ImageFilter.GaussianBlur(14))
    img.paste(Image.alpha_composite(img.convert("RGBA"), beam).convert("RGB"), (0, 0))
    d = ImageDraw.Draw(img, "RGBA")

    # tower: tapered, cream with red bands
    cx, y_top, y_bot = 1410, 1090, 1420
    hw_top, hw_bot = 34, 52

    def half_w(y):
        f = (y - y_top) / (y_bot - y_top)
        return hw_top + (hw_bot - hw_top) * f

    bands = [(1090, 1150, (232, 224, 206)), (1150, 1215, (200, 69, 44)),
             (1215, 1280, (232, 224, 206)), (1280, 1345, (200, 69, 44)),
             (1345, 1420, (232, 224, 206))]
    for (ya, yb, col) in bands:
        pts = [(cx - half_w(ya), ya), (cx + half_w(ya), ya),
               (cx + half_w(yb), yb), (cx - half_w(yb), yb)]
        d.polygon(pts, fill=col)
    # gallery + lamp room + dome
    d.rectangle([cx - 52, 1078, cx + 52, 1094], fill=(28, 42, 51))
    d.rectangle([cx - 34, 1036, cx + 34, 1078], fill=(255, 233, 168))
    d.rectangle([cx - 40, 1028, cx + 40, 1038], fill=(28, 42, 51))
    d.polygon([(cx - 46, 1028), (cx + 46, 1028), (cx, 1002)], fill=(200, 69, 44))
    # lamp glow
    img_rgba = img.convert("RGBA")
    glow(img_rgba, cx, 1057, 90, (255, 230, 150), 110, 40)
    img = img_rgba.convert("RGB")
    d = ImageDraw.Draw(img, "RGBA")

    # ---- sailboat (left sea) ----
    bx, by = 430, 1560
    d.polygon([(bx, by - 150), (bx, by - 10), (bx + 95, by - 10)], fill=(247, 238, 220))
    d.polygon([(bx - 12, by - 120), (bx - 12, by - 10), (bx - 85, by - 10)], fill=(232, 220, 198))
    d.line([(bx, by - 160), (bx, by)], fill=(30, 37, 71), width=5)
    d.polygon([(bx - 105, by), (bx + 115, by), (bx + 85, by + 34), (bx - 75, by + 34)],
              fill=(28, 42, 51))
    d.line([(bx - 60, by + 52), (bx + 70, by + 52)], fill=(255, 205, 120, 90), width=4)

    # ---- birds (kept clear of the masthead) ----
    for (bx2, by2, s) in [(560, 700, 26), (660, 640, 20), (1080, 560, 22),
                          (1700, 640, 24), (1800, 590, 18), (350, 780, 18)]:
        d.arc([bx2 - s, by2 - s // 2, bx2, by2 + s // 2], 200, 340, fill=(30, 37, 71), width=5)
        d.arc([bx2, by2 - s // 2, bx2 + s, by2 + s // 2], 200, 340, fill=(30, 37, 71), width=5)

    # ---- faint early stars in the deep top sky ----
    for (sx, sy, r) in [(180, 130, 5), (330, 210, 4), (1880, 150, 5),
                        (1730, 260, 4), (980, 120, 4), (150, 420, 4)]:
        d.ellipse([sx - r, sy - r, sx + r, sy + r], fill=(255, 240, 200, 150))

    # ---- frame ----
    d.rectangle([18, 18, W - 18, H - 18], outline=CREAM, width=10)
    d.rectangle([52, 52, W - 52, H - 52], outline=CREAM + (160,), width=3)

    # ---- type: name + tagline (top masthead) ----
    title_font = ImageFont.truetype(SERIF_BLACK, 235)
    tag_font = ImageFont.truetype(SANS_CONDB, 58)
    name = "LUMARIS"
    # letterspaced title, centred
    widths = [d.textlength(ch, font=title_font) for ch in name]
    track = 34
    total = sum(widths) + track * (len(name) - 1)
    x = (W - total) / 2
    y_title = 108
    for ch, wch in zip(name, widths):
        d.text((x + 5, y_title + 7), ch, font=title_font, fill=(20, 24, 48))
        d.text((x, y_title), ch, font=title_font, fill=CREAM_SOFT)
        x += wch + track
    # tagline, letterspaced, centred, with rules either side
    tag = "WHERE THE SUN RISES TWICE"
    tw = [d.textlength(ch, font=tag_font) for ch in tag]
    ttrack = 16
    ttotal = sum(tw) + ttrack * (len(tag) - 1)
    tx = (W - ttotal) / 2
    ty = 380
    for ch, wch in zip(tag, tw):
        d.text((tx + 2, ty + 3), ch, font=tag_font, fill=(20, 24, 48))
        d.text((tx, ty), ch, font=tag_font, fill=(255, 220, 150))
        tx += wch + ttrack
    # small rules flanking the tagline
    rule_y = ty + 30
    d.line([(tx + 60, rule_y), (tx + 260, rule_y)], fill=(255, 220, 150), width=4)
    d.line([(W - tx - 260, rule_y), (W - tx - 60, rule_y)], fill=(255, 220, 150), width=4)

    # ---- downscale + save ----
    img = img.resize((1024, 1024), Image.LANCZOS)
    img.save(OUT, optimize=True)
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
