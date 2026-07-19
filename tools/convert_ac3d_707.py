#!/usr/bin/env python3
"""
FlightGear FGAddon Boeing 707 (AC3D 格式) → models/b707.json（v2 壓縮格式）

來源：FlightGear FGAddon「Lake of Constance Hangar」707（Copyright M.Kraus，
GPLv3），比照 convert_fr24.py 的輸出格式手寫的 AC3D 解析器＋分類器（AC3D
是純文字格式，欄位語意與 glTF 1.0 完全不同，無法沿用原解析器）。

用法：python3 convert_ac3d_707.py <707.ac 所在資料夾> models/b707.json
資料夾需包含：707.ac、PWJT4.ac（引擎，四具實例位置寫死於本檔，取自 707.xml）

座標系（原始 AC3D，經驗證）：X 前後（機頭在負值）、Y 垂直向上、Z 左右展向。
烘焙後輸出座標系（專案慣例）：機鼻 +X、地面 y=0、機長縮放至 12 單位。
"""
import sys, os, re, json, base64
import numpy as np

# ── AC3D 解析器 ──────────────────────────────────────────────
def parse_ac3d(path):
    """回傳 dict: name -> {"loc":(x,y,z), "verts":Nx3 array, "tris":Mx3 index array}"""
    lines = open(path, encoding="utf-8", errors="replace").read().split("\n")
    objects = {}
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.startswith("OBJECT"):
            name, loc = None, (0.0, 0.0, 0.0)
            verts, tris = None, []
            j = i + 1
            while j < len(lines):
                l = lines[j]
                if l.startswith("name"):
                    name = l.split('"')[1]
                elif l.startswith("loc"):
                    loc = tuple(map(float, l.split()[1:4]))
                elif l.startswith("data"):
                    n = int(l.split()[1])
                    j += 1  # 跳過接下來的 data 字串本體（單行）
                elif l.startswith("numvert"):
                    n = int(l.split()[1])
                    verts = np.array([list(map(float, lines[j+1+k].split()))
                                       for k in range(n)])
                    j += n
                elif l.startswith("numsurf"):
                    n = int(l.split()[1])
                    k = j + 1
                    for _ in range(n):
                        while not lines[k].startswith("refs"):
                            k += 1
                        refs = int(lines[k].split()[1])
                        idx = [int(lines[k+1+r].split()[0]) for r in range(refs)]
                        # 扇形三角化（refs 通常已是 3，保險起見支援多邊形面）
                        for r in range(1, refs-1):
                            tris.append((idx[0], idx[r], idx[r+1]))
                        k += 1 + refs
                    j = k - 1
                elif l.startswith("OBJECT") and j > i:
                    break
                elif l.startswith("kids") and name is not None and verts is not None:
                    break
                j += 1
            if name and verts is not None:
                objects[name] = {"loc": loc, "verts": verts,
                                  "tris": np.array(tris, dtype=np.int64) if tris else np.zeros((0,3), dtype=np.int64)}
            i = j
        else:
            i += 1
    return objects

def object_tris(obj):
    """回傳該物件的三角形頂點陣列（已加 loc 偏移，未做座標系轉換）Nx3x3"""
    v = obj["verts"][:, :3] + np.array(obj["loc"])
    t = obj["tris"]
    if len(t) == 0:
        return np.zeros((0, 3, 3))
    return v[t]

# ── 部位分類（依 707.ac 實際物件命名）──────────────────────────
PART_MAP = {
    # 機身本體
    "fuselage": "fuselage", "fuselage.inner": "fuselage", "fuselage.belly": "fuselage",
    "nose": "fuselage", "nosewheelwell": "fuselage", "nonones": "fuselage",
    "antenaasa": "fuselage", "lampFrame": "fuselage", "probe": "fuselage",
    "doorFL": "fuselage", "doorRL": "fuselage", "doorCargo": "fuselage", "doorBelly": "fuselage",
    "lhdoorouter": "fuselage", "lhdoorinner": "fuselage",
    "rhdoorouter": "fuselage", "rhdoorinner": "fuselage",
    # 主翼（含副翼／襟翼／縫翼，靜態合併——專案動畫 surfaces 機制留待後續擴充）
    "wing": "wing",
    "rhobail": "wing", "rhibail": "wing", "lhobail": "wing", "lhibail": "wing",
    "rhobflap": "wing", "rhibflap": "wing", "lhobflap": "wing", "lhibflap": "wing",
    "rhfiletflap": "wing", "lhfiletflap": "wing",
    "slatsL": "wing", "slatsR": "wing",
    "engineSupport": "wing",  # 派龍支架，幾何上屬翼下掛架
    # 垂直尾翼
    "vertstab": "vstab", "rudder": "vstab",
    # 水平尾翼
    "rhsp1": "hstab", "rhsp3": "hstab", "lhsp1": "hstab", "lhsp3": "hstab",
    "rhelevator": "hstab", "lhelevator": "hstab", "elevwing": "hstab",
    # 起落架
    "LeftGear": "gear", "LeftGear.001": "gear", "LeftGearCompressor": "gear", "LeftGearCompressor1": "gear",
    "RightGear": "gear", "RightGear.001": "gear", "RightGearCompressor": "gear", "RightGearCompressor1": "gear",
    "NGear": "gear", "NGearStrut": "gear", "NoseWheel": "gear",
    "mgdoora": "gear", "mgdoorb": "gear", "mgdoorc": "gear",
    "rhmgdoora": "gear", "rhmgdoorb": "gear", "rhmgdoorc": "gear",
    "rhngdoor": "gear", "rhngdooraft": "gear", "lhngdoor": "gear", "lhngdooraft": "gear",
}

# 707.xml 讀出的引擎（Pratt & Whitney JT4）掛載座標，FG 座標系 x=前後 y=左右 z=垂直，
# 與 707.ac 內部 AC3D 座標系（x=前後 y=垂直 z=左右）軸序不同，需對應轉換：
# ac3d_x = fg_x, ac3d_y = fg_z, ac3d_z = fg_y
ENGINE_OFFSETS_FG = [
    ( 2.47, -14.835, -0.73),
    (-1.18, -10.077, -1.18),
    (-1.18,  10.077, -1.18),
    ( 2.47,  14.835, -0.73),
]

# 主起落架輪組（wheels.ac，707.ac 內的 LeftGear/RightGear 只是支柱，輪胎是外掛模型）
# 取自 707.xml 的 RightGearBase／LeftGearBase 掛載座標
GEAR_WHEEL_OFFSETS_FG = [
    ( 1.82,  2.76, -2.30),
    ( 1.82, -2.76, -2.30),
]

def convert(src_dir, dst):
    fuse_objs = parse_ac3d(os.path.join(src_dir, "707.ac"))
    eng_objs = parse_ac3d(os.path.join(src_dir, "PWJT4.ac"))
    wheel_objs = parse_ac3d(os.path.join(src_dir, "wheels.ac"))

    part_tris = {"fuselage": [], "wing": [], "engine": [], "vstab": [], "hstab": [], "gear": []}

    unmapped = []
    for name, obj in fuse_objs.items():
        if name in ("world", "Blender_export__707.ac"):
            continue
        pid = PART_MAP.get(name)
        if pid is None:
            unmapped.append(name)
            continue
        tris = object_tris(obj)
        if len(tris):
            part_tris[pid].append(tris.reshape(-1, 3))
    if unmapped:
        print("未分類物件（略過）：", unmapped)

    # 引擎：合併 PWJT4.ac 全部子物件為一顆引擎幾何，實例化 4 次到各掛載點
    eng_all = []
    for name, obj in eng_objs.items():
        if name == "world":
            continue
        tris = object_tris(obj)
        if len(tris):
            eng_all.append(tris.reshape(-1, 3))
    eng_geo = np.vstack(eng_all) if eng_all else np.zeros((0, 3))
    for fx, fy, fz in ENGINE_OFFSETS_FG:
        ax, ay, az = fx, fz, fy  # FG(x,y,z) → AC3D(x,y,z) 軸對應
        part_tris["engine"].append(eng_geo + np.array([ax, ay, az]))

    # 主起落架輪組：wheels.ac 合併全部子物件，實例化到左右兩個掛載點
    wheel_all = []
    for name, obj in wheel_objs.items():
        if name == "world":
            continue
        tris = object_tris(obj)
        if len(tris):
            wheel_all.append(tris.reshape(-1, 3))
    wheel_geo = np.vstack(wheel_all) if wheel_all else np.zeros((0, 3))
    for fx, fy, fz in GEAR_WHEEL_OFFSETS_FG:
        ax, ay, az = fx, fz, fy  # FG(x,y,z) → AC3D(x,y,z) 軸對應
        part_tris["gear"].append(wheel_geo + np.array([ax, ay, az]))

    # ── 座標系轉換＋烘焙：AC3D(x前後 y垂直 z展向，機頭-X) → 專案慣例(機鼻+X 地面y=0 長12) ──
    def to_world(pts):
        x = -pts[:, 0]   # 機頭轉為 +X
        y = pts[:, 1]
        z = pts[:, 2]
        return np.stack([x, y, z], axis=1)

    all_pts = np.vstack([to_world(np.vstack(v)) for v in part_tris.values() if v])
    mn, mx = all_pts.min(0), all_pts.max(0)
    cx = (mn[0] + mx[0]) / 2
    cz = (mn[2] + mx[2]) / 2
    scale = 12.0 / (mx[0] - mn[0])

    def bake(tri_list):
        pts = to_world(np.vstack(tri_list))
        pts[:, 0] -= cx
        pts[:, 1] -= mn[1]
        pts[:, 2] -= cz
        pts = (pts * scale).astype(np.float32)
        # X 取負造成鏡像，三角形環繞方向需交換兩點以修正法線朝向
        pts = pts.reshape(-1, 3, 3)
        pts = pts[:, [0, 2, 1], :]
        return pts.reshape(-1, 3)

    # ── 量化壓縮（沿用 convert_fr24.py 邏輯）──
    def weld_and_quantize(pos, idx):
        key_pos = np.round(pos, 4)
        uniq, inverse = np.unique(key_pos, axis=0, return_inverse=True)
        inverse = np.asarray(inverse).ravel().astype(np.uint32)
        nverts = len(uniq)
        welded_pos = np.zeros((nverts, 3), np.float32)
        welded_pos[inverse] = pos
        new_idx = inverse[idx]
        vmin = welded_pos.min(0)
        vrange = welded_pos.max(0) - vmin
        vrange[vrange < 1e-6] = 1e-6
        qpos = np.round((welded_pos - vmin) / vrange * 65535).astype(np.uint16)
        return qpos, vmin, vrange/65535.0, new_idx, nverts

    b64 = lambda a: base64.b64encode(np.ascontiguousarray(a).tobytes()).decode()

    COLORS = {"fuselage":(1,1,1,1), "wing":(0.72,0.73,0.75,1), "engine":(0.55,0.56,0.58,1),
              "vstab":(1,1,1,1), "hstab":(0.72,0.73,0.75,1), "gear":(0.12,0.12,0.13,1)}

    out_parts, anchors = {}, {}
    for pid, tri_list in part_tris.items():
        if not tri_list:
            continue
        pos = bake(tri_list)
        idx = np.arange(len(pos), dtype=np.uint32)
        qpos, qo, qs, new_idx, nv = weld_and_quantize(pos, idx)
        iw = 4 if nv > 65535 else 2
        idx_arr = new_idx.astype(np.uint32 if iw == 4 else np.uint16)
        entry = {"q": b64(qpos), "qo":[round(float(x),4) for x in qo],
                 "qs":[round(float(x),8) for x in qs],
                 "i": b64(idx_arr), "iw": iw, "c": list(COLORS[pid]), "t": 0}
        out_parts[pid] = [entry]
        bmn, bmx = pos.min(0), pos.max(0)
        c = (bmn+bmx)/2
        anchors[pid] = [round(float(c[0]),2), round(float(bmx[1]),2), round(float((c[2]+bmx[2])/2),2)]
        print(f"  {pid:10s} 頂點={nv}")

    result = {"meta": {"source": "FlightGear FGAddon 「Lake of Constance Hangar」 Boeing 707"
                                  "（Copyright M.Kraus，GPLv3）AC3D 模型轉換，未含貼圖（原始貼圖檔另行處理）",
                        "model": "b707", "format": 2},
              "texture": None, "parts": out_parts, "anchors": anchors}
    with open(dst, "w") as f:
        json.dump(result, f, separators=(",", ":"))
    kb = len(json.dumps(result, separators=(",", ":"))) // 1024
    print(f"輸出 {dst} ({kb} KB)")

if __name__ == "__main__":
    convert(sys.argv[1], sys.argv[2])
