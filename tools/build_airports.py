#!/usr/bin/env python3
"""
機場與跑道資料匯入（OurAirports 公共領域資料集，全量匯入）
來源: https://github.com/davidmegginson/ourairports-data (Public Domain)

用法: python3 build_airports.py <airports.csv> <runways.csv> <countries.csv> <輸出根目錄>

全量匯入：不篩選機型或代號，OurAirports 收錄的所有機場／跑道（含已關閉、
無代號的小型跑道）全數保留。為了不讓「隨頁載入」的搜尋索引肥大到拖慢
列表頁，欄位拆成兩層：

  data/airports.json        — 搜尋／列表用的輕量索引（僅列表需要的欄位）
  data/countries.json       — 國家代碼 → 名稱
  data/details/<ISO國碼>.json — 該國機場的完整明細（座標／標高／行政區碼／
                                跑道清單），點開機場才依國家整批載入一次
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
    airports = []          # 輕量搜尋索引
    details = {}           # ident → 完整明細（不含 runways，稍後補上）
    with open(airports_csv, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            ident = row["ident"]
            airports.append({
                "id": ident,
                "icao": row["icao_code"] or None,
                "iata": row["iata_code"] or None,
                "name": row["name"],
                "city": row["municipality"] or None,
                "country": row["iso_country"] or None,
                "type": row["type"],
            })
            details[ident] = {
                "lat": num(row["latitude_deg"]),
                "lon": num(row["longitude_deg"]),
                "elev": to_int(row["elevation_ft"]),
                "region": row["iso_region"] or None,
                "runways": [],
            }

    countries = {}
    with open(countries_csv, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            countries[row["code"]] = row["name"]

    n_rw = 0
    with open(runways_csv, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            ident = row["airport_ident"]
            if ident not in details:
                continue
            n_rw += 1
            details[ident]["runways"].append({
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

    # 明細依機場所屬國家分桶（座標＋跑道合併成一次 fetch）
    ident_country = {a["id"]: a["country"] for a in airports}
    by_country = collections.defaultdict(dict)
    for ident, d in details.items():
        c = ident_country.get(ident) or "ZZ"
        by_country[c][ident] = d

    data_dir = os.path.join(out_root, "data")
    det_dir = os.path.join(data_dir, "details")
    os.makedirs(det_dir, exist_ok=True)
    # 清掉舊的 runways/ 分桶目錄產物（已併入 details/）
    old_rw_dir = os.path.join(data_dir, "runways")
    if os.path.isdir(old_rw_dir):
        for fn in os.listdir(old_rw_dir):
            os.remove(os.path.join(old_rw_dir, fn))
        os.rmdir(old_rw_dir)

    with open(os.path.join(data_dir, "airports.json"), "w", encoding="utf-8") as f:
        json.dump({"airports": airports}, f, ensure_ascii=False, separators=(",", ":"))
    with open(os.path.join(data_dir, "countries.json"), "w", encoding="utf-8") as f:
        json.dump(countries, f, ensure_ascii=False, separators=(",", ":"))
    for c, m in by_country.items():
        safe = c if c and c.isalpha() else "ZZ"
        with open(os.path.join(det_dir, f"{safe}.json"), "w", encoding="utf-8") as f:
            json.dump(m, f, ensure_ascii=False, separators=(",", ":"))

    print(f"airports: {len(airports)}  runways: {n_rw}  countries(files): {len(by_country)}")

if __name__ == "__main__":
    build(*sys.argv[1:5])
