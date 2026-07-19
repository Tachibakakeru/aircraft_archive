#!/usr/bin/env python3
"""
FlightGear FGAddon McDonnell Douglas DC-10-30（AC3D 格式）→ models/dc10.json

來源：FlightGear FGAddon 官方機庫 DC-10-30，GPL v2+（2024.1 版本重製）。
三發廣體機，尾部第二具引擎嵌於垂尾根部；起落架為五輪三支柱配置
（左右翼下主起落架＋機腹中央第三組起落架）。

用法：python3 convert_ac3d_dc10.py <DC-10-30.ac 所在資料夾> models/dc10.json
"""
import sys, os
from ac3d_lib import parse_ac3d, classify_and_bake

FUSELAGE = [
    "FuselageMain", "Belly.001", "MainGearWell", "NoseGearWell",
    "Cargo1", "Cargo1Int", "Cargo2", "Cargo2Int",
    "DoorL1", "DoorL1Int", "DoorL2", "DoorL2Int", "DoorL3", "DoorL3Int", "DoorL4", "DoorL4Int",
    "DoorR1", "DoorR1Int", "DoorR2", "DoorR2Int", "DoorR3", "DoorR3Int", "DoorR4", "DoorR4Int",
    "Windows", "VHF.lowerA", "VHF.lowerF", "VHF.upper", "Sphere", "Interior", "Interior.001",
]
COCKPIT = ["CockpitFrame"]
WING = [
    "wing.1", "wing.1.part2", "wing.1.part3", "wing.2", "wing.2.part2", "wing.2.part3",
    "wing1.grey.part1", "wing1.grey.part2", "wing1.grey.part3",
    "wing2.grey.part1", "wing2.grey.part2", "wing2.grey.part3",
    "Pylons", "AileronL1", "AileronL2", "AileronR1", "AileronR2",
] + [f"flap.{n}" for n in ["000","015","1","10","10.part2","11","12","13","13.part2",
     "14","14.part2","2","3","4","5","6","7","8","9","9.part2"]
] + [f"slat.{n}" for n in ["1.part1","1.part2","1.part3","2","2.2","3","3.2",
     "4.part1","4.part2","4.part3"]
] + [f"sp.brake.{side}.{n}" for side in ("left","right") for n in range(1,6)]
ENGINE = [
    "Blades1", "Blades2", "Blades3", "EngineIntake", "EngineInterior",
    "EngineNozzle", "EngineNozzleRear", "Housing", "Housing.001", "Housing.002",
    "Intake", "Intake.001", "Nacelle1", "Nacelle2", "Nacelle3",
    "NacelleRear", "NacelleRear.001", "EngineNacelleRear",
    "Reverser1", "Reverser2", "Reverser3", "ReverserRear", "ReverserRear.001", "EngineReverserRear",
    "Nozzle", "Nozzle.001", "NozzleRear", "NozzleRear.001",
    "Shaft", "Shaft.001", "Shaft.002", "shroud", "shroud.001", "shroud.002",
    "caseSupports", "caseSupports.001", "caseSupports.002",
]
VSTAB = ["rudder.l", "rudder.u", "rudder_trailing.l", "rudder_trailing.u", "Vstab.001"]
HSTAB = ["HorzStab", "elevator.1i", "elevator.1o", "elevator.2i", "elevator.2o"]
GEAR = [
    "tyres", "tyres.central", "tyres.left.back", "tyres.left.front",
    "tyres.right.back", "tyres.right.front",
    "central.scissor.down", "central.scissor.up", "central.strut.low", "central.strut.up",
    "front.strut.high", "front.strut.low",
    "left.arm1", "left.arm2", "left.arm3", "left.main.door",
    "left.scissor.down", "left.scissor.up", "left.strut.low", "left.strut.low2", "left.strut.up",
    "nose.arm1", "nose.scissor.down", "nose.scissor.up",
    "right.arm1", "right.arm2", "right.arm3", "right.main.door",
    "right.scissor.down", "right.scissor.up", "right.strut.low", "right.strut.low2", "right.strut.up",
    "GearCDoorL1", "GearCDoorL2", "GearCDoorR1", "GearCDoorR2",
    "GearCDoorL1Int", "GearCDoorL2Int", "GearCDoorR1Int", "GearCDoorR2Int",
    "GearLDoor1", "GearLDoor1Int", "GearRDoor1", "GearRDoor1Int",
    "GearNDoorL1", "GearNDoorL2", "GearNDoorR1", "GearNDoorR2",
    "GearNDoorL1Int", "GearNDoorL2Int", "GearNDoorR1Int", "GearNDoorR2Int",
]

PART_MAP = {}
for names, pid in [(FUSELAGE,"fuselage"), (COCKPIT,"cockpit"), (WING,"wing"),
                    (ENGINE,"engine"), (VSTAB,"vstab"), (HSTAB,"hstab"), (GEAR,"gear")]:
    for n in names:
        PART_MAP[n] = pid

def convert(src_dir, dst):
    objects = parse_ac3d(os.path.join(src_dir, "DC-10-30.ac"))
    classify_and_bake(
        objects, PART_MAP, dst, "dc10",
        "FlightGear FGAddon 官方機庫 McDonnell Douglas DC-10-30 AC3D 模型轉換"
        "（GPLv2+），未含貼圖",
    )

if __name__ == "__main__":
    convert(sys.argv[1], sys.argv[2])
