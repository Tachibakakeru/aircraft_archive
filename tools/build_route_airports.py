"""產生首頁「隨機航線」與「航線規劃」用的輕量機場清單 data/route_airports.json。

來源：data/airports.json（全庫）取 type == large_airport 且有 IATA 代碼的機場，
座標取自 data/airport_codes.json，國家名稱取自 data/countries.json，城市中日文取自 data/city_names.json。
輸出格式（陣列以節省大小）：
  {"fields": ["id","iata","name","city","country","lat","lon","cityZh","cityJa"], "airports": [[...], ...]}
重跑：python tools/build_route_airports.py
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def load(name):
    return json.loads((ROOT / "data" / name).read_text(encoding="utf-8"))


def main():
    airports = load("airports.json")["airports"]
    codes = load("airport_codes.json")
    city_names = load("city_names.json")
    rows = []
    for a in airports:
        if a.get("type") != "large_airport" or not a.get("iata"):
            continue
        geo = codes.get(a["id"]) or codes.get(a["iata"])
        if not geo or geo.get("lat") is None:
            continue
        cn = city_names.get(f"{a.get('city')}|{a.get('country')}", {})
        rows.append([a["id"], a["iata"], a["name"], a.get("city") or "", a.get("country") or "",
                     round(geo["lat"], 4), round(geo["lon"], 4), cn.get("zh", ""), cn.get("ja", "")])
    rows.sort(key=lambda r: r[1])
    out = {"fields": ["id", "iata", "name", "city", "country", "lat", "lon", "cityZh", "cityJa"], "airports": rows}
    (ROOT / "data/route_airports.json").write_text(json.dumps(out, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    print(f"{len(rows)} airports, {(ROOT / 'data/route_airports.json').stat().st_size / 1024:.1f} KB")


if __name__ == "__main__":
    main()
