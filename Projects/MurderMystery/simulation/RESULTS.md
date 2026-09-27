# Implementation results — September 26

**Follow-up:** [Factual recall and evidence reasoning](REASONING.md) contains the newer controlled comparisons, negative results and regression tests. The counts below describe the original implementation pass.

**The execution milestone is reached: a local runner, incremental original fixtures, and two complete text-adaptation trajectories through an existing game's phases. The behavioral model is not yet reliable enough to diagnose game-design quality.** Its main value today is making failures inspectable instead of hiding them in an attractive transcript.

The next priority is a small, repeatable check set for what a participant received, what someone merely claimed, what is established, and what they choose to withhold. Improve that before adding a large trait system, writing a full game, or interpreting failed investigations as defects in someone else's scenario.

## What is working

- Separate contexts and exact event audiences; private assessments stay private. In the inspected relay requests, an unrelated private marker never reaches other players.
- Fixed encounters, random-pair baselines and optional scene-local contact triggers. There is no six-window or eight-player requirement. Reports distinguish a trigger firing from the schedule budget ending.
- Local Ollama calls, explicit context/output/call/time limits, retained failures, recorded replay and interruption recovery. Explicit continuation can reuse a compatible prefix without counting it as a new experiment.
- **25 automated tests pass.** They cover isolation, group/absence behavior, state integrity, journals, replay, continuation, locking, bounds and scene requirements. They establish software properties, not believable people.

We made **156 distinct local generation requests**, counting failed calls and excluding inherited prefixes from double counting. This includes original fixtures, the external experiment and four frozen-context diagnostics. No paid provider calls, model downloads or human playtests occurred. [Machine-readable execution summary](execution-summary.json)

## What the runs actually showed

| Exercise | Observation | Meaning |
|---|---|---|
| [Two-player exchange](evidence/01_exchange/report.md) | Asked, answered and located the envelope; 4 calls | Trivial machinery worked |
| [Early qwen3 relay](evidence/02_private_relay/report.md) | Ignored a supplied fact; empty final answers | Failed behavioral test; the old final-answer contract was too permissive |
| [Revised qwen3.5 relay](evidence/02_relay_revised/report.md) | Location passed through an intermediary and was correctly reported | A successful trace, not stable performance |
| [Latest concise relay](evidence/02_relay_final/report.md) | Same location was delivered, but the listener later claimed not to know it | Context-use regression; prompt/output limits changed, so this is not a nondeterminism experiment |
| [Four-role dilemma](evidence/03_dilemma/report.md) | Alice confessed; subsequent reconciliation included unsupported claims of innocence and a fabricated account of who handled the donation | Generated interaction, not evidence of fair deduction or multiple meaningful branches |
| Existing-game baseline | All adapted phases completed; 0 of 7 non-culprits identified the intended culprit, 6 chose others, 1 abstained | Poor reasoning/information flow in this configuration; no verdict on the source game |
| Existing-game reminder treatment | All adapted phases completed; 1 of 7 non-culprits identified the culprit | Some facts moved usefully, but trait reversals and unsupported explanations remained |
| Enriched solver diagnostic | 8 of 8 calls identified the intended culprit from supplied traits/clues | The model can solve this enriched task; changed framing and repeated inputs prevent a causal or human-validity claim |

One treatment answer reached the 600-character schema limit and ended mid-thought. The summary flags field-limit hits even when JSON is valid. “Complete” means the configured phases executed, not that every answer was meaningful. Culprit-role answers are excluded from the seven-player counts; they already possess privileged knowledge.

The final four-call diagnostic held the received-information context fixed, removed other-player reports for a control, and compared two installed models. qwen3.5 denied knowing the location even with the report. Gemma acknowledged learning it from the intermediary but omitted the actual cabinet number. Both expressed uncertainty without the report. This identifies a useful next test, **not a winner in model selection**. [Exact requests/responses](evidence/context-checks.json)

## Existing material: what “complete” means

We adapted the free Movie Murder Mystery through mingling, a prescribed host signal/player action, death, a digital hunt, private accusations and generated confession. Eight guest roles were used. The hunt privately sampled card copies; physical searching, real elapsed party time and optional awards were not reproduced. There was no extra post-hunt discussion.

The baseline required corrections for unavailable evidence references and rambling final answers. Its final trajectory reused 33 earlier conversations/actions and generated nine new turns; all failures remain recorded. The reminder treatment was a fresh run. These are exploratory revisions, not a controlled effect-size comparison.

[External mapping, source discrepancy, rights and limitations](external-run.md) · [Public measurements](external-results.json). Full source-derived traces remain locally inspectable under `local-private/movie/`, excluded from Git. An accessible complete packet is not independently verified human ground truth.

## Judgment and next slice

We now have the instrument needed to investigate the idea. We do **not** yet have a trustworthy simulated player. In particular, a player may receive the right fact and fail to use it, or turn a sympathetic account into unjustified certainty. A hidden clue and an ignored clue require different fixes.

Next: freeze a few tiny contexts with clear distinctions between testimony, knowledge, inference and disclosure; compare prompts/models on those same contexts; inspect mistakes without repairing them invisibly. Then return to encounter policies, motive-driven disclosure and richer existing scenarios. A complete original commercial game remains premature.

Verification: 25 tests; actual local calls; manual trace review with an independent reviewer; latest relay and both complete external trajectories replayed without new inference. No ongoing run is scheduled after this checkpoint.
