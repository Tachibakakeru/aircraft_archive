"""由 assets/earth_daymap.jpg（NASA Blue Marble，4096×2048 經緯度等距投影）產生首頁航線圖用的陸地遮罩。

輸出 data/landmask.json：
  {"w": 720, "h": 360, "res": 0.5, "rows": ["<run-length>", ...]}
每列從經度 -180° 開始、由北（+90°）往南，每格 0.5°；rows[i] 是以「海、陸、海、陸…」交替的
連續格數（36 進位、逗號分隔），第一段一定是海（可能為 0）。
判斷方式：每格取 4096 圖上對應的像素區塊，「偏藍且偏暗」視為海，陸地像素比例 ≥ 35% 即為陸地。
重跑：python tools/build_landmask.py
"""
import json
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
RES = 0.5
W, H = int(360 / RES), int(180 / RES)


def is_water(r, g, b):
    return b > r + 12 and b >= g - 4 and r < 90


def main():
    im = Image.open(ROOT / "assets/earth_daymap.jpg").convert("RGB")
    iw, ih = im.size
    px = im.load()
    sx, sy = iw / W, ih / H
    rows = []
    land_cells = 0
    for j in range(H):
        bits = []
        for i in range(W):
            x0, y0 = int(i * sx), int(j * sy)
            x1, y1 = max(x0 + 1, int((i + 1) * sx)), max(y0 + 1, int((j + 1) * sy))
            total = land = 0
            for y in range(y0, y1, 1):
                for x in range(x0, x1, 1):
                    total += 1
                    if not is_water(*px[x, y]):
                        land += 1
            bits.append(1 if land / total >= 0.35 else 0)
        land_cells += sum(bits)
        runs, cur, n = [], 0, 0
        for b in bits:
            if b == cur:
                n += 1
            else:
                runs.append(n)
                cur, n = b, 1
        runs.append(n)
        rows.append(",".join(base36(r) for r in runs))
    out = {"w": W, "h": H, "res": RES, "source": "assets/earth_daymap.jpg (NASA Blue Marble)", "rows": rows}
    (ROOT / "data/landmask.json").write_text(json.dumps(out, separators=(",", ":")), encoding="utf-8")
    print(f"landmask {W}x{H}, land {land_cells / (W * H):.1%}, {len(json.dumps(out)) / 1024:.1f} KB")


def base36(n):
    digits = "0123456789abcdefghijklmnopqrstuvwxyz"
    if n == 0:
        return "0"
    s = ""
    while n:
        n, r = divmod(n, 36)
        s = digits[r] + s
    return s


if __name__ == "__main__":
    main()
