"""Add current, physically-realized civil business aircraft missing from the archive."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FLEET_PATH = ROOT / "data" / "fleet.json"


def tr(zh: str, en: str, ja: str) -> dict[str, str]:
    return {"zh": zh, "en": en, "ja": ja}


CATEGORY = tr("公務機", "Business aircraft", "ビジネス機")


AIRCRAFT = [
    ("g400", "Gulfstream G400", "Gulfstream", "2024", "26.3 m", "最多 12", "7,778 km (4,200 nmi)", "2 × Pratt & Whitney PW812GA", "GLF4",
     "新世代大型客艙公務機，採主動式側桿與 Symmetry Flight Deck。", "A new-generation large-cabin jet with active-control sidesticks and the Symmetry Flight Deck.", "アクティブ・サイドスティックとSymmetry Flight Deckを備える新世代大型客室機です。", "https://www.gulfstream.com/en/aircraft/gulfstream-g400"),
    ("g500", "Gulfstream G500", "Gulfstream", "2015", "26.3 m", "最多 19", "9,816 km (5,300 nmi)", "2 × Pratt & Whitney PW814GA", "GLF5",
     "強調高速巡航與大型全新客艙的雙發公務機。", "A twinjet combining high-speed cruise with a clean-sheet large cabin.", "高速巡航と新設計の大型客室を両立する双発ビジネスジェットです。", "https://www.gulfstream.com/en/aircraft/gulfstream-g500"),
    ("g600", "Gulfstream G600", "Gulfstream", "2016", "29.0 m", "最多 19", "12,223 km (6,600 nmi)", "2 × Pratt & Whitney PW815GA", "GLF6",
     "G500 的長航程大型客艙姊妹型，可高速跨洲飛行。", "The longer-range large-cabin sister model to the G500 for fast intercontinental travel.", "G500の長距離型にあたる大型客室機で、高速大陸間飛行に対応します。", "https://www.gulfstream.com/en/aircraft/gulfstream-g600"),
    ("g700", "Gulfstream G700", "Gulfstream", "2020", "31.4 m", "最多 19", "14,353 km (7,750 nmi)", "2 × Rolls-Royce Pearl 700", "GLF7",
     "具多個生活區與超長程能力的 Gulfstream 大型旗艦。", "A Gulfstream flagship with multiple living areas and ultra-long-range capability.", "複数の居住区画と超長距離性能を持つガルフストリームの旗艦機です。", "https://www.gulfstream.com/en/aircraft/gulfstream-g700"),
    ("g800", "Gulfstream G800", "Gulfstream", "2022", "31.4 m", "最多 19", "15,186 km (8,200 nmi)", "2 × Rolls-Royce Pearl 700", "GLF8",
     "以 8,200 海里級航程為主軸的 Gulfstream 最長程機型。", "Gulfstream's longest-range model, centered on an 8,200-nautical-mile mission.", "8,200海里級の航続距離を持つガルフストリーム最長距離型です。", "https://www.gulfstream.com/en/aircraft/gulfstream-g800/"),
    ("cl3500", "Bombardier Challenger 3500", "Bombardier", "—", "21.0 m", "最多 10", "6,297 km (3,400 nmi)", "2 × Honeywell HTF7350", "CL35",
     "Challenger 350 平台的最新客艙與航電升級型。", "The latest cabin and avionics evolution of the Challenger 350 platform.", "Challenger 350を基礎に客室とアビオニクスを刷新した型です。", "https://bombardier.com/en/aircraft/challenger-3500"),
    ("cl650", "Bombardier Challenger 650", "Bombardier", "—", "19.6 m", "最多 12", "7,408 km (4,000 nmi)", "2 × General Electric CF34-3B", "CL60",
     "以寬敞客艙、成熟系統與洲際航程見長的大型公務機。", "A large business jet known for its wide cabin, mature systems, and transcontinental range.", "広い客室、実績あるシステム、大陸横断性能を特徴とする大型ビジネスジェットです。", "https://bombardier.com/en/aircraft/challenger-650"),
    ("global5500", "Bombardier Global 5500", "Bombardier", "2018", "28.7 m", "最多 16", "10,556 km (5,700 nmi)", "2 × Rolls-Royce Pearl 15", "GL5T",
     "採 Pearl 15 與新翼的 Global 中長程型。", "A Global-family long-range model with Pearl 15 engines and a redesigned wing.", "Pearl 15と新設計主翼を備えるGlobalファミリーの長距離型です。", "https://bombardier.com/en/aircraft/global-5500"),
    ("global6500", "Bombardier Global 6500", "Bombardier", "2018", "28.7 m", "最多 17", "12,223 km (6,600 nmi)", "2 × Rolls-Royce Pearl 15", "GL6T",
     "Global 5500 的加長航程姊妹型，兼顧高速與大型客艙。", "The longer-range sister to the Global 5500, combining speed with a large cabin.", "Global 5500の長距離姉妹型で、高速性能と大型客室を両立します。", "https://bombardier.com/en/aircraft/global-6500"),
    ("global7500", "Bombardier Global 7500", "Bombardier", "2016", "31.7 m", "最多 19", "14,260 km (7,700 nmi)", "2 × General Electric Passport", "GL7T",
     "四個獨立生活區與超長程航程的 Bombardier 旗艦。", "Bombardier's ultra-long-range flagship with four distinct living spaces.", "4つの独立した居住区画を備えるボンバルディアの超長距離旗艦機です。", "https://bombardier.com/en/aircraft/global-7500"),
    ("global8000", "Bombardier Global 8000", "Bombardier", "—", "31.7 m", "最多 19", "14,816 km (8,000 nmi)", "2 × General Electric Passport", "GL7T",
     "由 Global 7500 發展、提高航程與速度性能的超長程型。", "An ultra-long-range evolution of the Global 7500 with greater range and speed.", "Global 7500から航続距離と速度を高めた超長距離型です。", "https://bombardier.com/en/aircraft/global-8000"),
    ("f2000lxs", "Dassault Falcon 2000LXS", "Dassault", "—", "21.4 m", "8–10", "7,408 km (4,000 nmi)", "2 × Pratt & Whitney Canada PW308C", "F2TH",
     "雙發寬客艙 Falcon，兼顧短場性能與洲際航程。", "A wide-cabin twin-engine Falcon balancing short-field capability and intercontinental range.", "短距離性能と大陸間航続距離を両立する広胴双発Falconです。", "https://www.dassaultfalcon.com/aircraft/falcon-2000lxs/"),
    ("f900lx", "Dassault Falcon 900LX", "Dassault", "—", "21.4 m", "最多 14", "8,800 km (4,750 nmi)", "3 × Honeywell TFE731-60", "F900",
     "採三發配置與翼尖小翼的成熟大型 Falcon。", "A mature large-cabin Falcon distinguished by three engines and winglets.", "3発配置とウイングレットを特徴とする実績豊富な大型Falconです。", "https://www.dassaultfalcon.com/aircraft/falcon-900lx/"),
    ("f6x", "Dassault Falcon 6X", "Dassault", "2017", "25.9 m", "最多 16", "10,186 km (5,500 nmi)", "2 × Pratt & Whitney Canada PW812D", "FA6X",
     "具有超寬客艙與數位飛控的新世代雙發 Falcon。", "A new-generation twin-engine Falcon with an extra-wide cabin and digital flight controls.", "超広幅客室とデジタル飛行制御を備える新世代双発Falconです。", "https://www.dassaultfalcon.com/aircraft/falcon-6x/"),
    ("f8x", "Dassault Falcon 8X", "Dassault", "2015", "26.3 m", "最多 16", "11,945 km (6,450 nmi)", "3 × Pratt & Whitney Canada PW307D", "FA8X",
     "長客艙、三發與遠程能力兼具的 Falcon 旗艦之一。", "A long-cabin, three-engine Falcon combining range with flexible airport access.", "長い客室、3発、長距離性能を併せ持つFalconの旗艦機です。", "https://www.dassaultfalcon.com/aircraft/falcon-8x/"),
    ("f10x", "Dassault Falcon 10X", "Dassault", "—", "33.6 m", "最多 19", "13,890 km (7,500 nmi)", "2 × Rolls-Royce Pearl 10X", "", 
     "已完成實體出廠展示、採超寬客艙與複合材料機翼的次世代 Falcon。", "A rolled-out next-generation Falcon with an exceptionally wide cabin and composite wing.", "実機ロールアウト済みで、超広幅客室と複合材主翼を備える次世代Falconです。", "https://www.dassaultfalcon.com/aircraft/falcon-10x/"),
    ("phenom100ex", "Embraer Phenom 100EX", "Embraer", "—", "12.3 m", "最多 7", "2,182 km (1,178 nmi)", "2 × Pratt & Whitney Canada PW617F1-E", "E50P",
     "可單人駕駛的入門級雙發公務噴射機。", "A single-pilot-capable entry-level twin-engine business jet.", "単独操縦に対応するエントリー級双発ビジネスジェットです。", "https://embraer.com/executive-jets/phenom-100ex/en/"),
    ("phenom300ev", "Embraer Phenom 300EV", "Embraer", "—", "15.9 m", "最多 10", "3,723 km (2,010 nmi)", "2 × Pratt & Whitney Canada PW535E1", "E55P",
     "以高速、單人駕駛能力與自動油門為重點的輕型公務機。", "A light business jet focused on speed, single-pilot operation, and autothrottle capability.", "高速性能、単独操縦、自動推力制御を特徴とするライトジェットです。", "https://embraer.com/executive-jets/phenom-300ev/en/"),
    ("praetor500e", "Embraer Praetor 500E", "Embraer", "—", "20.7 m", "最多 9", "6,186 km (3,340 nmi)", "2 × Honeywell HTF7500E", "E545",
     "具線傳飛控與主動亂流抑制的中型公務機。", "A midsize business jet with fly-by-wire controls and active turbulence reduction.", "フライ・バイ・ワイヤと能動乱気流低減を備える中型ビジネスジェットです。", "https://embraer.com/executive-jets/praetor-500e/en/"),
    ("praetor600e", "Embraer Praetor 600E", "Embraer", "—", "21.5 m", "最多 12", "7,441 km (4,018 nmi)", "2 × Honeywell HTF7500E", "E550",
     "Praetor 家族的超中型長程型，可執行跨大西洋任務。", "The super-midsize, longer-range Praetor capable of transatlantic missions.", "大西洋横断に対応するPraetorファミリーのスーパー・ミッドサイズ長距離型です。", "https://embraer.com/executive-jets/praetor-600e/en/"),
    ("citationm2", "Cessna Citation M2 Gen3", "Cessna", "—", "14.4 m", "最多 7", "2,871 km (1,550 nmi)", "2 × Williams FJ44-1AP", "C25M",
     "配備 Garmin G3000、Autoland 與自動油門的入門 Citation。", "An entry-level Citation with Garmin G3000, Autoland, and autothrottles.", "Garmin G3000、Autoland、自動推力制御を備える入門Citationです。", "https://cessna.txtav.com/en/citation/m2"),
    ("citationcj3", "Cessna Citation CJ3 Gen3", "Cessna", "—", "16.7 m", "最多 9", "3,778 km (2,040 nmi)", "2 × Williams FJ44-3A", "C25B",
     "在 CJ3 平台加入新世代航電、自動油門與緊急自動降落。", "A CJ3 evolution with new-generation avionics, autothrottles, and emergency autoland.", "CJ3に新世代アビオニクス、自動推力制御、緊急自動着陸を加えた型です。", "https://cessna.txtav.com/en/citation/cj3"),
    ("citationcj4", "Cessna Citation CJ4 Gen3", "Cessna", "—", "15.5 m", "最多 10", "4,010 km (2,165 nmi)", "2 × Williams FJ44-4A", "C25C",
     "CJ 家族中航程與性能最高的單人駕駛型。", "The longest-range and highest-performance single-pilot member of the CJ family.", "CJファミリーで最長航続・最高性能の単独操縦対応型です。", "https://cessna.txtav.com/en/citation/cj4"),
    ("citationxls", "Cessna Citation XLS Gen2", "Cessna", "—", "17.2 m", "最多 12", "3,889 km (2,100 nmi)", "2 × Pratt & Whitney Canada PW545C", "C56X",
     "以短場性能和直立客艙見長的中型 Citation 最新升級。", "The latest midsize Citation evolution, known for short-field performance and a stand-up cabin.", "短距離性能と立って移動できる客室を特徴とする中型Citationの最新型です。", "https://cessna.txtav.com/en/citation/xls-gen2"),
    ("citationlat", "Cessna Citation Latitude", "Cessna", "2014", "22.1 m", "最多 9", "5,000 km (2,700 nmi)", "2 × Pratt & Whitney Canada PW306D1", "C68A",
     "以平地板寬客艙為特色的中型 Citation。", "A midsize Citation distinguished by its wide, flat-floor cabin.", "幅広いフラットフロア客室を特徴とする中型Citationです。", "https://cessna.txtav.com/en/citation/latitude"),
    ("citationlong", "Cessna Citation Longitude", "Cessna", "2016", "21.0 m", "最多 12", "6,482 km (3,500 nmi)", "2 × Honeywell HTF7700L", "C700",
     "Citation 家族的超中型旗艦，主打低客艙高度與長航程。", "Citation's super-midsize flagship, emphasizing low cabin altitude and long range.", "低い客室高度と長距離性能を重視するCitationのスーパー・ミッドサイズ旗艦です。", "https://cessna.txtav.com/en/citation/longitude"),
    ("hondajet", "HondaJet Elite II", "Honda Aircraft", "—", "12.1 m", "最多 8", "2,865 km (1,547 nmi)", "2 × GE Honda HF120", "HDJT",
     "採翼上引擎配置、可單人駕駛的輕型公務機。", "A single-pilot light jet distinguished by its over-the-wing engine mounts.", "主翼上面エンジン配置を特徴とする単独操縦対応ライトジェットです。", "https://www.hondajet.com/en/Products/HondaJet-Elite-II"),
    ("visionjet", "Cirrus Vision Jet G3", "Cirrus Aircraft", "—", "11.8 m", "最多 7", "2,361 km (1,275 nmi)", "1 × Williams FJ33", "SF50",
     "單發個人噴射機，具整機降落傘與 Safe Return 緊急自動降落。", "A single-engine personal jet with a whole-aircraft parachute and Safe Return emergency autoland.", "機体全体用パラシュートとSafe Return緊急自動着陸を備える単発パーソナルジェットです。", "https://cirrusaircraft.com/aircraft/vision-jet/"),
    ("pc24", "Pilatus PC-24", "Pilatus", "2015", "17.0 m", "最多 11", "3,704 km (2,000 nmi)", "2 × Williams FJ44-4A", "PC24",
     "可使用短小、甚至部分非鋪裝跑道的雙發公務噴射機。", "A twin-engine business jet designed for short and selected unpaved runways.", "短距離および一部未舗装滑走路に対応する双発ビジネスジェットです。", "https://www.pilatus-aircraft.com/en/fly/pc-24"),
    ("acj220", "Airbus ACJ TwoTwenty", "Airbus Corporate Jets", "2020", "35.1 m", "最多 19", "10,463 km (5,650 nmi)", "2 × Pratt & Whitney PW1500G", "BCS3",
     "以 A220-100 平台打造、具有多個生活區的大型商務機。", "A large business aircraft based on the A220-100 platform with multiple living areas.", "A220-100を基礎に複数の居住区画を備えた大型ビジネス機です。", "https://www.acj.airbus.com/en/exclusive-aircraft/acj-twotwenty"),
]


def detail(row: tuple[str, ...]) -> dict:
    ident, name, _manufacturer, first_flight, span, seats, range_, engine, _icao, zh, en, ja, source = row
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
    ident, name, manufacturer, first_flight, span, seats, _range, _engine, icao, zh, en, ja, _source = row
    return {
        "id": ident, "name": name, "manufacturer": manufacturer, "category": CATEGORY,
        "firstFlight": first_flight, "span": span, "seats": seats, "tagline": tr(zh, en, ja),
        "thumb": "assets/thumb_nomodel.svg", "icao": icao, "iata": "", "has3d": False,
    }


def main() -> None:
    ids = [row[0] for row in AIRCRAFT]
    assert len(ids) == len(set(ids))
    assert all(row[-1].startswith("https://") for row in AIRCRAFT)
    fleet = json.loads(FLEET_PATH.read_text(encoding="utf-8"))
    by_id = {item["id"]: item for item in fleet["aircraft"]}
    old_order = [item["id"] for item in fleet["aircraft"]]
    for row in AIRCRAFT:
        by_id[row[0]] = fleet_entry(row)
        (ROOT / "data" / f"{row[0]}.json").write_text(
            json.dumps(detail(row), ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
    fleet["aircraft"] = [by_id[ident] for ident in old_order]
    fleet["aircraft"].extend(by_id[ident] for ident in ids if ident not in old_order)
    FLEET_PATH.write_text(json.dumps(fleet, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Added or updated {len(AIRCRAFT)} current business aircraft.")


if __name__ == "__main__":
    main()
