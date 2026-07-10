#!/usr/bin/env python3
"""
機場與跑道資料匯入（OurAirports 公共領域資料集）
來源: https://github.com/davidmegginson/ourairports-data (Public Domain)

用法: python3 build_airports.py <airports.csv> <runways.csv> <countries.csv> <輸出根目錄>

篩選規則：large_airport／medium_airport，或任何有 IATA 代號的機場
（涵蓋全球有定期航班服務等級的機場，排除數萬個無代號的小型農用/私人跑道）。
輸出：
  data/airports.json          — 篩選後機場輕量索引（搜尋／列表用）
  data/countries.json         — 國家代碼 → 名稱
  data/runways/<ISO國碼>.json — 該國機場的跑道明細（依需求載入）
"""
import csv, json, os, sys, collections

def num(v):
    if v in (None, ""): return None
    try: return round(float(v), 4)
    except ValueError: return None

def to_int(v):
    if v in (None, ""): return None
    try: return int(float(v))
    except ValueError: return None

def build(airports_csv, runways_csv, countries_csv, out_root):
    keep_idents = set()
    airports = []
    with open(airports_csv, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row["type"] not in ("large_airport", "medium_airport") and not row["iata_code"]:
                continue
            keep_idents.add(row["ident"])
            airports.append({
                "id": row["ident"],
                "icao": row["icao_code"] or None,
                "iata": row["iata_code"] or None,
                "name": row["name"],
                "city": row["municipality"] or None,
                "country": row["iso_country"] or None,
                "region": row["iso_region"] or None,
                "type": row["type"],
                "lat": num(row["latitude_deg"]),
                "lon": num(row["longitude_deg"]),
                "elev": to_int(row["elevation_ft"]),
            })

    countries = {}
    with open(countries_csv, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            countries[row["code"]] = row["name"]

    runways_by_country = collections.defaultdict(list)
    n_rw = 0
    with open(runways_csv, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            ident = row["airport_ident"]
            if ident not in keep_idents:
                continue
            # 用機場所屬國家分桶（機場清單裡查得到）
            n_rw += 1
            runways_by_country[ident].append({
                "len": to_int(row["length_ft"]),
                "wid": to_int(row["width_ft"]),
                "surf": row["surface"] or None,
                "lit": row["lighted"] == "1",
                "closed": row["closed"] == "1",
                "le": {"id": row["le_ident"] or None, "hdg": num(row["le_heading_degT"]),
                       "lat": num(row["le_latitude_deg"]), "lon": num(row["le_longitude_deg"])},
                "he": {"id": row["he_ident"] or None, "hdg": num(row["he_heading_degT"]),
                       "lat": num(row["he_latitude_deg"]), "lon": num(row["he_longitude_deg"])},
            })

    # 依機場所屬國家把跑道分桶（機場 ident → country 查表）
    ident_country = {a["id"]: a["country"] for a in airports}
    by_country = collections.defaultdict(dict)
    for ident, rws in runways_by_country.items():
        c = ident_country.get(ident) or "ZZ"
        by_country[c][ident] = rws

    data_dir = os.path.join(out_root, "data")
    rw_dir = os.path.join(data_dir, "runways")
    os.makedirs(rw_dir, exist_ok=True)

    with open(os.path.join(data_dir, "airports.json"), "w", encoding="utf-8") as f:
        json.dump({"airports": airports}, f, ensure_ascii=False, separators=(",", ":"))
    with open(os.path.join(data_dir, "countries.json"), "w", encoding="utf-8") as f:
        json.dump(countries, f, ensure_ascii=False, separators=(",", ":"))
    for c, m in by_country.items():
        safe = c if c and c.isalpha() else "ZZ"
        with open(os.path.join(rw_dir, f"{safe}.json"), "w", encoding="utf-8") as f:
            json.dump(m, f, ensure_ascii=False, separators=(",", ":"))

    print(f"airports: {len(airports)}  runways: {n_rw}  countries(files): {len(by_country)}")

if __name__ == "__main__":
    build(*sys.argv[1:5])
