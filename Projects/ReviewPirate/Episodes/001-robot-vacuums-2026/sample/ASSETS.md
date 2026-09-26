# Asset provenance

- Video graphics and animation: original code in `render.py`; no third-party footage, logos or product photography.
- Narration: Piper `en_US-ljspeech-high`; [model card](https://huggingface.co/rhasspy/piper-voices/blob/main/en/en_US/ljspeech/high/MODEL_CARD) identifies public-domain LJ Speech data. [Dataset publisher](https://keithito.com/LJ-Speech-Dataset/) confirms its public-domain status. No voice cloning was performed.
- Piper engine: [OHF-Voice/piper1-gpl](https://github.com/OHF-Voice/piper1-gpl), GPL-3.0. Engine/model downloads are not redistributed in this repository.
- Font: installed DejaVu Sans / Mono; [project license](https://dejavu-fonts.github.io/License.html). Font files are not redistributed.
- Encoder: FFmpeg binary supplied by imageio-ffmpeg; no encoder binary redistributed.
- Source names are textual editorial attribution, not endorsements. Original research URLs are in `EVIDENCE.md` and `review.html`.
- Music: none. No stock or generated cinematic footage.
- Lessac, Ryan and HFC voice candidates were inspected at the model-card level but not used because their underlying dataset terms were less straightforward for a commercial project. LJSpeech was selected instead.
