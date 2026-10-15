#!/usr/bin/env python3
"""Optimise look photos for production.

Source: design/photo-src/<look>/<name>.jpg (gitignored originals, 1536x1024, AI-generated per Hans 15 Oct 2026).
Output: public/looks/photos/<look>/<name>-<w>.webp at widths 768 and 1536, plus <name>-1536.jpg (progressive) fallback.
Crops (Hans feedback) are applied here, deterministically. Re-run is idempotent.
"""
from pathlib import Path
from PIL import Image

SRC = Path("design/photo-src")
OUT = Path("public/looks/photos")
WIDTHS = (768, 1536)
# (look, name) -> crop box as fractions (left, top, right, bottom)
CROPS = {
    ("k", "hero"): (0.0, 0.30, 1.0, 1.0),  # Hans: no head — shoulder + arm only
}


def main():
    n = 0
    for f in sorted(SRC.glob("*/*.jpg")):
        look, name = f.parent.name, f.stem
        im = Image.open(f).convert("RGB")
        if (look, name) in CROPS:
            l, t, r, b = CROPS[(look, name)]
            W, H = im.size
            im = im.crop((round(l * W), round(t * H), round(r * W), round(b * H)))
        dst = OUT / look
        dst.mkdir(parents=True, exist_ok=True)
        for w in WIDTHS:
            w2 = min(w, im.width)
            h2 = round(im.height * w2 / im.width)
            r = im.resize((w2, h2), Image.Resampling.LANCZOS)
            r.save(dst / f"{name}-{w}.webp", "WEBP", quality=78, method=6)
            n += 1
            if w == WIDTHS[-1]:  # one progressive JPEG fallback for old browsers
                r.save(dst / f"{name}-{w}.jpg", "JPEG", quality=76, optimize=True, progressive=True)
                n += 1
    print(f"optimize-photos: wrote {n} files to {OUT}")


if __name__ == "__main__":
    main()
