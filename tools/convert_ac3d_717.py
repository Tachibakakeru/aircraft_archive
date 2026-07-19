#!/usr/bin/env python3
"""
FlightGear FGAddon Boeing 717-200（AC3D 格式）→ models/b717.json（v2 壓縮格式）

來源：FlightGear FGAddon 官方機庫 717-200，GPLv2+。與 707 不同，引擎／
起落架輪組皆內嵌於主檔案，無需額外掛載外部模型。座標系與 707 相同：
X 前後（機頭在負值）、Y 垂直向上、Z 左右展向。

用法：python3 convert_ac3d_717.py <717-200.ac 所在資料夾> models/b717.json
"""
import sys, os
from ac3d_lib import parse_ac3d, classify_and_bake

PART_MAP = {
    "Fuselage": "fuselage", "Belly.001": "fuselage", "Belly_0": "fuselage",
    "Antennas": "fuselage", "Belly": "fuselage", "Strake": "fuselage", "Strake.001": "fuselage",
    "antlo.003": "fuselage", "MainWells": "fuselage", "StabFairing": "fuselage",
    "WheelWells": "fuselage", "WinFrames": "fuselage", "Windows": "fuselage",
    "WindowsCockpit": "cockpit",
    "Wings": "wing", "AileronL": "wing", "AileronR": "wing",
    "FairingL1": "wing", "FairingL2": "wing", "FairingL3": "wing", "FairingL4": "wing",
    "FairingPylons": "wing",
    "FairingR1": "wing", "FairingR2": "wing", "FairingR3": "wing", "FairingR4": "wing",
    "FlapL": "wing", "FlapR": "wing",
    "SpoilerL1": "wing", "SpoilerL2": "wing", "SpoilerR1": "wing", "SpoilerR2": "wing",
    "EngMounts": "engine", "FandiskTurbofanL": "engine", "FandiskTurbofanR": "engine",
    "ReverserDownL": "engine", "ReverserDownR": "engine",
    "ReverserUpL": "engine", "ReverserUpR": "engine",
    "TurbofanL": "engine", "TurbofanR": "engine",
    "Vstab": "vstab", "Rudder": "vstab",
    "HStabilizerL": "hstab", "ElevatorL": "hstab",
    "ElTabAntifloatL": "hstab", "ElTabControlL": "hstab", "ElTabGearedL": "hstab",
    "HStabilizerR": "hstab", "ElevatorR": "hstab",
    "ElTabAntifloatR": "hstab", "ElTabControlR": "hstab", "ElTabGearedR": "hstab",
    "GearLDoor": "gear", "GearRDoor": "gear", "GearLDoorInt": "gear", "GearRDoorInt": "gear",
    "GearLScissorHi": "gear", "GearLScissorLo": "gear",
    "GearLStrutHi": "gear", "GearLStrutLo": "gear", "GearLTires": "gear",
    "GearNStrutHi": "gear", "GearNStrutLo": "gear", "GearNTires": "gear",
    "GearRScissorHi": "gear", "GearRScissorLo": "gear",
    "GearRStrutHi": "gear", "GearRStrutLo": "gear", "GearRTires": "gear",
    "LGNDoorAftL": "gear", "LGNDoorAftR": "gear", "LGNDoorForL": "gear", "LGNDoorForR": "gear",
}

def convert(src_dir, dst):
    objects = parse_ac3d(os.path.join(src_dir, "717-200.ac"))
    objects = [o for o in objects if o["name"] != "world"]
    classify_and_bake(
        objects, PART_MAP, dst, "b717",
        "FlightGear FGAddon 官方機庫 Boeing 717-200 AC3D 模型轉換"
        "（GPLv2+），未含貼圖",
    )

if __name__ == "__main__":
    convert(sys.argv[1], sys.argv[2])
