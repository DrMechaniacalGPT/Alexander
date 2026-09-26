# First external scenario: execution, not validation

Source: Dennis Spielman's [free Movie Murder Mystery Party PDF](https://www.dennisspielman.com/photos/games/moviemurdermystery/movie_murder_mystery_party_game.pdf), 2020 revision, retrieved September 26, 2026. SHA256 `0a73e3aefa07c5b083fb8f5f94907c0e86ba2447227b607ed2c8e0e7f134843a` (236,456 bytes). A research agent read the full 20-page packet and extracted role/clue data; the integrator inspected the selected briefs and actual runs.

**One complete text adaptation has executed. It is not a faithful reproduction of physical play, and its results cannot establish the quality of the source game.** We have not obtained human outcome distributions or independently verified a successful party using this exact version. Accessible authored material is a structural reference, not a known-good behavioral oracle.

## Mapping and assumptions

Eight selected guests use their own complete briefs; an engine-controlled host advances prescribed phases. The sequence covers mingling, the host signal and required player action, death, digital clue discovery, private accusations, and a generated confession. Optional awards and physical performance are omitted. No source-authored confession speech exists; our ending speech is model output.

The printed clue sheets contain 16 distinct statements in three copies each (48 objects), while a reference inventory lists 18. We use the printed sheets and record the discrepancy. We do not silently invent the missing cards.

The mingling baseline has two random-pair windows with two utterances per player per encounter. This is deliberately limited coverage, not a recommended party duration. The host signal is a shared beat, separate from those conversations. The hunt samples physical-copy IDs without replacement, privately giving three copies to each guest. Equal search success is an idealization; no walking, clue-location strategy, competition for cards or sharing during the hunt is simulated. No unsupported post-hunt conversation phase is added. Accusations remain private until all are collected.

## Failures and explicit continuation

The initial run stopped when a model cited an event outside its context. The engine rejected it; the output schema now offers only visible event IDs, while independent validation remains in place.

The next run reached accusations but one answer exhausted 384 output tokens. Increasing the allowance to 768 in an explicit continuation did not fix the rambling answer. A second continuation reused only the 33 accepted pre-assessment turns, then regenerated all eight accusations with concise-answer instructions and bounded fields, followed by confession. The earlier failed runs remain intact. This is one trajectory with revised final assessments, **not several independent successful games**.

The final baseline trajectory contains 42 accepted model turns: 33 inherited and nine newly generated. A replay revalidated the compatible recorded views/actions without calling a model. Phase completion and final accusation quality are reported separately in [RESULTS.md](RESULTS.md).

## Diagnostic and exploratory repair

A separate solver diagnostic supplies all selected personality-trait blocks and the printed clue set. It omits secret motives and explicit culprit labels, and does not enact a party. It also changes participants into investigators and emphasizes reliable information, so it is **not a clean causal comparison of information alone**. Portrayal actions and opening prose are not added to the trait blocks. Its purpose is to check whether the local model can identify the intended suspect from substantially enriched data.

An exploratory conversation treatment explicitly reminds participants to share a previously unmentioned personality fact with their current partner. It also clarifies keeping the scripted murder/confession until its phase. The newer output bounds apply throughout that fresh run. Report this as an adapter/prompt revision with confounds, not a measured effect size or proof of natural behavior.

## Local evidence and rights

`local-private/movie/` contains the original PDF, checked extraction, private JSON inputs, all source-derived requests/responses and failure/continuation traces. It is ignored by Git and restricted to the local owner. The main local paths are `run17`, `run17_schema`, `run17_extended`, `run17_concise`, `control17`, and `reminder17`. The source grants free access and limited host-script flexibility, but we found no blanket redistribution license. Its text is not relicensed under this repository's MIT license.

The public adapter contains our mechanics, not source-owned role or clue text. [external-results.json](external-results.json) publishes non-reconstructive measurements and manual classifications. The local source packet, generated confessions and full character/clue traces should not be copied into a public PR without resolving their terms.

## Interpretation

A bad outcome can originate in the original design, our encoding, the encounter/hunt abstraction, the participant prompt, or the model. Source discrepancies belong in the source record; model inventions belong in the behavioral audit; scheduling assumptions belong in the adapter record. None should be silently assigned to the game's author.
