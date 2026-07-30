from __future__ import annotations

import hashlib
import io
import json
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFont, ImageOps

JOB_PATH = Path("media/jobs/IMG-007-shared-direction.json")
OUTPUT_ROOT = Path("artifacts/mclp/IMG-007")
OUTPUT_PATH = OUTPUT_ROOT / "IMG-007-shared-direction.png"
SOURCE_PATH = OUTPUT_ROOT / "source-photo.jpg"
RECEIPT_PATH = OUTPUT_ROOT / "render-receipt.json"

WIDTH = 1080
HEIGHT = 1350
MARGIN = 56
PHOTO_TOP = 470
PHOTO_WIDTH = WIDTH - MARGIN * 2
PHOTO_HEIGHT = 650
CLOSING_TOP = 1160


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def font_path(*candidates: str) -> str:
    for candidate in candidates:
        if Path(candidate).is_file():
            return candidate
    raise FileNotFoundError(f"No font found in candidates: {candidates}")


def cover_crop(image: Image.Image, width: int, height: int, focus_x: float = 0.50, focus_y: float = 0.53) -> Image.Image:
    ratio = max(width / image.width, height / image.height)
    resized = image.resize((round(image.width * ratio), round(image.height * ratio)), Image.Resampling.LANCZOS)
    left = max(0, min(resized.width - width, round(resized.width * focus_x - width / 2)))
    top = max(0, min(resized.height - height, round(resized.height * focus_y - height / 2)))
    return resized.crop((left, top, left + width, top + height))


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


def rounded_photo(image: Image.Image, radius: int = 28) -> Image.Image:
    mask = Image.new("L", image.size, 0)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.rounded_rectangle((0, 0, image.width, image.height), radius=radius, fill=255)
    result = Image.new("RGB", image.size, "white")
    result.paste(image, (0, 0), mask)
    return result


def main() -> None:
    job = json.loads(JOB_PATH.read_text(encoding="utf-8"))
    if job["process_id"] != "MCLP-001" or job["artifact_id"] != "IMG-007":
        raise ValueError("Unexpected job identity")
    if job.get("revision") != 1:
        raise ValueError("Unexpected IMG-007 revision")
    if job["production_method"] != "deterministic_alignment_editorial_composition":
        raise ValueError("Unexpected production method")
    if job["publishing_authorized"] is not False or job["paid_service_authorized"] is not False:
        raise ValueError("Publishing and paid service use must remain disabled")
    if job["layout_contract"].get("distinct_from_IMG_004") is not True:
        raise ValueError("IMG-007 must be explicitly distinct from IMG-004")

    source = job["source_photo"]
    parsed = urllib.parse.urlparse(source["url"])
    if parsed.scheme != "https" or parsed.netloc != "upload.wikimedia.org":
        raise ValueError("Source URL must remain on the verified Wikimedia upload host")

    OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)
    request = urllib.request.Request(
        source["url"],
        headers={"User-Agent": "MCLP-001-mission-groundwork-editorial/1.0"},
    )
    with urllib.request.urlopen(request, timeout=120) as response:
        source_bytes = response.read()
        content_type = response.headers.get("Content-Type", "")
        final_host = urllib.parse.urlparse(response.geturl()).netloc
    if final_host != "upload.wikimedia.org":
        raise RuntimeError(f"Unexpected source host: {final_host}")
    if not content_type.startswith("image/") or len(source_bytes) < 100_000:
        raise RuntimeError(f"Invalid source response: {content_type}, {len(source_bytes)} bytes")

    source_sha1 = hashlib.sha1(source_bytes).hexdigest()
    if source_sha1 != source["expected_sha1"]:
        raise RuntimeError(f"Source SHA-1 mismatch: {source_sha1}")
    if len(source_bytes) != source["expected_bytes"]:
        raise RuntimeError(f"Source byte count mismatch: {len(source_bytes)}")
    SOURCE_PATH.write_bytes(source_bytes)

    palette = job["brand"]
    canvas = Image.new("RGB", (WIDTH, HEIGHT), palette["off_white"])
    draw = ImageDraw.Draw(canvas)

    condensed_bold = font_path(
        "/usr/share/fonts/truetype/dejavu/DejaVuSansCondensed-Bold.ttf",
        "/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf",
    )
    sans = font_path(
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf",
    )
    sans_bold = font_path(
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf",
    )

    kicker_font = ImageFont.truetype(sans_bold, 22)
    headline_font = ImageFont.truetype(condensed_bold, 58)
    body_font = ImageFont.truetype(sans, 28)
    closing_font = ImageFont.truetype(sans_bold, 25)
    credit_font = ImageFont.truetype(sans, 15)

    draw.rectangle((0, 0, WIDTH, 18), fill=palette["foundation_green"])
    draw.rectangle((0, 18, WIDTH, 34), fill=palette["muted_clay"])

    draw.text((MARGIN, 76), job["kicker"], font=kicker_font, fill=palette["foundation_green"])
    kicker_width = draw.textlength(job["kicker"], font=kicker_font)
    draw.rectangle((MARGIN, 116, MARGIN + min(260, kicker_width), 123), fill=palette["muted_clay"])

    draw.rounded_rectangle((MARGIN, 150, MARGIN + 14, 414), radius=7, fill=palette["muted_clay"])

    headline_lines = job["headline"].splitlines()
    if len(headline_lines) != 2:
        raise ValueError("IMG-007 requires exactly two headline lines")
    headline_x = MARGIN + 36
    headline_y = 150
    max_headline_width = WIDTH - headline_x - MARGIN
    for index, line in enumerate(headline_lines):
        line_width = draw.textlength(line, font=headline_font)
        if line_width > max_headline_width:
            raise RuntimeError(f"Headline exceeds safe width: {line_width} > {max_headline_width}: {line}")
        fill = palette["slate"] if index == 0 else palette["foundation_green"]
        draw.text((headline_x, headline_y), line, font=headline_font, fill=fill)
        headline_y += 74

    body_y = headline_y + 18
    body_lines = wrap_by_pixels(draw, job["body"], body_font, 830)
    if len(body_lines) > 3:
        raise RuntimeError(f"Body exceeds three lines: {body_lines}")
    for line in body_lines:
        draw.text((headline_x, body_y), line, font=body_font, fill=palette["slate"])
        body_y += 42
    if body_y > PHOTO_TOP - 24:
        raise RuntimeError("Body collides with photo region")

    source_image = Image.open(io.BytesIO(source_bytes)).convert("RGB")
    photo = cover_crop(source_image, PHOTO_WIDTH, PHOTO_HEIGHT)
    photo = ImageEnhance.Contrast(photo).enhance(1.04)
    photo = ImageEnhance.Color(photo).enhance(0.84)
    warm_overlay = Image.new("RGB", photo.size, palette["warm_stone"])
    photo = Image.blend(photo, warm_overlay, 0.08)
    photo = rounded_photo(photo)

    draw.rounded_rectangle(
        (MARGIN - 8, PHOTO_TOP - 8, MARGIN + PHOTO_WIDTH + 8, PHOTO_TOP + PHOTO_HEIGHT + 8),
        radius=34,
        fill=palette["warm_stone"],
    )
    canvas.paste(photo, (MARGIN, PHOTO_TOP))

    draw.rectangle((0, CLOSING_TOP, WIDTH, 1248), fill=palette["foundation_green"])
    closing_width = draw.textlength(job["closing"], font=closing_font)
    if closing_width > WIDTH - MARGIN * 2:
        raise RuntimeError("Closing statement exceeds safe width")
    draw.text((WIDTH / 2, 1204), job["closing"], font=closing_font, fill=palette["off_white"], anchor="mm")

    credit_lines = [
        "Photo: USAID in Africa / public domain. Participatory land-use planning context.",
        "Contextual editorial image only; not a Mission GroundWork client, engagement, result, or endorsement.",
    ]
    credit_y = 1272
    for line in credit_lines:
        line_width = draw.textlength(line, font=credit_font)
        if line_width > WIDTH - MARGIN * 2:
            raise RuntimeError(f"Credit exceeds safe width: {line}")
        draw.text((MARGIN, credit_y), line, font=credit_font, fill="#6D6256")
        credit_y += 24
    if credit_y > HEIGHT - 12:
        raise RuntimeError("Credit exceeds bottom safe area")

    canvas.save(OUTPUT_PATH, format="PNG", optimize=True)

    receipt = {
        "schema_version": 1,
        "process_id": "MCLP-001",
        "receipt_id": "IMG-007-RENDER-REVISION-1",
        "artifact_id": "IMG-007",
        "revision": 1,
        "captured_at": datetime.now(timezone.utc).isoformat(),
        "status": "PASS_TECHNICAL",
        "evidence_state": "OBSERVED_ONCE",
        "terminal_state": "USER_REVIEW_REQUIRED",
        "production_method": job["production_method"],
        "family_test": {
            "project": "Mission GroundWork",
            "prior_artifact": "IMG-004",
            "distinct_source": True,
            "distinct_composition": True,
            "shared_project_quality_profile": True,
        },
        "layout_checks": {
            "headline_lines": len(headline_lines),
            "body_lines": len(body_lines),
            "text_photo_overlap": False,
            "continuous_action_band": True,
            "dashboard_cards_or_metric_tiles": False,
            "credit_within_safe_area": True,
        },
        "source": {
            "title": source["title"],
            "creator": source["creator"],
            "context": source["context"],
            "license": source["license"],
            "source_page": source["source_page"],
            "sha1": source_sha1,
            "bytes": len(source_bytes),
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
            "Independent creative and project-owner review remain pending.",
            "The photograph is contextual public-domain imagery, not client or outcome evidence.",
            "One second project image tests family consistency but does not establish unlimited template reuse.",
        ],
    }
    RECEIPT_PATH.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(receipt, indent=2))


if __name__ == "__main__":
    main()
