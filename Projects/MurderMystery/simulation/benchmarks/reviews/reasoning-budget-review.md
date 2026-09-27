# Independent reasoning-budget probe review

Inspected all eight completed structured outputs against the saved `benchmarks/reasoning-budget-v1.json` rubrics. Scored `say`, `private_note`, `evidence`, `conclusion`, and `action`; did not inspect, score, quote, or reproduce the separate internal reasoning trace. No model calls or fixture edits.

For each matched pair, the serialized requests are identical after removing the `think` field. Thus the requested model, prompt/profile, seed, schema, context and generation cap are held fixed. This does not eliminate runtime state, caching, or stochastic variation as confounds, and there is only one output per condition/case.

## Semantic and contract findings

| Probe | Thinking off | Thinking on | Concrete comparison |
|---|---|---|---|
| Secret possession | Information possession acknowledged; explicit no-repetition contract fails in both private_note and conclusion. | Possession acknowledged and marker absent from every structured output field. | Clear improvement on this instance. This is compliance with an output restriction, not evidence that routing previously exposed a secret to another player. |
| Moral choice | Unsupported claim that Sofia is innocent; supplied medicine explanation omitted. Chosen protection is permitted, but the factual justification fails. | Avoids declaring Sofia innocent and explicitly says the withdrawn alibi does not establish who stole. However, it asserts that Sofia's plea shows concern for hardship victims and still omits the specific, unverified medicine account. | Partial improvement, not a clean pass. The newer answer substitutes an unsupported character interpretation for evidence. Protecting people is allowed; inferring the sincerity or moral significance of the plea is not established by the supplied testimony. |
| Authoritative inventory | Correct location, authoritative source and treatment of contrary guess. | Same correct result and source hierarchy. | Both satisfy the positive-evidence criterion. Thinking does not simply cause blanket uncertainty, but adds no observed correctness benefit on this case. |
| Conflicting accounts | Correct speakers, incompatible accounts, and possibility of mistake rather than compulsory deliberate deception. | Correct speakers and incompatibility, with explicit unresolved truth. | Both satisfy the core contradiction rubric. On is more explicit about epistemic limits; off's 'lying or mistaken' is already a permissible uncertainty formulation. Do not invent an off failure to exaggerate the gain. |

All outputs are parseable structured actions with empty `say`, nonempty `conclusion`, legal `none` action, and visible/appropriate evidence IDs. No invented evidence identifier occurs. A small instruction-level exception: thinking-off `changed_conflict.private_note` is 31 whitespace-separated words against the prompt's 30-word limit. It still meets the generated schema. Record this as a minor length-contract miss, not a reasoning failure.

The choice answers both name Alice's withdrawn alibi, but neither preserves the full medicine explanation as an unverified account. This is a meaningful omission under the saved rubric, rather than a demand to enumerate every incidental detail. The on condition's private note correctly distinguishes role-supplied personal innocence from the other people's statements; its conclusion still overinterprets Sofia's plea. Daniel's own innocence is supplied and should not be penalized as unsupported certainty.

## Runtime tradeoff

| Probe | Off wall seconds | On wall seconds |
|---|---:|---:|
| Secret | 19.666 | 19.813 |
| Choice | 5.156 | 24.309 |
| Positive inventory | 4.790 | 27.501 |
| Conflict | 6.029 | 29.445 |
| Recorded total | 35.641 | 101.068 |

The nearly equal secret times are misleading: the off secret request included approximately **14.869 seconds of model loading**, while the on request did not. Across all four calls, off has about 14.871 seconds of reported loading versus about 0.003 seconds for on. Excluding the recorded load component leaves roughly **20.770 seconds off versus 101.065 seconds on**: about 4.9 times as much remaining wall time for on. This subtraction is descriptive, not a controlled warm-cache performance estimate.

Reported generation counts total 405 off versus 2,294 on. With thinking enabled, the generation count need not represent only visible action text; do not describe it as dialogue verbosity or quote the internal trace. All eight responses ended normally rather than exhausting the cap.

## Interpretation and next use

Thinking materially improves one observed confidentiality-output failure and reduces one form of unsupported exoneration, at a substantial runtime cost. It does not make the moral-choice answer fully grounded, and two already-correct cases merely become slower. These probes are selected development cases that previously exposed problems, not a representative success-rate sample.

The fresh multi-turn fixture is the appropriate next check: inspect whether the same setting preserves identity, hearsay, and knowledge while allowing voluntary withholding. A deliberate refusal or unresolved question there must not be scored as failure merely because this fixed secret probe demands a specific acknowledgment. No recommendation for universal thinking-on follows from these eight outputs alone.
