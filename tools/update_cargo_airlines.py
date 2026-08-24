"""Add or refresh the curated cargo / express airline collection.

Run: python tools/update_cargo_airlines.py
Facts with date-sensitive fleets come from the operator sources recorded in Progress.md.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AIRLINES_PATH = ROOT / "data" / "airlines.json"
GEO_PATH = ROOT / "data" / "airline_geo.json"
CODES_PATH = ROOT / "data" / "airport_codes.json"


def t(zh, en, ja):
    return {"zh": zh, "en": en, "ja": ja}


RECORDS = [
    {
        "id": "fdx", "name": "FedEx Express", "nameZh": "聯邦快遞", "nameJa": "フェデックス・エクスプレス",
        "icao": "FDX", "iata": "FX", "callsign": "FEDEX", "country": t("美國", "United States", "アメリカ"),
        "founded": 1971, "alliance": "none", "tier": "cargo", "hubs": ["MEM", "IND", "ANC", "OAK", "CDG"],
        "fleetTotal": 700,
        "fleet": [
            {"type": "Boeing 757-200F", "count": 92, "fleetId": "b752"},
            {"type": "Boeing 767F", "count": 138, "fleetId": "b763"},
            {"type": "Boeing 777F", "count": 57},
            {"type": "Boeing MD-11F", "count": 37, "fleetId": "md11"},
            {"type": "Airbus A300-600F", "count": 67},
        ],
        "routes": ["DUB", "HKG", "DXB"],
        "tagline": t(
            "全球整合型快遞航空網路，以孟菲斯為核心。FedEx FY26 公開資料列約 700 架飛機；主要機型的細目採 FY24 官方統計，持續以 767F、777F、ATR 72-600F 與 Cessna 408 更新機隊。",
            "The global integrated express network centered on Memphis. FedEx reports about 700 aircraft for FY26; the major-type breakdown follows FY24 official figures while the fleet continues to modernize with 767Fs, 777Fs, ATR 72-600Fs and Cessna 408s.",
            "メンフィスを中核とする世界的な統合エクスプレス網。FY26 の公開値は約700機で、主要機種の内訳はFY24の公式統計に基づく。767F、777F、ATR 72-600F、Cessna 408への更新を継続している。",
        ), "logoSrc": "flightaware_logos",
    },
    {
        "id": "ups", "name": "UPS Airlines", "nameZh": "聯合包裹航空", "nameJa": "UPS航空",
        "icao": "UPS", "iata": "5X", "callsign": "UPS", "country": t("美國", "United States", "アメリカ"),
        "founded": 1988, "alliance": "none", "tier": "cargo", "hubs": ["SDF", "ONT", "DFW", "PHX", "CGN"],
        "fleetTotal": 272,
        "fleet": [
            {"type": "Boeing 757-200F", "count": 75, "fleetId": "b752"},
            {"type": "Airbus A300-600F", "count": 52},
            {"type": "Boeing 767-300F", "count": 102, "fleetId": "b763"},
            {"type": "Boeing 747-400F", "count": 13, "fleetId": "b744"},
            {"type": "Boeing 747-8F", "count": 30, "fleetId": "b748"},
        ], "routes": ["ANC", "HKG", "LGG"],
        "tagline": t(
            "UPS 的航空貨運子公司，世界港位於路易斯維爾 Muhammad Ali 國際機場。2026-03-31 官方機隊表列 UPS Airlines 共 272 架自營飛機（不含已退役 MD-11）。",
            "UPS's air-cargo subsidiary, with Worldport at Louisville Muhammad Ali International Airport. Its 31 March 2026 fact sheet lists 272 UPS Airlines aircraft, excluding retired MD-11s.",
            "UPSの航空貨物子会社。世界ハブはルイビル・ムハンマド・アリ国際空港にあり、2026年3月31日付の公式資料では、退役済みMD-11を除き自社機272機を運航する。",
        ), "logoSrc": "flightaware_logos",
    },
    {
        "id": "tay", "name": "ASL Airlines Belgium", "nameZh": "ASL 比利時航空（前 TNT 航空）", "nameJa": "ASL航空ベルギー（旧TNT航空）",
        "icao": "TAY", "iata": "3V", "callsign": "QUALITY", "country": t("比利時", "Belgium", "ベルギー"),
        "founded": 1999, "alliance": "none", "tier": "cargo", "hubs": ["LGG"], "fleetTotal": None,
        "fleet": [{"type": "Boeing 747-400F", "count": 3, "fleetId": "b744"}], "routes": ["JFK", "NRT"],
        "tagline": t(
            "比利時貨運航空公司，前身為 TNT Airways；以列日為基地，營運波音 737 貨機與 747-400ERF。ASL 於 2020 年確認其自營三架 747-400F；未將 ASL 集團 140 架的全球總數誤列為比利時單一 AOC 機隊。",
            "Belgian cargo carrier and former TNT Airways operator, based at Liège and flying Boeing 737 freighters and 747-400ERFs. ASL confirmed three operated 747-400Fs in 2020; the group-wide 140-aircraft figure is deliberately not assigned to this single AOC.",
            "リエージュを拠点とするベルギーの貨物航空会社で、旧TNT Airways。B737貨物機と747-400ERFを運航する。2020年に自社運航747-400F 3機を確認しており、ASLグループ全体140機を単独AOCの保有数としては扱わない。",
        ), "logoSrc": "flightaware_logos",
    },
    {
        "id": "bcs", "name": "European Air Transport Leipzig", "nameZh": "歐洲航空運輸萊比錫", "nameJa": "ヨーロピアン・エア・トランスポート・ライプツィヒ",
        "icao": "BCS", "iata": "QY", "callsign": "POSTMAN", "country": t("德國", "Germany", "ドイツ"),
        "founded": 2006, "alliance": "none", "tier": "cargo", "hubs": ["LEJ"], "fleetTotal": 35,
        "fleet": [{"type": "Airbus／Boeing 貨機", "count": 35}], "routes": ["CVG", "BAH", "HKG"],
        "tagline": t(
            "DHL Group 100% 持有、隸屬 DHL Express 的貨運航空與維修公司，基地在萊比錫／哈雷。DHL 現行介紹列有 35 架自有 Airbus 與 Boeing 飛機，並同時負責維修與飛航訓練。",
            "A DHL Group–owned DHL Express cargo airline and maintenance provider based at Leipzig/Halle. DHL's current profile lists 35 owned Airbus and Boeing aircraft alongside its MRO and flight-training operation.",
            "DHL Groupが100%保有するDHL Expressの貨物航空・整備会社で、拠点はライプツィヒ／ハレ。DHLの現行紹介では、自有のAirbus／Boeing機35機を運航し、整備と飛行訓練も担う。",
        ), "logoSrc": "flightaware_logos",
    },
    {
        "id": "dhl", "name": "DHL Air UK", "nameZh": "DHL 英國航空", "nameJa": "DHLエアUK",
        "icao": "DHL", "iata": "D0", "callsign": "WORLD EXPRESS", "country": t("英國", "United Kingdom", "イギリス"),
        "founded": 1982, "alliance": "none", "tier": "cargo", "hubs": ["EMA", "CVG", "BAH"], "fleetTotal": 7,
        "fleet": [{"type": "Boeing 777F", "count": 7}], "routes": ["LEJ", "HKG"],
        "tagline": t(
            "DHL Express 的英國貨運航空營運商，以東密德蘭機場為核心。DHL 2023 年報確認其 777F 自三架擴增至七架；後續 777-200LR 改裝貨機正逐步加入，機隊數會持續變動。",
            "DHL Express's UK cargo operator, centered on East Midlands Airport. DHL's 2023 report confirmed its 777F operation had grown from three to seven aircraft; converted 777-200LR freighters are being introduced, so the total remains fluid.",
            "イースト・ミッドランズ空港を中核とするDHL Expressの英国貨物運航会社。DHLの2023年報では777Fは3機から7機へ拡大。777-200LR改造貨物機も導入中のため、機数は変動する。",
        ), "logoSrc": "flightaware_logos",
    },
    {
        "id": "ahk", "name": "Air Hong Kong", "nameZh": "香港華民航空", "nameJa": "エア・ホンコン",
        "icao": "AHK", "iata": "LD", "callsign": "AIR HONG KONG", "country": t("香港", "Hong Kong", "香港"),
        "founded": 1986, "alliance": "none", "tier": "cargo", "hubs": ["HKG"], "fleetTotal": 14,
        "fleet": [{"type": "Airbus A330-243F", "count": 4}, {"type": "Airbus A330-300P2F", "count": 10}],
        "routes": ["BKK", "SIN", "TPE", "NRT"],
        "tagline": t(
            "國泰航空集團的全貨運航空公司，為 DHL Express 亞太網路營運快遞貨機。2025 年完成汰換 A300-600F，轉為 14 架 A330 貨機，專供 DHL Express 貨運使用。",
            "Cathay Group's all-cargo airline operating express freighters for DHL Express in Asia-Pacific. Its 2025 renewal completed the retirement of A300-600Fs in favor of 14 A330 freighters dedicated to DHL Express shipments.",
            "キャセイグループの全貨物航空会社で、DHL Expressのアジア太平洋ネットワークを運航。2025年にA300-600Fを退役させ、DHL Express専用のA330貨物機14機へ更新した。",
        ), "logoSrc": "flightaware_logos",
    },
    {
        "id": "clx", "name": "Cargolux", "nameZh": "盧森堡貨運航空", "nameJa": "カーゴルックス",
        "icao": "CLX", "iata": "CV", "callsign": "CARGOLUX", "country": t("盧森堡", "Luxembourg", "ルクセンブルク"),
        "founded": 1970, "alliance": "none", "tier": "cargo", "hubs": ["LUX"], "fleetTotal": 30,
        "fleet": [{"type": "Boeing 747-400F／747-8F", "count": 30, "fleetId": "b748"}], "routes": ["ORD", "HKG", "JFK"],
        "tagline": t(
            "以盧森堡為基地的全貨運航空公司，也是 747-8F 的首位營運者。官方機隊頁列 Cargolux Group 共 30 架 747-400F 與 747-8F 專用貨機。",
            "Luxembourg-based all-cargo carrier and launch operator of the 747-8F. Its official fleet page lists 30 purpose-built 747-400F and 747-8F freighters across the Cargolux Group.",
            "ルクセンブルクを拠点とする全貨物航空会社で、747-8Fのローンチオペレーター。公式機隊ページではCargolux Groupで747-400F／747-8Fの専用貨物機30機を掲げる。",
        ), "logoSrc": "flightaware_logos",
    },
    {
        "id": "gti", "name": "Atlas Air", "nameZh": "亞特拉斯航空", "nameJa": "アトラス航空",
        "icao": "GTI", "iata": "5Y", "callsign": "GIANT", "country": t("美國", "United States", "アメリカ"),
        "founded": 1992, "alliance": "none", "tier": "cargo", "hubs": ["JFK", "ANC"], "fleetTotal": 113,
        "fleet": [
            {"type": "Boeing 747-8F", "count": 17, "fleetId": "b748"},
            {"type": "Boeing 747-400F", "count": 39, "fleetId": "b744"},
            {"type": "Boeing 777-200F", "count": 13},
            {"type": "Boeing 767-300F", "count": 5, "fleetId": "b763"},
        ], "routes": [],
        "tagline": t(
            "提供 ACMI／CMI 濕租、包機與貨機營運的全球航空公司；其航線依客戶合約調度，並非固定班表。Atlas Air Worldwide 2025 年資料列全體機隊 113 架，含全球最大 747 貨機機隊。",
            "Global ACMI/CMI, charter and cargo operator whose routes are customer-contract driven rather than a fixed schedule. Atlas Air Worldwide's 2025 presentation lists 113 aircraft and the world's largest 747 freighter fleet.",
            "ACMI／CMI、チャーター、貨物運航を提供する世界的オペレーター。路線は固定時刻表ではなく顧客契約により運航される。2025年資料では全体113機、世界最大の747貨物機群を保有する。",
        ), "logoSrc": "flightaware_logos",
    },
    {
        "id": "usps", "name": "United States Postal Service", "nameZh": "美國郵政署（USPS）", "nameJa": "アメリカ合衆国郵便公社（USPS）",
        "icao": None, "iata": None, "callsign": None, "country": t("美國", "United States", "アメリカ"),
        "founded": 1971, "alliance": "none", "tier": "cargo", "hubs": [], "fleetTotal": None, "fleet": [], "routes": [],
        "tagline": t(
            "USPS 是郵政營運機構而非持有 AOC 的航空公司；其航空郵件網路由契約承運人提供運能，因此不虛列 ICAO／IATA 代碼或自有機隊。列入本分類便於比較快遞與郵政航空物流體系。",
            "USPS is a postal operator, not an airline holding an AOC. Its air-mail network buys capacity from contracted carriers, so no ICAO/IATA code or owned fleet is invented here. It is included to compare express and postal air-logistics systems.",
            "USPSはAOCを持つ航空会社ではなく郵便事業体であり、航空郵便網は契約運航会社の輸送力で構成される。架空のICAO／IATAコードや自社機隊は記載せず、エクスプレスと郵便航空物流の比較対象として収録する。",
        ),
    },
]

GEO_CODES = {
    "fdx": {"hubs": ["MEM", "IND", "ANC", "OAK", "CDG"], "routes": ["DUB", "HKG", "DXB"]},
    "ups": {"hubs": ["SDF", "ONT", "DFW", "PHX", "CGN"], "routes": ["ANC", "HKG", "LGG"]},
    "tay": {"hubs": ["LGG"], "routes": ["JFK", "NRT"]},
    "bcs": {"hubs": ["LEJ"], "routes": ["CVG", "BAH", "HKG"]},
    "dhl": {"hubs": ["EMA", "CVG", "BAH"], "routes": ["LEJ", "HKG"]},
    "ahk": {"hubs": ["HKG"], "routes": ["BKK", "SIN", "TPE", "NRT"]},
    "clx": {"hubs": ["LUX"], "routes": ["ORD", "HKG", "JFK"]},
    "gti": {"hubs": ["JFK", "ANC"], "routes": []},
}


def airport_entry(codes, code):
    item = codes.get(code)
    if not item:
        raise KeyError(f"airport code not found: {code}")
    return {"text": code, "icao": item["id"], "lat": item["lat"], "lon": item["lon"]}


def main():
    airlines_data = json.loads(AIRLINES_PATH.read_text(encoding="utf-8"))
    by_id = {a["id"]: a for a in airlines_data["airlines"]}
    for record in RECORDS:
        existing = by_id.get(record["id"])
        if existing:
            existing.update(record)
        else:
            airlines_data["airlines"].append(record)
    for record in airlines_data["airlines"]:
        if record["id"] in {"tus", "acp", "snc", "vas", "icl", "kzu", "gec", "sqc", "ncr"}:
            record["tier"] = "cargo"
    AIRLINES_PATH.write_text(json.dumps(airlines_data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    geo = json.loads(GEO_PATH.read_text(encoding="utf-8"))
    codes = json.loads(CODES_PATH.read_text(encoding="utf-8"))
    for airline_id, groups in GEO_CODES.items():
        geo[airline_id] = {key: [airport_entry(codes, code) for code in values] for key, values in groups.items()}
    GEO_PATH.write_text(json.dumps(geo, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    by_id = {a["id"]: a for a in airlines_data["airlines"]}
    assert len({a["id"] for a in airlines_data["airlines"]}) == len(airlines_data["airlines"])
    assert all(by_id[item["id"]]["tier"] == "cargo" for item in RECORDS)
    assert all(geo[airline_id]["hubs"] for airline_id in GEO_CODES)
    print(f"cargo collection OK: {sum(a.get('tier') == 'cargo' for a in airlines_data['airlines'])} airlines")


if __name__ == "__main__":
    main()
