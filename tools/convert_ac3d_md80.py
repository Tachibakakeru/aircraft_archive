#!/usr/bin/env python3
"""
FlightGear Octal450/MD-80（AC3D 格式）→ models/md80.json（v2 壓縮格式）

來源：https://github.com/Octal450/MD-80，GPL-2.0，第三方社群維護（非
FGAddon 官方機庫，但授權明確為 GPL-2.0）。命名品質良好，可直接依名稱分類。

用法：python3 convert_ac3d_md80.py <mesh_airframe.ac 所在資料夾> models/md80.json
"""
import sys, os
from ac3d_lib import parse_ac3d, classify_and_bake

FUSELAGE = [
    "Fuselage", "FuselageOther", "FuselageStuff", "StabFairing", "WheelWellsMG",
    "WiperL", "WiperR", "AxisWiperL", "AxisWiperR",
]
COCKPIT = ["WindowsCockpit"]
WING = [
    "WingL1", "WingL2", "WingL3", "WingR1", "WingR2", "WingR3", "WingFairing",
    "AileronL", "AileronR", "AilTabControlL", "AilTabControlR", "AilTabTrimL", "AilTabTrimR",
    "FlapDoorL", "FlapDoorR", "FlapGussetL", "FlapGussetR",
    "FlapHorns2InL", "FlapHorns2InR", "FlapHorns2OutL", "FlapHorns2OutR",
    "FlapIn2L", "FlapIn2R", "FlapInL", "FlapInR", "FlapOut2L", "FlapOut2R", "FlapOutL", "FlapOutR",
    "SlatStrutsL1", "SlatStrutsL2", "SlatStrutsL3", "SlatStrutsR1", "SlatStrutsR2", "SlatStrutsR3",
    "SlatsL1", "SlatsL2", "SlatsL3", "SlatsR1", "SlatsR2", "SlatsR3",
    "SpoilerL1", "SpoilerL2", "SpoilerL3", "SpoilerR1", "SpoilerR2", "SpoilerR3",
    "WingLightL", "WingLightR", "AxisWingLightL", "AxisWingLightR",
]
ENGINE = [
    "Engines", "EngExhaustL", "EngExhaustR", "EngFanDiskL", "EngFanDiskL1",
    "EngFanDiskR", "EngFanDiskR1", "EngRevDL", "EngRevDR",
    "EngRevStrutADL", "EngRevStrutADR", "EngRevStrutAVL", "EngRevStrutAVR",
    "EngRevStrutFDL", "EngRevStrutFDR", "EngRevStrutFVL", "EngRevStrutFVR",
    "EngRevVL", "EngRevVR",
]
VSTAB = ["VStabilizer", "Rudder", "RudderTabControl"]
HSTAB = [
    "Stabilizer", "ElevatorL", "ElevatorR",
    "ElTabAntifloatL", "ElTabAntifloatR", "ElTabControlL", "ElTabControlR",
    "ElTabGearedL", "ElTabGearedR",
]
GEAR = [
    "LGDoorInL", "LGDoorInR", "LGDoorOutL", "LGDoorOutR",
    "LGLBraceLow", "LGLBraceUp", "LGLStrutLow", "LGLStrutUp", "LGLTires",
    "LGLTorqueBarLow", "LGLTorqueBarUp",
    "LGNDoorAftL", "LGNDoorAftR", "LGNDoorForL", "LGNDoorForR", "LGNDrag",
    "LGNStrutLow", "LGNStrutUp", "LGNTires", "LGNTorqueBarLow", "LGNTorqueBarUp",
    "LGRBraceLow", "LGRBraceUp", "LGRStrutLow", "LGRStrutUp", "LGRTires",
    "LGRTorqueBarLow", "LGRTorqueBarUp",
]

PART_MAP = {}
for names, pid in [(FUSELAGE,"fuselage"), (COCKPIT,"cockpit"), (WING,"wing"),
                    (ENGINE,"engine"), (VSTAB,"vstab"), (HSTAB,"hstab"), (GEAR,"gear")]:
    for n in names:
        PART_MAP[n] = pid

def convert(src_dir, dst):
    objects = parse_ac3d(os.path.join(src_dir, "mesh_airframe.ac"))
    classify_and_bake(
        objects, PART_MAP, dst, "md80",
        "FlightGear Octal450/MD-80（https://github.com/Octal450/MD-80）"
        "AC3D 模型轉換（GPL-2.0），未含貼圖",
    )

if __name__ == "__main__":
    convert(sys.argv[1], sys.argv[2])
