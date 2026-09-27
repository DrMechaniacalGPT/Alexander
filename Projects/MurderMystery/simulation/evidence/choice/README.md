# Required guesses and symbolic evidence

Start with [the decision memo](../../CHOICE_BASELINE.md).

- `required-guess-metadata.json`: fourteen saved-context Gemma calls with a required suspect plus explanation.
- `choice-only-metadata.json`: fourteen calls on the same original contexts with a single vote field.
- `stronger-review.json`: three independently isolated Codex reviews of selected failed player contexts. Messages and schema match the local comparisons, but the execution wrapper differs; this is not an API benchmark.
- `complete-information-v2.json`: the corrected eight-case inventory/interpretation comparison.
- `sharing-strict-v2.json` and `sharing-ordinary-v2.json`: corrected 100-seed sharing studies, each with twelve conditions and seven scored nonculprits per party.
- `source-weight-sensitivity.json`: a fixed-transport comparison of clue-match versus distinct-fact-source ranking.
- `packet-assessment-metadata.json` and `alias-metadata.json`: seven structured-evidence votes and three label/order robustness checks.
- `self-vote-metadata.json`: three legal-choice corrections, all still incorrect.
- `museum-sweep.json`: original four-player fixture, five seeds and four partner counts.

The earlier `complete-information.json`, `sharing-strict.json` and `sharing-ordinary.json` are retained as superseded: review corrected a derived assertion that could activate before both sources arrived, and a lifetime-career description that had been encoded as exclusive. Their results must not be used as the final conclusions.

The generic engine and original fixture are public. Source-derived cards, encoding tables, detailed external traces and model-native reasoning remain in ignored `local-private`. Public hashes identify those inputs without reconstructing the packet. Counts over simulated players share party histories; they are not independent human trials or estimates of real-party performance.
