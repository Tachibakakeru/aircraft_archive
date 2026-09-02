"""Record which fleet entries do not have a matching 3D model JSON."""

from __future__ import annotations

import json
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    aircraft = json.loads((ROOT / "data" / "fleet.json").read_text(encoding="utf-8"))["aircraft"]
    missing = [
        {"id": item["id"], "name": item["name"], "manufacturer": item.get("manufacturer", "")}
        for item in aircraft
        if not (ROOT / "models" / f"{item['id']}.json").exists()
    ]
    report = {
        "updated": date.today().isoformat(),
        "fleetCount": len(aircraft),
        "modelCount": len(aircraft) - len(missing),
        "missingCount": len(missing),
        "missing": missing,
    }
    (ROOT / "data" / "model_inventory.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    assert report["fleetCount"] == report["modelCount"] + report["missingCount"]
    print(f"{report['modelCount']}/{report['fleetCount']} entries have 3D models; {len(missing)} missing.")


if __name__ == "__main__":
    main()
