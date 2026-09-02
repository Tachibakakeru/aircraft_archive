"""Add current major-manufacturer piston and turboprop civil aircraft."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FLEET_PATH = ROOT / "data" / "fleet.json"


def tr(zh: str, en: str, ja: str) -> dict[str, str]:
    return {"zh": zh, "en": en, "ja": ja}


CATEGORIES = {
    "piston": tr("活塞通用航空", "Piston general aviation", "ピストン一般航空"),
    "turboprop": tr("渦輪螺旋槳", "Turboprop", "ターボプロップ"),
    "trainer": tr("飛行訓練機", "Flight trainer", "飛行訓練機"),
    "utility": tr("通用運輸機", "Utility transport", "汎用輸送機"),
}


# id, name, maker, category, first flight, span, occupants, range, engine, ICAO,
# zh/en/ja summary, official source
AIRCRAFT = [
    ("c172", "Cessna 172 Skyhawk", "Cessna", "trainer", "1955", "11.0 m", "最多 4", "1,185 km (640 nmi)", "1 × Lycoming IO-360-L2A", "C172", "全球最普及的四座單發訓練與旅行機之一。", "One of the world's most widely used four-seat single-engine trainers and touring aircraft.", "世界で最も広く使われる4座単発練習・旅行機の一つです。", "https://cessna.txtav.com/en/piston/skyhawk"),
    ("c182", "Cessna 182 Skylane", "Cessna", "piston", "1956", "11.2 m", "最多 4", "1,695 km (915 nmi)", "1 × Lycoming IO-540-AB1A5", "C182", "具固定起落架與較高酬載能力的四座高翼旅行機。", "A four-seat high-wing touring aircraft with fixed gear and greater payload capability.", "固定脚と高い搭載力を持つ4座高翼旅行機です。", "https://cessna.txtav.com/en/piston/skylane"),
    ("c182t", "Cessna Turbo Skylane", "Cessna", "piston", "—", "11.2 m", "最多 4", "1,798 km (971 nmi)", "1 × Lycoming TIO-540-AK1A", "C182", "渦輪增壓 Skylane，提升高空與高溫機場性能。", "The turbocharged Skylane, improving high-altitude and hot-weather performance.", "高高度・高温条件での性能を高めたターボ過給Skylaneです。", "https://cessna.txtav.com/en/piston/turbo-skylane"),
    ("c206", "Cessna Turbo Stationair HD", "Cessna", "utility", "—", "11.0 m", "最多 6", "1,302 km (703 nmi)", "1 × Lycoming TIO-540-AJ1A", "C206", "具大型艙門、六座與高有效載重的單發多用途機。", "A six-seat single-engine utility aircraft with large doors and a high useful load.", "大型扉、6座、高い有効搭載量を持つ単発多用途機です。", "https://cessna.txtav.com/en/piston/turbo-stationair-hd"),
    ("c208", "Cessna Caravan", "Cessna", "utility", "1982", "15.9 m", "最多 14", "1,982 km (1,070 nmi)", "1 × Pratt & Whitney Canada PT6A-114A", "C208", "可在簡易跑道運作、兼顧客貨任務的單發渦槳機。", "A single-engine turboprop for passenger and cargo work from austere airstrips.", "簡易滑走路で旅客・貨物任務に使える単発ターボプロップです。", "https://cessna.txtav.com/en/turboprop/caravan"),
    ("c208b", "Cessna Grand Caravan EX", "Cessna", "utility", "—", "15.9 m", "最多 14", "1,689 km (912 nmi)", "1 × Pratt & Whitney Canada PT6A-140", "C208", "Caravan 的加長高功率型，增加客艙與貨運能力。", "The stretched, higher-powered Caravan with greater cabin and cargo capability.", "客室と貨物能力を高めたCaravanの長胴・高出力型です。", "https://cessna.txtav.com/en/turboprop/grand-caravan-ex"),
    ("bonanza", "Beechcraft Bonanza G36", "Beechcraft", "piston", "—", "10.2 m", "最多 6", "1,704 km (920 nmi)", "1 × Continental IO-550-B", "BE36", "V 尾早期家族後續發展出的六座傳統尾翼單發旅行機。", "A six-seat conventional-tail single-engine tourer descended from the historic Bonanza family.", "歴史あるBonanza系列から発展した6座・通常尾翼の単発旅行機です。", "https://beechcraft.txtav.com/en/bonanza-g36"),
    ("baron", "Beechcraft Baron G58", "Beechcraft", "piston", "—", "11.5 m", "最多 6", "2,741 km (1,480 nmi)", "2 × Continental IO-550-C", "BE58", "六座雙發活塞旅行機，具玻璃座艙與較高巡航性能。", "A six-seat twin-piston tourer with a glass cockpit and strong cruise performance.", "グラスコックピットと高い巡航性能を備える6座双発ピストン機です。", "https://beechcraft.txtav.com/en/baron-g58"),
    ("kingair260", "Beechcraft King Air 260", "Beechcraft", "turboprop", "—", "17.7 m", "最多 9", "3,185 km (1,720 nmi)", "2 × Pratt & Whitney Canada PT6A-52", "BE20", "King Air 家族的小型雙發加壓渦槳機。", "The smaller pressurized twin-turboprop in the current King Air family.", "現行King Airファミリーの小型加圧双発ターボプロップです。", "https://beechcraft.txtav.com/en/king-air-260"),
    ("kingair360", "Beechcraft King Air 360", "Beechcraft", "turboprop", "—", "17.7 m", "最多 11", "3,345 km (1,806 nmi)", "2 × Pratt & Whitney Canada PT6A-60A", "B350", "King Air 旗艦標準型，強調加壓客艙與多任務能力。", "The standard King Air flagship, emphasizing a pressurized cabin and multi-mission utility.", "加圧客室と多用途性を重視するKing Airの標準旗艦型です。", "https://beechcraft.txtav.com/en/king-air-360"),
    ("kingair360er", "Beechcraft King Air 360ER", "Beechcraft", "turboprop", "—", "17.7 m", "最多 11", "4,985 km (2,692 nmi)", "2 × Pratt & Whitney Canada PT6A-60A", "B350", "增加燃油與航程、常用於特種任務的 King Air 360 衍生型。", "An extended-range King Air 360 derivative often used for special missions.", "燃料搭載量と航続距離を増やし、特殊任務にも使われるKing Air 360派生型です。", "https://beechcraft.txtav.com/en/king-air-360er"),
    ("denali", "Beechcraft Denali", "Beechcraft", "turboprop", "2021", "16.5 m", "最多 11", "2,963 km (1,600 nmi)", "1 × GE Aerospace Catalyst", "", "採全新 Catalyst 引擎與大型客艙的單發加壓渦槳機。", "A pressurized single-engine turboprop with a clean-sheet Catalyst engine and large cabin.", "新設計Catalystエンジンと大型客室を備える加圧単発ターボプロップです。", "https://beechcraft.txtav.com/en/denali"),
    ("m700", "Piper M700 Fury", "Piper", "turboprop", "—", "13.1 m", "最多 6", "3,430 km (1,852 nmi)", "1 × Pratt & Whitney Canada PT6A-52", "P46T", "具 700 shp、Autoland 與加壓客艙的 Piper M-Class 旗艦。", "Piper's M-Class flagship with 700 shp, Autoland, and a pressurized cabin.", "700 shp、Autoland、加圧客室を備えるPiper M-Classの旗艦です。", "https://www.piper.com/model/m700-fury/"),
    ("m500", "Piper M500", "Piper", "turboprop", "—", "13.1 m", "最多 6", "1,852 km (1,000 nmi)", "1 × Pratt & Whitney Canada PT6A-42A", "P46T", "以操作效率與加壓舒適性為主的單發渦槳 M-Class。", "A pressurized M-Class single turboprop focused on operating efficiency.", "運用効率と加圧快適性を重視するM-Class単発ターボプロップです。", "https://www.piper.com/model/m500/"),
    ("m350", "Piper M350", "Piper", "piston", "—", "13.1 m", "最多 6", "2,487 km (1,343 nmi)", "1 × Lycoming TIO-540-AE2A", "PA46", "少數仍提供加壓客艙的單發活塞旅行機之一。", "One of the few current single-engine piston touring aircraft with a pressurized cabin.", "現行機では数少ない加圧客室付き単発ピストン旅行機です。", "https://www.piper.com/model/m350/"),
    ("archerlx", "Piper Archer LX", "Piper", "piston", "—", "10.7 m", "最多 4", "967 km (522 nmi)", "1 × Lycoming IO-360-B4A", "P28A", "PA-28 家族的現代四座私人旅行型。", "The modern four-seat personal touring member of the PA-28 family.", "PA-28ファミリーの現代的な4座個人旅行型です。", "https://www.piper.com/model/archer-lx/"),
    ("archerdx", "Piper Archer DX", "Piper", "trainer", "—", "10.7 m", "最多 4", "1,570 km (848 nmi)", "1 × Continental CD-155", "P28A", "使用 Jet A 柴油循環引擎的 Archer 訓練型。", "An Archer training variant powered by a Jet-A-burning compression-ignition engine.", "Jet A対応ディーゼルサイクルエンジンを搭載するArcher練習型です。", "https://www.piper.com/model/archer-dx/"),
    ("pilot100i", "Piper Pilot 100i", "Piper", "trainer", "—", "10.7 m", "最多 3", "967 km (522 nmi)", "1 × Lycoming IO-360-B4A", "P28A", "為飛行學校成本與耐用性設計的三座入門訓練機。", "A three-seat primary trainer designed around flight-school cost and durability.", "飛行学校のコストと耐久性を重視した3座初等練習機です。", "https://www.piper.com/model/pilot-100i/"),
    ("seminole", "Piper Seminole", "Piper", "trainer", "1976", "11.8 m", "最多 4", "1,296 km (700 nmi)", "2 × Lycoming L/O-360-A1H6", "PA44", "廣泛用於多發儀表與商用飛行員訓練的雙發活塞機。", "A twin-piston aircraft widely used for multi-engine, instrument, and commercial-pilot training.", "多発・計器・事業用操縦士訓練に広く使われる双発ピストン機です。", "https://www.piper.com/model/seminole/"),
    ("sr20", "Cirrus SR20 G7+", "Cirrus Aircraft", "piston", "—", "11.7 m", "最多 5", "1,161 km (627 nmi)", "1 × Lycoming IO-390-C3B6", "SR20", "具 CAPS 整機降落傘與 Safe Return 自動降落的入門 SR 系列。", "The entry SR Series model with CAPS whole-aircraft parachute and Safe Return autoland.", "CAPS機体パラシュートとSafe Return自動着陸を備えるSRシリーズ入門型です。", "https://cirrusaircraft.com/aircraft/sr-series/"),
    ("sr22", "Cirrus SR22 G7+", "Cirrus Aircraft", "piston", "—", "11.7 m", "最多 5", "2,165 km (1,169 nmi)", "1 × Continental IO-550-N", "SR22", "高性能自然進氣 SR 系列，結合複合材料機體與整機降落傘。", "The high-performance naturally aspirated SR model with a composite airframe and whole-aircraft parachute.", "複合材機体と機体パラシュートを備える高性能自然吸気SRモデルです。", "https://cirrusaircraft.com/aircraft/sr-series/"),
    ("sr22t", "Cirrus SR22T G7+", "Cirrus Aircraft", "piston", "—", "11.7 m", "最多 5", "1,891 km (1,021 nmi)", "1 × Continental TSIO-550-K", "S22T", "SR22 的渦輪增壓高空型，可在高海拔維持較佳性能。", "The turbocharged high-altitude SR22 variant for stronger performance at elevation.", "高高度で性能を維持しやすいSR22のターボ過給型です。", "https://cirrusaircraft.com/aircraft/sr-series/"),
    ("da20", "Diamond DA20 Series", "Diamond Aircraft", "trainer", "1991", "10.9 m", "最多 2", "1,302 km (703 nmi)", "1 × Rotax 912 iS3c / Continental IO-240", "DV20", "採複合材料機身與座艙罩視野的雙座初級訓練機。", "A two-seat primary trainer with a composite airframe and panoramic canopy.", "複合材機体と広視界キャノピーを持つ2座初等練習機です。", "https://www.diamondaircraft.com/en/private-owners/aircraft/da20/overview/"),
    ("da40", "Diamond DA40 Series", "Diamond Aircraft", "piston", "1997", "11.9 m", "最多 4", "1,730 km (934 nmi)", "1 × Austro AE300 / Lycoming IO-360", "DA40", "四座複合材料旅行與訓練機，可選 Jet A 或 AVGAS 動力。", "A four-seat composite tourer and trainer offered with Jet-A or avgas power.", "Jet AまたはAVGAS動力を選べる4座複合材旅行・練習機です。", "https://www.diamondaircraft.com/en/private-owners/aircraft/da40/overview/"),
    ("da42", "Diamond DA42-VI", "Diamond Aircraft", "piston", "2002", "13.6 m", "最多 4", "2,269 km (1,225 nmi)", "2 × Austro AE300", "DA42", "使用 Jet A 柴油循環引擎的四座複合材料雙發機。", "A four-seat composite twin powered by Jet-A compression-ignition engines.", "Jet A対応ディーゼルサイクルエンジンを搭載する4座複合材双発機です。", "https://www.diamondaircraft.com/en/private-owners/aircraft/da42/overview/"),
    ("da50", "Diamond DA50 RG", "Diamond Aircraft", "piston", "2019", "13.4 m", "最多 5", "1,396 km (754 nmi)", "1 × Continental CD-300", "DA50", "具可收放起落架、五座寬客艙與 Jet A 動力的單發機。", "A five-seat, wide-cabin single with retractable gear and Jet-A power.", "引込脚、5座ワイドキャビン、Jet A動力を備える単発機です。", "https://www.diamondaircraft.com/en/private-owners/aircraft/da50/overview/"),
    ("da62", "Diamond DA62", "Diamond Aircraft", "piston", "2012", "14.6 m", "最多 7", "2,385 km (1,288 nmi)", "2 × Austro AE330", "DA62", "可載七人的大型複合材料雙發活塞旅行機。", "A large composite twin-piston touring aircraft seating up to seven.", "最大7人を収容する大型複合材双発ピストン旅行機です。", "https://www.diamondaircraft.com/en/private-owners/aircraft/da62/overview/"),
    ("tbm910", "Daher TBM 910", "Daher", "turboprop", "—", "12.8 m", "最多 6", "3,204 km (1,730 nmi)", "1 × Pratt & Whitney Canada PT6A-66D", "TBM9", "採 G1000 NXi 的高速單發加壓渦槳機。", "A fast pressurized single turboprop equipped with Garmin G1000 NXi avionics.", "Garmin G1000 NXiを備える高速加圧単発ターボプロップです。", "https://www.daher.com/en/aircraft-manufacturer-turboprop-business-aircraft/"),
    ("tbm960", "Daher TBM 960", "Daher", "turboprop", "—", "12.8 m", "最多 6", "3,204 km (1,730 nmi)", "1 × Pratt & Whitney Canada PT6E-66XT", "TBM9", "具數位引擎與螺旋槳控制、Autoland 的 TBM 旗艦。", "The TBM flagship with digital engine/propeller control and Autoland.", "デジタル式エンジン・プロペラ制御とAutolandを備えるTBM旗艦です。", "https://www.daher.com/en/aircraft-manufacturer-turboprop-business-aircraft/"),
    ("kodiak100", "Daher Kodiak 100 Series III", "Daher", "utility", "—", "13.7 m", "最多 10", "約 1,861 km (1,005 nmi)", "1 × Pratt & Whitney Canada PT6A-34", "K100", "可在粗糙短跑道與水面運作的堅固單發渦槳機。", "A rugged single turboprop for short, rough strips and optional float operations.", "短い未舗装滑走路やフロート運用に対応する堅牢な単発ターボプロップです。", "https://prod-kodiak.daher.com/en/aircraft/kodiak-100"),
    ("kodiak900", "Daher Kodiak 900", "Daher", "utility", "2020", "13.7 m", "最多 10", "2,091 km (1,129 nmi)", "1 × Pratt & Whitney Canada PT6A-140A", "K900", "Kodiak 100 的加長高速型，保留短場與偏遠地區能力。", "A stretched, faster Kodiak retaining short-field and remote-airstrip capability.", "短距離・僻地運用能力を保ちながら延長・高速化したKodiakです。", "https://prod-kodiak.daher.com/en/aircraft/kodiak-900"),
    ("pc12pro", "Pilatus PC-12 PRO", "Pilatus", "turboprop", "—", "16.3 m", "最多 9", "3,269 km (1,765 nmi)", "1 × Pratt & Whitney Canada PT6E-67XP", "PC12", "具大型貨門、非鋪裝跑道能力與新 G3000 Prime 座艙的單發渦槳機。", "A single turboprop with a large cargo door, unpaved-runway capability, and a new G3000 Prime cockpit.", "大型貨物扉、未舗装滑走路能力、新G3000 Primeコックピットを備える単発ターボプロップです。", "https://www.pilatus-aircraft.com/en/pc-12"),
    ("pmentor", "Tecnam P-Mentor", "Tecnam", "trainer", "2022", "8.9 m", "最多 2", "約 1,352 km (730 nmi)", "1 × Rotax 912 iS3c", "PMEN", "為初級、儀表與複雜飛行訓練設計的雙座機。", "A two-seat aircraft designed for primary, instrument, and complex-aircraft training.", "初等・計器・複雑機訓練向けの2座機です。", "https://tecnam.com/aircraft/p-mentor/"),
    ("p2010", "Tecnam P2010", "Tecnam", "piston", "2012", "10.3 m", "最多 4", "最多 2,408 km (1,300 nmi)", "1 × Continental CD-170 / Lycoming IO-360", "P201", "金屬機翼與複合材料機身結合的四座高翼旅行機。", "A four-seat high-wing tourer combining metal wings with a composite fuselage.", "金属主翼と複合材胴体を組み合わせた4座高翼旅行機です。", "https://tecnam.com/aircraft/p2010/"),
    ("p2006t", "Tecnam P2006T NG", "Tecnam", "trainer", "2007", "11.4 m", "最多 4", "1,722 km (930 nmi)", "2 × Rotax 912 iS3c", "P200", "以低油耗 Rotax 引擎為特色的四座輕型雙發訓練機。", "A four-seat light twin trainer distinguished by fuel-efficient Rotax engines.", "低燃費Rotaxエンジンを特徴とする4座軽双発練習機です。", "https://tecnam.com/aircraft/p2006t-ng/"),
    ("p2012", "Tecnam P2012 Traveller", "Tecnam", "utility", "2016", "14.0 m", "最多 11", "1,760 km (950 nmi)", "2 × Lycoming TEO-540-C1A", "P212", "供支線、包機與貨運任務使用的十一座高翼雙發機。", "An eleven-seat high-wing twin for commuter, charter, and cargo missions.", "コミューター、チャーター、貨物任務向けの11座高翼双発機です。", "https://tecnam.com/aircraft/p2012-traveller/"),
    ("p2012stol", "Tecnam P2012 STOL", "Tecnam", "utility", "2022", "14.0 m", "最多 11", "—", "2 × Lycoming TEO-540-C1A", "P212", "針對短跑道與偏遠社區運輸強化的 P2012 衍生型。", "A P2012 derivative optimized for short runways and remote-community transport.", "短い滑走路と遠隔地域輸送向けに最適化したP2012派生型です。", "https://tecnam.com/aircraft/p2012-stol/"),
]


def detail(row: tuple[str, ...]) -> dict:
    ident, name, _maker, _cat, first, span, occupants, range_, engine, _icao, zh, en, ja, source = row
    return {"title": name, "sub": tr(zh, en, ja), "sources": [source], "specifications": {
        "機組員與載客": [["典型載客量", occupants], ["首飛年份", first]],
        "尺寸": [["翼展", span]], "性能": [["飛行距離（滿載）", range_]], "發動機": [["型號", engine]],
    }}


def fleet_entry(row: tuple[str, ...]) -> dict:
    ident, name, maker, cat, first, span, occupants, _range, _engine, icao, zh, en, ja, _source = row
    return {"id": ident, "name": name, "manufacturer": maker, "category": CATEGORIES[cat],
            "firstFlight": first, "span": span, "seats": occupants, "tagline": tr(zh, en, ja),
            "thumb": "assets/thumb_nomodel.svg", "icao": icao, "iata": "", "has3d": False}


def main() -> None:
    ids = [row[0] for row in AIRCRAFT]
    assert len(ids) == len(set(ids))
    assert all(row[-1].startswith("https://") for row in AIRCRAFT)
    fleet = json.loads(FLEET_PATH.read_text(encoding="utf-8"))
    by_id = {item["id"]: item for item in fleet["aircraft"]}
    old_order = [item["id"] for item in fleet["aircraft"]]
    for row in AIRCRAFT:
        by_id[row[0]] = fleet_entry(row)
        (ROOT / "data" / f"{row[0]}.json").write_text(json.dumps(detail(row), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    fleet["aircraft"] = [by_id[ident] for ident in old_order]
    fleet["aircraft"].extend(by_id[ident] for ident in ids if ident not in old_order)
    FLEET_PATH.write_text(json.dumps(fleet, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Added or updated {len(AIRCRAFT)} current general-aviation aircraft.")


if __name__ == "__main__":
    main()
