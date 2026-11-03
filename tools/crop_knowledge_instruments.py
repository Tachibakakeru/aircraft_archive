"""Crop real aircraft instruments into separate, attributable photos.

Source: https://commons.wikimedia.org/wiki/File:Six_flight_instruments.JPG
Meggar, CC BY-SA 3.0. Coordinates follow that file's Commons annotations.
The original is downloaded for processing and is not redistributed in this repo.
"""

from io import BytesIO
from pathlib import Path

import requests
from PIL import Image, ImageOps

ROOT = Path(__file__).parents[1]
OUT = ROOT / "assets" / "knowledge"
SOURCE = "https://commons.wikimedia.org/wiki/Special:FilePath/Six_flight_instruments.JPG"
# x, y, width, height in the 1503 × 927 original photograph.
BOXES = {
    "asi": (70, 24, 415, 429),
    "ai": (558, 30, 423, 410),
    "alt": (1037, 32, 430, 419),
    "tc": (70, 466, 413, 404),
    "hdg": (558, 468, 421, 401),
    "vsi": (1039, 468, 425, 399),
}

response = requests.get(SOURCE, headers={"User-Agent": "SkyArchiveDev/1.0 (educational image crop)"}, timeout=30)
response.raise_for_status()
with Image.open(BytesIO(response.content)) as original:
    assert original.size == (1503, 927), f"unexpected source dimensions: {original.size}"
    OUT.mkdir(parents=True, exist_ok=True)
    for topic, (x, y, width, height) in BOXES.items():
        crop = original.crop((x, y, x + width, y + height)).convert("RGB")
        path = OUT / f"six-pack-{topic}.jpg"
        crop.save(path, format="JPEG", quality=94, optimize=True, subsampling=0)
        print(f"{topic}: {crop.width}x{crop.height} -> {path.relative_to(ROOT)}")

# A real ADF bearing indicator installed on a B-17G, not the receiver/control
# stack previously shown for this topic. Pi3.124, CC BY-SA 4.0.
# https://commons.wikimedia.org/wiki/File:Automatic_Radio_Direction_Finder_R-5_ARN7_indicator.jpg
adf_url = "https://commons.wikimedia.org/wiki/Special:FilePath/Automatic_Radio_Direction_Finder_R-5_ARN7_indicator.jpg"
response = requests.get(adf_url, headers={"User-Agent": "SkyArchiveDev/1.0 (educational image crop)"}, timeout=30)
response.raise_for_status()
with Image.open(BytesIO(response.content)) as source:
    upright = ImageOps.exif_transpose(source)
    assert upright.size == (1960, 4032), f"unexpected ADF source dimensions: {upright.size}"
    crop = upright.crop((200, 400, 1760, 1960)).convert("RGB")
    path = OUT / "adf-b17-radio-compass.jpg"
    crop.save(path, format="JPEG", quality=94, optimize=True, subsampling=0)
    print(f"adf: {crop.width}x{crop.height} -> {path.relative_to(ROOT)}")
