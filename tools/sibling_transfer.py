"""
同機族操縱面「借用」轉換器 —— 專供 737NG 家族（b736/b737/b739 借 b738）。

b738 的來源 .glb 節點命名完整（flap1/slat1/spoiler1...），已能正確
自動分件；b736/b737/b739 的來源檔案幾何雖然一樣拆成上百個獨立
primitive，但全部掛在同一個匿名 rootNode 下，沒有任何名稱可用。

因為同家族機翼設計共用，把每個 primitive 的重心座標，除以該機型
自己的（翼展, 機高, 機長）做正規化，兩個機型的機翼結構應落在幾乎
相同的相對位置。對「目標機型」每個 primitive，在「參考機型
（b738）」裡找正規化座標最近的 primitive；如果那個參考 primitive
被分類為 flap/slat/spoiler/aileron，就把同樣的分類「借」過來，
再用目標機型自己的實際幾何重新估一次鉸鏈（不是照搬 b738 的數字）。

用法：python sibling_transfer.py <ref.glb> <target.glb> <out.json>

注意：這是「盡力而為」的推測式做法，不是精確重建。門檻（THRESH）
與正規化方式是針對 737NG 家族手動調校過的參考值，套用到其他機族
前務必重新用 collect_prims()/classify_prims() 診斷距離分布，並在
瀏覽器裡實際展開檢查有沒有穿模、浮空等異常，再決定要不要採用。
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import convert_fr24 as c
import numpy as np

def collect_prims(src):
    j, body = c.load_gltf1(src)

    prims = []
    def walk(nid, parent_m, inherited):
        n = j["nodes"][nid]
        m = parent_m @ c.node_matrix(n)
        own = c.name_part(nid)
        part_hint = own or inherited
        for mid in n.get("meshes", []):
            for p in j["meshes"][mid]["primitives"]:
                if p.get("mode", 4) != 4:
                    continue
                pos = c.accessor(j, body, p["attributes"]["POSITION"]).astype(np.float64)
                pos_w = (m[:3,:3] @ pos.T).T + m[:3,3]
                uv = c.accessor(j, body, p["attributes"]["TEXCOORD_0"]) \
                     if "TEXCOORD_0" in p["attributes"] else None
                prims.append({"node": nid, "hint": part_hint, "mat": p["material"],
                              "pos": pos_w, "uv": uv,
                              "idx": c.accessor(j, body, p["indices"]).ravel()})
        for ch in n.get("children", []):
            walk(ch, m, part_hint)
    for root in j["scenes"][j["scene"]]["nodes"]:
        walk(root, np.eye(4), None)

    all_pos = np.vstack([p["pos"] for p in prims])
    mn, mx = all_pos.min(0), all_pos.max(0)
    dims = mx - mn
    return prims, mn, mx, dims

def classify_prims(prims, mn, mx, dims):
    """幫每個 primitive 決定 type（跟 convert() 內的邏輯一致）。
    正規化用單一比例尺（翼展）而非各軸分別除以自己的（翼展,機高,機長），
    因為同家族機長不同、但機翼共用設計，用機長分別正規化 Z 軸
    反而會讓短機身機型（如 b736）的機翼相對位置被拉偏。"""
    center = (mn + mx) / 2
    span = dims[0] if dims[0] > 1e-6 else 1.0
    for p in prims:
        pmn, pmx = p["pos"].min(0), p["pos"].max(0)
        p["type"] = p["hint"] or c.classify(p["node"], p["mat"], pmn, pmx, pmx-pmn, mn, dims)
        p["centroid_norm"] = ((pmn+pmx)/2 - center) / span

def transfer(ref_src, target_src, dst):
    ref_prims, ref_mn, ref_mx, ref_dims = collect_prims(ref_src)
    classify_prims(ref_prims, ref_mn, ref_mx, ref_dims)
    ref_animatable = [p for p in ref_prims if p["type"] in c.ANIMATABLE]
    print(f"參考機型：{len(ref_prims)} primitives，其中 {len(ref_animatable)} 個已分類為可動操縱面")

    tgt_prims, tgt_mn, tgt_mx, tgt_dims = collect_prims(target_src)
    classify_prims(tgt_prims, tgt_mn, tgt_mx, tgt_dims)

    ref_centroids = np.vstack([p["centroid_norm"] for p in ref_animatable])
    ref_types = [p["type"] for p in ref_animatable]
    ref_nodes = [p["node"] for p in ref_animatable]

    THRESH = 0.045   # 正規化座標距離門檻（依翼展等比例），超過視為無對應
    borrowed = 0
    for p in tgt_prims:
        if p["type"] in c.ANIMATABLE:
            continue   # 目標本來就有名稱資訊，不覆蓋
        if p["type"] != "wing":
            continue   # 只在「原本會被歸為機翼」的 primitive 裡找可動面，避免誤傷機身/引擎等
        d = np.linalg.norm(ref_centroids - p["centroid_norm"], axis=1)
        i = int(np.argmin(d))
        if d[i] < THRESH:
            p["type"] = ref_types[i]
            p["hint"] = ref_types[i]
            p["_borrowed_from"] = ref_nodes[i]
            borrowed += 1
    print(f"目標機型：從參考機型借用了 {borrowed} 個 primitive 的操縱面分類")

    # ── 沿用 convert() 的後半段（encode_plist / compute_hinge / weld_and_quantize）──
    # 直接重新呼叫 convert_fr24.convert() 會重新跑一次分類（用不到我們借來的 hint），
    # 所以在這裡複製一份簡化版輸出邏輯，只處理我們關心的 ANIMATABLE 部分＋沿用
    # 原始 classify() 結果的其餘部位。
    j, body = c.load_gltf1(target_src)
    texture_uri = None
    for img in j.get("images", {}).values():
        ext = img.get("extensions", {}).get("KHR_binary_glTF")
        if ext:
            bv = j["bufferViews"][ext["bufferView"]]
            raw = body[bv.get("byteOffset",0): bv.get("byteOffset",0)+bv["byteLength"]]
            texture_uri = c.recompress_texture(raw, ext.get("mimeType","image/jpeg"))
            break

    def mat_info(mid):
        v = j["materials"].get(mid, {}).get("values", {})
        d = v.get("diffuse", [0.8,0.8,0.8,1])
        if isinstance(d, str):
            return {"tex":1, "color":[1,1,1,1]}
        alpha = d[3] if len(d)>3 else 1
        if "glass" in mid.lower(): alpha = min(alpha, 0.45)
        return {"tex":0, "color":[d[0],d[1],d[2],alpha]}

    cx, cz = (tgt_mn[0]+tgt_mx[0])/2, (tgt_mn[2]+tgt_mx[2])/2
    scale = 12.0 / tgt_dims[2]
    def bake(pos):
        p = pos.copy()
        p[:,0] -= cx; p[:,1] -= tgt_mn[1]; p[:,2] -= cz
        x, z = -p[:,2].copy(), p[:,0].copy()
        p[:,0], p[:,2] = x, z
        return (p * scale).astype(np.float32)

    b64 = lambda a: c.base64.b64encode(np.ascontiguousarray(a).tobytes()).decode()

    def weld_and_quantize(pos, idx, uv):
        key_pos = np.round(pos, 4)
        keys = np.concatenate([key_pos, np.round(uv, 4)], axis=1) if uv is not None else key_pos
        uniq, inverse = np.unique(keys, axis=0, return_inverse=True)
        inverse = np.asarray(inverse).ravel().astype(np.uint32)
        nverts = len(uniq)
        welded_pos = np.zeros((nverts, 3), np.float32)
        welded_pos[inverse] = pos
        welded_uv = None
        if uv is not None:
            welded_uv = np.zeros((nverts, 2), np.float32)
            welded_uv[inverse] = uv
        new_idx = inverse[idx]
        vmin = welded_pos.min(0)
        vrange = welded_pos.max(0) - vmin
        vrange[vrange < 1e-6] = 1e-6
        qpos = np.round((welded_pos - vmin) / vrange * 65535).astype(np.uint16)
        return qpos, vmin, vrange/65535.0, welded_uv, new_idx, nverts

    def encode_plist(plist):
        groups = {}
        for p in plist:
            mi = mat_info(p["mat"])
            gk = (tuple(round(cc,3) for cc in mi["color"]), mi["tex"])
            g = groups.setdefault(gk, {"pos":[], "uv":[], "idx":[], "off":0})
            g["idx"].append(p["idx"] + g["off"])
            g["pos"].append(bake(p["pos"]))
            g["off"] += len(p["pos"])
            if p["uv"] is not None and mi["tex"]:
                g["uv"].append(p["uv"].astype(np.float32))
            else:
                g["uv"].append(np.zeros((len(p["pos"]),2), np.float32))
        entries = []
        for (color, tex), g in groups.items():
            pos = np.vstack(g["pos"])
            uv = np.vstack(g["uv"]) if tex else None
            idx = np.concatenate(g["idx"])
            qpos, qo, qs, welded_uv, new_idx, nv = weld_and_quantize(pos, idx, uv)
            iw = 4 if nv > 65535 else 2
            idx_arr = new_idx.astype(np.uint32 if iw==4 else np.uint16)
            e = {"q": b64(qpos), "qo":[round(float(x),4) for x in qo],
                 "qs":[round(float(x),8) for x in qs],
                 "i": b64(idx_arr), "iw": iw, "c": list(color), "t": tex}
            if tex and welded_uv is not None:
                quv = np.round(np.clip(welded_uv,0,1) * 65535).astype(np.uint16)
                e["u"] = b64(quv)
            entries.append(e)
        return entries

    part_prims = {}
    for p in tgt_prims:
        part_prims.setdefault(p["type"], []).append(p)

    out_parts, anchors, surfaces = {}, {}, []
    for pid, plist in part_prims.items():
        if pid in c.ANIMATABLE:
            bynode = {}
            for p in plist:
                # 借來的片段沒有真實節點名可去重複編號，直接各自成片
                key = p.get("_borrowed_from") or c.SUFFIX_RE.sub("", str(p["node"]))
                bynode.setdefault(key, []).append(p)
            for node, nplist in bynode.items():
                entries = encode_plist(nplist)
                Ph = np.vstack([bake(p["pos"]) for p in nplist])
                axis, pivot, side = c.compute_hinge(Ph, pid)
                surfaces.append({"t": pid,
                                 "ax": [round(float(x),4) for x in axis],
                                 "pv": [round(float(x),3) for x in pivot],
                                 "sd": side, "e": entries})
            continue
        entries = encode_plist(plist)
        out_parts[pid] = entries
        allpos = np.vstack([bake(p["pos"]) for p in plist])
        bmn2, bmx2 = allpos.min(0), allpos.max(0)
        cctr = (bmn2+bmx2)/2
        anchors[pid] = [round(float(cctr[0]),2), round(float(bmx2[1]),2),
                        round(float((cctr[2]+bmx2[2])/2),2)]

    result = {"meta":{"source":"Flightradar24/fr24-3d-models (GPL-2.0)",
                      "model": target_src.split("/")[-1].split("\\")[-1], "format": 2},
              "texture": texture_uri, "parts": out_parts, "anchors": anchors}
    if surfaces:
        result["surfaces"] = surfaces
    with open(dst, "w") as f:
        c.json.dump(result, f, separators=(",",":"))
    print(f"輸出 {dst}：{len(surfaces)} 片操縱面（借用轉移法）")
    types = {}
    for s in surfaces: types[s["t"]] = types.get(s["t"],0)+1
    print("  類型統計：", types)

if __name__ == "__main__":
    transfer(sys.argv[1], sys.argv[2], sys.argv[3])
