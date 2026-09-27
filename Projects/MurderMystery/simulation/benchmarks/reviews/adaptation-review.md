# Private-source adaptation review

Read-only review of the existing adapter, external-run documentation, and already-local source instructions. No model calls, fixture edits, external searches, or source-text reproduction. Paths below are local provenance only; this memo contains no role identities, solution, or reconstructive clue details.

## Does discussion stop immediately after clue delivery?

Yes. `tools/import_movie.py` creates the clue-discovery phase with `mode: delivery_only`. It appends no speaking encounters after those deliveries. The runner then collects private accusations; the next public generated speech is the prescribed ending. The adapter's provenance explicitly lists no extra post-hunt discussion. Thus players cannot ask new questions prompted by their discovered clues, compare findings, or request relevant candidate facts before accusing.

The earlier mingling abstraction is also narrow: two random-pair windows, two utterances per person in each encounter. It does not ensure that important character facts circulate. The report's global contact count includes shared audiences and cannot establish that everyone had an investigative conversation with everyone else.

## What the local source supports

The source's host-instruction section explicitly encourages participants to learn about one another and disclose character/personality facts during play, with personality traits available as prompts for questions. The scripted sequence describes a short timed search followed by accusations and confession. It does **not** explicitly prescribe a separate post-search discussion interval.

The preparation instructions permit the host to adapt the explanatory script while retaining critical information. That supports host flexibility in general; it does not specifically validate a new discussion phase or its duration. The inspected instructions do not expressly ban conversation during the search, but absence of a ban is weaker than affirmative evidence that clue sharing or interrogation is intended then. Real search behavior is not represented by instantaneous private delivery.

Therefore, the existing accusation timing has direct support in the written sequence, while the complete lack of conversation during digital discovery is an abstraction. Adding post-discovery dialogue is a sensible **experimental variation**, not a correction that can be claimed to restore an explicitly required source phase. The source's affirmative information-sharing objective also means inadequate pre-discovery trait coverage deserves attention independently of post-discovery timing.

## One bounded controlled comparison

Use a **frozen common prefix through clue delivery**, preserving cast, exact prior utterances, private clue allocation, model, prompt profile, thinking setting, generation cap and assessment question.

- **A: Immediate assessment.** The current baseline: collect private accusations immediately.
- **B: One added paired discussion window.** Before the same private assessment, give each player one partner and two alternating utterances each: 16 additional speech calls across eight players. Choose and record the four pairs using a schedule-only rule before seeing accusations; if choosing previously unmet partners, use prior scheduled encounters, not culprit knowledge or clue contents. Use the same neutral discussion instruction for everyone, without supplying hidden candidate attributes, recommending suspects, or requiring revelation.

Describe B as adding a limited opportunity to exchange information after discovery. It changes time and compute as well as opportunities; this is not a pure estimate of timing independent of dialogue budget. A later equal-budget before-versus-after comparison could separate those factors, but is not part of this first bounded comparison. The shared prefix means these are two continuations of one trajectory, not independent full parties.

Inspect each participant's actual context at assessment. Record newly delivered candidate attributes, whether they have traceable speakers, acknowledged contradictions, explicit unknowns, and whether accusations rely on unsupported properties. Report nonculprit correct/wrong/abstain separately, with added latency and calls. More shared misinformation is not a benefit, and fewer abstentions alone is not improvement. Keep all reconstructive traces local.

## Interpretation boundary

Zero correct accusations among seven nonculprits is not by itself an inference failure. A player can lack enough candidate facts to identify anyone; explicit insufficient evidence can be the appropriate answer. The previous audit found unsupported reasoning in several actual requests, which is separate evidence of model problems. Both adaptation coverage and reasoning can fail at once.

If B adds reliable relevant information and a participant then uses it correctly, that supports the usefulness of this opportunity within this one adaptation. If B adds little, the dialogue policy or role execution may be the bottleneck. If information arrives but conclusions remain unsupported, that more directly implicates evidence use. None of these outcomes measures human solvability or the original game's quality.

## Local provenance

Base directory: `/home/drbone/.codex/worktrees/mystery-discovery/Alexander/Projects/MurderMystery/simulation/`.

- `tools/import_movie.py`: scene sequence, fixed mingling budget, private clue allocation and explicit no-post-hunt assumption.
- `external-run.md`: adaptation limits, prior controlled/changed-prompt attempts, and limits on interpreting the external result.
- `local-private/movie/source-layout.txt`: opening setup, explanatory host instructions and transition/death-note sections, corresponding to the initial five pages of the locally retained packet.
- `local-private/movie/source.pdf`: local source packet, documented SHA-256 `0a73e3aefa07c5b083fb8f5f94907c0e86ba2447227b607ed2c8e0e7f134843a`.

The source packet remains private; this memo intentionally paraphrases only the scheduling and information-sharing implications necessary for this review.
