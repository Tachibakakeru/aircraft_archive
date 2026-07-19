#!/usr/bin/env python3
"""
FlightGear FGAddon Boeing 727-230（AC3D 格式）→ models/b727.json（v2 壓縮格式）

來源：FlightGear FGAddon 官方機庫 727-230，GPL v2+。這個來源檔案命名品質
明顯較差（大量 Blender 預設名稱 Plane.NNN/Cube.NNN/Circle.NNN，且部分
「Fuselage.NNN」實際是垂尾/水平尾翼——依幾何位置與尺寸比對而非名稱判斷），
另含大量駕駛艙內裝細節（節流閥、起落架拉桿、儀表面板等）刻意不納入，
因為站上檢視器只看外觀不看內裝。原始檔案行尾字元異常（每行後夾帶一個
空白行），已在 ac3d_lib.parse_ac3d 中處理。

用法：python3 convert_ac3d_727.py <727-230.ac 所在資料夾> models/b727.json
"""
import sys, os
from ac3d_lib import parse_ac3d, classify_and_bake

FUSELAGE = [
    "Cube.004", "windows.001", "Fuselage.004", "Fuselage.005", "Fuselage.006",
    "frontdoorleft", "frontdoorleft.001", "lhfuselage.004_0", "Plane.004",
    "antlo", "antup", "aoa1", "aoa2", "vane1", "vane2",
    "pitot1", "pitot2", "pitot3", "pitot4",
    "lbeaconbase", "lbeaconlenz", "ubeaconbase", "ubeaconlenz",
    "Cube.011_0", "Cube.011_1",
]
COCKPIT = ["glas"]
WING = [
    "Plane.005", "leftaileron", "rightaileron", "edger",
    "flap1", "flap1.1", "flap2", "flap2.1", "flap3", "flap3.1", "flap4", "flap4.1",
    "slat1", "slat1.1", "slat1.2", "slat1.3", "slat1.004",
    "slat2", "slat2.1", "slat2.2", "slat2.3",
    "inneraileronl_0", "inneraileronl_1", "inneraileronr_0", "inneraileronr_1",
    "Plane.025_0", "Plane.025_1_0", "Plane.025_1_1", "Plane.031", "Plane.013",
]
ENGINE = ["inlet", "Circle", "Circle.001", "Circle.002", "Circle.003", "rhfan",
          "Plane.020", "Plane.018", "Cube.005"]
VSTAB = ["Fuselage.003", "rudder", "rudder.002"]
HSTAB = ["Plane", "leftelevator", "rightelevator"]
GEAR = [
    "rmgt", "lmgt", "tyrern", "tyreln",
    "lglhlowerstrut", "lgouterstrut", "lhsteercyl", "lmgaxle", "lmgdoor", "lmgdoor.001",
    "mglhtyrelh.003", "mgrhtyrelh.003", "mgrhtyrerh.003",
    "nlinklower", "nlinkupper", "nlowerstrut", "nouterstrut",
    "noseaxle", "nosegearbay",
    "rglhlowerstrut", "rgouterstrut", "rhsteercyl", "rmgaxle", "rmgdoor", "rmgdoor.001",
    "lmgdoor1", "lmgdoor1.001", "lmgdoor2", "lmgdoor2.001",
    "rmgdoor1", "rmgdoor1.001", "rmgdoor2", "rmgdoor2.001",
    "lhngdoor", "lhngdoor_0", "lhngdoor_1", "rhngdoor", "rhngdoor_1", "rhngdoor_1_0", "rhngdoor_1_1",
]
# 明確排除：駕駛艙內裝與通用無語意物件（節流閥、起落架/襟翼拉桿、儀表面板、
# 座艙側壁等），站上檢視器僅需外觀幾何，這些略過不影響外觀完整性。

PART_MAP = {}
for names, pid in [(FUSELAGE,"fuselage"), (COCKPIT,"cockpit"), (WING,"wing"),
                    (ENGINE,"engine"), (VSTAB,"vstab"), (HSTAB,"hstab"), (GEAR,"gear")]:
    for n in names:
        PART_MAP[n] = pid

def convert(src_dir, dst):
    objects = parse_ac3d(os.path.join(src_dir, "727-230.ac"))
    classify_and_bake(
        objects, PART_MAP, dst, "b727",
        "FlightGear FGAddon 官方機庫 Boeing 727-230 AC3D 模型轉換"
        "（GPLv2+），未含貼圖；來源檔案命名不完整，部分部位依幾何位置人工比對分類",
    )

if __name__ == "__main__":
    convert(sys.argv[1], sys.argv[2])
