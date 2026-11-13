#!/usr/bin/env python3
"""Create local, metadata-free daylight photo variants. Run from the repository root."""
from pathlib import Path
from PIL import Image, ImageOps

NAMES = ('desk-pullfocus', 'people-approve', 'people-hands-rack', 'people-meeting', 'rack-plant', 'review-table')
root = Path(__file__).resolve().parents[1]
out = root / 'public/looks/photos/dag'
out.mkdir(parents=True, exist_ok=True)
for name in NAMES:
    with Image.open(root / f'design/photo-src-dag/{name}.jpg') as original:
        image = ImageOps.exif_transpose(original).convert('RGB')
        for width in sorted({640, min(1280, image.width)}):
            resized = image.resize((width, round(image.height * width / image.width)), Image.Resampling.LANCZOS)
            resized.save(out / f'{name}-{width}.avif', quality=43, speed=6)
            resized.save(out / f'{name}-{width}.webp', quality=66, method=6)
        image.thumbnail((1280, 1280), Image.Resampling.LANCZOS)
        image.save(out / f'{name}-1280.jpg', quality=72, progressive=True, optimize=True)
