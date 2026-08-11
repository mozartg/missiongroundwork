# Mission GroundWork — three-path video trial

## Purpose
Demonstrate what becomes possible when GitHub produces inspectable media inputs and receipts instead of merely passing a workflow.

## Common creative brief
- Format: 1080 × 1920, H.264, yuv420p, 30 fps, 18–22 seconds.
- Audience: nonprofit leaders and operations teams.
- Tone: grounded, assured, human; no hype.
- Script: "Busy teams do not usually need another plan. They need clarity. Who owns the work? What happens next? Where is support missing? Mission GroundWork helps nonprofit leaders turn activity into accountable action, so the team can move forward on solid ground."
- Visual source: Pexels, “Two Businesspeople Working Together at a Computer in an Office,” by Mizuno K.
- Music source: “Soft Corporate” by MusicLFiles, CC BY 4.0.
- Publishing: disabled. Human review is required.

## Quality floor
A candidate is not accepted because a workflow passes. It must also:
1. use real licensed footage rather than a text-only card;
2. keep all essential text inside a 90 px horizontal and 150 px vertical safe area;
3. deliver intelligible narration with no clipping and no long accidental silence;
4. keep music subordinate to narration through ducking and loudness normalization;
5. play correctly as 1080 × 1920 H.264/yuv420p with fast-start;
6. include source, license, tool, and checksum receipts;
7. be judged by a human on voice authenticity, visual hierarchy, pacing, emotional credibility, and brand fit.

## Paths
- A — cloud-only: GitHub Actions downloads rights-cleared inputs, generates Edge TTS narration, edits, mixes, verifies, and packages the video.
- B — cloud/local: the cloud-generated narration and mezzanine footage are downloaded; a distinct local edit is assembled and verified.
- C — local-only runtime: a portable Piper model and engine are bootstrapped as an artifact, then voice synthesis, editing, mixing, and verification run locally without a media-generation API.

These paths deliberately preserve the same script, footage, and music so differences are attributable to workflow and voice/edit decisions rather than changed content.
