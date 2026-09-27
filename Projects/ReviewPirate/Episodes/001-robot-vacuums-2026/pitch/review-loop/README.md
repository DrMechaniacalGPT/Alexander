# Listening-pitch review loop

This directory retains complete frozen attempts, their exact scene data, local media hashes, and review findings. The author revises an artifact before a new isolated reviewer sees it; unchanged drafts are not repeatedly sampled to seek a favorable verdict.

The independent audience reviewer sees the actual browser-rendered scene images and exact narration, first without the detailed criteria, then with the eight criteria in `../REVIEW_PROTOCOL.md`. It does not see project notes, earlier reviews or the conversation. A separate evidence reviewer can inspect primary sources. Only after both pass does the author compare the same artifact with the full recovered conversation.

## Local reproduction

Run a local Python HTTP server from the pitch directory on port 8771. Open the desired `review-loop/rN/` page. Scene JSON is the narration and panel source; index.html includes a frozen copy so no API or build service is needed. The page uses the local assets directory and local WAV clips. These generated media files are deliberately excluded from GitHub; source checkout alone does not recreate the visual assets.

To regenerate draft audio, use that revision's `make_audio.py` with the official Kokoro ONNX model directory in KOKORO_MODEL_DIR. The development environment used kokoro-onnx 0.6.1, onnxruntime, soundfile and numpy. Voice af_heart, speed 0.98, 24 kHz PCM16. Then run `python3 review-loop/freeze.py rN` from the pitch directory to synchronize narration durations and record hashes. Do not regenerate or edit a passed version in place: copy it into a new revision and rerun all gates.

Passing an image/transcript review does not establish final voice delivery or cinematic motion. This is a listening-pitch review point, not publication approval. Local server availability was checked before delivery; if it stops, the HTML and audio files remain on disk.
