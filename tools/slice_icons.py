"""Slice viewport/assets/icons.png (6 columns x 3 rows sprite sheet) into icon-1.png ... icon-18.png.
Trims each cell to its ink and pads it square. python -m tools.slice_icons"""
from pathlib import Path

from PIL import Image, ImageOps

ASSETS = Path(__file__).resolve().parents[1] / "viewport" / "assets"
sheet = Image.open(ASSETS / "icons.png").convert("RGB")
W, H = sheet.size
cw, ch = W / 6, H / 3
for r in range(3):
    for c in range(6):
        cell = sheet.crop((round(c * cw), round(r * ch), round((c + 1) * cw), round((r + 1) * ch)))
        ink = ImageOps.invert(cell.convert("L")).point(lambda v: 255 if v > 40 else 0)
        box = ink.getbbox() or (0, 0, cell.width, cell.height)
        icon = cell.crop(box)
        side = max(icon.size) + 8
        canvas = Image.new("RGB", (side, side), "white")
        canvas.paste(icon, ((side - icon.width) // 2, (side - icon.height) // 2))
        canvas.resize((128, 128), Image.LANCZOS).save(ASSETS / f"icon-{r * 6 + c + 1}.png")
print("wrote 18 icons to", ASSETS)
