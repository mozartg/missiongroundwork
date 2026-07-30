from __future__ import annotations

import hashlib
import io
import json
import textwrap
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont

JOB_PATH = Path("media/jobs/IMG-004-ownership-is-fuzzy.json")
OUTPUT_ROOT = Path("artifacts/mclp/IMG-004")
OUTPUT_PATH = OUTPUT_ROOT / "IMG-004-ownership-is-fuzzy.png"
SOURCE_PATH = OUTPUT_ROOT / "source-photo.jpg"
RECEIPT_PATH = OUTPUT_ROOT / "render-receipt.json"

WIDTH = 1080
HEIGHT = 1350


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def font_path(preferred: str, fallback: str) -> str:
    for candidate in (preferred, fallback):
        if Path(candidate).is_file():
            return candidate
    raise FileNotFoundError(f"No font found: {preferred} or {fallback}")


def cover_crop(image: Image.Image, width: int, height: int, focus_x: float = 0.57, focus_y: float = 0.48) -> Image.Image:
    ratio = max(width / image.width, height / image.height)
    resized = image.resize((round(image.width * ratio), round(image.height * ratio)), Image.Resampling.LANCZOS)
    left = max(0, min(resized.width - width, round(resized.width * focus_x - width / 2)))
    top = max(0, min(resized.height - height, round(resized.height * focus_y - height / 2)))
    return resized.crop((left, top, left + width, top + height))


def rounded_mask(size: tuple[int, int], radius: int) -> Image.Image:
    mask = Image.new("L", size, 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle((0, 0, size[0], size[1]), radius=radius, fill=255)
    return mask


def wrap_by_pixels(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.FreeTypeFont, max_width: int) -> list[str]:
    lines: list[str] = []
    for paragraph in text.splitlines():
        words = paragraph.split()
        current = ""
        for word in words:
            candidate = f"{current} {word}".strip()
            if draw.textlength(candidate, font=font) <= max_width:
                current = candidate
            else:
                if current:
                    lines.append(current)
                current = word
        if current:
            lines.append(current)
    return lines


def main() -> None:
    job = json.loads(JOB_PATH.read_text(encoding="utf-8"))
    if job["process_id"] != "MCLP-001" or job["artifact_id"] != "IMG-004":
        raise ValueError("Unexpected job identity")
    if job["production_method"] != "deterministic_editorial_photo_composition":
        raise ValueError("Unexpected production method")
    if job["publishing_authorized"] is not False or job["paid_service_authorized"] is not False:
        raise ValueError("Publishing and paid service use must remain disabled")

    OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)
    request = urllib.request.Request(
        job["source_photo"]["url"],
        headers={"User-Agent": "MCLP-001-deterministic-editorial/1.0"},
    )
    with urllib.request.urlopen(request, timeout=90) as response:
        source_bytes = response.read()
        content_type = response.headers.get("Content-Type", "")
    if not content_type.startswith("image/") or len(source_bytes) < 100_000:
        raise RuntimeError(f"Invalid source response: {content_type}, {len(source_bytes)} bytes")
    source_sha1 = hashlib.sha1(source_bytes).hexdigest()
    if source_sha1 != job["source_photo"]["expected_sha1"]:
        raise RuntimeError(f"Source SHA-1 mismatch: {source_sha1}")
    SOURCE_PATH.write_bytes(source_bytes)

    palette = job["brand"]
    canvas = Image.new("RGB", (WIDTH, HEIGHT), palette["off_white"])
    draw = ImageDraw.Draw(canvas)

    photo = Image.open(io.BytesIO(source_bytes)).convert("RGB")
    photo = cover_crop(photo, 710, 1190)
    photo = ImageEnhance.Color(photo).enhance(0.82)
    photo = ImageEnhance.Contrast(photo).enhance(1.08)
    warm = Image.new("RGB", photo.size, palette["warm_stone"])
    photo = Image.blend(photo, warm, 0.08)

    photo_panel = Image.new("RGB", (750, 1230), palette["off_white"])
    shadow = Image.new("RGBA", photo_panel.size, (0, 0, 0, 0))
    shadow_draw = ImageDraw.Draw(shadow)
    shadow_draw.rounded_rectangle((24, 26, 734, 1216), radius=42, fill=(30, 39, 39, 62))
    shadow = shadow.filter(ImageFilter.GaussianBlur(18))
    canvas.paste(shadow, (312, 60), shadow)
    photo_panel.paste(photo, (20, 20), rounded_mask(photo.size, 36))
    canvas.paste(photo_panel, (312, 60))

    overlay = Image.new("RGBA", (710, 1190), (0, 0, 0, 0))
    overlay_draw = ImageDraw.Draw(overlay)
    for x in range(260):
        alpha = round(145 * (1 - x / 260) ** 1.8)
        overlay_draw.line((x, 0, x, 1190), fill=(23, 35, 59, alpha))
    canvas.paste(overlay, (332, 80), overlay)

    heading_font = ImageFont.truetype(
        font_path("/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf", "/usr/share/fonts/truetype/liberation2/LiberationSerif-Bold.ttf"),
        76,
    )
    body_font = ImageFont.truetype(
        font_path("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", "/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf"),
        31,
    )
    small_bold = ImageFont.truetype(
        font_path("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", "/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf"),
        23,
    )
    cta_font = ImageFont.truetype(
        font_path("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", "/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf"),
        27,
    )
    credit_font = ImageFont.truetype(
        font_path("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", "/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf"),
        16,
    )

    draw.text((64, 76), "MISSION GROUNDWORK", font=small_bold, fill=palette["foundation_green"])
    draw.rectangle((64, 122, 208, 132), fill=palette["muted_clay"])
    draw.text((64, 164), "OPERATING CLARITY", font=small_bold, fill=palette["slate"])

    lines = wrap_by_pixels(draw, job["headline"], heading_font, 510)
    y = 260
    for index, line in enumerate(lines):
        fill = palette["foundation_green"] if index < len(lines) - 1 else palette["muted_clay"]
        draw.text((64, y), line, font=heading_font, fill=fill)
        y += 82

    body_lines = wrap_by_pixels(draw, job["body"], body_font, 430)
    y = max(y + 44, 690)
    for line in body_lines:
        draw.text((64, y), line, font=body_font, fill=palette["slate"])
        y += 45

    cta_box = (64, 1000, 356, 1072)
    draw.rounded_rectangle(cta_box, radius=20, fill=palette["foundation_green"])
    draw.text((210, 1036), job["cta"], font=cta_font, fill=palette["off_white"], anchor="mm")

    draw.text((64, 1128), "HELPING YOUR TEAM START ON SOLID GROUND.", font=small_bold, fill=palette["slate"])
    draw.line((64, 1178, 270, 1178), fill=palette["warm_stone"], width=4)

    credit = "Context photo: Community meeting, Sierra Leone — USAID/E. Benya, public domain. Not a client or case study."
    credit_lines = textwrap.wrap(credit, width=72)
    cy = 1256
    for line in credit_lines:
        draw.text((64, cy), line, font=credit_font, fill="#65706F")
        cy += 21

    canvas.save(OUTPUT_PATH, format="PNG", optimize=True)

    receipt = {
        "schema_version": 1,
        "process_id": "MCLP-001",
        "receipt_id": "IMG-004-RENDER",
        "artifact_id": "IMG-004",
        "captured_at": datetime.now(timezone.utc).isoformat(),
        "status": "PASS_TECHNICAL",
        "evidence_state": "OBSERVED_ONCE",
        "terminal_state": "USER_REVIEW_REQUIRED",
        "production_method": job["production_method"],
        "source": {
            "title": job["source_photo"]["title"],
            "creator": job["source_photo"]["creator"],
            "license": job["source_photo"]["license"],
            "source_page": job["source_photo"]["source_page"],
            "sha1": source_sha1,
            "saved_path": str(SOURCE_PATH),
        },
        "output": {
            "path": str(OUTPUT_PATH),
            "width": WIDTH,
            "height": HEIGHT,
            "format": "PNG",
            "bytes": OUTPUT_PATH.stat().st_size,
            "sha256": sha256(OUTPUT_PATH),
        },
        "publishing_authorized": False,
        "paid_service_used": False,
        "limitations": [
            "Creative review remains pending.",
            "The source photograph is contextual and must not be presented as a client or case study.",
            "Observed-once output is not a promoted production lane."
        ],
    }
    RECEIPT_PATH.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(receipt, indent=2))


if __name__ == "__main__":
    main()
