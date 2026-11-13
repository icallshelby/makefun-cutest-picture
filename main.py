#!/usr/bin/env python3
"""make.fun cutest-picture-01 entry: Two friends cuddling (cream kitten hugging a tiny yellow chick).
Pure Python 3 standard library. v3: refined pointy cat ears with outline, open happy smile with tongue,
and visible chick wing hugging back on the right side.
"""

import math
import os
import struct
import zlib

W = 1024
H = 1024
HYPOT = math.hypot

class Canvas:
    def __init__(self, w, h):
        self.w = w
        self.h = h
        self.px = bytearray(w * h * 3)

    def set_bg(self, top, bottom):
        w, h, px = self.w, self.h, self.px
        for y in range(h):
            t = y / (h - 1)
            r = int(top[0] + (bottom[0] - top[0]) * t)
            g = int(top[1] + (bottom[1] - top[1]) * t)
            b = int(top[2] + (bottom[2] - top[2]) * t)
            row = y * w * 3
            px[row:row + w * 3] = bytes((r, g, b)) * w

    def paint(self, bbox, dist_fn, color):
        x0, y0, x1, y1 = bbox
        x0 = max(0, x0); y0 = max(0, y0)
        x1 = min(self.w - 1, x1); y1 = min(self.h - 1, y1)
        px, w = self.px, self.w
        cr, cg, cb = color
        for y in range(y0, y1 + 1):
            base = y * w * 3
            for x in range(x0, x1 + 1):
                d = dist_fn(x, y)
                if d < 0.75:
                    a = 1.0 if d <= -0.75 else (0.75 - d) / 1.5
                    i = base + x * 3
                    ia = 1.0 - a
                    px[i] = int(cr * a + px[i] * ia + 0.5)
                    px[i + 1] = int(cg * a + px[i + 1] * ia + 0.5)
                    px[i + 2] = int(cb * a + px[i + 2] * ia + 0.5)

    def paint_fn(self, bbox, fn):
        x0, y0, x1, y1 = bbox
        x0 = max(0, x0); y0 = max(0, y0)
        x1 = min(self.w - 1, x1); y1 = min(self.h - 1, y1)
        px, w = self.px, self.w
        for y in range(y0, y1 + 1):
            base = y * w * 3
            for x in range(x0, x1 + 1):
                out = fn(x, y)
                if out is not None:
                    color, a = out
                    if a > 0.0:
                        if a > 1.0: a = 1.0
                        i = base + x * 3
                        ia = 1.0 - a
                        px[i] = int(color[0] * a + px[i] * ia + 0.5)
                        px[i + 1] = int(color[1] * a + px[i + 1] * ia + 0.5)
                        px[i + 2] = int(color[2] * a + px[i + 2] * ia + 0.5)

def clamp(v, lo, hi):
    return lo if v < lo else hi if v > hi else v

def d_circle(x, y, cx, cy, r):
    return HYPOT(x - cx, y - cy) - r

def d_ellipse(x, y, cx, cy, rx, ry):
    return (HYPOT((x - cx) / rx, (y - cy) / ry) - 1.0) * (rx if rx < ry else ry)

def d_segment(x, y, ax, ay, bx, by):
    px, py = x - ax, y - ay
    dx, dy = bx - ax, by - ay
    l2 = dx * dx + dy * dy
    t = 0.0 if l2 == 0 else clamp((px * dx + py * dy) / l2, 0.0, 1.0)
    return HYPOT(px - dx * t, py - dy * t)

def d_triangle(x, y, ax, ay, bx, by, cx, cy):
    def edge(px, py, qx, qy, rx, ry):
        return (qx - px) * (ry - py) - (qy - py) * (rx - px)
    s1 = edge(ax, ay, bx, by, x, y)
    s2 = edge(bx, by, cx, cy, x, y)
    s3 = edge(cx, cy, ax, ay, x, y)
    inside = (s1 >= 0 and s2 >= 0 and s3 >= 0) or (s1 <= 0 and s2 <= 0 and s3 <= 0)
    d = min(
        d_segment(x, y, ax, ay, bx, by),
        d_segment(x, y, bx, by, cx, cy),
        d_segment(x, y, cx, cy, ax, ay),
    )
    return -d if inside else d

def draw():
    cv = Canvas(W, H)
    BG_TOP = (255, 248, 242)
    BG_BOT = (212, 244, 232)
    cv.set_bg(BG_TOP, BG_BOT)

    # Ground shadow
    cv.paint((150, 840, 874, 915), lambda x, y: d_ellipse(x, y, 512, 878, 330, 34), (180, 215, 200))

    CREAM = (255, 243, 230)
    CREAM_SHADOW = (245, 220, 198)
    WHITE = (255, 255, 255)
    PINK_BLUSH = (252, 175, 188)
    PINK_TONGUE = (255, 135, 155)
    NOSE_COL = (242, 110, 138)
    EYE_IRIS = (45, 140, 215)
    EYE_IRIS_LT = (110, 205, 245)
    EYE_DARK = (20, 25, 35)
    MINT = (110, 200, 165)
    MINT_DARK = (80, 160, 130)
    CHICK_BODY = (255, 222, 70)
    CHICK_ORANGE = (245, 130, 35)
    DAISY_YELLOW = (255, 205, 45)

    # 1. Kitten Body & Shoulders (generous bounding boxes)
    cv.paint((280, 560, 744, 900), lambda x, y: d_ellipse(x, y, 512, 730, 220, 160), CREAM_SHADOW)
    cv.paint((290, 570, 734, 890), lambda x, y: d_ellipse(x, y, 512, 720, 205, 150), CREAM)

    # 2. Kitten Head
    cv.paint((270, 210, 754, 730), lambda x, y: d_circle(x, y, 512, 450, 220), CREAM_SHADOW)
    cv.paint((280, 220, 744, 720), lambda x, y: d_circle(x, y, 512, 450, 210), CREAM)

    # 3. Kitten Ears (Pointy cat ears with CREAM_SHADOW outline for separation and smaller pink inner ear)
    # Left Ear Outline (slightly expanded triangle or offset)
    cv.paint((265, 165, 435, 425), lambda x, y: d_triangle(x, y, 310, 325, 342, 168, 428, 315), CREAM_SHADOW)
    # Left Ear Cream Outer
    cv.paint((270, 170, 430, 420), lambda x, y: d_triangle(x, y, 315, 320, 342, 174, 423, 310), CREAM)
    # Left Ear Inner Pink
    cv.paint((310, 205, 400, 390), lambda x, y: d_triangle(x, y, 332, 310, 344, 212, 398, 300), PINK_BLUSH)

    # Right Ear Outline
    cv.paint((585, 165, 755, 425), lambda x, y: d_triangle(x, y, 710, 325, 678, 168, 592, 315), CREAM_SHADOW)
    # Right Ear Cream Outer
    cv.paint((590, 170, 750, 420), lambda x, y: d_triangle(x, y, 705, 320, 678, 174, 597, 310), CREAM)
    # Right Ear Inner Pink
    cv.paint((620, 205, 710, 390), lambda x, y: d_triangle(x, y, 688, 310, 676, 212, 622, 300), PINK_BLUSH)

    # 4. Mint Scarf around neck (higher up, above chick/paws)
    cv.paint((330, 510, 694, 600), lambda x, y: d_ellipse(x, y, 512, 550, 170, 38), MINT_DARK)
    cv.paint((340, 515, 684, 595), lambda x, y: d_ellipse(x, y, 512, 545, 160, 32), MINT)
    cv.paint((460, 560, 530, 640), lambda x, y: d_ellipse(x, y, 495, 595, 22, 35), MINT)
    cv.paint((465, 580, 525, 635), lambda x, y: d_ellipse(x, y, 495, 610, 16, 12), MINT_DARK)

    # 5. Muzzle
    cv.paint((402, 475, 622, 600), lambda x, y: d_ellipse(x, y, 512, 525, 110, 75), WHITE)

    # 6. Eyes (Huge sparkling sapphire eyes)
    # Left Eye
    cv.paint((340, 350, 470, 500), lambda x, y: d_circle(x, y, 405, 425, 56), EYE_DARK)
    cv.paint((350, 360, 460, 490), lambda x, y: d_circle(x, y, 405, 425, 49), EYE_IRIS)
    cv.paint((360, 370, 450, 480), lambda x, y: d_circle(x, y, 410, 430, 39), EYE_IRIS_LT)
    cv.paint((365, 375, 430, 445), lambda x, y: d_circle(x, y, 390, 410, 19), WHITE)
    cv.paint((410, 430, 450, 470), lambda x, y: d_circle(x, y, 425, 440, 8), WHITE)

    # Right Eye
    cv.paint((550, 350, 680, 500), lambda x, y: d_circle(x, y, 615, 425, 56), EYE_DARK)
    cv.paint((560, 360, 670, 490), lambda x, y: d_circle(x, y, 615, 425, 49), EYE_IRIS)
    cv.paint((570, 370, 660, 480), lambda x, y: d_circle(x, y, 610, 430, 39), EYE_IRIS_LT)
    cv.paint((575, 375, 640, 445), lambda x, y: d_circle(x, y, 595, 410, 19), WHITE)
    cv.paint((620, 430, 660, 470), lambda x, y: d_circle(x, y, 635, 440, 8), WHITE)

    # 7. Rosy Blush
    cv.paint((320, 450, 415, 530), lambda x, y: d_ellipse(x, y, 368, 490, 48, 26), PINK_BLUSH)
    cv.paint((600, 450, 700, 530), lambda x, y: d_ellipse(x, y, 654, 490, 48, 26), PINK_BLUSH)

    # 8. Nose & Open Happy Smile with Tongue
    cv.paint((492, 495, 532, 530), lambda x, y: d_triangle(x, y, 512, 505, 498, 490, 526, 490), NOSE_COL)
    # Open happy mouth cavity
    cv.paint((492, 515, 532, 550), lambda x, y: d_ellipse(x, y, 512, 532, 14, 10), EYE_DARK)
    # Pink tongue inside mouth
    cv.paint((500, 526, 524, 542), lambda x, y: d_ellipse(x, y, 512, 536, 8, 5), PINK_TONGUE)
    # Smile curve outline / lips
    cv.paint((488, 515, 536, 545), lambda x, y: d_segment(x, y, 492, 524, 512, 538), EYE_DARK)
    cv.paint((488, 515, 536, 545), lambda x, y: d_segment(x, y, 512, 538, 532, 524), EYE_DARK)

    # 9. Tiny Yellow Chick tucked against chest (with visible right wing reaching toward kitten)
    cv.paint((432, 610, 592, 770), lambda x, y: d_circle(x, y, 512, 690, 76), CHICK_ORANGE)
    cv.paint((437, 615, 587, 765), lambda x, y: d_circle(x, y, 512, 690, 71), CHICK_BODY)
    # Chick wing on the right side reaching up/out toward kitten's right paw
    cv.paint((545, 655, 590, 705), lambda x, y: d_ellipse(x, y, 568, 678, 14, 8), CHICK_ORANGE)
    cv.paint((548, 658, 587, 702), lambda x, y: d_ellipse(x, y, 568, 678, 11, 6), CHICK_BODY)
    # Chick beak
    cv.paint((492, 680, 532, 715), lambda x, y: d_triangle(x, y, 512, 705, 497, 690, 527, 690), CHICK_ORANGE)
    # Chick closed eyes (^ ^)
    cv.paint((475, 665, 505, 695), lambda x, y: d_segment(x, y, 480, 680, 490, 672), EYE_DARK)
    cv.paint((475, 655, 505, 685), lambda x, y: d_segment(x, y, 490, 672, 500, 680), EYE_DARK)
    cv.paint((519, 665, 549, 695), lambda x, y: d_segment(x, y, 524, 680, 534, 672), EYE_DARK)
    cv.paint((519, 655, 549, 685), lambda x, y: d_segment(x, y, 534, 672, 544, 680), EYE_DARK)
    # Chick feet
    cv.paint((482, 750, 512, 775), lambda x, y: d_circle(x, y, 497, 762, 9), CHICK_ORANGE)
    cv.paint((512, 750, 542, 775), lambda x, y: d_circle(x, y, 527, 762, 9), CHICK_ORANGE)

    # 10. Kitten Paws wrapping around chick
    cv.paint((382, 650, 482, 750), lambda x, y: d_ellipse(x, y, 432, 700, 50, 40), CREAM_SHADOW)
    cv.paint((392, 655, 472, 745), lambda x, y: d_ellipse(x, y, 432, 700, 44, 34), CREAM)
    cv.paint((542, 650, 642, 750), lambda x, y: d_ellipse(x, y, 592, 700, 50, 40), CREAM_SHADOW)
    cv.paint((552, 655, 632, 745), lambda x, y: d_ellipse(x, y, 592, 700, 44, 34), CREAM)

    # 11. Daisy Crown on head
    def draw_daisy(cx, cy):
        for a_off in range(5):
            angle = a_off * (2 * math.pi / 5)
            px_c = cx + int(18 * math.cos(angle))
            py_c = cy + int(18 * math.sin(angle))
            cv.paint((px_c - 14, py_c - 14, px_c + 14, py_c + 14), lambda x, y: d_circle(x, y, px_c, py_c, 12), WHITE)
        cv.paint((cx - 12, cy - 12, cx + 12, cy + 12), lambda x, y: d_circle(x, y, cx, cy, 10), DAISY_YELLOW)

    draw_daisy(380, 255)
    draw_daisy(445, 230)
    draw_daisy(512, 225)
    draw_daisy(579, 235)
    draw_daisy(644, 260)

    # 12. Floating hearts & sparkles
    def heart(cx, cy, s, color, alpha):
        def fn(x, y):
            lx = (x - cx) / s
            ly = (cy - y) / s
            v = (lx * lx + ly * ly - 1) ** 3 - lx * lx * ly ** 3
            return (color, alpha) if v < 0 else None
        pad = int(s * 1.5)
        cv.paint_fn((cx - pad, cy - pad, cx + pad, cy + pad), fn)

    heart(215, 340, 24, PINK_BLUSH, 0.85)
    heart(805, 370, 28, PINK_BLUSH, 0.85)

    return cv

def write_png(cv, path):
    w, h = cv.w, cv.h
    raw = bytearray()
    rowlen = w * 3
    for y in range(h):
        raw.append(0)
        raw += cv.px[y * rowlen:(y + 1) * rowlen]

    def chunk(tag, data):
        c = struct.pack(">I", len(data)) + tag + data
        c += struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)
        return c

    png = bytearray(b"\x89PNG\r\n\x1a\n")
    png += chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 2, 0, 0, 0))
    png += chunk(b"IDAT", zlib.compress(bytes(raw), 9))
    png += chunk(b"IEND", b"")
    with open(path, "wb") as f:
        f.write(png)

def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    cv = draw()
    write_png(cv, os.path.join(out_dir, "entry.png"))

if __name__ == "__main__":
    main()
