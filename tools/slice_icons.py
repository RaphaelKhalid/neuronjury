"""Slice viewport/assets/icons.png (6 x 3 sprite sheet, cells separated by thin rules) into icon-1..18.png.
Finds the ruled grid lines automatically, cuts inside them, trims each icon to its ink and pads it square.
python -m tools.slice_icons"""
from pathlib import Path

import numpy as np
from PIL import Image

ASSETS = Path(__file__).resolve().parents[1] / "viewport" / "assets"


def rules(dark: np.ndarray, axis: int, want: int) -> list[int]:
    """Positions of long straight rules: rows/cols where most pixels are dark, merged into single lines."""
    frac = dark.mean(axis=axis)
    idx = np.nonzero(frac > 0.5)[0]
    groups, cur = [], []
    for i in idx:
        if cur and i - cur[-1] > 3:
            groups.append(cur)
            cur = []
        cur.append(i)
    if cur:
        groups.append(cur)
    pos = [int(np.mean(g)) for g in groups]
    if len(pos) != want:
        raise SystemExit(f"expected {want} rules along axis {axis}, found {len(pos)}: {pos}")
    return pos


def main():
    sheet = Image.open(ASSETS / "icons.png").convert("RGB")
    g = np.asarray(sheet.convert("L")).astype(np.float32)
    dark = g < 140
    xs = rules(dark, 0, 7)   # 6 columns -> 7 vertical rules
    ys = rules(dark, 1, 4)   # 3 rows -> 4 horizontal rules
    n = 0
    for r in range(3):
        for c in range(6):
            x0, x1, y0, y1 = xs[c] + 6, xs[c + 1] - 6, ys[r] + 6, ys[r + 1] - 6
            cell = sheet.crop((x0, y0, x1, y1))
            ink = np.asarray(cell.convert("L")) < 200
            yy, xx = np.nonzero(ink)
            box = (xx.min(), yy.min(), xx.max() + 1, yy.max() + 1) if len(xx) else (0, 0, cell.width, cell.height)
            icon = cell.crop(box)
            side = max(icon.size) + 10
            canvas = Image.new("RGB", (side, side), "white")
            canvas.paste(icon, ((side - icon.width) // 2, (side - icon.height) // 2))
            n += 1
            canvas.resize((160, 160), Image.LANCZOS).save(ASSETS / f"icon-{n}.png")
    print(f"wrote {n} icons to {ASSETS}")


if __name__ == "__main__":
    main()
