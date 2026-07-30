from __future__ import annotations

import hashlib
import importlib.util
import io
import json
import subprocess
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFont

BASE_SCRIPT = Path("scripts/render_mclp_vid_003.py")
SPEC = importlib.util.spec_from_file_location("vid003_base", BASE_SCRIPT)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("Unable to load VID-003 base renderer")
base = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(base)

JOB_PATH = Path("media/jobs/VID-003-ownership-visual-essay-revision-2.json")
OUTPUT_ROOT = Path("artifacts/mclp/VID-003-revision-2")
OUTPUT_VIDEO = OUTPUT_ROOT / "VID-003-ownership-visual-essay.mp4"
SOURCE_PATH = OUTPUT_ROOT / "source-photo.jpg"
RECEIPT_PATH = OUTPUT_ROOT / "render-receipt.json"
STORYBOARD_PATH = OUTPUT_ROOT / "storyboard-contact-sheet.png"
SCENES_ROOT = OUTPUT_ROOT / "representative-scenes"

INTERNAL_WIDTH = base.INTERNAL_WIDTH
INTERNAL_HEIGHT = base.INTERNAL_HEIGHT
OUTPUT_WIDTH = base.OUTPUT_WIDTH
OUTPUT_HEIGHT = base.OUTPUT_HEIGHT
FPS = base.FPS
DURATION_SECONDS = base.DURATION_SECONDS
TOTAL_FRAMES = base.TOTAL_FRAMES
SCENE_FRAMES = base.SCENE_FRAMES
TRANSITION_FRAMES = base.TRANSITION_FRAMES


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def scene_frame_v2(scene_index: int, local_progress: float, source: Image.Image, job: dict, fonts: dict[str, ImageFont.FreeTypeFont]) -> Image.Image:
    if scene_index != 3:
        return base.scene_frame(scene_index, local_progress, source, job, fonts)

    palette = job["brand"]
    green = palette["foundation_green"]
    stone = palette["warm_stone"]
    off_white = palette["off_white"]
    clay = palette["muted_clay"]

    photo_width = 190
    text_left = 222
    text_right = INTERNAL_WIDTH - 28
    panel_width = text_right - text_left

    frame = Image.new("RGB", (INTERNAL_WIDTH, INTERNAL_HEIGHT), green)
    detail = base.cover_crop(source, photo_width, INTERNAL_HEIGHT, 0.36, 0.58, 1.05 - 0.03 * base.ease(local_progress))
    detail = ImageEnhance.Color(detail).enhance(0.72)
    detail = ImageEnhance.Contrast(detail).enhance(1.1)
    frame.paste(detail, (0, 0))
    overlay = Image.new("RGBA", (photo_width, INTERNAL_HEIGHT), (46, 94, 78, 55))
    frame = frame.convert("RGBA")
    frame.alpha_composite(overlay, (0, 0))
    draw = ImageDraw.Draw(frame)

    draw.text((text_left, 72), "02 / ALIGN", font=fonts["label"], fill=stone)
    lines = job["scenes"][3]["headline"].splitlines()
    if len(lines) != 4:
        raise ValueError("Revision 2 scene 4 requires exactly four headline lines")
    for line in lines:
        if draw.textlength(line, font=fonts["headline_scene4"]) > panel_width:
            raise RuntimeError(f"Scene 4 line exceeds safe panel width: {line}")

    y = 210
    for index, line in enumerate(lines):
        offset = round((1 - base.ease(local_progress)) * (18 + index * 3))
        fill = off_white if index % 2 == 0 else "#F0E8DD"
        draw.text((text_left + offset, y), line, font=fonts["headline_scene4"], fill=fill)
        y += 82

    line_width = round((panel_width - 8) * base.ease(local_progress))
    draw.rectangle((text_left, 570, text_left + line_width, 578), fill=clay)
    body = "The handoff is part\nof the work."
    body_lines = body.splitlines()
    body_y = 630
    for line in body_lines:
        if draw.textlength(line, font=fonts["body_narrow"]) > panel_width:
            raise RuntimeError(f"Scene 4 body exceeds safe panel width: {line}")
        draw.text((text_left, body_y), line, font=fonts["body_narrow"], fill="#E6ECE8")
        body_y += 38
    draw.text((text_left, 882), "Context photo · not a client or case study", font=fonts["credit_scene4"], fill="#CCD8D0")
    return frame.convert("RGB")


def validate_fixed_text(job: dict, fonts: dict[str, ImageFont.FreeTypeFont]) -> dict:
    probe = Image.new("RGB", (INTERNAL_WIDTH, INTERNAL_HEIGHT), "white")
    draw = ImageDraw.Draw(probe)
    checks: dict[str, float | int | bool] = {}

    scene4_width = INTERNAL_WIDTH - 28 - 222
    scene4_lines = job["scenes"][3]["headline"].splitlines()
    checks["scene4_line_count"] = len(scene4_lines)
    checks["scene4_max_line_width_px"] = round(max(draw.textlength(line, font=fonts["headline_scene4"]) for line in scene4_lines))
    checks["scene4_panel_width_px"] = scene4_width
    checks["scene4_headline_fits"] = checks["scene4_max_line_width_px"] <= scene4_width

    cta = job["scenes"][4]["cta"]
    cta_width = draw.textlength(cta, font=fonts["cta"]) + 58
    checks["scene5_cta_box_width_px"] = round(cta_width)
    checks["scene5_cta_fits"] = cta_width <= INTERNAL_WIDTH - 68

    checks["scene3_name_width_px"] = round(draw.textlength("DECISION.", font=fonts["headline_large"]))
    checks["scene3_name_fits"] = checks["scene3_name_width_px"] <= 255

    if not all(value for key, value in checks.items() if key.endswith("_fits")):
        raise RuntimeError(f"Fixed text preflight failed: {checks}")
    return checks


def main() -> None:
    job = json.loads(JOB_PATH.read_text(encoding="utf-8"))
    if job["process_id"] != "MCLP-001" or job["artifact_id"] != "VID-003":
        raise ValueError("Unexpected job identity")
    if job.get("revision") != 2:
        raise ValueError("Revision 2 renderer requires revision 2 job")
    if job["production_method"] != "deterministic_multi_scene_editorial_video":
        raise ValueError("Unexpected production method")
    if job["publishing_authorized"] is not False or job["paid_service_authorized"] is not False:
        raise ValueError("Publishing and paid service use must remain disabled")
    if len(job["scenes"]) != 5:
        raise ValueError("VID-003 requires exactly five scenes")

    OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)
    SCENES_ROOT.mkdir(parents=True, exist_ok=True)
    request = urllib.request.Request(job["source_photo"]["url"], headers={"User-Agent": "MCLP-001-VID-003/2.0"})
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

    serif = base.font_path(
        "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf",
        "/usr/share/fonts/truetype/liberation2/LiberationSerif-Bold.ttf",
    )
    sans = base.font_path(
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf",
    )
    sans_bold = base.font_path(
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf",
    )
    fonts = {
        "label": ImageFont.truetype(sans_bold, 19),
        "headline": ImageFont.truetype(serif, 47),
        "headline_small": ImageFont.truetype(serif, 43),
        "headline_large": ImageFont.truetype(serif, 66),
        "headline_tight": ImageFont.truetype(serif, 36),
        "headline_scene4": ImageFont.truetype(serif, 34),
        "headline_end": ImageFont.truetype(serif, 54),
        "body": ImageFont.truetype(sans, 23),
        "body_narrow": ImageFont.truetype(sans, 20),
        "cta": ImageFont.truetype(sans_bold, 21),
        "credit": ImageFont.truetype(sans, 13),
        "credit_scene4": ImageFont.truetype(sans, 10),
        "credit_bold": ImageFont.truetype(sans_bold, 14),
    }
    preflight = validate_fixed_text(job, fonts)

    representative: list[Path] = []
    for scene_index in range(5):
        image = scene_frame_v2(scene_index, 0.55, source, job, fonts)
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
    assert process.stdin is not None and process.stderr is not None
    try:
        for frame_index in range(TOTAL_FRAMES):
            scene_index = min(4, frame_index // SCENE_FRAMES)
            frame_in_scene = frame_index - scene_index * SCENE_FRAMES
            local_progress = frame_in_scene / max(1, SCENE_FRAMES - 1)
            frame = scene_frame_v2(scene_index, local_progress, source, job, fonts)
            if scene_index < 4 and frame_in_scene >= SCENE_FRAMES - TRANSITION_FRAMES:
                transition_index = frame_in_scene - (SCENE_FRAMES - TRANSITION_FRAMES)
                alpha = transition_index / max(1, TRANSITION_FRAMES - 1)
                next_frame = scene_frame_v2(scene_index + 1, 0.0, source, job, fonts)
                frame = base.blend_transition(frame, next_frame, alpha)
            process.stdin.write(frame.convert("RGB").tobytes())
        process.stdin.close()
        stderr = process.stderr.read().decode("utf-8", errors="replace")
        return_code = process.wait()
        if return_code != 0:
            raise RuntimeError(f"FFmpeg failed with exit code {return_code}: {stderr[-4000:]}")
    finally:
        if process.stdin and not process.stdin.closed:
            process.stdin.close()

    media = base.ffprobe(OUTPUT_VIDEO)
    video_streams = [stream for stream in media.get("streams", []) if stream.get("codec_type") == "video"]
    audio_streams = [stream for stream in media.get("streams", []) if stream.get("codec_type") == "audio"]
    if len(video_streams) != 1 or audio_streams:
        raise RuntimeError("VID-003 revision 2 must contain exactly one video stream and no audio stream")
    stream = video_streams[0]
    duration = float(media["format"]["duration"])
    if int(stream["width"]) != OUTPUT_WIDTH or int(stream["height"]) != OUTPUT_HEIGHT:
        raise RuntimeError("Unexpected output dimensions")
    if not 14.8 <= duration <= 15.2:
        raise RuntimeError(f"Unexpected duration: {duration}")

    receipt = {
        "schema_version": 1,
        "process_id": "MCLP-001",
        "receipt_id": "VID-003-RENDER-REVISION-2",
        "artifact_id": "VID-003",
        "revision": 2,
        "captured_at": datetime.now(timezone.utc).isoformat(),
        "status": "PASS_TECHNICAL",
        "evidence_state": "REPEATED",
        "terminal_state": "USER_REVIEW_REQUIRED",
        "production_method": job["production_method"],
        "scene_count": len(job["scenes"]),
        "distinct_scene_constructions": 5,
        "single_static_image_loop": False,
        "fixed_text_preflight": preflight,
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
            "Repeated technical output does not promote the deterministic short-video lane."
        ],
    }
    RECEIPT_PATH.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(receipt, indent=2))


if __name__ == "__main__":
    main()
