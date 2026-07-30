from __future__ import annotations

import hashlib
import io
import json
import math
import subprocess
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont

JOB_PATH = Path("media/jobs/VID-003-ownership-visual-essay.json")
OUTPUT_ROOT = Path("artifacts/mclp/VID-003")
OUTPUT_VIDEO = OUTPUT_ROOT / "VID-003-ownership-visual-essay.mp4"
SOURCE_PATH = OUTPUT_ROOT / "source-photo.jpg"
RECEIPT_PATH = OUTPUT_ROOT / "render-receipt.json"
STORYBOARD_PATH = OUTPUT_ROOT / "storyboard-contact-sheet.png"
SCENES_ROOT = OUTPUT_ROOT / "representative-scenes"

INTERNAL_WIDTH = 540
INTERNAL_HEIGHT = 960
OUTPUT_WIDTH = 1080
OUTPUT_HEIGHT = 1920
FPS = 24
DURATION_SECONDS = 15
TOTAL_FRAMES = FPS * DURATION_SECONDS
SCENE_SECONDS = 3
SCENE_FRAMES = FPS * SCENE_SECONDS
TRANSITION_SECONDS = 0.35
TRANSITION_FRAMES = round(FPS * TRANSITION_SECONDS)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def font_path(preferred: str, fallback: str) -> str:
    for candidate in (preferred, fallback):
        if Path(candidate).is_file():
            return candidate
    raise FileNotFoundError(f"No font found: {preferred} or {fallback}")


def cover_crop(image: Image.Image, width: int, height: int, focus_x: float, focus_y: float, zoom: float = 1.0) -> Image.Image:
    target_width = round(width * zoom)
    target_height = round(height * zoom)
    ratio = max(target_width / image.width, target_height / image.height)
    resized = image.resize((round(image.width * ratio), round(image.height * ratio)), Image.Resampling.LANCZOS)
    left = max(0, min(resized.width - target_width, round(resized.width * focus_x - target_width / 2)))
    top = max(0, min(resized.height - target_height, round(resized.height * focus_y - target_height / 2)))
    crop = resized.crop((left, top, left + target_width, top + target_height))
    if zoom != 1.0:
        crop = crop.resize((width, height), Image.Resampling.LANCZOS)
    return crop


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


def gradient_overlay(size: tuple[int, int], top_alpha: int, bottom_alpha: int, color: tuple[int, int, int]) -> Image.Image:
    overlay = Image.new("RGBA", size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    height = size[1]
    for y in range(height):
        alpha = round(top_alpha + (bottom_alpha - top_alpha) * y / max(1, height - 1))
        draw.line((0, y, size[0], y), fill=(*color, alpha))
    return overlay


def ease(value: float) -> float:
    value = max(0.0, min(1.0, value))
    return value * value * (3 - 2 * value)


def scene_frame(scene_index: int, local_progress: float, source: Image.Image, job: dict, fonts: dict[str, ImageFont.FreeTypeFont]) -> Image.Image:
    palette = job["brand"]
    green = palette["foundation_green"]
    stone = palette["warm_stone"]
    slate = palette["slate"]
    off_white = palette["off_white"]
    clay = palette["muted_clay"]

    if scene_index == 0:
        zoom = 1.0 + 0.045 * ease(local_progress)
        frame = cover_crop(source, INTERNAL_WIDTH, INTERNAL_HEIGHT, 0.57, 0.50, zoom)
        frame = ImageEnhance.Color(frame).enhance(0.82)
        frame = ImageEnhance.Contrast(frame).enhance(1.08)
        frame = frame.convert("RGBA")
        frame.alpha_composite(gradient_overlay(frame.size, 35, 190, (16, 35, 31)))
        draw = ImageDraw.Draw(frame)
        draw.text((34, 42), "MISSION GROUNDWORK", font=fonts["label"], fill=off_white)
        draw.rectangle((34, 78, 132, 84), fill=clay)
        headline = job["scenes"][0]["headline"]
        lines = wrap_by_pixels(draw, headline, fonts["headline"], 455)
        y = 690
        for line in lines:
            draw.text((34, y), line, font=fonts["headline"], fill=off_white)
            y += 58
        draw.text((34, 885), "Context photo · USAID / public domain", font=fonts["credit"], fill="#D7DDD8")
        return frame.convert("RGB")

    if scene_index == 1:
        zoom = 1.08 - 0.035 * ease(local_progress)
        frame = cover_crop(source, INTERNAL_WIDTH, INTERNAL_HEIGHT, 0.44, 0.56, zoom)
        frame = ImageEnhance.Color(frame).enhance(0.65)
        frame = ImageEnhance.Contrast(frame).enhance(1.12)
        tint = Image.new("RGB", frame.size, green)
        frame = Image.blend(frame, tint, 0.36).convert("RGBA")
        frame.alpha_composite(gradient_overlay(frame.size, 55, 155, (13, 31, 27)))
        draw = ImageDraw.Draw(frame)
        bar_height = round(230 * ease(local_progress))
        draw.rectangle((0, 0, 18, bar_height), fill=clay)
        draw.text((34, 90), "THE OPERATING QUESTION", font=fonts["label"], fill=stone)
        lines = wrap_by_pixels(draw, job["scenes"][1]["headline"], fonts["headline_small"], 455)
        y = 330
        for line in lines:
            draw.text((34, y), line, font=fonts["headline_small"], fill=off_white)
            y += 54
        draw.line((34, 515, 330 + round(150 * ease(local_progress)), 515), fill=stone, width=5)
        draw.text((34, 860), "Important work still needs a named owner.", font=fonts["body"], fill=off_white)
        return frame.convert("RGB")

    if scene_index == 2:
        frame = Image.new("RGB", (INTERNAL_WIDTH, INTERNAL_HEIGHT), off_white)
        draw = ImageDraw.Draw(frame)
        ghost = cover_crop(source, 250, 960, 0.68, 0.50, 1.0)
        ghost = ImageEnhance.Color(ghost).enhance(0.15)
        ghost = ImageEnhance.Contrast(ghost).enhance(0.95)
        ghost_tint = Image.new("RGB", ghost.size, stone)
        ghost = Image.blend(ghost, ghost_tint, 0.52)
        ghost.putalpha(round(85 + 35 * ease(local_progress)))
        frame = frame.convert("RGBA")
        frame.alpha_composite(ghost, (290, 0))
        draw = ImageDraw.Draw(frame)
        draw.text((34, 62), "01 / CLARIFY", font=fonts["label"], fill=clay)
        words = ["NAME", "THE", "DECISION."]
        y = 225
        for index, word in enumerate(words):
            offset = round((1 - ease(local_progress)) * (28 + index * 12))
            fill = green if index < 2 else clay
            draw.text((34 + offset, y), word, font=fonts["headline_large"], fill=fill)
            y += 105
        draw.rectangle((34, 600, 170 + round(180 * ease(local_progress)), 608), fill=stone)
        draw.text((34, 655), "Before activity becomes rework.", font=fonts["body"], fill=slate)
        draw.text((34, 890), "Mission GroundWork", font=fonts["credit_bold"], fill=green)
        return frame.convert("RGB")

    if scene_index == 3:
        frame = Image.new("RGB", (INTERNAL_WIDTH, INTERNAL_HEIGHT), green)
        detail = cover_crop(source, 245, INTERNAL_HEIGHT, 0.36, 0.58, 1.05 - 0.03 * ease(local_progress))
        detail = ImageEnhance.Color(detail).enhance(0.72)
        detail = ImageEnhance.Contrast(detail).enhance(1.1)
        frame.paste(detail, (0, 0))
        overlay = Image.new("RGBA", (245, INTERNAL_HEIGHT), (46, 94, 78, 55))
        frame = frame.convert("RGBA")
        frame.alpha_composite(overlay, (0, 0))
        draw = ImageDraw.Draw(frame)
        draw.text((280, 78), "02 / ALIGN", font=fonts["label"], fill=stone)
        lines = job["scenes"][3]["headline"].splitlines()
        y = 255
        for index, line in enumerate(lines):
            offset = round((1 - ease(local_progress)) * 24)
            draw.text((280 + offset, y), line, font=fonts["headline_tight"], fill=off_white)
            y += 115
        line_width = round(205 * ease(local_progress))
        draw.rectangle((280, 590, 280 + line_width, 598), fill=clay)
        draw.text((280, 650), "The handoff is part of the work.", font=fonts["body_narrow"], fill="#E6ECE8")
        draw.text((280, 875), "Context photo · not a client or case study", font=fonts["credit"], fill="#CCD8D0")
        return frame.convert("RGB")

    frame = Image.new("RGB", (INTERNAL_WIDTH, INTERNAL_HEIGHT), off_white)
    draw = ImageDraw.Draw(frame)
    horizon_y = 510
    line_start = 70
    line_end = 470
    progress_width = round((line_end - line_start) * ease(local_progress))
    draw.text((34, 64), "MISSION GROUNDWORK", font=fonts["label"], fill=green)
    draw.text((270, 235), "START ON", font=fonts["headline_end"], fill=slate, anchor="ma")
    draw.text((270, 325), "SOLID GROUND.", font=fonts["headline_end"], fill=green, anchor="ma")
    draw.rectangle((line_start, horizon_y, line_start + progress_width, horizon_y + 8), fill=clay)
    cta = job["scenes"][4]["cta"]
    cta_width = round(draw.textlength(cta, font=fonts["cta"]) + 58)
    cta_left = round((INTERNAL_WIDTH - cta_width) / 2)
    draw.rounded_rectangle((cta_left, 625, cta_left + cta_width, 686), radius=18, fill=green)
    draw.text((INTERNAL_WIDTH / 2, 656), cta, font=fonts["cta"], fill=off_white, anchor="mm")
    draw.text((270, 750), "Clarify the work. Align the people.", font=fonts["body"], fill=slate, anchor="ma")
    draw.text((270, 790), "Build the operating foundation.", font=fonts["body"], fill=slate, anchor="ma")
    draw.text((270, 900), "Review-only canary · publishing disabled", font=fonts["credit"], fill="#697470", anchor="ma")
    return frame


def blend_transition(current: Image.Image, next_frame: Image.Image, alpha: float) -> Image.Image:
    return Image.blend(current, next_frame, ease(alpha))


def ffprobe(path: Path) -> dict:
    completed = subprocess.run(
        [
            "ffprobe", "-v", "error",
            "-show_entries", "format=duration,size,bit_rate:stream=index,codec_type,codec_name,width,height,r_frame_rate,pix_fmt",
            "-of", "json", str(path),
        ],
        capture_output=True,
        text=True,
        check=True,
    )
    return json.loads(completed.stdout)


def main() -> None:
    job = json.loads(JOB_PATH.read_text(encoding="utf-8"))
    if job["process_id"] != "MCLP-001" or job["artifact_id"] != "VID-003":
        raise ValueError("Unexpected job identity")
    if job.get("revision") != 1:
        raise ValueError("Unexpected revision")
    if job["production_method"] != "deterministic_multi_scene_editorial_video":
        raise ValueError("Unexpected production method")
    if job["publishing_authorized"] is not False or job["paid_service_authorized"] is not False:
        raise ValueError("Publishing and paid service use must remain disabled")
    if len(job["scenes"]) != 5:
        raise ValueError("VID-003 requires exactly five scenes")
    if job["format"] != {"width": 1080, "height": 1920, "fps": 24, "duration_seconds": 15, "audio": False}:
        raise ValueError("Unexpected output format contract")

    OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)
    SCENES_ROOT.mkdir(parents=True, exist_ok=True)
    request = urllib.request.Request(job["source_photo"]["url"], headers={"User-Agent": "MCLP-001-VID-003/1.0"})
    with urllib.request.urlopen(request, timeout=90) as response:
        source_bytes = response.read()
        content_type = response.headers.get("Content-Type", "")
    if not content_type.startswith("image/") or len(source_bytes) < 100_000:
        raise RuntimeError(f"Invalid source response: {content_type}, {len(source_bytes)} bytes")
    source_sha1 = hashlib.sha1(source_bytes).hexdigest()
    if source_sha1 != job["source_photo"]["expected_sha1"]:
        raise RuntimeError(f"Source SHA-1 mismatch: {source_sha1}")
    SOURCE_PATH.write_bytes(source_bytes)
    source = Image.open(io.BytesIO(source_bytes)).convert("RGB")

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
    fonts = {
        "label": ImageFont.truetype(sans_bold, 19),
        "headline": ImageFont.truetype(serif, 47),
        "headline_small": ImageFont.truetype(serif, 43),
        "headline_large": ImageFont.truetype(serif, 66),
        "headline_tight": ImageFont.truetype(serif, 36),
        "headline_end": ImageFont.truetype(serif, 54),
        "body": ImageFont.truetype(sans, 23),
        "body_narrow": ImageFont.truetype(sans, 20),
        "cta": ImageFont.truetype(sans_bold, 21),
        "credit": ImageFont.truetype(sans, 13),
        "credit_bold": ImageFont.truetype(sans_bold, 14),
    }

    representative = []
    for scene_index in range(5):
        image = scene_frame(scene_index, 0.55, source, job, fonts)
        path = SCENES_ROOT / f"scene-{scene_index + 1}.png"
        image.resize((OUTPUT_WIDTH, OUTPUT_HEIGHT), Image.Resampling.LANCZOS).save(path, format="PNG", optimize=True)
        representative.append(path)

    storyboard = Image.new("RGB", (OUTPUT_WIDTH * 5, OUTPUT_HEIGHT), "white")
    for index, path in enumerate(representative):
        storyboard.paste(Image.open(path).convert("RGB"), (index * OUTPUT_WIDTH, 0))
    storyboard = storyboard.resize((1350, 480), Image.Resampling.LANCZOS)
    storyboard.save(STORYBOARD_PATH, format="PNG", optimize=True)

    command = [
        "ffmpeg", "-y",
        "-f", "rawvideo", "-vcodec", "rawvideo", "-pix_fmt", "rgb24",
        "-s", f"{INTERNAL_WIDTH}x{INTERNAL_HEIGHT}", "-r", str(FPS), "-i", "-",
        "-an",
        "-vf", f"scale={OUTPUT_WIDTH}:{OUTPUT_HEIGHT}:flags=lanczos,format=yuv420p",
        "-c:v", "libx264", "-preset", "medium", "-crf", "18",
        "-movflags", "+faststart", str(OUTPUT_VIDEO),
    ]
    process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
    assert process.stdin is not None
    assert process.stderr is not None
    try:
        for frame_index in range(TOTAL_FRAMES):
            scene_index = min(4, frame_index // SCENE_FRAMES)
            frame_in_scene = frame_index - scene_index * SCENE_FRAMES
            local_progress = frame_in_scene / max(1, SCENE_FRAMES - 1)
            frame = scene_frame(scene_index, local_progress, source, job, fonts)
            if scene_index < 4 and frame_in_scene >= SCENE_FRAMES - TRANSITION_FRAMES:
                transition_index = frame_in_scene - (SCENE_FRAMES - TRANSITION_FRAMES)
                alpha = transition_index / max(1, TRANSITION_FRAMES - 1)
                next_frame = scene_frame(scene_index + 1, 0.0, source, job, fonts)
                frame = blend_transition(frame, next_frame, alpha)
            process.stdin.write(frame.convert("RGB").tobytes())
        process.stdin.close()
        stderr = process.stderr.read().decode("utf-8", errors="replace")
        return_code = process.wait()
        if return_code != 0:
            raise RuntimeError(f"FFmpeg failed with exit code {return_code}: {stderr[-4000:]}")
    finally:
        if process.stdin and not process.stdin.closed:
            process.stdin.close()

    media = ffprobe(OUTPUT_VIDEO)
    streams = media.get("streams", [])
    video_streams = [stream for stream in streams if stream.get("codec_type") == "video"]
    audio_streams = [stream for stream in streams if stream.get("codec_type") == "audio"]
    if len(video_streams) != 1 or audio_streams:
        raise RuntimeError("VID-003 must contain exactly one video stream and no audio stream")
    stream = video_streams[0]
    if int(stream["width"]) != OUTPUT_WIDTH or int(stream["height"]) != OUTPUT_HEIGHT:
        raise RuntimeError("Unexpected output dimensions")
    duration = float(media["format"]["duration"])
    if not 14.8 <= duration <= 15.2:
        raise RuntimeError(f"Unexpected duration: {duration}")

    receipt = {
        "schema_version": 1,
        "process_id": "MCLP-001",
        "receipt_id": "VID-003-RENDER-REVISION-1",
        "artifact_id": "VID-003",
        "revision": 1,
        "captured_at": datetime.now(timezone.utc).isoformat(),
        "status": "PASS_TECHNICAL",
        "evidence_state": "OBSERVED_ONCE",
        "terminal_state": "USER_REVIEW_REQUIRED",
        "production_method": job["production_method"],
        "scene_count": len(job["scenes"]),
        "distinct_scene_constructions": 5,
        "single_static_image_loop": False,
        "source": {
            "title": job["source_photo"]["title"],
            "creator": job["source_photo"]["creator"],
            "license": job["source_photo"]["license"],
            "source_page": job["source_photo"]["source_page"],
            "sha1": source_sha1,
            "saved_path": str(SOURCE_PATH),
        },
        "output": {
            "path": str(OUTPUT_VIDEO),
            "bytes": OUTPUT_VIDEO.stat().st_size,
            "sha256": sha256(OUTPUT_VIDEO),
            "duration_seconds": duration,
            "width": int(stream["width"]),
            "height": int(stream["height"]),
            "fps": stream.get("r_frame_rate"),
            "codec": stream.get("codec_name"),
            "pix_fmt": stream.get("pix_fmt"),
            "audio_streams": len(audio_streams),
        },
        "storyboard": {
            "path": str(STORYBOARD_PATH),
            "sha256": sha256(STORYBOARD_PATH),
            "representative_scene_paths": [str(path) for path in representative],
        },
        "publishing_authorized": False,
        "paid_service_used": False,
        "limitations": [
            "Creative and project-owner review remain pending.",
            "The contextual photo is not a Mission GroundWork client, case study, or event.",
            "This silent canary does not establish audio or multimedia quality.",
            "Observed-once output does not promote the deterministic short-video lane."
        ],
    }
    RECEIPT_PATH.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(receipt, indent=2))


if __name__ == "__main__":
    main()
