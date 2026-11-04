"""由 3D 模型產生航線動畫用的「俯視剪影」圖示，並為每個機型指定要用哪一張。

輸出：
  assets/silhouettes/<模型 id>.png   192×192 白色剪影（透明背景、機頭朝上），48 個 3D 模型各一張
  data/silhouettes.json              {"<機型 id>": {"s": "<剪影檔名>", "span": 翼展公尺}, ...}
                                     沒有 3D 模型的機型，依名稱對應同家族的模型，否則依類別用代表剪影。

做法：讀 models/<id>.json（v1／v2 格式，與 tools/make_thumb.py 相同），把所有三角形投影到 x–z 平面
（x 為機頭方向、z 為左右），以 4 倍超取樣填色後縮小，得到平滑邊緣。起落架不畫。
重跑：python tools/build_silhouettes.py
"""
import base64
import json
import re
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "assets/silhouettes"
SIZE, SS = 192, 4          # 輸出邊長、超取樣倍率
PAD = 0.06                 # 四周留白比例


def triangles(model):
    groups = list(model["parts"].items()) + [(s.get("part", "wing"), s["e"]) for s in model.get("surfaces", [])]
    out = []
    for pid, entries in groups:
        if pid == "gear":
            continue
        for e in entries:
            if "q" in e:
                q = np.frombuffer(base64.b64decode(e["q"]), np.uint16).reshape(-1, 3).astype(np.float32)
                pos = q * np.array(e["qs"], np.float32) + np.array(e["qo"], np.float32)
            else:
                pos = np.frombuffer(base64.b64decode(e["p"]), np.float32).reshape(-1, 3)
            idx = np.frombuffer(base64.b64decode(e["i"]), np.uint32 if e["iw"] == 4 else np.uint16)
            out.append(pos[idx.astype(np.int64)].reshape(-1, 3, 3))
    return np.concatenate(out)


def silhouette(model_id):
    model = json.loads((ROOT / f"models/{model_id}.json").read_text(encoding="utf-8"))
    tris = triangles(model)
    xs, zs = tris[:, :, 0], tris[:, :, 2]
    span = max(xs.max() - xs.min(), zs.max() - zs.min())
    big = SIZE * SS
    scale = big * (1 - 2 * PAD) / span
    cx, cz = (xs.max() + xs.min()) / 2, (zs.max() + zs.min()) / 2
    img = Image.new("L", (big, big), 0)
    draw = ImageDraw.Draw(img)
    # 機頭朝上：畫面 y = −x，畫面 x = z
    px = big / 2 + (zs - cz) * scale
    py = big / 2 - (xs - cx) * scale
    for k in range(len(tris)):
        draw.polygon([(px[k, 0], py[k, 0]), (px[k, 1], py[k, 1]), (px[k, 2], py[k, 2])], fill=255)
    alpha = img.resize((SIZE, SIZE), Image.LANCZOS)
    rgba = Image.new("RGBA", (SIZE, SIZE), (255, 255, 255, 0))
    rgba.putalpha(alpha)
    OUT.mkdir(parents=True, exist_ok=True)
    rgba.save(OUT / f"{model_id}.png", optimize=True)
    return float(zs.max() - zs.min())


# 沒有 3D 模型時：先依名稱對應同家族模型，再依類別用代表剪影
FAMILY = [
    (r"A220-100|CS100", "cs100"), (r"A220-300|CS300", "cs300"),
    (r"A318", "a318"), (r"A319", "a319"), (r"A320", "a320"), (r"A321", "a321"),
    (r"A330-200|A330-800|A330 MRTT|Beluga ?XL", "a332"), (r"A330", "a333"),
    (r"A340-[56]", "a346"), (r"A340", "a343"), (r"A350", "a359"), (r"A380", "a380"),
    (r"737-600", "b736"), (r"737-700|737 MAX 7", "b737"), (r"737-9|737 MAX 9|737 MAX 10", "b739"), (r"737", "b738"),
    (r"747-8", "b748"), (r"747", "b744"), (r"757-3", "b753"), (r"757", "b752"),
    (r"767-2", "b762"), (r"767-4", "b764"), (r"767", "b763"),
    (r"777-2|777F|777-8", "b772"), (r"777", "b773"), (r"787-8", "b788"), (r"787", "b789"),
    (r"707|720", "b707"), (r"717|MD-95", "b717"), (r"727", "b727"), (r"DC-9", "dc9"), (r"MD-8|MD-9", "md80"),
    (r"DC-10|KC-10", "dc10"), (r"MD-11", "md11"), (r"An-225", "an225"), (r"An-124|C-5|Il-76|C-17|A400M", "an225"),
    (r"CRJ ?900|CRJ ?1000", "crj900"), (r"CRJ", "crj700"), (r"E17|E-17|ERJ-17", "e170"), (r"E19|E-19|E2", "e190"),
    (r"ERJ|BAe 146|Avro RJ|C909|ARJ21", "bae146"), (r"Concorde|Tu-144", "concorde"),
    (r"Q400|Dash 8|DHC-8", "q400"), (r"ATR|Saab|Dornier 328|Twin Otter|Caravan|C-130|Hercules|Y-12|Beech 1900|King Air", "atr42"),
    (r"Citation|Learjet|Gulfstream|Falcon|Global|Challenger|Phenom|Praetor|Legacy|HondaJet|PC-24|Hawker", "citation"),
    (r"Cessna 1[5-8]|Cherokee|PA-28|Piper|Cirrus|Diamond|Mooney|Bonanza|Robin|Tecnam", "pa28"),
    (r"ASK|Glider|Discus|Ventus|DG-", "ask21"),
]
CATEGORY = {
    "窄體客機": "a320", "廣體客機": "b789", "貨機": "b744", "區域客機": "e190", "支線客機": "crj700",
    "渦輪螺旋槳": "atr42", "通用運輸機": "atr42", "公務機": "citation", "直升機": "heli",
    "活塞通用航空": "pa28", "飛行訓練機": "pa28", "輕型運動機": "pa28", "套件機": "pa28", "通用航空": "pa28",
    "特技機": "pa28", "水陸兩用機": "pa28", "滑翔機": "ask21", "超音速客機": "concorde",
}


def span_of(entry):
    m = re.search(r"([\d.]+)\s*m", entry.get("span") or "")
    return float(m.group(1)) if m else None


def main():
    fleet = json.loads((ROOT / "data/fleet.json").read_text(encoding="utf-8"))["aircraft"]
    models = sorted(p.stem for p in (ROOT / "models").glob("*.json"))
    model_span = {m: silhouette(m) for m in models}
    out, via = {}, {"model": 0, "family": 0, "category": 0}
    for a in fleet:
        sid = a["id"] if a["id"] in model_span else None
        if sid:
            via["model"] += 1
        else:
            for pat, target in FAMILY:
                if re.search(pat, a["name"], re.I) and target in model_span:
                    sid = target
                    via["family"] += 1
                    break
        if not sid:
            sid = CATEGORY.get(a["category"]["zh"], "a320")
            via["category"] += 1
        out[a["id"]] = {"s": sid, "span": span_of(a) or round(model_span.get(sid, 30), 1)}
    (ROOT / "data/silhouettes.json").write_text(json.dumps(out, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    total = sum(p.stat().st_size for p in OUT.glob("*.png"))
    print(f"{len(models)} silhouettes ({total / 1024:.0f} KB), {len(out)} aircraft mapped: {via}")


if __name__ == "__main__":
    main()
