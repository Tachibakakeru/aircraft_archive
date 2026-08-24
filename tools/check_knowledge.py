"""Minimal integrity check for data/knowledge.json."""
import json
from pathlib import Path

topics = json.loads((Path(__file__).parents[1] / "data" / "knowledge.json").read_text(encoding="utf-8"))["topics"]
ids = [topic["id"] for topic in topics]
assert len(ids) == len(set(ids)), "duplicate knowledge topic id"
for topic in topics:
    for field in ("name", "summary", "fact"):
        assert all(topic.get(field, {}).get(lang) for lang in ("zh", "en", "ja")), f"{topic['id']}: missing {field} translation"
assert "high-bypass" in ids, "missing high-bypass topic"
print(f"knowledge OK: {len(topics)} topics")
