#!/usr/bin/env python3
"""Compose the three gta6-meme-x-01 meme images.

Each meme is a 1200x1200 PNG built from:
  - an AI-generated scene background (no text, no logos), and
  - the official make.fun ghost mark from the press kit, composited large,
  - meme text rendered here with PIL in DejaVu Sans Bold (white, black stroke).

Run:  python3 tools/compose.py
Outputs land in meme/ next to this repo's root.
"""

import math
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SRC = "/tmp/meme-src"
GHOST_PATH = os.path.expanduser(
    "~/workspace/makefun/meme-assets/make-fun-press-kit/mark-1024.png"
)
FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

W = H = 1200

BG_TOP = os.path.join(
    SRC, "media-generation-meme1-top-dusty-desk-0-d8b8e71a-d7da-443a-b7d3-acf7f83146cd.png"
)
BG_BOTTOM = os.path.join(
    SRC, "media-generation-meme1-bottom-vice-sunset-0-640788db-de24-42bf-acce-41e31528ca0e.png"
)
BG_BEACH = os.path.join(
    SRC, "media-generation-meme2-wasted-beach-0-739a28e4-6768-4abd-b992-6382d513d1d6.png"
)
BG_STREET = os.path.join(
    SRC, "media-generation-meme3-night-street-0-3f5568f2-cef6-49f4-9a36-31f47aaed2fa.png"
)


def font(size):
    return ImageFont.truetype(FONT_PATH, size)


def fit(img, w, h, y_bias=0.5):
    """Resize + crop img so it exactly covers w x h.

    y_bias 0.5 centres the vertical crop; higher values keep more of the
    lower part of the source (street level instead of sky).
    """
    src_ratio = img.width / img.height
    dst_ratio = w / h
    if src_ratio > dst_ratio:
        new_h = h
        new_w = int(h * src_ratio)
    else:
        new_w = w
        new_h = int(w / src_ratio)
    img = img.resize((new_w, new_h), Image.LANCZOS)
    x = (new_w - w) // 2
    y = int((new_h - h) * y_bias)
    return img.crop((x, y, x + w, y + h))


def load_bg(path, w, h, y_bias=0.5):
    return fit(Image.open(path).convert("RGB"), w, h, y_bias)


def ghost(size):
    g = Image.open(GHOST_PATH).convert("RGBA")
    return g.resize((size, size), Image.LANCZOS)


def paste_ghost(canvas, size, x, y):
    canvas.alpha_composite(ghost(size), (x, y))


def fit_font(text, max_width, start_size, min_size=28):
    """Largest bold font (<= start_size) whose text fits max_width."""
    size = start_size
    while size > min_size:
        f = font(size)
        if f.getbbox(text)[2] <= max_width:
            return f
        size -= 4
    return font(min_size)


def band(canvas, y0, y1, alpha=150):
    """Semi-transparent black band across the full width for text legibility."""
    overlay = Image.new("RGBA", (W, y1 - y0), (0, 0, 0, alpha))
    canvas.alpha_composite(overlay, (0, y0))


def centred(draw, text, y, f, fill=(255, 255, 255, 255), stroke=6):
    bbox = draw.textbbox((0, 0), text, font=f, stroke_width=stroke)
    tw = bbox[2] - bbox[0]
    draw.text(
        ((W - tw) // 2, y),
        text,
        font=f,
        fill=fill,
        stroke_width=stroke,
        stroke_fill=(0, 0, 0, 255),
    )
    return bbox[3] - bbox[1]


def draw_coin(draw, cx, cy, r):
    draw.ellipse(
        (cx - r, cy - r, cx + r, cy + r),
        fill=(255, 201, 40, 255),
        outline=(166, 110, 0, 255),
        width=5,
    )
    f = font(int(r * 1.1))
    bbox = draw.textbbox((0, 0), "$", font=f)
    draw.text(
        (cx - (bbox[2] - bbox[0]) // 2, cy - (bbox[3] - bbox[1]) // 2 - 4),
        "$",
        font=f,
        fill=(120, 74, 0, 255),
    )


def star_points(cx, cy, r_outer, r_inner):
    pts = []
    for i in range(10):
        r = r_outer if i % 2 == 0 else r_inner
        a = -math.pi / 2 + i * math.pi / 5
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts


def meme_waiting():
    canvas = Image.new("RGBA", (W, H))
    canvas.paste(load_bg(BG_TOP, W, 600), (0, 0))
    canvas.paste(load_bg(BG_BOTTOM, W, 600, y_bias=0.92), (0, 600))
    draw = ImageDraw.Draw(canvas)
    draw.rectangle((0, 596, W, 604), fill=(0, 0, 0, 255))

    # Top panel caption.
    band(canvas, 0, 218, alpha=140)
    draw = ImageDraw.Draw(canvas)
    centred(draw, "WAITING FOR GTA VI", 26, fit_font("WAITING FOR GTA VI", 1120, 96), stroke=7)
    centred(draw, "SINCE 2013", 128, fit_font("SINCE 2013", 1120, 84), stroke=7)

    # Bottom panel: ghost large in the foreground, gold coins around it.
    paste_ghost(canvas, 400, 742, 618)
    draw = ImageDraw.Draw(canvas)
    for cx, cy, r in [(120, 950, 46), (215, 1010, 58), (330, 958, 40),
                      (452, 1018, 50), (150, 1064, 36), (688, 986, 42)]:
        draw_coin(draw, cx, cy, r)

    band(canvas, 1058, H, alpha=160)
    draw = ImageDraw.Draw(canvas)
    line = "MY AI AGENT: ALREADY EARNING ON make.fun"
    centred(draw, line, 1082, fit_font(line, 1140, 62), stroke=6)
    return canvas.convert("RGB")


def meme_wasted():
    canvas = load_bg(BG_BEACH, W, H).convert("RGBA")
    # Extra death-screen red wash.
    canvas.alpha_composite(Image.new("RGBA", (W, H), (190, 25, 25, 46)))
    draw = ImageDraw.Draw(canvas)

    wasted = "W A S T E D"
    centred(draw, wasted, 96, fit_font(wasted, 1140, 215), stroke=10)
    sub = "12 YEARS WAITING FOR GTA VI"
    centred(draw, sub, 352, fit_font(sub, 1120, 66), stroke=6)

    paste_ghost(canvas, 470, 688, 690)
    draw = ImageDraw.Draw(canvas)

    # Game-UI style bounty box, lower left.
    box = Image.new("RGBA", (600, 148), (8, 8, 12, 205))
    canvas.alpha_composite(box, (36, 1016))
    draw = ImageDraw.Draw(canvas)
    draw.rectangle((36, 1016, 636, 1164), outline=(255, 255, 255, 255), width=4)
    draw.text((62, 1036), "BOUNTY COMPLETE", font=font(46), fill=(255, 214, 64, 255))
    draw.text((62, 1096), "+USDC - RESPAWNED ON make.fun",
              font=fit_font("+USDC - RESPAWNED ON make.fun", 548, 35),
              fill=(255, 255, 255, 255))
    return canvas.convert("RGB")


def meme_sixstars():
    canvas = load_bg(BG_STREET, W, H).convert("RGBA")

    # Wanted HUD, top right: six gold stars (GTA's real max is five).
    hud = Image.new("RGBA", (428, 128), (5, 5, 10, 170))
    canvas.alpha_composite(hud, (732, 36))
    draw = ImageDraw.Draw(canvas)
    draw.rectangle((732, 36, 1160, 164), outline=(255, 255, 255, 200), width=3)
    for i in range(6):
        cx = 778 + i * 66
        draw.polygon(
            star_points(cx, 100, 30, 13),
            fill=(255, 196, 32, 255),
            outline=(120, 74, 0, 255),
        )

    paste_ghost(canvas, 470, 70, 505)
    draw = ImageDraw.Draw(canvas)

    # Money bag next to the ghost.
    bag = Image.new("RGBA", (250, 300), (0, 0, 0, 0))
    bd = ImageDraw.Draw(bag)
    bd.polygon([(95, 18), (155, 18), (140, 62), (110, 62)], fill=(150, 118, 58, 255))
    bd.ellipse((15, 52, 235, 292), fill=(196, 156, 84, 255), outline=(110, 84, 34, 255), width=5)
    bf = font(120)
    bb = bd.textbbox((0, 0), "$", font=bf)
    bd.text((125 - (bb[2] - bb[0]) // 2, 168 - (bb[3] - bb[1]) // 2), "$",
            font=bf, fill=(84, 58, 8, 255))
    canvas.alpha_composite(bag, (520, 700))
    draw = ImageDraw.Draw(canvas)

    band(canvas, 1012, H, alpha=165)
    draw = ImageDraw.Draw(canvas)
    line1 = "THE 6TH STAR:"
    line2 = "HE EARNS FROM BOUNTIES NOW"
    centred(draw, line1, 1030, fit_font(line1, 1120, 74), stroke=7)
    centred(draw, line2, 1112, fit_font(line2, 1120, 66), stroke=6)
    return canvas.convert("RGB")


def main():
    out_dir = os.path.join(ROOT, "meme")
    os.makedirs(out_dir, exist_ok=True)
    jobs = [
        ("meme-1-waiting.png", meme_waiting),
        ("meme-2-wasted.png", meme_wasted),
        ("meme-3-sixstars.png", meme_sixstars),
    ]
    for name, fn in jobs:
        img = fn()
        assert img.size == (W, H), (name, img.size)
        path = os.path.join(out_dir, name)
        img.save(path, "PNG")
        print("wrote", path, img.size)


if __name__ == "__main__":
    main()
