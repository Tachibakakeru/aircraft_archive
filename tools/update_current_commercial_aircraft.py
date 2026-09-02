"""Add current-production civil transport aircraft that are missing from the archive."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FLEET_PATH = ROOT / "data" / "fleet.json"


def tr(zh: str, en: str, ja: str) -> dict[str, str]:
    return {"zh": zh, "en": en, "ja": ja}


CATEGORIES = {
    "narrow": tr("窄體客機", "Narrow-body", "ナローボディ"),
    "wide": tr("廣體客機", "Wide-body", "ワイドボディ"),
    "regional": tr("區域客機", "Regional airliner", "リージョナル旅客機"),
    "turboprop": tr("渦輪螺旋槳", "Turboprop", "ターボプロップ"),
    "cargo": tr("貨機", "Freighter", "貨物機"),
    "utility": tr("通用運輸機", "Utility transport", "汎用輸送機"),
}


AIRCRAFT = [
    # id, name, manufacturer, category, first flight, span, seats/payload,
    # range, engine, ICAO, IATA, zh, en, ja, official source
    ("a319n", "Airbus A319neo", "Airbus", "narrow", "2017", "35.8 m", "120–150", "6,950 km (3,750 nmi)", "2 × CFM LEAP-1A / Pratt & Whitney PW1100G-JM", "A19N", "319",
     "A320neo 家族的短機身型，兼顧較低需求航線與長程能力。", "The short-fuselage A320neo-family member, combining lower-capacity economics with long-range capability.", "A320neoファミリーの短胴型で、低需要路線と長距離性能を両立します。", "https://www.airbus.com/en/products-services/commercial-aircraft/passenger-aircraft/a320-family"),
    ("a320n", "Airbus A320neo", "Airbus", "narrow", "2014", "35.8 m", "150–180", "6,300 km (3,400 nmi)", "2 × CFM LEAP-1A / Pratt & Whitney PW1100G-JM", "A20N", "32N",
     "換裝新世代引擎與 Sharklet 的 A320 主力新世代型。", "The core new-generation A320 variant with new engines and Sharklets.", "新世代エンジンとシャークレットを備えるA320の主力型です。", "https://www.airbus.com/en/products-services/commercial-aircraft/passenger-aircraft/a320-family"),
    ("a321n", "Airbus A321neo", "Airbus", "narrow", "2016", "35.8 m", "180–220", "7,400 km (4,000 nmi)", "2 × CFM LEAP-1A / Pratt & Whitney PW1100G-JM", "A21N", "32Q",
     "A320neo 家族的加長高容量型，可執行中長程單走道航線。", "The stretched, high-capacity A320neo-family member for medium- and long-range single-aisle routes.", "A320neoファミリーの長胴・大容量型で、中長距離路線に対応します。", "https://www.airbus.com/en/products-services/commercial-aircraft/passenger-aircraft/a320-family"),
    ("a321xlr", "Airbus A321XLR", "Airbus", "narrow", "2022", "35.8 m", "180–220", "8,700 km (4,700 nmi)", "2 × CFM LEAP-1A / Pratt & Whitney PW1100G-JM", "A21N", "32Q",
     "增設中央油箱與強化起落架的超長程 A321neo 衍生型。", "The extra-long-range A321neo derivative with an integrated centre tank and reinforced landing gear.", "中央燃料タンクと強化降着装置を備えたA321neoの超長距離型です。", "https://www.airbus.com/en/products-services/commercial-aircraft/passenger-aircraft/a320-family"),
    ("a338", "Airbus A330-800", "Airbus", "wide", "2018", "64.0 m", "220–260", "15,000 km (8,100 nmi)", "2 × Rolls-Royce Trent 7000", "A338", "338",
     "A330neo 家族的短機身長航程型，採 Trent 7000 與新翼尖。", "The shorter, longer-range A330neo with Trent 7000 engines and new wingtip devices.", "Trent 7000と新型翼端を備えるA330neoの短胴・長距離型です。", "https://www.airbus.com/en/products-services/commercial-aircraft/passenger-aircraft/a330-family"),
    ("a339", "Airbus A330-900", "Airbus", "wide", "2017", "64.0 m", "260–300", "13,600 km (7,350 nmi)", "2 × Rolls-Royce Trent 7000", "A339", "339",
     "A330neo 家族主力型，在 A330-300 尺寸上導入新翼與新引擎。", "The principal A330neo variant, adding a new wing and engines to the A330-300-sized airframe.", "A330-300級の機体に新主翼と新エンジンを導入したA330neoの主力型です。", "https://www.airbus.com/en/products-services/commercial-aircraft/passenger-aircraft/a330-family"),
    ("a35k", "Airbus A350-1000", "Airbus", "wide", "2016", "64.75 m", "350–410", "16,100 km (8,700 nmi)", "2 × Rolls-Royce Trent XWB-97", "A35K", "351",
     "A350 家族的加長高容量型，配備推力更大的 Trent XWB-97。", "The stretched, higher-capacity A350 powered by the higher-thrust Trent XWB-97.", "高推力Trent XWB-97を搭載するA350の長胴・大容量型です。", "https://www.airbus.com/en/products-services/commercial-aircraft/passenger-aircraft/a350-family"),
    ("belugaxl", "Airbus BelugaXL", "Airbus", "cargo", "2018", "60.3 m", "最大酬載 51 t", "4,000 km (2,200 nmi)", "2 × Rolls-Royce Trent 700", "A337", "",
     "以 A330-200F 為基礎的大型超尺寸零件運輸機，服務 Airbus 生產網路。", "An outsized-component transporter based on the A330-200F for Airbus industrial logistics.", "A330-200Fを基礎とし、エアバスの大型部品輸送に使われる特殊貨物機です。", "https://www.airbus.com/en/products-services/commercial-aircraft/beluga"),
    ("b37m", "Boeing 737 MAX 7", "Boeing", "narrow", "2018", "35.9 m", "138–153", "7,130 km (3,850 nmi)", "2 × CFM LEAP-1B", "B37M", "7M7",
     "737 MAX 家族的短機身長航程型，承接 737-700 級距市場。", "The short-fuselage, long-range 737 MAX member succeeding the 737-700 size class.", "737-700級市場を継ぐ737 MAXの短胴・長距離型です。", "https://www.boeing.com/commercial/737max"),
    ("b38m", "Boeing 737 MAX 8", "Boeing", "narrow", "2016", "35.9 m", "162–178", "6,480 km (3,500 nmi)", "2 × CFM LEAP-1B", "B38M", "7M8",
     "737 MAX 家族的主力型，採 LEAP-1B 與 Advanced Technology 翼尖小翼。", "The core 737 MAX variant with LEAP-1B engines and Advanced Technology winglets.", "LEAP-1BとAdvanced Technologyウイングレットを備える737 MAXの主力型です。", "https://www.boeing.com/commercial/737max"),
    ("b39m", "Boeing 737 MAX 9", "Boeing", "narrow", "2017", "35.9 m", "178–193", "6,110 km (3,300 nmi)", "2 × CFM LEAP-1B", "B39M", "7M9",
     "737 MAX 8 的加長型，提高座位與貨艙容量。", "A stretched 737 MAX 8 derivative with greater seating and cargo capacity.", "737 MAX 8を延長し、座席数と貨物容量を増やした型です。", "https://www.boeing.com/commercial/737max"),
    ("b3xm", "Boeing 737 MAX 10", "Boeing", "narrow", "2021", "35.9 m", "188–204", "5,740 km (3,100 nmi)", "2 × CFM LEAP-1B", "B3XM", "7MJ",
     "737 MAX 家族最長、容量最大的型號，採改良式主起落架。", "The longest and highest-capacity 737 MAX, with revised main landing gear geometry.", "737 MAXで最長・最大容量の型で、改良型主脚を採用します。", "https://www.boeing.com/commercial/737max"),
    ("b779", "Boeing 777-9", "Boeing", "wide", "2020", "71.8 m（地面折翼 64.8 m）", "約 426", "13,500 km (7,285 nmi)", "2 × General Electric GE9X", "B779", "779",
     "777X 家族的大型客機，採複合材料機翼、折疊翼尖與 GE9X。", "The large 777X passenger model with a composite wing, folding tips, and GE9X engines.", "複合材主翼、折り畳み翼端、GE9Xを備える777Xの大型旅客型です。", "https://www.boeing.com/commercial/777x"),
    ("b78x", "Boeing 787-10", "Boeing", "wide", "2017", "60.1 m", "約 336", "11,730 km (6,330 nmi)", "2 × GEnx-1B / Rolls-Royce Trent 1000", "B78X", "781",
     "787 家族最長、載客量最高的型號，適合高需求中長程航線。", "The longest and highest-capacity 787, optimized for high-demand medium- and long-haul routes.", "787で最長・最大容量の型で、需要の高い中長距離路線向けです。", "https://www.boeing.com/commercial/787"),
    ("b763f", "Boeing 767-300F", "Boeing", "cargo", "1995", "47.6 m", "最大酬載約 52.5 t", "6,025 km (3,255 nmi)", "2 × General Electric CF6-80C2", "B763", "76Y",
     "目前仍列於 Boeing 貨機產品線的中型雙發貨機。", "A medium twin-engine freighter that remains in Boeing's commercial product lineup.", "ボーイングの製品群に残る中型双発貨物機です。", "https://www.boeing.com/commercial/freighters"),
    ("b77f", "Boeing 777 Freighter", "Boeing", "cargo", "2008", "64.8 m", "最大酬載約 102 t", "9,200 km (4,970 nmi)", "2 × General Electric GE90-110B1L", "B77L", "77X",
     "以 777-200LR 為基礎的長程大型雙發貨機。", "A long-range large twin-engine freighter derived from the 777-200LR.", "777-200LRを基礎とする長距離大型双発貨物機です。", "https://www.boeing.com/commercial/freighters"),
    ("e175", "Embraer E175", "Embraer", "regional", "2003", "26.0 m", "76–88", "4,074 km (2,200 nmi)", "2 × General Electric CF34-8E", "E75L", "E75",
     "E-Jet 家族廣泛使用的支線型，主打 70 至 80 席級市場。", "A widely used E-Jet regional model serving the 70- to 80-seat market.", "70～80席市場で広く使われるE-Jetのリージョナル型です。", "https://www.embraercommercialaviation.com/commercial-jets/e175/"),
    ("e190e2", "Embraer E190-E2", "Embraer", "regional", "2016", "33.7 m", "97–114", "5,278 km (2,850 nmi)", "2 × Pratt & Whitney PW1900G", "E290", "290",
     "第二代 E-Jet 中型支線客機，採新機翼與齒輪傳動渦扇。", "The mid-size second-generation E-Jet with a new wing and geared turbofans.", "新主翼とギヤードターボファンを採用する第2世代E-Jetの中型機です。", "https://www.embraercommercialaviation.com/commercial-jets/e190-e2/"),
    ("e195e2", "Embraer E195-E2", "Embraer", "regional", "2017", "35.1 m", "120–146", "5,556 km (3,000 nmi)", "2 × Pratt & Whitney PW1900G", "E295", "295",
     "E2 家族最大型，座位容量接近小型主線窄體客機。", "The largest E2-family aircraft, approaching small mainline narrow-body capacity.", "小型幹線ナローボディに近い容量を持つE2ファミリー最大型です。", "https://www.embraercommercialaviation.com/commercial-jets/e195-e2/"),
    ("atr72", "ATR 72-600", "ATR", "turboprop", "2009", "27.1 m", "68–78", "1,370 km (740 nmi)", "2 × Pratt & Whitney Canada PW127XT-M", "AT76", "ATR",
     "ATR 家族的高容量渦輪螺旋槳支線客機。", "The higher-capacity turboprop regional airliner in the ATR family.", "ATRファミリーの大容量ターボプロップ・リージョナル機です。", "https://www.atr-aircraft.com/our-aircraft/atr-72-600/"),
    ("atr72f", "ATR 72-600F", "ATR", "cargo", "2020", "27.1 m", "最大酬載約 9.2 t", "1,528 km (825 nmi)", "2 × Pratt & Whitney Canada PW127M", "AT76", "",
     "原廠新造、配備大型貨門的 ATR 72 專用貨機。", "A purpose-built ATR 72 freighter with a large main-deck cargo door.", "大型貨物扉を備える新造ATR 72専用貨物機です。", "https://www.atr-aircraft.com/our-aircraft/atr-72-600f-freighter/"),
    ("dhc6-400", "De Havilland Canada DHC-6 Twin Otter Series 400", "De Havilland Canada", "utility", "2008", "19.8 m", "最多 19", "1,435 km (775 nmi)", "2 × Pratt & Whitney Canada PT6A-34", "DHC6", "DHT",
     "可裝輪式、浮筒或雪橇起落架的短場多用途雙發渦槳機。", "A short-field twin turboprop utility aircraft available with wheels, floats, or skis.", "車輪・フロート・スキーに対応する短距離離着陸用の双発多用途ターボプロップです。", "https://dehavilland.com/twin-otter/"),
    ("c408", "Cessna 408 SkyCourier", "Cessna", "utility", "2020", "22.0 m", "19 或 3 個 LD3 貨櫃", "1,704 km (920 nmi)", "2 × Pratt & Whitney Canada PT6A-65SC", "C408", "",
     "可快速切換客運與貨運任務的高翼雙發通勤運輸機。", "A high-wing twin turboprop commuter designed for passenger and freighter missions.", "旅客・貨物任務に対応する高翼双発コミューター輸送機です。", "https://cessna.txtav.com/en/turboprop/skycourier"),
    ("l410ng", "Aircraft Industries L 410 NG", "Aircraft Industries", "utility", "2015", "20.0 m", "最多 19", "2,570 km", "2 × GE Aerospace H85-200", "L410", "L4T",
     "L 410 家族的現代化短場通勤機，採新翼、玻璃座艙與 H85 引擎。", "The modernized short-field L 410 with a new wing, glass cockpit, and H85 engines.", "新主翼、グラスコックピット、H85エンジンを備えるL 410の近代化型です。", "https://www.let.cz/en/l410ng"),
]


def detail(row: tuple[str, ...]) -> dict:
    (ident, name, manufacturer, category, first_flight, span, seats, range_, engine,
     _icao, _iata, zh, en, ja, source) = row
    return {
        "title": name,
        "sub": tr(zh, en, ja),
        "sources": [source],
        "specifications": {
            "機組員與載客": [["典型載客量", seats], ["首飛年份", first_flight]],
            "尺寸": [["翼展", span]],
            "性能": [["飛行距離（滿載）", range_]],
            "發動機": [["型號", engine]],
        },
    }


def fleet_entry(row: tuple[str, ...]) -> dict:
    (ident, name, manufacturer, category, first_flight, span, seats, _range, _engine,
     icao, iata, zh, en, ja, _source) = row
    return {
        "id": ident,
        "name": name,
        "manufacturer": manufacturer,
        "category": CATEGORIES[category],
        "firstFlight": first_flight,
        "span": span,
        "seats": seats,
        "tagline": tr(zh, en, ja),
        "thumb": "assets/thumb_nomodel.svg",
        "icao": icao,
        "iata": iata,
        "has3d": False,
    }


def main() -> None:
    ids = [row[0] for row in AIRCRAFT]
    assert len(ids) == len(set(ids)), "duplicate aircraft id"
    assert all(row[-1].startswith("https://") for row in AIRCRAFT), "official source required"

    fleet = json.loads(FLEET_PATH.read_text(encoding="utf-8"))
    by_id = {item["id"]: item for item in fleet["aircraft"]}
    for row in AIRCRAFT:
        ident = row[0]
        by_id[ident] = fleet_entry(row)
        (ROOT / "data" / f"{ident}.json").write_text(
            json.dumps(detail(row), ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )

    old_order = [item["id"] for item in fleet["aircraft"]]
    fleet["aircraft"] = [by_id[ident] for ident in old_order]
    fleet["aircraft"].extend(by_id[ident] for ident in ids if ident not in old_order)
    FLEET_PATH.write_text(json.dumps(fleet, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    assert all((ROOT / "data" / f"{ident}.json").exists() for ident in ids)
    print(f"Added or updated {len(AIRCRAFT)} current civil transport aircraft.")


if __name__ == "__main__":
    main()
