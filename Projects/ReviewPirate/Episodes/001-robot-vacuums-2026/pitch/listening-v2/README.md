# Listening comparison, version 2

Three complete options, with one scene and neutral narration clip at a time. `index.html` is built from `scenes.json`, `options.json` and `matrix.json`. Generated audio and reference images remain local and are not committed.

From the pitch directory run `python3 -m http.server 8771 --bind 127.0.0.1`, then open http://127.0.0.1:8771/listening-v2/ .

Audio generation: the existing Kokoro environment and local models are reused by `make_audio.py`; set `KOKORO_MODEL_DIR` to the model directory. Local setup is described in the preceding listening folder. No paid credits.

This is an editorial storyboard. It is not a static-slideshow video production proposal. Real motion, custom acting and source-image axes remain unproduced.
