from __future__ import annotations

import hashlib
import io
import json
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
MARGIN = 56
PHOTO_TOP = 150
PHOTO_HEIGHT = 610
PHOTO_WIDTH = WIDTH - MARGIN * 2
TEXT_TOP = 825


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def font_path(preferred: str, fallback: str) -> str:
    for candidate in (preferred, fallback):
        if Path(candidate).is_file():
            return candidate
    raise FileNotFoundError(f"No font found: {preferred} or {fallback}")


def cover_crop(image: Image.Image, width: int, height: int, focus_x: float = 0.55, focus_y: float = 0.52) -> Image.Image:
    ratio = max(width / image.width, height / image.height)
    resized = image.resize((round(image.width * ratio), round(image.height * ratio)), Image.Resampling.LANCZOS)
    left = max(0, min(resized.width - width, round(resized.width * focus_x - width / 2)))
    top = max(0, min(resized.height - height, round(resized.height * focus_y - height / 2)))
    return resized.crop((left, top, left + width, top + height))


def rounded_mask(size: tuple[int, int], radius: int) -> Image.Image:
    mask = Image.new("L", size, 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, size[0], size[1]), radius=radius, fill=255)
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
    if job.get("revision") != 2:
        raise ValueError("This renderer is restricted to IMG-004 revision 2")
    if job["production_method"] != "deterministic_editorial_photo_composition":
        raise ValueError("Unexpected production method")
    if job["publishing_authorized"] is not False or job["paid_service_authorized"] is not False:
        raise ValueError("Publishing and paid service use must remain disabled")

    OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)
    request = urllib.request.Request(
        job["source_photo"]["url"],
        headers={"User-Agent": "MCLP-001-deterministic-editorial/2.0"},
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

    serif = font_path(
        "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf",
        "/usr/share/fonts/truetype/liberation2/LiberationSerif-Bold.ttf",
    )
    sans = font_path(
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf",
    )
    sans_bold = font_path(
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf",
    )
    headline_font = ImageFont.truetype(serif, 60)
    body_font = ImageFont.truetype(sans, 31)
    label_font = ImageFont.truetype(sans_bold, 22)
    cta_font = ImageFont.truetype(sans_bold, 25)
    credit_font = ImageFont.truetype(sans, 18)

    draw.text((MARGIN, 54), "MISSION GROUNDWORK", font=label_font, fill=palette["foundation_green"])
    draw.text((WIDTH - MARGIN, 54), "OPERATING CLARITY", font=label_font, fill=palette["slate"], anchor="ra")
    draw.rectangle((MARGIN, 104, MARGIN + 150, 112), fill=palette["muted_clay"])

    source = Image.open(io.BytesIO(source_bytes)).convert("RGB")
    photo = cover_crop(source, PHOTO_WIDTH, PHOTO_HEIGHT)
    photo = ImageEnhance.Color(photo).enhance(0.78)
    photo = ImageEnhance.Contrast(photo).enhance(1.06)
    warm = Image.new("RGB", photo.size, palette["warm_stone"])
    photo = Image.blend(photo, warm, 0.07)

    shadow = Image.new("RGBA", (PHOTO_WIDTH + 40, PHOTO_HEIGHT + 40), (0, 0, 0, 0))
    shadow_draw = ImageDraw.Draw(shadow)
    shadow_draw.rounded_rectangle((20, 20, PHOTO_WIDTH + 20, PHOTO_HEIGHT + 20), radius=34, fill=(25, 35, 34, 55))
    shadow = shadow.filter(ImageFilter.GaussianBlur(15))
    canvas.paste(shadow, (MARGIN - 20, PHOTO_TOP - 20), shadow)
    canvas.paste(photo, (MARGIN, PHOTO_TOP), rounded_mask(photo.size, 30))

    lower_overlay = Image.new("RGBA", photo.size, (0, 0, 0, 0))
    overlay_draw = ImageDraw.Draw(lower_overlay)
    for y in range(280):
        alpha = round(150 * (y / 279) ** 1.6)
        overlay_draw.line((0, PHOTO_HEIGHT - 280 + y, PHOTO_WIDTH, PHOTO_HEIGHT - 280 + y), fill=(20, 38, 33, alpha))
    canvas.paste(lower_overlay, (MARGIN, PHOTO_TOP), lower_overlay)
    draw.text((MARGIN + 30, PHOTO_TOP + PHOTO_HEIGHT - 44), "CONTEXT: COMMUNITY DECISION-MAKING", font=label_font, fill=palette["off_white"], anchor="ls")

    headline_lines = job["headline"].splitlines()
    if len(headline_lines) != 2:
        raise ValueError("Revision 2 requires exactly two headline lines")
    y = TEXT_TOP
    draw.text((MARGIN, y), headline_lines[0], font=headline_font, fill=palette["foundation_green"])
    y += 72
    draw.text((MARGIN, y), headline_lines[1], font=headline_font, fill=palette["muted_clay"])

    body_y = y + 92
    body_lines = wrap_by_pixels(draw, job["body"], body_font, 685)
    for line in body_lines:
        draw.text((MARGIN, body_y), line, font=body_font, fill=palette["slate"])
        body_y += 43

    cta_text_width = draw.textlength(job["cta"], font=cta_font)
    cta_width = round(cta_text_width + 64)
    cta_height = 62
    cta_x = WIDTH - MARGIN - cta_width
    cta_y = 1122
    if cta_x < 590 or cta_x + cta_width > WIDTH - MARGIN:
        raise RuntimeError("CTA bounds violate layout contract")
    draw.rounded_rectangle((cta_x, cta_y, cta_x + cta_width, cta_y + cta_height), radius=18, fill=palette["foundation_green"])
    draw.text((cta_x + cta_width / 2, cta_y + cta_height / 2), job["cta"], font=cta_font, fill=palette["off_white"], anchor="mm")

    draw.text((MARGIN, 1140), "HELPING YOUR TEAM START", font=label_font, fill=palette["slate"])
    draw.text((MARGIN, 1172), "ON SOLID GROUND.", font=label_font, fill=palette["foundation_green"])
    draw.line((MARGIN, 1212, MARGIN + 225, 1212), fill=palette["warm_stone"], width=4)

    credit_lines = [
        "Context photo: Community meeting, Sierra Leone — USAID/E. Benya, public domain.",
        "Contextual imagery only; not a Mission GroundWork client or case study.",
    ]
    credit_y = 1250
    for line in credit_lines:
        if draw.textlength(line, font=credit_font) > WIDTH - MARGIN * 2:
            raise RuntimeError("Credit line exceeds safe width")
        draw.text((MARGIN, credit_y), line, font=credit_font, fill="#65706F")
        credit_y += 27
    if credit_y > HEIGHT - 20:
        raise RuntimeError("Credit exceeds bottom safe area")

    canvas.save(OUTPUT_PATH, format="PNG", optimize=True)

    receipt = {
        "schema_version": 1,
        "process_id": "MCLP-001",
        "receipt_id": "IMG-004-RENDER-REVISION-2",
        "artifact_id": "IMG-004",
        "revision": 2,
        "captured_at": datetime.now(timezone.utc).isoformat(),
        "status": "PASS_TECHNICAL",
        "evidence_state": "OBSERVED_ONCE",
        "terminal_state": "USER_REVIEW_REQUIRED",
        "production_method": job["production_method"],
        "layout_checks": {
            "separate_photo_and_type_regions": True,
            "cta_full_text_width_px": round(cta_text_width),
            "cta_box_width_px": cta_width,
            "credit_within_safe_area": True,
            "minimum_margin_px": MARGIN,
        },
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
