# Listening storyboard

Open `index.html` through the pitch preview server. Sixteen individually playable WAV clips accompany reference stills and source overlays. No automatic playback or scene advance.

Draft voice: Kokoro af_heart, speed 0.98. This is not the assistant live voice or final character performance. No vidIQ credits used. RTINGS is spoken as another testing lab and remains credited on screen.

Rebuild audio with Python packages `kokoro-onnx==0.6.1`, `soundfile==0.14.0` and the model/voice files linked by https://github.com/thewh1teagle/kokoro-onnx . Set KOKORO_MODEL_DIR to their local directory and run make_audio.py, then build.py. WAVs and generated PNGs stay local and ignored.

Durations are measured from samples. Playback/metadata checks do not constitute a subjective listening approval. Repeated reference poses represent ungenerated production shots.
