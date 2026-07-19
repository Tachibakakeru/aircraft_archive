#!/usr/bin/env python3
"""
FlightGear FGMEMBERS-NONGPL/DC-9-32（AC3D 格式）→ models/dc9.json

來源：https://github.com/FGMEMBERS-NONGPL/DC-9-32，作者 Lester Boffo，
授權 CC BY-NC-SA 4.0（僅限非商業使用、需具名歸屬、以同授權分享）。
本站為非商業性質的興趣資料庫，符合授權範圍；轉出的模型 JSON 依
ShareAlike 條款同樣採 CC BY-NC-SA 4.0 釋出（與其他機型的 GPL 授權不同，
見 README 授權聲明分項說明）。

用法：python3 convert_ac3d_dc9.py <DC-9-32.ac 所在資料夾> models/dc9.json
"""
import sys, os
from ac3d_lib import parse_ac3d, classify_and_bake

FUSELAGE = [
    "Fuselage", "Belly", "BeaconMount", "LampBeacon", "LampBeaconOn", "LampBeaconOn.001",
    "WinFrames", "WheelWellsMG", "WheelWellsMG.001", "WheelWellsNose",
    "Strake", "StrakeEng", "StrakeEng.001", "object",
]
COCKPIT = ["WindowsCockpit"]
WING = [
    "Wings", "AileronL", "AileronR", "FlapDoorL", "FlapDoorR", "FlapL", "FlapR",
    "SpoilerL1", "SpoilerL2", "SpoilerR1", "SpoilerR2",
    "FairingL1", "FairingL2", "FairingL3", "FairingL4",
    "FairingR2", "FairingR3", "FairingR4", "FairingPylons",
    "EngMounts", "EngMounts.001",
]
ENGINE = [
    "EngExhaustL", "EngExhaustR", "EngFanDiskL", "EngFanDiskR", "EngHubL", "EngHubR",
    "EngRevFrameL", "EngRevFrameR",
    "EngRevStrutADL", "EngRevStrutADR", "EngRevStrutAVL", "EngRevStrutAVR",
    "EngRevStrutFDL", "EngRevStrutFDR", "EngRevStrutFVL", "EngRevStrutFVR",
    "EngineL", "EngineL.001", "EngineLIntake", "EngineLReverserDown", "EngineLReverserUp",
    "EngineR", "EngineR.001", "EngineRIntake", "EngineRReverserDown", "EngineRReverserUp",
]
VSTAB = ["Vstab", "Rudder"]
HSTAB = ["Hstabs", "ElevatorL", "ElevatorR"]
GEAR = [
    "GearLDoor", "GearNAftDoorL", "GearNAftDoorR", "GearNFwdDoorL", "GearNFwdDoorR", "GearRDoor",
    "LGDoorOutL", "LGDoorOutR",
    "LGLBraceLow", "LGLBraceUp", "LGLStrutLow", "LGLStrutUp", "LGLTires",
    "LGLTorqueBarLow", "LGLTorqueBarLow.001", "LGLTorqueBarUp",
    "LGNDrag", "LGNStrutLow", "LGNStrutUp", "LGNTires", "LGNTorqueBarLow", "LGNTorqueBarUp",
    "LGRBraceLow", "LGRBraceUp", "LGRStrutLow", "LGRStrutUp", "LGRTires",
    "LGRTorqueBarLow", "LGRTorqueBarUp",
]

PART_MAP = {}
for names, pid in [(FUSELAGE,"fuselage"), (COCKPIT,"cockpit"), (WING,"wing"),
                    (ENGINE,"engine"), (VSTAB,"vstab"), (HSTAB,"hstab"), (GEAR,"gear")]:
    for n in names:
        PART_MAP[n] = pid

def convert(src_dir, dst):
    objects = parse_ac3d(os.path.join(src_dir, "DC-9-32.ac"))
    classify_and_bake(
        objects, PART_MAP, dst, "dc9",
        "FlightGear FGMEMBERS-NONGPL/DC-9-32（https://github.com/FGMEMBERS-NONGPL/DC-9-32），"
        "作者 Lester Boffo，AC3D 模型轉換，CC BY-NC-SA 4.0（非商業使用），未含貼圖",
    )

if __name__ == "__main__":
    convert(sys.argv[1], sys.argv[2])
