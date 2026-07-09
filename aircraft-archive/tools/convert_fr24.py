#!/usr/bin/env python3
"""
fr24 glTF 1.0 (.glb) → 部位分類 JSON 轉換器
用法: python3 convert_fr24.py <input.glb> <output.json>

流程:
1. 解析 glTF 1.0 二進位格式（Three.js GLTFLoader 不支援 1.0，故離線轉換）
2. 走訪節點樹烘焙世界變換
3. 依「節點名稱 + 材質名稱 + 包圍盒幾何特徵」自動分類部位
4. 正規化座標（機鼻朝 +X、地面 y=0、機長縮放至 12 單位）
5. 輸出精簡 JSON（base64 幾何 + 內嵌貼圖）與三視圖驗證 PNG
"""
import struct, json, base64, sys, zlib
import numpy as np

CT = {5120:'b',5121:'B',5122:'h',5123:'H',5125:'I',5126:'f'}
NC = {"SCALAR":1,"VEC2":2,"VEC3":3,"VEC4":4,"MAT4":16}
COLORS = {"fuselage":(201,210,220),"cockpit":(80,160,255),"wing":(120,160,220),
          "engine":(255,120,80),"vstab":(255,181,71),"hstab":(120,220,160),
          "gear":(220,80,220)}

def load_gltf1(path):
    data = open(path,'rb').read()
    # 二進位 glb：以 magic "glTF" 開頭
    if data[:4] == b'glTF':
        magic, version, _, content_len, _ = struct.unpack("<4sIIII", data[:20])
        assert version == 1, f"僅支援 glTF 1.0，讀到 version={version}"
        j = json.loads(data[20:20+content_len])
        return j, data[20+content_len:]
    # 文字版 .gltf：buffer 以 data-URI 內嵌或外部 .bin
    j = json.loads(data.decode("utf-8"))
    assert j.get("asset",{}).get("version","1.0").startswith("1"), \
        f"僅支援 glTF 1.0，讀到 {j.get('asset',{}).get('version')}"
    # 取第一個 buffer 當主 body（fr24 模型皆單一 buffer）
    buf = list(j["buffers"].values())[0]
    uri = buf.get("uri","")
    if uri.startswith("data:"):
        body = base64.b64decode(uri.split(",",1)[1])
    else:   # 外部 .bin，與 gltf 同目錄
        import os
        body = open(os.path.join(os.path.dirname(path), uri),"rb").read()
    return j, body

def accessor(j, body, aid):
    a = j["accessors"][aid]
    bv = j["bufferViews"][a["bufferView"]]
    off = bv.get("byteOffset",0) + a.get("byteOffset",0)
    n = a["count"] * NC[a["type"]]
    arr = np.frombuffer(body, dtype=np.dtype(CT[a["componentType"]]), count=n, offset=off)
    arr = arr.reshape(a["count"], NC[a["type"]]) if NC[a["type"]] > 1 else arr
    return arr.astype(np.float32 if CT[a["componentType"]]=='f' else np.uint32)

def node_matrix(n):
    if "matrix" in n:
        return np.array(n["matrix"], dtype=np.float64).reshape(4,4).T  # column-major
    m = np.eye(4)
    if "translation" in n: m[:3,3] = n["translation"]
    return m

# ── 部位分類 ──────────────────────────────────────────────
# 第一層：節點名稱關鍵字（依序比對，先中先贏）
import re
NAME_RULES = [
    ("engine",  r"eng|fan|prop|pylon|revers|duct|nacell|nac|intake|nozzle|exhaust|tailpipe|shroud|casing|blade|cowl|core|spinner"),
    ("gear",    r"gear|wheel|tyre|tire|bogie|oleo|ww|mgd|ngd"),
    ("vstab",   r"vstab|rudder|vertical|dorsal"),
    ("hstab",   r"hstab|stab|elevator|horizontal|tailplane"),
    ("wing",    r"wing|slat|flap|spoiler|aileron|ible|oble|krueger"),
    ("cockpit", r"cockpit|windshield|windscreen|canopy"),
    ("fuselage",r"fuselage|window|door|dorr|exit|apu|cargo|antenna|beacon|radome|belly"),
]
GENERIC_NODE = re.compile(r"^(rootnode|node_\d+|scene|root|mesh_?\d*)$")

def name_part(node_name):
    """節點名稱可辨識時回傳部位，否則 None。"""
    n = node_name.lower()
    if GENERIC_NODE.match(n):
        return None
    for pid, pat in NAME_RULES:
        if re.search(pat, n):
            return pid
    return None

def classify(node_name, mat_name, bb_min, bb_max, dims, model_min, model_dims):
    """回傳 partId。座標系為模型原始座標（-Z 機鼻、+Y 上、X 翼展）。"""
    mat = mat_name.lower()
    SPAN, H, L = model_dims
    ground = model_min[1]
    z_front = bb_min[2] < -L*0.28
    z_aft   = bb_min[2] >  L*0.30
    lateral = max(abs(bb_min[0]), abs(bb_max[0]))      # 離中線最遠距離

    if "pylon" in mat:                                  return "engine"
    if "cockpitframe" in mat:                           return "cockpit"
    if "glass" in mat and z_front:                      return "cockpit"  # 風擋
    if "geardoor" in mat:                               return "gear"
    # 起落架：貼地起算 + 高度矮 + 貼近中線（排除翼尖小翼、腹部整流罩）
    if bb_min[1] < ground + H*0.15 and dims[1] < H*0.14 and lateral < SPAN*0.10:
        return "gear"
    # 引擎短艙（幾何推斷）：離中線但不在翼尖、體積似吊艙、位於機身中前段
    lat_c = abs(bb_min[0] + bb_max[0]) / 2
    if (SPAN*0.07 < lat_c < SPAN*0.42
        and L*0.02 < dims[2] < L*0.20
        and H*0.04 < dims[1] < H*0.30
        and dims[0] < SPAN*0.14
        and bb_min[2] < L*0.25):
        return "engine"
    if z_aft and bb_max[1] > ground + H*0.55 and dims[0] < SPAN*0.05:
        return "vstab"                                                    # 尾段/高/薄
    if z_aft and dims[0] > SPAN*0.12:                   return "hstab"
    if dims[0] > SPAN*0.5:                              return "wing"     # 大展幅
    if lateral > SPAN*0.10 and dims[1] < H*0.12:        return "wing"     # 翼面細件
    return "fuselage"

# ── 三視圖驗證輸出 ────────────────────────────────────────
def render_views(parts, prefix):
    W,H,S = 900,620,62
    def png_write(path, buf):
        def chunk(t, d):
            c = t+d
            return struct.pack(">I",len(d))+c+struct.pack(">I",zlib.crc32(c))
        raw = b"".join(b"\x00"+bytes(buf[y*W*3:(y+1)*W*3]) for y in range(H))
        open(path,"wb").write(b"\x89PNG\r\n\x1a\n"
            +chunk(b"IHDR",struct.pack(">IIBBBBB",W,H,8,2,0,0,0))
            +chunk(b"IDAT",zlib.compress(raw))+chunk(b"IEND",b""))
    views = {v:(bytearray(b"\x12"*(W*H*3)), np.full(W*H,-1e9,np.float32))
             for v in ("top","side","front")}
    def plot(view, sx, sy, depth, rgb):
        x,y = int(sx), int(sy)
        if 0<=x<W and 0<=y<H:
            buf, zb = views[view]; i=y*W+x
            if depth>=zb[i]:
                zb[i]=depth; buf[i*3:i*3+3]=bytes(rgb)
    for pid, entries in parts.items():
        rgb = COLORS.get(pid,(255,255,255))
        for e in entries:
            if "q" in e:   # v2 量化格式
                q = np.frombuffer(base64.b64decode(e["q"]),np.uint16).reshape(-1,3).astype(np.float32)
                pos = q * np.array(e["qs"],np.float32) + np.array(e["qo"],np.float32)
            else:          # v1 舊格式
                pos = np.frombuffer(base64.b64decode(e["p"]),np.float32).reshape(-1,3)
            idx = np.frombuffer(base64.b64decode(e["i"]),
                                np.uint32 if e["iw"]==4 else np.uint16)
            tri = pos[idx.astype(np.int64)].reshape(-1,3,3)
            area = np.linalg.norm(np.cross(tri[:,1]-tri[:,0],tri[:,2]-tri[:,0]),axis=1)/2
            for t,a in zip(tri,area):
                k = max(4,min(300,int(a*S*S*0.6)))
                u,v = np.random.rand(k),np.random.rand(k)
                f = u+v>1; u[f],v[f] = 1-u[f],1-v[f]
                pts = t[0]+np.outer(u,t[1]-t[0])+np.outer(v,t[2]-t[0])
                for p in pts:
                    plot("top",  W/2+p[0]*S, H/2+p[2]*S, p[1], rgb)
                    plot("side", W/2+p[0]*S, H/2+40-p[1]*S, p[2], rgb)
                    plot("front",W/2-p[2]*S, H/2+40-p[1]*S, p[0], rgb)
    for v,(buf,_) in views.items():
        png_write(f"{prefix}_{v}.png", buf)
    print("驗證圖:", ", ".join(f"{prefix}_{v}.png" for v in views))

# ── 貼圖重新編碼（縮解析度 + JPEG 壓縮）──
def recompress_texture(raw, mime, max_dim=1024, quality=80):
    try:
        from PIL import Image
        import io
        im = Image.open(io.BytesIO(raw))
        if im.mode not in ("RGB", "L"):
            im = im.convert("RGB")
        w, h = im.size
        if max(w, h) > max_dim:
            s = max_dim / max(w, h)
            im = im.resize((round(w*s), round(h*s)), Image.LANCZOS)
        buf = io.BytesIO()
        im.save(buf, format="JPEG", quality=quality, optimize=True)
        out = buf.getvalue()
        # 若重編碼後反而更大（原圖已高度壓縮），保留原圖
        if len(out) >= len(raw):
            return f"data:{mime};base64," + base64.b64encode(raw).decode()
        return "data:image/jpeg;base64," + base64.b64encode(out).decode()
    except Exception:
        return f"data:{mime};base64," + base64.b64encode(raw).decode()

# ── 主流程 ────────────────────────────────────────────────
def convert(src, dst):
    j, body = load_gltf1(src)

    texture_uri = None
    for img in j.get("images", {}).values():
        ext = img.get("extensions", {}).get("KHR_binary_glTF")
        if ext:   # glb：圖片存在 bufferView
            bv = j["bufferViews"][ext["bufferView"]]
            raw = body[bv.get("byteOffset",0): bv.get("byteOffset",0)+bv["byteLength"]]
            texture_uri = recompress_texture(raw, ext.get("mimeType","image/jpeg"))
            break
        uri = img.get("uri","")
        if uri.startswith("data:"):   # 文字 gltf：圖片為 data-URI
            mime = uri.split(";",1)[0].split(":",1)[1]
            raw = base64.b64decode(uri.split(",",1)[1])
            texture_uri = recompress_texture(raw, mime)
            break

    def mat_info(mid):
        v = j["materials"].get(mid, {}).get("values", {})
        d = v.get("diffuse", [0.8,0.8,0.8,1])
        if isinstance(d, str):
            return {"tex":1, "color":[1,1,1,1]}
        alpha = d[3] if len(d)>3 else 1
        if "glass" in mid.lower(): alpha = min(alpha, 0.45)
        return {"tex":0, "color":[d[0],d[1],d[2],alpha]}

    prims = []
    def walk(nid, parent_m, inherited):
        n = j["nodes"][nid]
        m = parent_m @ node_matrix(n)
        # 自身名稱優先，其次繼承父節點的名稱分類
        own = name_part(nid)
        part_hint = own or inherited
        for mid in n.get("meshes", []):
            for p in j["meshes"][mid]["primitives"]:
                if p.get("mode", 4) != 4:   # 只取 TRIANGLES
                    continue
                pos = accessor(j, body, p["attributes"]["POSITION"]).astype(np.float64)
                pos_w = (m[:3,:3] @ pos.T).T + m[:3,3]
                uv = accessor(j, body, p["attributes"]["TEXCOORD_0"]) \
                     if "TEXCOORD_0" in p["attributes"] else None
                prims.append({"node":nid, "hint":part_hint, "mat":p["material"],
                              "pos":pos_w, "uv":uv,
                              "idx":accessor(j, body, p["indices"]).ravel()})
        for c in n.get("children", []):
            walk(c, m, part_hint)
    for root in j["scenes"][j["scene"]]["nodes"]:
        walk(root, np.eye(4), None)

    all_pos = np.vstack([p["pos"] for p in prims])
    mn, mx = all_pos.min(0), all_pos.max(0)
    dims_model = mx - mn
    print(f"原始包圍盒 min={mn.round(2)} max={mx.round(2)} 尺寸={dims_model.round(2)}")

    part_prims = {}
    for p in prims:
        pmn, pmx = p["pos"].min(0), p["pos"].max(0)
        pid = p["hint"] or classify(p["node"], p["mat"], pmn, pmx,
                                    pmx-pmn, mn, dims_model)
        part_prims.setdefault(pid, []).append(p)

    cx, cz = (mn[0]+mx[0])/2, (mn[2]+mx[2])/2
    scale = 12.0 / dims_model[2]
    def bake(pos):
        p = pos.copy()
        p[:,0] -= cx; p[:,1] -= mn[1]; p[:,2] -= cz
        x, z = -p[:,2].copy(), p[:,0].copy()   # 繞 Y 軸 -90°：機鼻 -Z → +X
        p[:,0], p[:,2] = x, z
        return (p * scale).astype(np.float32)

    # ── 壓縮寫出 ──
    # 格式 v2：每部位所有 primitive 依材質合併 → 頂點去重 → 位置量化為 uint16
    #  q  : 量化後的位置 (uint16, 3/頂點) base64
    #  qo : 反量化偏移 [x,y,z]（float）
    #  qs : 反量化尺度 [x,y,z]（float，= 範圍/65535）
    #  i  : 索引 base64；iw: 索引位元組寬度
    #  c  : 顏色 [r,g,b,a]；t: 是否用貼圖
    #  u  : UV (uint16 量化，0..1 → 0..65535) base64（僅貼圖件）
    b64 = lambda a: base64.b64encode(np.ascontiguousarray(a).tobytes()).decode()

    def weld_and_quantize(pos, idx, uv):
        """頂點去重（位置+UV 一併雜湊）後量化位置為 uint16。"""
        key_pos = np.round(pos, 4)
        if uv is not None:
            keys = np.concatenate([key_pos, np.round(uv, 4)], axis=1)
        else:
            keys = key_pos
        # NumPy 2.0 起 return_inverse 可能回傳 (N,1)，用 ravel 保證 1 維
        uniq, inverse = np.unique(keys, axis=0, return_inverse=True)
        inverse = np.asarray(inverse).ravel().astype(np.uint32)
        nverts = len(uniq)

        # 重建去重後的頂點屬性（同鍵值屬性一致，直接散佈賦值）
        welded_pos = np.zeros((nverts, 3), np.float32)
        welded_pos[inverse] = pos
        welded_uv = None
        if uv is not None:
            welded_uv = np.zeros((nverts, 2), np.float32)
            welded_uv[inverse] = uv

        new_idx = inverse[idx]      # 原三角形索引 → 去重後索引

        # 位置量化為 uint16
        vmin = welded_pos.min(0)
        vrange = welded_pos.max(0) - vmin
        vrange[vrange < 1e-6] = 1e-6
        qpos = np.round((welded_pos - vmin) / vrange * 65535).astype(np.uint16)
        return qpos, vmin, vrange/65535.0, welded_uv, new_idx, nverts

    out_parts, anchors, stats = {}, {}, {}
    tot_before = tot_after = 0
    for pid, plist in part_prims.items():
        # 依「材質顏色 + 是否貼圖」分組合併
        groups = {}
        for p in plist:
            mi = mat_info(p["mat"])
            gk = (tuple(round(c,3) for c in mi["color"]), mi["tex"])
            groups.setdefault(gk, {"pos":[], "uv":[], "idx":[], "off":0})
            g = groups[gk]
            g["idx"].append(p["idx"] + g["off"])
            g["pos"].append(bake(p["pos"]))
            g["off"] += len(p["pos"])
            if p["uv"] is not None and mi["tex"]:
                g["uv"].append(p["uv"].astype(np.float32))
            else:
                g["uv"].append(np.zeros((len(p["pos"]),2), np.float32))

        entries, bmn, bmx, vtot = [], None, None, 0
        for (color, tex), g in groups.items():
            pos = np.vstack(g["pos"])
            uv  = np.vstack(g["uv"]) if tex else None
            idx = np.concatenate(g["idx"])
            tot_before += len(pos)

            qpos, qo, qs, welded_uv, new_idx, nv = weld_and_quantize(pos, idx, uv)
            tot_after += nv
            vtot += nv
            # 反量化後的實際包圍盒（供錨點/地面用原始 pos 即可）
            bmn = pos.min(0) if bmn is None else np.minimum(bmn, pos.min(0))
            bmx = pos.max(0) if bmx is None else np.maximum(bmx, pos.max(0))

            iw = 4 if nv > 65535 else 2
            idx_arr = new_idx.astype(np.uint32 if iw==4 else np.uint16)
            e = {"q": b64(qpos),
                 "qo": [round(float(x),4) for x in qo],
                 "qs": [round(float(x),8) for x in qs],
                 "i": b64(idx_arr), "iw": iw,
                 "c": list(color), "t": tex}
            if tex and welded_uv is not None:
                quv = np.round(np.clip(welded_uv,0,1) * 65535).astype(np.uint16)
                e["u"] = b64(quv)
            entries.append(e)
        out_parts[pid] = entries
        c = (bmn+bmx)/2
        anchors[pid] = [round(float(c[0]),2), round(float(bmx[1]),2),
                        round(float((c[2]+bmx[2])/2),2)]
        stats[pid] = (len(entries), vtot)

    result = {"meta":{"source":"Flightradar24/fr24-3d-models (GPL-2.0)",
                      "model": src.split("/")[-1], "format": 2},
              "texture": texture_uri, "parts": out_parts, "anchors": anchors}
    with open(dst, "w") as f:
        json.dump(result, f, separators=(",",":"))
    kb = len(json.dumps(result, separators=(',',':')))//1024
    dedup = 100*(1 - tot_after/max(tot_before,1))
    print(f"輸出 {dst}  ({kb} KB)  頂點去重 {tot_before}→{tot_after} (-{dedup:.0f}%)")
    for pid,(np_,nv) in sorted(stats.items()):
        print(f"  {pid:10s} groups={np_:3d} 頂點={nv}")
    if "--views" in sys.argv:
        render_views(out_parts, dst.replace(".json",""))

if __name__ == "__main__":
    convert(sys.argv[1], sys.argv[2])
