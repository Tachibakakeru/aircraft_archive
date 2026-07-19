#!/usr/bin/env python3
"""
FlightGear Octal450/MD-11（AC3D 格式）→ models/md11.json（v2 壓縮格式）

來源：https://github.com/Octal450/MD-11，GPL-2.0，第三方社群維護。與同
作者的 DC-10 模型命名慣例高度相似（wing.1/wing.2、tyres.central、
central.strut 等），三發廣體機，垂尾未見獨立命名物件（融合於機身/機尾
結構中），以 rudder.l/rudder.u（方向舵，本身即涵蓋相當高度）代表垂尾。

用法：python3 convert_ac3d_md11.py <MD-11-GE.ac 所在資料夾> models/md11.json
"""
import sys, os
from ac3d_lib import parse_ac3d, classify_and_bake

FUSELAGE = [
    "fuselage", "fuselage.001", "fuselage.002",
    "fuselage.cone", "fuselage.cone.001", "fuselage.cone.002", "fuselage.cone.003", "fuselage.cone_2",
    "cargo1", "cargo2", "cargo3",
    "ldoor.1", "ldoor.2", "ldoor.3", "ldoor.4", "rdoor.1", "rdoor.2", "rdoor.3", "rdoor.4",
    "VHF.lowerA", "VHF.lowerF", "VHF.upper", "Sphere", "Sphere.001",
    "ldglight.left", "ldglight.left.glass", "ldglight.right", "ldglight.right.glass",
]
COCKPIT = ["Windshield", "windshield.frames", "wiper.left", "wiper.right"]
WING = [
    "wing.1", "wing.1.part2", "wing.1.part3", "wing.2", "wing.2.part2", "wing.2.part3",
    "wing1.grey.part1", "wing1.grey.part2", "wing1.grey.part3",
    "wing2.grey.part1", "wing2.grey.part2", "wing2.grey.part3",
    "winglet.left", "winglet.right", "wing.antennas.left", "wing.antennas.right",
    "wing.glass.left", "wing.glass.right", "Pylons",
    "AileronL1", "AileronL2", "AileronR1", "AileronR2",
] + [f"flap.{n}" for n in ["000","015","1","10","10.part2","11","12","13","13.part2",
     "14","14.part2","2","3","3.part2","4","5","5.part2","6","7","8","9","9.part2"]
] + [f"slat.{n}" for n in ["000","005","1.part1","1.part2","1.part3","2","2.2","3","3.2",
     "4.part1","4.part2","4.part3"]
] + [f"sp.brake.{side}.{n}" for side in ("left","right") for n in range(1,6)]
ENGINE = [
    "Intakes", "engines", "engines.001", "engines.002", "engines.003", "engines.004",
    "engines.005", "engines.006", "engines.chrome", "engines_2_duct.x", "engines_2_vanedisk",
    "engine_1_3_nozzlecone", "engine_2_nozzlecone",
    "fan_1", "fan_1.center", "fan_1_fast", "fan_2", "fan_2.center", "fan_2_fast",
    "fan_3", "fan_3.center", "fan_3_fast",
    "center.reverser", "center.reverser_inner", "left.reverser",
    "right.reverser", "right.reverser.001", "right.reverser.002", "right.reverser.005",
]
VSTAB = ["rudder.l", "rudder.u", "rudder_trailing.l", "rudder_trailing.u"]
HSTAB = ["HorzStab1", "HorzStab2", "elevator.1i", "elevator.1o", "elevator.2i", "elevator.2o"]
GEAR = [
    "tyres", "tyres.central", "tyres.left.back", "tyres.left.front",
    "tyres.right.back", "tyres.right.front",
    "central.back.left", "central.back.right", "central.front.left", "central.front.right",
    "central.scissor.down", "central.scissor.up", "central.strut.low", "central.strut.up",
    "front.strut.high", "front.strut.low",
    "left.arm1", "left.arm2", "left.arm3", "left.main.door",
    "left.scissor.down", "left.scissor.up", "left.strut.low", "left.strut.low2", "left.strut.up",
    "nose.arm1", "nose.scissor.down", "nose.scissor.up",
    "right.arm1", "right.arm2", "right.arm3", "right.main.door",
    "right.scissor.down", "right.scissor.up", "right.strut.low", "right.strut.low2", "right.strut.up",
    "main.left.door", "main.right.door",
    "lgdoor.left.front", "lgdoor.left.front.2", "lgdoor.right.front", "lgdoor.right.front.2",
]

PART_MAP = {}
for names, pid in [(FUSELAGE,"fuselage"), (COCKPIT,"cockpit"), (WING,"wing"),
                    (ENGINE,"engine"), (VSTAB,"vstab"), (HSTAB,"hstab"), (GEAR,"gear")]:
    for n in names:
        PART_MAP[n] = pid

def convert(src_dir, dst):
    objects = parse_ac3d(os.path.join(src_dir, "MD-11-GE.ac"))
    classify_and_bake(
        objects, PART_MAP, dst, "md11",
        "FlightGear Octal450/MD-11（https://github.com/Octal450/MD-11）"
        "AC3D 模型轉換（GPL-2.0），未含貼圖；垂尾無獨立命名物件，"
        "以方向舵（rudder.l/rudder.u）代表",
    )

if __name__ == "__main__":
    convert(sys.argv[1], sys.argv[2])
