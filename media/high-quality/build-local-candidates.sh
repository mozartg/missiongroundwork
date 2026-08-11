#!/usr/bin/env bash
set -euo pipefail

ROOT="${1:-$(pwd)}"
IN="${CLOUD_PACKAGE_DIR:-$ROOT/cloud-package}"
KIT="${LOCAL_VOICE_KIT_DIR:-$ROOT/local-voice-kit}"
OUT="${OUTPUT_DIR:-$ROOT/deliverables}"
FONT="/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_BOLD="/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

mkdir -p "$OUT"

SCRIPT="Busy teams do not usually need another plan. They need clarity. Who owns the work? What happens next? Where is support missing? Mission GroundWork helps nonprofit leaders turn activity into accountable action, so the team can move forward on solid ground."

# C's narration is synthesized by the downloaded Piper runtime. The fallback
# patch is only needed in restricted sandboxes that do not expose /proc/self/exe.
PIPER_RUN="$KIT/piper/piper"
chmod +x "$PIPER_RUN"
if [[ ! -e /proc/self/exe ]]; then
  PIPER_RUN="$OUT/piper-sandbox"
  cp "$KIT/piper/piper" "$PIPER_RUN"
  offset="$(grep -aob '/proc/self/exe' "$PIPER_RUN" | head -n 1 | cut -d: -f1)"
  printf '/dev/null\0\0\0\0\0' | dd of="$PIPER_RUN" bs=1 seek="$offset" conv=notrunc status=none
  chmod +x "$PIPER_RUN"
fi

export LD_LIBRARY_PATH="$KIT/piper${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
printf '%s\n' "$SCRIPT" | "$PIPER_RUN" \
  --model "$KIT/model/en_US-joe-medium.onnx" \
  --espeak_data "$KIT/piper/espeak-ng-data" \
  --tashkeel_model "$KIT/piper/libtashkeel_model.ort" \
  --length_scale 1.04 \
  --sentence_silence 0.28 \
  --output_file "$OUT/narration-local.wav"

# B — cloud narration, local editorial system. Minimal top identity, three
# manually timed lower-thirds, subtle reframing, voice-led music ducking.
ffmpeg -hide_banner -y \
  -i "$IN/visual-master.mp4" \
  -i "$IN/narration-cloud.mp3" \
  -stream_loop -1 -i "$IN/music.ogg" \
  -filter_complex "\
[0:v]scale=1188:2112,crop=1080:1920:x='54+28*sin(t*0.35)':y='96+18*cos(t*0.25)',\
eq=contrast=1.06:saturation=0.88:brightness=-0.015,vignette=PI/7,\
drawbox=x=0:y=0:w=iw:h=235:color=0x071C2C@0.78:t=fill,\
drawbox=x=76:y=76:w=7:h=92:color=0xE9C46A@1:t=fill,\
drawtext=fontfile=$FONT_BOLD:text='MISSION':fontcolor=white:fontsize=37:x=106:y=73,\
drawtext=fontfile=$FONT_BOLD:text='GROUNDWORK':fontcolor=0xF4D88A:fontsize=37:x=106:y=120,\
drawtext=fontfile=$FONT:text='OPERATING CLARITY FOR NONPROFIT TEAMS':fontcolor=white@0.78:fontsize=21:x=535-text_w/2:y=185,\
drawbox=x=64:y=1470:w=952:h=300:color=0x071C2C@0.80:t=fill:enable='between(t,0.4,5.2)',\
drawtext=fontfile=$FONT_BOLD:text='MAKE OWNERSHIP VISIBLE':fontcolor=white:fontsize=47:x=96:y=1537:enable='between(t,0.4,5.2)',\
drawtext=fontfile=$FONT:text='Clarity begins with who owns the work.':fontcolor=0xF4D88A:fontsize=31:x=96:y=1620:enable='between(t,0.4,5.2)',\
drawbox=x=64:y=1470:w=952:h=300:color=0x071C2C@0.80:t=fill:enable='between(t,5.2,11.1)',\
drawtext=fontfile=$FONT_BOLD:text='NAME THE NEXT STEP':fontcolor=white:fontsize=47:x=96:y=1537:enable='between(t,5.2,11.1)',\
drawtext=fontfile=$FONT:text='Activity becomes accountable action.':fontcolor=0xF4D88A:fontsize=31:x=96:y=1620:enable='between(t,5.2,11.1)',\
drawbox=x=64:y=1470:w=952:h=300:color=0x071C2C@0.80:t=fill:enable='between(t,11.1,17.3)',\
drawtext=fontfile=$FONT_BOLD:text='MOVE ON SOLID GROUND':fontcolor=white:fontsize=47:x=96:y=1537:enable='between(t,11.1,17.3)',\
drawtext=fontfile=$FONT:text='See where support is missing.':fontcolor=0xF4D88A:fontsize=31:x=96:y=1620:enable='between(t,11.1,17.3)',\
fade=t=in:st=0:d=0.35,fade=t=out:st=16.8:d=0.4[v];\
[1:a]highpass=f=70,lowpass=f=10500,acompressor=threshold=-20dB:ratio=2.5:attack=12:release=120,loudnorm=I=-16:LRA=6:TP=-1.5,asplit=2[bvoice_sc][bvoice_mix];\
[2:a]volume=0.14[bmusic];\
[bmusic][bvoice_sc]sidechaincompress=threshold=0.025:ratio=12:attack=18:release=320[bduck];\
[bvoice_mix][bduck]amix=inputs=2:duration=first:dropout_transition=2,loudnorm=I=-14:LRA=7:TP=-1[a]" \
  -map "[v]" -map "[a]" -shortest \
  -c:v libx264 -preset medium -crf 18 -pix_fmt yuv420p \
  -c:a aac -b:a 192k -ar 48000 -movflags +faststart \
  "$OUT/mission-groundwork-cloud-local.mp4"

# C — fully local runtime narration and local assembly. A warmer grade and
# restrained central information system distinguish it from B.
ffmpeg -hide_banner -y \
  -i "$IN/visual-master.mp4" \
  -i "$OUT/narration-local.wav" \
  -stream_loop -1 -i "$IN/music.ogg" \
  -filter_complex "\
[0:v]scale=1134:2016,crop=1080:1920:x='27-20*sin(t*0.30)':y='48-16*cos(t*0.22)',\
eq=contrast=1.08:saturation=0.74:gamma=0.98,colorbalance=rs=.035:gs=.015:bs=-.025,\
drawbox=x=0:y=0:w=iw:h=210:color=0x102A2E@0.80:t=fill,\
drawtext=fontfile=$FONT_BOLD:text='MISSION GROUNDWORK':fontcolor=0xF3DB9B:fontsize=42:x=74:y=68,\
drawtext=fontfile=$FONT:text='FROM MOTION TO DIRECTION':fontcolor=white@0.78:fontsize=24:x=74:y=130,\
drawbox=x=70:y=1430:w=940:h=330:color=0x102A2E@0.84:t=fill:enable='between(t,0.5,5.0)',\
drawtext=fontfile=$FONT:text='01  OWNERSHIP':fontcolor=0xF3DB9B:fontsize=25:x=108:y=1485:enable='between(t,0.5,5.0)',\
drawtext=fontfile=$FONT_BOLD:text='Who owns the work?':fontcolor=white:fontsize=51:x=108:y=1555:enable='between(t,0.5,5.0)',\
drawtext=fontfile=$FONT:text='Make responsibility unmistakable.':fontcolor=white@0.82:fontsize=30:x=108:y=1640:enable='between(t,0.5,5.0)',\
drawbox=x=70:y=1430:w=940:h=330:color=0x102A2E@0.84:t=fill:enable='between(t,5.0,10.7)',\
drawtext=fontfile=$FONT:text='02  NEXT STEP':fontcolor=0xF3DB9B:fontsize=25:x=108:y=1485:enable='between(t,5.0,10.7)',\
drawtext=fontfile=$FONT_BOLD:text='What happens next?':fontcolor=white:fontsize=51:x=108:y=1555:enable='between(t,5.0,10.7)',\
drawtext=fontfile=$FONT:text='Turn activity into accountable action.':fontcolor=white@0.82:fontsize=29:x=108:y=1640:enable='between(t,5.0,10.7)',\
drawbox=x=70:y=1430:w=940:h=330:color=0x102A2E@0.84:t=fill:enable='between(t,10.7,16.5)',\
drawtext=fontfile=$FONT:text='03  SUPPORT':fontcolor=0xF3DB9B:fontsize=25:x=108:y=1485:enable='between(t,10.7,16.5)',\
drawtext=fontfile=$FONT_BOLD:text='Where is support missing?':fontcolor=white:fontsize=45:x=108:y=1555:enable='between(t,10.7,16.5)',\
drawtext=fontfile=$FONT:text='Move forward on solid ground.':fontcolor=white@0.82:fontsize=30:x=108:y=1640:enable='between(t,10.7,16.5)',\
fade=t=in:st=0:d=0.35,fade=t=out:st=16.0:d=0.4[v];\
[1:a]volume=0.9,highpass=f=65,lowpass=f=10000,equalizer=f=210:t=q:w=1.2:g=-1.5,equalizer=f=3200:t=q:w=1:g=1.2,acompressor=threshold=-21dB:ratio=2.8:attack=10:release=140,loudnorm=I=-16:LRA=6:TP=-1.5,asplit=2[cvoice_sc][cvoice_mix];\
[2:a]volume=0.12[cmusic];\
[cmusic][cvoice_sc]sidechaincompress=threshold=0.025:ratio=12:attack=18:release=340[cduck];\
[cvoice_mix][cduck]amix=inputs=2:duration=first:dropout_transition=2,loudnorm=I=-14:LRA=7:TP=-1[a]" \
  -map "[v]" -map "[a]" -shortest \
  -c:v libx264 -preset medium -crf 18 -pix_fmt yuv420p \
  -c:a aac -b:a 192k -ar 48000 -movflags +faststart \
  "$OUT/mission-groundwork-local-only.mp4"

for candidate in \
  "$OUT/mission-groundwork-cloud-local.mp4" \
  "$OUT/mission-groundwork-local-only.mp4"
do
  stem="$(basename "$candidate" .mp4)"
  ffprobe -v error -show_format -show_streams -of json "$candidate" > "$OUT/$stem.ffprobe.json"
  ffmpeg -hide_banner -i "$candidate" -af loudnorm=I=-14:LRA=7:TP=-1:print_format=json -f null - 2> "$OUT/$stem.loudness.log"
  ffmpeg -hide_banner -i "$candidate" -vf "blackdetect=d=1.2:pix_th=0.02" -an -f null - 2> "$OUT/$stem.blackdetect.log"
done

sha256sum \
  "$OUT/mission-groundwork-cloud-local.mp4" \
  "$OUT/mission-groundwork-local-only.mp4" \
  "$OUT/narration-local.wav" > "$OUT/SHA256SUMS-local"
