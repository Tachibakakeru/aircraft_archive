"""Apply reviewed Wikimedia Commons photographs to empty knowledge image slots.

The input catalog is hand-reviewed. This script deliberately does not select
search results automatically: many matches are drawings or unrelated photos.
"""
import json
import html
import re
import sys
from pathlib import Path
from urllib.parse import quote
import requests

ROOT = Path(__file__).parents[1]
DATA = ROOT / "data" / "knowledge.json"
CATALOG = ROOT / "tools" / "knowledge_photo_catalog.json"

text = DATA.read_text(encoding="utf-8")
topics = {topic["id"]: topic for topic in json.loads(text)["topics"]}
catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
if sys.argv[1:] == ["--credits"]:
    sys.stdout.reconfigure(encoding="utf-8")
    files = list(dict.fromkeys(item["file"] for item in catalog.values()))
    info = {}
    for offset in range(0, len(files), 20):
        titles = "|".join("File:" + name for name in files[offset:offset + 20])
        response = requests.get("https://commons.wikimedia.org/w/api.php", params={
            "action": "query", "titles": titles, "prop": "imageinfo",
            "iiprop": "size|extmetadata", "format": "json",
        }, headers={"User-Agent": "SkyArchivePhotoResearch/1.0 (educational; no uploads)"}, timeout=40)
        response.raise_for_status()
        info.update({page["title"].removeprefix("File:"): page.get("imageinfo", [{}])[0]
                     for page in response.json().get("query", {}).get("pages", {}).values()})
    for topic_id, item in catalog.items():
        found = info.get(item["file"])
        if not found:
            print(topic_id, "MISSING", item["file"])
            continue
        meta = found.get("extmetadata", {})
        license_name = meta.get("LicenseShortName", {}).get("value", "")
        artist = re.sub(r"<[^>]+>", " ", meta.get("Artist", {}).get("value", ""))
        artist = " ".join(html.unescape(artist).split())[:100]
        print(topic_id, found.get("width"), license_name, artist)
        if re.fullmatch(r"CC BY(?:-SA)? [0-9.]+|CC0|Public domain", license_name):
            item["credit"] = f"{artist or 'Wikimedia Commons'} · {license_name}"
    CATALOG.write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    sys.exit(0)
for topic_id, entry in catalog.items():
    assert topic_id in topics, f"unknown topic: {topic_id}"
    title = entry["file"].replace(" ", "_")
    path = quote(title, safe="(),-._")
    image = {
        "src": entry.get("local") or f"https://commons.wikimedia.org/wiki/Special:FilePath/{path}?width=960",
        "caption": entry["caption"],
        "source": f"https://commons.wikimedia.org/wiki/File:{path}",
        "credit": entry["credit"],
    }
    if entry.get("license"):
        image["license"] = entry["license"]
    if entry.get("licenseName"):
        image["licenseName"] = entry["licenseName"]
    if entry.get("cropped"):
        image["cropped"] = True
    if entry.get("replaces"):
        image["replaces"] = entry["replaces"]
    assert all(image["caption"].get(lang) for lang in ("zh", "en", "ja")), topic_id
    if topics[topic_id]["images"]:
        assert topics[topic_id]["images"][0]["source"] == image["source"], f"{topic_id}: existing image differs"
        assert topics[topic_id]["images"][0]["src"] == image["src"], f"{topic_id}: existing image URL differs"
        continue
    # All topics use an empty array on one line before curation. Limit the
    # replacement to the block after this exact ID, preserving unrelated JSON.
    pattern = rf'("id": "{re.escape(topic_id)}",[\s\S]*?"images": )\[\]'
    text, count = re.subn(pattern, lambda m: m.group(1) + json.dumps([image], ensure_ascii=False), text, count=1)
    assert count == 1, f"{topic_id}: could not find empty image array"
DATA.write_text(text, encoding="utf-8")
print(f"verified/applied {len(catalog)} photographs")
