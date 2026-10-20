"""Minimal integrity check for data/knowledge.json."""
import json
import re
from pathlib import Path

root = Path(__file__).parents[1]
topics = json.loads((root / "data" / "knowledge.json").read_text(encoding="utf-8"))["topics"]
ids = [topic["id"] for topic in topics]
assert len(ids) == len(set(ids)), "duplicate knowledge topic id"
for topic in topics:
    for field in ("name", "summary", "fact"):
        assert all(topic.get(field, {}).get(lang) for lang in ("zh", "en", "ja")), f"{topic['id']}: missing {field} translation"
js = (root / "js" / "knowledge.js").read_text(encoding="utf-8")
scene_ids = []
for scene in ("INSTRUMENT", "RUNWAY", "NAV", "SYSTEMS"):
    block = re.search(rf"const {scene}_TOPICS = \[(.*?)\];", js, re.S)
    assert block, f"missing {scene} scene"
    scene_ids.extend(re.findall(r'\{ id: "([^"]+)"', block.group(1)))
assert len(scene_ids) == len(set(scene_ids)), "duplicate scene topic id"
assert set(ids) == set(scene_ids), f"unlisted topics: {set(ids) - set(scene_ids)}; missing data: {set(scene_ids) - set(ids)}"
assert "high-bypass" in ids, "missing high-bypass topic"
print(f"knowledge OK: {len(topics)} topics")
