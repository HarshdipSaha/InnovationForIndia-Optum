"""Render docs/assets/demo.gif — SAAKSHI 4-layer forensic detectors & citizen verification.

Generates an animated dark-theme demo GIF showing:
  1. Real CAG Karnataka MGNREGA case file (₹4.2L farm pond claimed complete)
  2. Four independent forensic detector layers discovering evidence
  3. Lakshmi's citizen verification call via toll-free voice
  4. GHADI statutory RTI countdown clock

Supports:
    python scripts/make_demo_gif.py                 # writes docs/assets/demo.gif
    python scripts/make_demo_gif.py --still         # writes docs/assets/demo_still.png
    python scripts/make_demo_gif.py --from-video    # converts 03_Demo_Video/SAAKSHI_demo.mp4
"""
from __future__ import annotations

import os
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "assets"
OUT.mkdir(parents=True, exist_ok=True)

# --- GitHub dark theme palette ---
BG        = (13, 16, 22)
PANEL     = (22, 27, 34)
BORDER    = (44, 51, 62)
TRACK     = (33, 39, 48)
TXT       = (230, 237, 243)
MUTED     = (139, 148, 158)
FAINT     = (85, 95, 108)
AMBER     = (240, 185, 80)
RED       = (248, 96, 88)
GREEN     = (63, 185, 80)
INDIGO    = (150, 130, 250)
BLUE      = (88, 166, 255)
CHIP_BG   = (32, 38, 47)

S = 2
W, H = 920, 460

F = "C:/Windows/Fonts/"
def font(name: str, size: int):
    path = F + name
    if os.path.exists(path):
        return ImageFont.truetype(path, size * S)
    return ImageFont.load_default()

f_lbl   = font("seguisb.ttf", 11)
f_title = font("segoeuib.ttf", 15)
f_meta  = font("segoeui.ttf", 12)
f_chip  = font("seguisb.ttf", 12)
f_bold  = font("seguisb.ttf", 13)
f_desc  = font("segoeui.ttf", 12)
f_badge = font("seguisb.ttf", 11)
f_foot  = font("seguisb.ttf", 12)
f_sub   = font("segoeui.ttf", 11)

LAYERS = [
    {
        "name": "CHITRAGUPTA · Photos",
        "tag": "REUSED PHOTO (dHash 0/64)",
        "color": RED,
        "detail": "Duplicate completion photo matched across works 61.4 km apart (Koppal <-> Kalaburagi)",
        "stat": "nmms_88213 ↔ nmms_71104",
        "conf": "HIGH CONFIDENCE",
    },
    {
        "name": "CHITRAGUPTA · Payments",
        "tag": "CAG AUDIT RE-DERIVED",
        "color": AMBER,
        "detail": "462 stage payments AFTER claimed completion (₹1.19 cr) + threshold split below ₹5L",
        "stat": "462 payments · ₹1.19 Cr lag",
        "conf": "CAG MATCHED",
    },
    {
        "name": "CHITRAGUPTA · Network",
        "tag": "SOLE-BIDDER CARTEL",
        "color": AMBER,
        "detail": "Vendor V-04412 won 11/11 block tenders as sole bidder (68.8% single-bid rate vs 14% natl)",
        "stat": "68.8% single-bid · +2.1% premium",
        "conf": "COLLUSION FLAG",
    },
    {
        "name": "PRAMAAN · Citizen Voice",
        "tag": "GROUND TRUTH VERIFIED",
        "color": GREEN,
        "detail": "Lakshmi calls toll-free 1800-SAAKSHI in Kannada: 'No pond exists at survey 112/3'",
        "stat": "3 independent callers · zkSNARK",
        "conf": "CITIZEN VERIFIED",
    },
]


def R(*v):
    return tuple(int(round(x * S)) for x in v)


def rr(d: ImageDraw.ImageDraw, box, radius, fill=None, outline=None, width=1):
    d.rounded_rectangle(R(*box), radius=int(radius * S), fill=fill,
                        outline=outline, width=int(width * S))


def tx(d: ImageDraw.ImageDraw, xy, s: str, fnt, fill, anchor="la"):
    d.text((int(xy[0] * S), int(xy[1] * S)), s, font=fnt, fill=fill, anchor=anchor)


def tl(d: ImageDraw.ImageDraw, s: str, fnt) -> float:
    return d.textlength(s, font=fnt) / S


def dot(d: ImageDraw.ImageDraw, cx, cy, r, color):
    d.ellipse(R(cx - r, cy - r, cx + r, cy + r), fill=color)


def badge(d: ImageDraw.ImageDraw, x, y, text, color, bg):
    w = tl(d, text, f_badge)
    h = 20
    rr(d, (x, y, x + w + 16, y + h), 5, fill=bg, outline=color, width=1)
    tx(d, (x + 8, y + 3), text, f_badge, color)
    return w + 16


def render(step: int) -> Image.Image:
    img = Image.new("RGB", (W * S, H * S), BG)
    d = ImageDraw.Draw(img)

    # Top Case Card
    rr(d, (20, 18, W - 20, 96), 12, fill=PANEL, outline=BORDER, width=1)
    
    # Left accent indicator
    rr(d, (20, 18, 24, 96), 2, fill=BLUE)
    
    tx(d, (36, 28), "CASE KA-KLB-2026-00412", f_title, TXT)
    tx(d, (245, 30), "· Kamalapur GP, Kalaburagi · LGD 226534", f_meta, MUTED)
    
    badge(d, W - 245, 27, "AWAITING DEPARTMENT RESPONSE", AMBER, (46, 36, 18))
    
    tx(d, (36, 52), "Work: Farm pond, survey no. 112/3  ·  Scheme: MGNREGA  ·  Sanction: ₹4,20,000", f_meta, TXT)
    tx(d, (36, 72), "Claimed Status: Completed 14 June 2026  ·  Verification Window: 30 Days", f_meta, FAINT)

    # Render forensic layers
    y = 108
    for i, layer in enumerate(LAYERS):
        if step < i + 1:
            break
        row_h = 58
        rr(d, (20, y, W - 20, y + row_h), 10, fill=PANEL, outline=BORDER, width=1)
        rr(d, (20, y, 24, y + row_h), 2, fill=layer["color"])

        # Chip / Name
        nw = tl(d, layer["name"], f_chip)
        rr(d, (34, y + 10, 34 + nw + 18, y + 30), 5, fill=CHIP_BG)
        dot(d, 42, y + 20, 3, layer["color"])
        tx(d, (50, y + 12), layer["name"], f_chip, TXT)

        # Stat text next to name
        tx(d, (34 + nw + 28, y + 13), layer["stat"], f_sub, layer["color"])

        # Description
        tx(d, (34, y + 35), layer["detail"], f_desc, MUTED)

        # Right-side Confidence Pill
        bw = tl(d, layer["conf"], f_badge)
        bx = W - 36 - bw - 16
        rr(d, (bx, y + 18, bx + bw + 16, y + 40), 6, fill=(28, 33, 40), outline=layer["color"], width=1)
        tx(d, (bx + 8, y + 21), layer["conf"], f_badge, layer["color"])

        y += 66

    # Bottom Accountability Banner (step 5)
    if step >= 5:
        rr(d, (20, 380, W - 20, 442), 10, fill=(18, 25, 38), outline=INDIGO, width=1)
        dot(d, 36, 411, 5, GREEN)
        tx(d, (48, 390), "GHADI ACCOUNTABILITY CLOCK  ·  RTI §6(1) AUTO-DRAFTED", f_foot, TXT)
        tx(d, (48, 414), "Statutory 30-Day Countdown: 16 Days Elapsed · 14 Days Remaining · Zero Composite Score", f_sub, MUTED)
        
        bw = tl(d, "CONTESTABLE EVIDENCE FILE", f_badge)
        bx = W - 36 - bw - 16
        rr(d, (bx, 398, bx + bw + 16, 424), 5, fill=(35, 30, 60), outline=INDIGO, width=1)
        tx(d, (bx + 8, 403), "CONTESTABLE EVIDENCE FILE", f_badge, INDIGO)

    return img


def build_frames():
    frames, durs = [], []

    def add(im, ms):
        frames.append(im)
        durs.append(ms)

    def xfade(a, b, n=3, ms=45):
        for i in range(1, n + 1):
            add(Image.blend(a, b, i / (n + 1)), ms)

    # Hold times per step
    holds = {
        0: 700,   # Case card
        1: 1300,  # Photo forensics
        2: 1300,  # Payment split & timing
        3: 1300,  # Procurement graph
        4: 1700,  # Citizen verification call
        5: 3200,  # Accountability clock summary
    }

    prev = None
    for step in range(6):
        cur = render(step)
        if prev is not None:
            xfade(prev, cur)
        add(cur, holds[step])
        prev = cur

    return frames, durs


def down(im: Image.Image) -> Image.Image:
    return im.resize((W, H), Image.LANCZOS)


def convert_video_to_gif(video_path: Path, out_path: Path):
    """Convert an MP4 video to an optimized GIF."""
    try:
        import cv2
    except ImportError:
        print("OpenCV (cv2) required for video conversion. Run: pip install opencv-python")
        sys.exit(1)

    if not video_path.exists():
        print(f"Video not found: {video_path}")
        sys.exit(1)

    print(f"Converting video {video_path} -> {out_path}...")
    cap = cv2.VideoCapture(str(video_path))
    fps = cap.get(cv2.CAP_PROP_FPS) or 30
    step = max(1, int(round(fps / 10)))  # target ~10 fps for crisp size
    frames = []
    idx = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        if idx % step == 0:
            h, w = frame.shape[:2]
            target_w = 880
            target_h = int(h * (target_w / w))
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            im = Image.fromarray(rgb).resize((target_w, target_h), Image.BILINEAR)
            frames.append(im)
        idx += 1
    cap.release()

    if not frames:
        print("No frames extracted from video.")
        sys.exit(1)

    print(f"Extracted {len(frames)} frames. Optimizing palette...")
    sample = Image.new("RGB", (frames[0].width, frames[0].height * 3))
    sample.paste(frames[0], (0, 0))
    sample.paste(frames[len(frames) // 2], (0, frames[0].height))
    sample.paste(frames[-1], (0, frames[0].height * 2))
    pal = sample.quantize(colors=160, method=Image.MEDIANCUT)

    pf = [f.quantize(palette=pal, dither=Image.FLOYDSTEINBERG) for f in frames]
    pf[0].save(out_path, save_all=True, append_images=pf[1:], loop=0,
               duration=100, disposal=2, optimize=True)
    size_mb = out_path.stat().st_size / (1024 * 1024)
    print(f"Wrote {out_path} ({len(pf)} frames, {size_mb:.2f} MB)")


def main():
    if "--from-video" in sys.argv:
        video = ROOT / "03_Demo_Video" / "SAAKSHI_demo.mp4"
        convert_video_to_gif(video, OUT / "demo.gif")
        return

    if "--still" in sys.argv:
        still_img = down(render(5))
        still_img.save(OUT / "demo_still.png")
        print("Wrote", OUT / "demo_still.png")
        return

    print("Rendering animated demo frames...")
    frames, durs = build_frames()
    frames = [down(f) for f in frames]

    master = Image.new("RGB", (W, H * 2), BG)
    master.paste(frames[-1], (0, 0))
    master.paste(frames[0], (0, H))
    pal = master.quantize(colors=220, method=Image.MEDIANCUT, dither=Image.NONE)
    pf = [f.quantize(palette=pal, dither=Image.NONE) for f in frames]

    gif_path = OUT / "demo.gif"
    pf[0].save(
        gif_path,
        save_all=True,
        append_images=pf[1:],
        loop=0,
        duration=durs,
        disposal=2,
        optimize=True
    )
    kb = gif_path.stat().st_size / 1024
    print(f"Wrote {gif_path} ({len(pf)} frames, {kb:.0f} KB)")


if __name__ == "__main__":
    main()
