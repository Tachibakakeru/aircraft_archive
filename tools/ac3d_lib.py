"""
AC3D（.ac）格式解析與量化壓縮共用工具，供 convert_ac3d_*.py 系列腳本使用。

FlightGear FGAddon 機模皆為此格式；同一機型常見同名物件重複出現
（依材質或 LOD 分割成多個同名子網格），故解析結果為 list 而非 dict，
避免同名物件互相覆蓋掉遺失幾何。
"""
import base64
import numpy as np

def parse_ac3d(path):
    """遞迴解析 AC3D 物件樹（world/group/poly，"kids N" 標記子物件數量），
    沿祖先鏈累加 loc 偏移後攤平回傳 list[dict]：
    {"name", "loc":(x,y,z)（已含祖先累加）, "verts":Nx4, "tris":Mx3 index}。
    僅支援平移（loc），不支援旋轉矩陣（"rot"）——目前處理過的 FGAddon 機模皆未使用。
    允許同名物件重複出現，呼叫端自行以 name 分類再合併。"""
    # 濾掉空白行：少數來源檔案（如 727-230.ac）行尾字元異常，每行內容後都夾帶
    # 一個空白行，會讓位置式掃描（numvert/refs 行數對應）整批錯位。
    lines = [l for l in open(path, encoding="utf-8", errors="replace").read().split("\n") if l.strip()]
    idx = [0]

    def parse_one(parent_loc):
        idx[0] += 1  # 消耗 "OBJECT <type>" 本行
        name, loc = None, (0.0, 0.0, 0.0)
        verts, tris, kids = None, [], 0
        while idx[0] < len(lines):
            l = lines[idx[0]]
            if l.startswith("name"):
                name = l.split('"')[1]; idx[0] += 1
            elif l.startswith("loc"):
                loc = tuple(map(float, l.split()[1:4])); idx[0] += 1
            elif l.startswith("data"):
                idx[0] += 2   # "data N" 本行 + 接下來一行字串本體
            elif l.startswith("numvert"):
                n = int(l.split()[1])
                rows = [list(map(float, lines[idx[0]+1+k].split())) for k in range(n)]
                # 少數來源檔案有單行頂點資料損毀（欄位數不為 3），
                # 該物件幾何不可信，以空陣列處理並略過，不中斷整批解析。
                if all(len(r) == 3 for r in rows):
                    verts = np.array(rows)
                else:
                    verts = np.zeros((0, 3))
                idx[0] += 1 + n
            elif l.startswith("numsurf"):
                n = int(l.split()[1])
                idx[0] += 1
                for _ in range(n):
                    while not lines[idx[0]].startswith("refs"):
                        idx[0] += 1
                    refs = int(lines[idx[0]].split()[1])
                    ridx = [int(lines[idx[0]+1+r].split()[0]) for r in range(refs)]
                    for r in range(1, refs-1):   # 扇形三角化（支援 >3 邊面）
                        tris.append((ridx[0], ridx[r], ridx[r+1]))
                    idx[0] += 1 + refs
            elif l.startswith("kids"):
                kids = int(l.split()[1]); idx[0] += 1
                break   # "kids N" 是該物件屬性區塊的結尾，後面緊接 N 個子物件
            else:
                idx[0] += 1

        world_loc = (parent_loc[0]+loc[0], parent_loc[1]+loc[1], parent_loc[2]+loc[2])
        leaves = []
        if verts is not None and len(verts) > 0:
            leaves.append({"name": name, "loc": world_loc, "verts": verts,
                            "tris": np.array(tris, dtype=np.int64) if tris else np.zeros((0,3), dtype=np.int64)})
        for _ in range(kids):
            leaves.extend(parse_one(world_loc))
        return leaves

    return parse_one((0.0, 0.0, 0.0))

def object_tris(obj):
    """回傳該物件的三角形頂點陣列（已加 loc 偏移，未做座標系轉換）Nx3x3"""
    v = obj["verts"][:, :3] + np.array(obj["loc"])
    t = obj["tris"]
    if len(t) == 0:
        return np.zeros((0, 3, 3))
    return v[t]

def weld_and_quantize(pos, idx):
    """頂點去重＋位置量化為 uint16（沿用 convert_fr24.py 的壓縮邏輯）"""
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

def b64(a):
    return base64.b64encode(np.ascontiguousarray(a).tobytes()).decode()

COLORS = {"fuselage":(1,1,1,1), "cockpit":(0.05,0.07,0.10,1),
          "wing":(0.72,0.73,0.75,1), "engine":(0.55,0.56,0.58,1),
          "vstab":(1,1,1,1), "hstab":(0.72,0.73,0.75,1), "gear":(0.12,0.12,0.13,1)}

def classify_and_bake(objects, part_map, dst, model_id, source_note,
                       nose_negative_x=True, unmapped_report=True):
    """依 part_map（name→partId）分類、烘焙座標（機鼻+X、地面y=0、長12單位）、
    量化輸出為 v2 格式 JSON。objects 可額外混入其他來源檔案（如外掛引擎/輪組）
    展開後的物件 list，一併傳入即可。"""
    import json

    part_tris = {pid: [] for pid in set(part_map.values())}
    unmapped = []
    for obj in objects:
        pid = part_map.get(obj["name"])
        if pid is None:
            unmapped.append(obj["name"])
            continue
        tris = object_tris(obj)
        if len(tris):
            part_tris.setdefault(pid, []).append(tris.reshape(-1, 3))
    if unmapped_report and unmapped:
        print("未分類物件（略過）：", sorted(set(unmapped)))

    def to_world(pts):
        x = -pts[:, 0] if nose_negative_x else pts[:, 0]
        return np.stack([x, pts[:, 1], pts[:, 2]], axis=1)

    nonempty = {k: v for k, v in part_tris.items() if v}
    all_pts = np.vstack([to_world(np.vstack(v)) for v in nonempty.values()])
    mn, mx = all_pts.min(0), all_pts.max(0)
    cx, cz = (mn[0]+mx[0])/2, (mn[2]+mx[2])/2
    scale = 12.0 / (mx[0] - mn[0])

    def bake(tri_list):
        pts = to_world(np.vstack(tri_list))
        pts[:, 0] -= cx; pts[:, 1] -= mn[1]; pts[:, 2] -= cz
        pts = (pts * scale).astype(np.float32)
        pts = pts.reshape(-1, 3, 3)
        if nose_negative_x:
            pts = pts[:, [0, 2, 1], :]   # X 取負造成鏡像，交換兩點修正法線
        return pts.reshape(-1, 3)

    out_parts, anchors = {}, {}
    for pid, tri_list in nonempty.items():
        pos = bake(tri_list)
        idx = np.arange(len(pos), dtype=np.uint32)
        qpos, qo, qs, new_idx, nv = weld_and_quantize(pos, idx)
        iw = 4 if nv > 65535 else 2
        idx_arr = new_idx.astype(np.uint32 if iw == 4 else np.uint16)
        entry = {"q": b64(qpos), "qo":[round(float(x),4) for x in qo],
                 "qs":[round(float(x),8) for x in qs],
                 "i": b64(idx_arr), "iw": iw, "c": list(COLORS.get(pid,(0.7,0.7,0.7,1))), "t": 0}
        out_parts[pid] = [entry]
        bmn, bmx = pos.min(0), pos.max(0)
        c = (bmn+bmx)/2
        anchors[pid] = [round(float(c[0]),2), round(float(bmx[1]),2), round(float((c[2]+bmx[2])/2),2)]
        print(f"  {pid:10s} 頂點={nv}")

    result = {"meta": {"source": source_note, "model": model_id, "format": 2},
              "texture": None, "parts": out_parts, "anchors": anchors}
    with open(dst, "w") as f:
        json.dump(result, f, separators=(",", ":"))
    kb = len(json.dumps(result, separators=(",", ":"))) // 1024
    print(f"輸出 {dst} ({kb} KB)")
