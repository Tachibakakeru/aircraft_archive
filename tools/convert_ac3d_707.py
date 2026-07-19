#!/usr/bin/env python3
"""
FlightGear FGAddon Boeing 707（AC3D 格式）→ models/b707.json（v2 壓縮格式）

來源：FlightGear FGAddon「Lake of Constance Hangar」707（Copyright M.Kraus，
GPLv3）。座標系（原始 AC3D，經驗證）：X 前後（機頭在負值）、Y 垂直向上、
Z 左右展向。烘焙後輸出座標系（專案慣例）：機鼻 +X、地面 y=0、機長縮放至
12 單位。

用法：python3 convert_ac3d_707.py <707.ac 所在資料夾> models/b707.json
資料夾需含：707.ac、PWJT4.ac（引擎）、wheels.ac（主起落架輪組，707.ac
內的 LeftGear/RightGear 只是支柱，輪胎另外掛載）
"""
import sys, os
import numpy as np
from ac3d_lib import parse_ac3d, object_tris, classify_and_bake

PART_MAP = {
    "fuselage": "fuselage", "fuselage.inner": "fuselage", "fuselage.belly": "fuselage",
    "nose": "fuselage", "nosewheelwell": "fuselage", "nonones": "fuselage",
    "antenaasa": "fuselage", "lampFrame": "fuselage", "probe": "fuselage",
    "doorFL": "fuselage", "doorRL": "fuselage", "doorCargo": "fuselage", "doorBelly": "fuselage",
    "lhdoorouter": "fuselage", "lhdoorinner": "fuselage",
    "rhdoorouter": "fuselage", "rhdoorinner": "fuselage",
    "wing": "wing",
    "rhobail": "wing", "rhibail": "wing", "lhobail": "wing", "lhibail": "wing",
    "rhobflap": "wing", "rhibflap": "wing", "lhobflap": "wing", "lhibflap": "wing",
    "rhfiletflap": "wing", "lhfiletflap": "wing",
    "slatsL": "wing", "slatsR": "wing",
    "engineSupport": "wing",
    "vertstab": "vstab", "rudder": "vstab",
    "rhsp1": "hstab", "rhsp3": "hstab", "lhsp1": "hstab", "lhsp3": "hstab",
    "rhelevator": "hstab", "lhelevator": "hstab", "elevwing": "hstab",
    "LeftGear": "gear", "LeftGear.001": "gear", "LeftGearCompressor": "gear", "LeftGearCompressor1": "gear",
    "RightGear": "gear", "RightGear.001": "gear", "RightGearCompressor": "gear", "RightGearCompressor1": "gear",
    "NGear": "gear", "NGearStrut": "gear", "NoseWheel": "gear",
    "mgdoora": "gear", "mgdoorb": "gear", "mgdoorc": "gear",
    "rhmgdoora": "gear", "rhmgdoorb": "gear", "rhmgdoorc": "gear",
    "rhngdoor": "gear", "rhngdooraft": "gear", "lhngdoor": "gear", "lhngdooraft": "gear",
}

# 707.xml 讀出的外掛模型掛載座標，FG 座標系 x=前後 y=左右 z=垂直，
# 與 AC3D 內部座標系（x=前後 y=垂直 z=左右）軸序不同：ac3d(x,y,z) = fg(x,z,y)
ENGINE_OFFSETS_FG = [
    ( 2.47, -14.835, -0.73), (-1.18, -10.077, -1.18),
    (-1.18,  10.077, -1.18), ( 2.47,  14.835, -0.73),
]
GEAR_WHEEL_OFFSETS_FG = [(1.82, 2.76, -2.30), (1.82, -2.76, -2.30)]

def instanced(objects, offsets_fg, part_id):
    """將一組外掛模型物件（原點在自身局部座標）依 FG 掛載座標實例化多份，
    回傳可直接併入分類清單的 dict list（略過分類，直接標記 part_id）。"""
    out = []
    for fx, fy, fz in offsets_fg:
        ax, ay, az = fx, fz, fy
        for obj in objects:
            o = dict(obj)
            o["loc"] = (obj["loc"][0]+ax, obj["loc"][1]+ay, obj["loc"][2]+az)
            o["_forced_part"] = part_id
            out.append(o)
    return out

def convert(src_dir, dst):
    fuse_objs = parse_ac3d(os.path.join(src_dir, "707.ac"))
    eng_objs = parse_ac3d(os.path.join(src_dir, "PWJT4.ac"))
    wheel_objs = parse_ac3d(os.path.join(src_dir, "wheels.ac"))

    eng_objs = [o for o in eng_objs if o["name"] != "world"]
    wheel_objs = [o for o in wheel_objs if o["name"] != "world"]

    all_objects = [o for o in fuse_objs if o["name"] not in ("world", "Blender_export__707.ac")]
    all_objects += instanced(eng_objs, ENGINE_OFFSETS_FG, "engine")
    all_objects += instanced(wheel_objs, GEAR_WHEEL_OFFSETS_FG, "gear")

    # 用 _forced_part 覆蓋一般 PART_MAP 分類（外掛模型物件名稱與機身可能重複但意義不同）
    part_map = dict(PART_MAP)
    for o in all_objects:
        if "_forced_part" in o:
            part_map[o["name"]] = o["_forced_part"]  # 供 classify_and_bake 查表一致

    # classify_and_bake 以 name 查表分類，_forced_part 物件其 name 可能與 PART_MAP
    # 既有鍵衝突（如未來機型），此處 707 目前無此問題，直接沿用共用邏輯。
    classify_and_bake(
        all_objects, part_map, dst, "b707",
        "FlightGear FGAddon 「Lake of Constance Hangar」 Boeing 707"
        "（Copyright M.Kraus，GPLv3）AC3D 模型轉換，未含貼圖（原始貼圖檔另行處理）",
    )

if __name__ == "__main__":
    convert(sys.argv[1], sys.argv[2])
