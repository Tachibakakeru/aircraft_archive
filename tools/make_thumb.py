#!/usr/bin/env python3
"""
從 convert_fr24.py 的輸出產生列表頁側視縮圖
用法: python3 make_thumb.py <models/xxx.json> <assets/thumb_xxx.png>
輸出 640x360 RGBA PNG：機體剪影（垂直尾翼以琥珀色標示）
"""
import json, base64, struct, zlib, sys
import numpy as np

W, H = 640, 360
BODY  = (174, 186, 199)   # 機體
VSTAB = (255, 181, 71)    # 尾翼識別色

def main(src, dst):
    d = json.load(open(src))
    # 收集全部三角形（附部位標記）
    tris_all = []
    for pid, entries in d["parts"].items():
        rgb = VSTAB if pid == "vstab" else BODY
        for e in entries:
            if "q" in e:   # v2 量化格式
                q = np.frombuffer(base64.b64decode(e["q"]), np.uint16).reshape(-1,3).astype(np.float32)
                pos = q * np.array(e["qs"], np.float32) + np.array(e["qo"], np.float32)
            else:          # v1 舊格式
                pos = np.frombuffer(base64.b64decode(e["p"]), np.float32).reshape(-1,3)
            idx = np.frombuffer(base64.b64decode(e["i"]),
                                np.uint32 if e["iw"]==4 else np.uint16)
            tris_all.append((pos[idx.astype(np.int64)].reshape(-1,3,3), rgb))

    # 依整體包圍盒決定縮放（側視：畫 x-y 平面）
    mn = np.min([t.reshape(-1,3).min(0) for t,_ in tris_all], axis=0)
    mx = np.max([t.reshape(-1,3).max(0) for t,_ in tris_all], axis=0)
    span_x, span_y = mx[0]-mn[0], mx[1]-mn[1]
    S = min((W-60)/span_x, (H-60)/span_y)
    cx, cy = (mn[0]+mx[0])/2, (mn[1]+mx[1])/2

    rgba  = np.zeros((H, W, 4), np.uint8)
    depth = np.full((H, W), -1e9, np.float32)

    for tris, rgb in tris_all:
        area = np.linalg.norm(np.cross(tris[:,1]-tris[:,0], tris[:,2]-tris[:,0]), axis=1)/2
        for t, a in zip(tris, area):
            k = max(3, min(400, int(a*S*S*0.9)))
            u, v = np.random.rand(k), np.random.rand(k)
            f = u+v > 1; u[f], v[f] = 1-u[f], 1-v[f]
            pts = t[0] + np.outer(u, t[1]-t[0]) + np.outer(v, t[2]-t[0])
            xs = (W/2 + (pts[:,0]-cx)*S).astype(int)
            ys = (H/2 - (pts[:,1]-cy)*S).astype(int)
            zs = pts[:,2]
            ok = (xs>=0)&(xs<W)&(ys>=0)&(ys<H)
            for x, y, z in zip(xs[ok], ys[ok], zs[ok]):
                if z >= depth[y, x]:
                    depth[y, x] = z
                    rgba[y, x] = (*rgb, 255)

    # 寫出 RGBA PNG
    def chunk(t, data):
        c = t + data
        return struct.pack(">I", len(data)) + c + struct.pack(">I", zlib.crc32(c))
    raw = b"".join(b"\x00" + rgba[y].tobytes() for y in range(H))
    with open(dst, "wb") as f:
        f.write(b"\x89PNG\r\n\x1a\n"
                + chunk(b"IHDR", struct.pack(">IIBBBBB", W, H, 8, 6, 0, 0, 0))
                + chunk(b"IDAT", zlib.compress(raw, 6))
                + chunk(b"IEND", b""))
    print(f"縮圖輸出: {dst}")

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
