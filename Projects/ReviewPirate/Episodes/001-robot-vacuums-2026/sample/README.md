# First sample: answer first, evidence in motion

September 26, 2026. **56.5-second creative prototype, not a release-ready buying guide.**

The generated video and contact sheet are retained in the local checkout; their GitHub upload was declined and was not retried. Rebuild them with the commands below. Locally, watch `sample-v1.mp4` or open `review.html`. Read the short [decision note](DECISION.md), [source ledger](EVIDENCE.md), [creative alternatives](CREATIVE.md), and [software comparison](SOFTWARE.md).

The owner approved moving to the sample review point, clarified that Review Pirate is a code name, rejected assuming a pirate/parrot identity, and requested sophisticated but approachable presentation, quick usefulness, original-source referrals and engaging motion. The owner prefers reserving vidIQ credits for research. Approximately $100 for a worthwhile subscription trial is acceptable in principle, but no purchase was authorized or made.

This sample prioritizes demonstrating the format with a tightly verified claim set. It does **not** complete the original full eight-source/product coverage audit or balanced owner study. Those remain open before a full episode.

## What is here

- `sample-v1.mp4`: H.264, 1280×720, 30 fps, synthetic voice, burnt-in captions.
- `review.html`: local viewing page with clickable original sources and transcript.
- `scenes.json`, `timing.json`, `captions.srt`: script, actual segment timings, subtitles.
- `render.py`: original per-frame vector animation, not a slide export.
- `make_audio.py`: local Piper synthesis; voice model is a separate download.
- `contact-sheet.jpg`: representative frames for quick visual review.

## Rebuild

Use Python 3.12 and a virtual environment. Install the pinned dependencies in `requirements.txt`. Obtain the LJSpeech high ONNX voice and matching JSON from the [Piper voice repository](https://huggingface.co/rhasspy/piper-voices/tree/main/en/en_US/ljspeech/high), into `models/`. Read the linked model card. The model file is not committed.

```
python make_audio.py
python render.py --stills
python render.py
```

The renderer uses DejaVu Sans fonts at the common Linux `/usr/share/fonts/truetype/dejavu/` location; change `F` for other environments. `imageio-ffmpeg` supplies the executable. Run from this directory or via the script's absolute path. Re-synthesizing may change durations slightly; `make_audio.py` regenerates the timing manifest. For exact visual rerendering, retain the original `narration.wav` and `timing.json` from the local working artifacts.

This is one small episode-specific renderer, not a general video editor. Paid media generation is deliberately absent.

## Verification

Nine representative scene frames visually inspected. Full MP4 decoded successfully: 1,695 video frames and an audio stream; duration 56.50 seconds. Text/claim mapping checked against the sources below. Scene timing derives from synthesized audio, with captions distributed by phrase length within each scene; this is approximate caption alignment, not word-level forced alignment. Local player verification and audio checks are recorded in `QA.md`.

No assertion of commercial voice quality, audience engagement, full-source saturation or brand validation follows from this prototype. The strongest remaining creative question is whether this visual style feels lively enough; the clearest likely upgrade is voice performance and a small amount of controlled illustrative footage.
