"""Add current civil helicopters and normalize the existing AW139 entry."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FLEET_PATH = ROOT / "data" / "fleet.json"


def tr(zh: str, en: str, ja: str) -> dict[str, str]:
    return {"zh": zh, "en": en, "ja": ja}


CATEGORY = tr("直升機", "Helicopter", "ヘリコプター")


# id, name, maker, first flight, rotor diameter, occupants, range, engine, ICAO,
# zh/en/ja summary, official source
AIRCRAFT = [
    ("h125", "Airbus H125", "Airbus Helicopters", "1974", "10.7 m", "1 + 6", "約 630 km", "1 × Safran Arriel 2D", "AS50", "高溫高原性能突出的輕型單發多用途直升機。", "A light single-engine utility helicopter noted for hot-and-high performance.", "高温・高高度性能に優れる軽単発多用途ヘリコプターです。", "https://www.airbus.com/en/products-services/helicopters/civil-helicopters/h125"),
    ("h130", "Airbus H130", "Airbus Helicopters", "1999", "10.7 m", "1 + 7", "約 644 km", "1 × Safran Arriel 2D", "EC30", "具寬客艙與 Fenestron 涵道尾旋翼的觀光與私人運輸直升機。", "A sightseeing and private-transport helicopter with a wide cabin and Fenestron tail rotor.", "広い客室とフェネストロンを備える遊覧・個人輸送ヘリコプターです。", "https://www.airbus.com/en/products-services/helicopters/civil-helicopters/h130"),
    ("h135", "Airbus H135", "Airbus Helicopters", "1994", "10.4 m", "1–2 + 5–6", "626 km", "2 × Safran Arrius 2B2 Plus / Pratt & Whitney PW206B3", "EC35", "廣泛用於醫療、警務、訓練與私人運輸的輕型雙發直升機。", "A light twin widely used for EMS, police, training, and private transport.", "救急、警察、訓練、個人輸送に広く使われる軽双発ヘリコプターです。", "https://www.airbus.com/en/products-services/helicopters/civil-helicopters/h135"),
    ("h140", "Airbus H140", "Airbus Helicopters", "2025", "10.8 m（約）", "1–2 + 6", "約 650 km", "2 × Safran Arrius 2E", "", "已完成實體首飛的新一代三噸級輕型雙發直升機。", "A new-generation three-tonne-class light twin that has completed its physical first flight.", "実機初飛行を完了した新世代3トン級軽双発ヘリコプターです。", "https://www.airbus.com/en/products-services/helicopters/civil-helicopters/h140"),
    ("h145", "Airbus H145", "Airbus Helicopters", "1999", "10.8 m", "1–2 + 最多 9", "約 650 km", "2 × Safran Arriel 2E", "EC45", "採五葉主旋翼與 Fenestron、適合醫療與公共服務的四噸級雙發機。", "A four-tonne twin with a five-blade rotor and Fenestron, optimized for EMS and public-service missions.", "5枚主ローターとフェネストロンを備え、救急・公共任務に適する4トン級双発機です。", "https://www.airbus.com/en/products-services/helicopters/civil-helicopters/h145"),
    ("h160", "Airbus H160", "Airbus Helicopters", "2015", "13.4 m", "2 + 最多 12", "約 880 km", "2 × Safran Arrano 1A", "H160", "採 Blue Edge 槳葉、傾斜 Fenestron 與 Helionix 的中型雙發直升機。", "A medium twin with Blue Edge blades, a canted Fenestron, and Helionix avionics.", "Blue Edgeブレード、傾斜フェネストロン、Helionixを備える中型双発機です。", "https://www.airbus.com/en/products-services/helicopters/civil-helicopters/h160"),
    ("h175", "Airbus H175", "Airbus Helicopters", "2009", "14.8 m", "2 + 最多 16", "約 1,067 km", "2 × Pratt & Whitney Canada PT6C-67E", "EC75", "面向海上能源、搜救與企業運輸的超中型雙發直升機。", "A super-medium twin for offshore energy, search and rescue, and corporate transport.", "洋上エネルギー、捜索救難、企業輸送向けのスーパー・ミディアム双発機です。", "https://www.airbus.com/en/products-services/helicopters/civil-helicopters/h175"),
    ("h215", "Airbus H215", "Airbus Helicopters", "1978", "16.2 m", "2 + 最多 19", "約 841 km", "2 × Safran Makila 1A1", "AS32", "Super Puma 家族的重型多用途型，保留寬大客艙與外吊能力。", "A heavy multi-role Super Puma retaining a large cabin and external-lift capability.", "大型客室と外部吊下げ能力を持つSuper Puma系列の重多用途型です。", "https://www.airbus.com/en/products-services/helicopters/civil-helicopters/h215"),
    ("h225", "Airbus H225", "Airbus Helicopters", "2000", "16.2 m", "2 + 最多 19", "約 857 km", "2 × Safran Makila 2A1", "EC25", "Super Puma 家族長航程重型雙發型，用於海上、搜救與政府運輸。", "The long-range heavy Super Puma for offshore, SAR, and government transport.", "洋上、捜索救難、政府輸送に使われるSuper Puma系列の長距離重双発型です。", "https://www.airbus.com/en/products-services/helicopters/civil-helicopters/h225"),
    ("bell505", "Bell 505 Jet Ranger X", "Bell", "2014", "11.3 m", "1 + 4", "566 km (306 nmi)", "1 × Safran Arrius 2R", "B505", "採 G1000H 航電與開放式客艙的輕型單發直升機。", "A light single with G1000H avionics and an open, flexible cabin.", "G1000Hアビオニクスと開放的で柔軟な客室を持つ軽単発機です。", "https://www.bellflight.com/products/bell-505"),
    ("bell407", "Bell 407GXi", "Bell", "1995", "10.7 m", "1 + 6", "624 km (337 nmi)", "1 × Rolls-Royce 250-C47E/4", "B407", "四葉主旋翼、G1000H NXi 與高機動性兼具的輕型單發機。", "A light single combining a four-blade rotor, G1000H NXi, and agile handling.", "4枚主ローター、G1000H NXi、高い機動性を併せ持つ軽単発機です。", "https://www.bellflight.com/products/bell-407"),
    ("bell429", "Bell 429", "Bell", "2007", "11.0 m", "1 + 7", "689 km (372 nmi)", "2 × Pratt & Whitney Canada PW207D1", "B429", "具寬敞平地板客艙與 IFR 能力的輕型雙發多任務直升機。", "A light twin multi-mission helicopter with a spacious flat-floor cabin and IFR capability.", "広いフラットフロア客室とIFR能力を持つ軽双発多任務ヘリコプターです。", "https://www.bellflight.com/products/bell-429"),
    ("bell412", "Subaru Bell 412EPX", "Bell / Subaru", "1979", "14.0 m", "1–2 + 最多 14", "約 659 km", "2 × Pratt & Whitney Canada PT6T-9 Twin-Pac", "B412", "Bell 412 家族最新重載版本，強化傳動與最大起飛重量。", "The latest heavy-lift Bell 412 evolution with upgraded transmission and gross weight.", "伝動系と最大重量を強化したBell 412系列の最新重搭載型です。", "https://www.bellflight.com/products/bell-412"),
    ("bell525", "Bell 525 Relentless", "Bell", "2015", "16.2 m", "2 + 16", "1,146 km (619 nmi)", "2 × General Electric CT7-2F1", "B525", "已完成實體試飛、採線傳飛控與大型客艙的超中型雙發直升機。", "A flight-tested super-medium twin with fly-by-wire controls and a large cabin.", "実機飛行試験済みで、フライ・バイ・ワイヤと大型客室を備えるスーパー・ミディアム双発機です。", "https://www.bellflight.com/products/bell-525"),
    ("aw109", "Leonardo AW109 Trekker", "Leonardo", "2016", "10.8 m", "2 + 最多 6", "約 828 km", "2 × Pratt & Whitney Canada PW207C", "A109", "以滑橇起落架強化野外任務能力的 AW109 輕型雙發型。", "A skid-equipped light-twin AW109 variant optimized for field operations.", "スキッド脚で野外任務能力を高めたAW109軽双発型です。", "https://helicopters.leonardo.com/en/products/aw109-trekker"),
    ("aw119", "Leonardo AW119Kx", "Leonardo", "1995", "10.8 m", "1 + 最多 7", "約 954 km", "1 × Pratt & Whitney Canada PT6B-37A", "A119", "具寬客艙、IFR 航電與高功率的輕型單發直升機。", "A light single combining a spacious cabin, IFR avionics, and strong power.", "広い客室、IFRアビオニクス、高出力を備える軽単発ヘリコプターです。", "https://helicopters.leonardo.com/en/products/aw119kx"),
    ("heli", "Leonardo AW139", "Leonardo", "2001", "13.8 m", "2 + 最多 15", "約 1,061 km", "2 × Pratt & Whitney Canada PT6C-67C", "A139", "廣泛用於海上、搜救、醫療與企業運輸的中型雙發直升機。", "A widely used intermediate twin for offshore, SAR, EMS, and corporate transport.", "洋上、捜索救難、救急、企業輸送に広く使われる中型双発ヘリコプターです。", "https://helicopters.leonardo.com/en/products/aw139"),
    ("aw169", "Leonardo AW169", "Leonardo", "2012", "12.1 m", "2 + 最多 10", "約 820 km", "2 × Pratt & Whitney Canada PW210A", "A169", "AWFamily 中的輕中型雙發機，採可變轉速主旋翼與玻璃座艙。", "The light-intermediate AWFamily twin with variable rotor speed and a glass cockpit.", "可変ローター回転数とグラスコックピットを備えるAWFamilyの軽中間双発機です。", "https://helicopters.leonardo.com/en/products/aw169"),
    ("aw189", "Leonardo AW189", "Leonardo", "2011", "14.6 m", "2 + 最多 16", "約 907 km", "2 × General Electric CT7-2E1", "A189", "面向海上能源與搜救的超中型雙發直升機。", "A super-medium twin designed for offshore energy and search-and-rescue missions.", "洋上エネルギーと捜索救難向けのスーパー・ミディアム双発ヘリコプターです。", "https://helicopters.leonardo.com/en/products/aw189"),
    ("aw09", "Leonardo AW09", "Leonardo", "2020", "10.8 m（約）", "1 + 最多 7", "約 800 km", "1 × Safran Arriel 2K", "", "已完成實體試飛、具複合材料機身與寬客艙的新世代輕型單發機。", "A flight-tested new-generation light single with a composite airframe and wide cabin.", "実機飛行試験済みで、複合材機体と広い客室を備える新世代軽単発機です。", "https://helicopters.leonardo.com/en/products/aw09"),
    ("r22", "Robinson R22 Beta II", "Robinson", "1975", "7.7 m", "2", "約 463 km", "1 × Lycoming O-360-J2A", "R22", "結構簡潔、成本較低的雙座活塞訓練與私人直升機。", "A simple, economical two-seat piston helicopter for training and private flying.", "簡素で経済的な2座ピストン練習・個人用ヘリコプターです。", "https://www.robinsonheli.com/r22-beta-ii"),
    ("r44", "Robinson R44 Raven II", "Robinson", "1990", "10.1 m", "4", "約 563 km", "1 × Lycoming IO-540-AE1A5", "R44", "四座活塞直升機，廣泛用於私人、訓練與巡查任務。", "A four-seat piston helicopter widely used for private, training, and patrol work.", "個人、訓練、巡視に広く使われる4座ピストンヘリコプターです。", "https://www.robinsonheli.com/r44-raven-ii"),
    ("r44cadet", "Robinson R44 Cadet", "Robinson", "—", "10.1 m", "2", "約 555 km", "1 × Lycoming O-540-F1B5", "R44", "以 R44 機體打造、降低載重與功率的雙座訓練型。", "A two-seat training derivative using the R44 airframe with reduced weight and power.", "R44機体を使い、重量と出力を抑えた2座練習型です。", "https://www.robinsonheli.com/r44-cadet"),
    ("r66", "Robinson R66 NxG", "Robinson", "2007", "10.1 m", "5", "約 648 km", "1 × Rolls-Royce RR300", "R66", "五座渦輪軸直升機，保留 Robinson 簡潔機體與低營運成本取向。", "A five-seat turboshaft helicopter retaining Robinson's simple, cost-conscious design philosophy.", "Robinsonの簡潔で低運航費志向の設計を受け継ぐ5座ターボシャフト機です。", "https://www.robinsonheli.com/r66"),
    ("md500e", "MD Helicopters MD 500E", "MD Helicopters", "—", "8.1 m", "1 + 4", "約 605 km", "1 × Rolls-Royce 250-C20B/C20R", "H500", "採五葉主旋翼、機身緊湊且機動性高的輕型單發直升機。", "A compact, agile light single with a five-blade main rotor.", "5枚主ローターを備える小型で機動性の高い軽単発ヘリコプターです。", "https://www.mdhelicopters.com/models/md-500e/"),
    ("md530f", "MD Helicopters MD 530F", "MD Helicopters", "—", "8.3 m", "1 + 4", "約 432 km", "1 × Rolls-Royce 250-C30", "H500", "針對高溫高原與外吊任務強化的 MD 500 家族型。", "An MD 500-family variant strengthened for hot-and-high and external-load missions.", "高温・高高度および外部吊下げ任務向けに強化したMD 500系列型です。", "https://www.mdhelicopters.com/models/md-530f/"),
    ("s92", "Sikorsky S-92A+", "Sikorsky", "—", "17.2 m", "2 + 最多 19", "約 1,014 km", "2 × General Electric CT7-8A6", "S92", "S-92 的新造升級型，增強引擎、變速箱、酬載與重型民用任務能力。", "The new-production S-92 evolution with upgraded engines, gearbox, payload, and heavy civil capability.", "エンジン、変速機、搭載量を強化した新造S-92の重民用型です。", "https://www.lockheedmartin.com/en-us/products/sikorsky-s-92-helicopter.html"),
]


def detail(row: tuple[str, ...]) -> dict:
    ident, name, _maker, first, rotor, occupants, range_, engine, _icao, zh, en, ja, source = row
    return {"title": name, "sub": tr(zh, en, ja), "sources": [source], "specifications": {
        "機組員與載客": [["典型載客量", occupants], ["首飛年份", first]],
        "尺寸": [["主旋翼直徑", rotor]], "性能": [["飛行距離（滿載）", range_]], "發動機": [["型號", engine]],
    }}


def fleet_entry(row: tuple[str, ...], old: dict | None = None) -> dict:
    ident, name, maker, first, rotor, occupants, _range, _engine, icao, zh, en, ja, _source = row
    return {"id": ident, "name": name, "manufacturer": maker, "category": CATEGORY,
            "firstFlight": first, "span": rotor, "seats": occupants, "tagline": tr(zh, en, ja),
            "thumb": (old or {}).get("thumb", "assets/thumb_nomodel.svg"), "icao": icao, "iata": "",
            **({} if ident == "heli" else {"has3d": False})}


def main() -> None:
    ids = [row[0] for row in AIRCRAFT]
    assert len(ids) == len(set(ids))
    assert all(row[-1].startswith("https://") for row in AIRCRAFT)
    fleet = json.loads(FLEET_PATH.read_text(encoding="utf-8"))
    by_id = {item["id"]: item for item in fleet["aircraft"]}
    old_order = [item["id"] for item in fleet["aircraft"]]
    for row in AIRCRAFT:
        ident = row[0]
        by_id[ident] = fleet_entry(row, by_id.get(ident))
        path = ROOT / "data" / f"{ident}.json"
        if ident == "heli":
            saved = json.loads(path.read_text(encoding="utf-8"))
            saved["title"] = row[1]
            saved["sub"] = tr(row[9], row[10], row[11])
            saved["sources"] = [row[-1]]
        else:
            saved = detail(row)
        path.write_text(json.dumps(saved, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    fleet["aircraft"] = [by_id[ident] for ident in old_order]
    fleet["aircraft"].extend(by_id[ident] for ident in ids if ident not in old_order)
    FLEET_PATH.write_text(json.dumps(fleet, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Added or updated {len(AIRCRAFT)} current civil helicopters.")


if __name__ == "__main__":
    main()
