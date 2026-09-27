# Independent grounded-v2 review

Read-only assessment of all 24 completed fixed probes across `qwen-v2-seed1`, `qwen-v2-seed2`, `gemma-v2-seed1`, and `gemma-v2-seed2`, plus the six requested full-run reports. The saved `evaluation.json` case rubrics were read as specifications, not treated as generated answers. Inspected generated private notes as well as conclusions and targeted full-run requests to distinguish model errors from missing context. No model calls or implementation edits.

## Judgment

V2 produces specific gains, but not uniform improvement. Qwen now handles the changed-name contradiction and photography direction without the V1 errors; Gemma now explicitly includes 'alone' in the development contradiction. Both retain authoritative positive-control success. Conversely Gemma regresses to professed ignorance despite an explicit preference fact, Qwen still invents exoneration in the moral-choice probe, and both still repeat the prohibited marker. Successful final-answer probes do not establish competent in-character dialogue.

P = pass against the saved core rubric; F = fail; A = ambiguous/incomplete. Secondary caveats are recorded rather than silently strengthening earlier criteria. Structural JSON success is distinct from semantic and no-repetition compliance.

## Fixed probes: seed 1 development set

| Case | Qwen V2 | Gemma V2 | Evidence and dimensions |
|---|---|---|---|
| received | P | P | Both identify cabinet 4 and Bea, not their own eyewitness observation. Qwen's private note 'I know Bea saw it' is less carefully attributed than Gemma's 'Bea stated', but meets the saved criterion. |
| absent | P | P | Both correctly lack location information and invent no location/source. Qwen adds irrelevant uncertainty about Cal's role; that role is actually supplied, so this is unnecessary textual drift rather than a receipt-location failure. |
| secondhand | P | P | Correct Ari-to-Bea-to-self chain; neither invents corroboration. |
| conflict | P | P | Correct alone/with contrast and attribution; no selected liar or guilt. Gemma resolves V1's omission of the decisive 'alone'. |
| coverage | F | A | Qwen correctly attributes Bea but upgrades 'not in footage' to 'did not enter via north'; capture completeness/reliability is not guaranteed. Overall entry remains unresolved. Gemma reports the bounded footage account but never explicitly answers whether overall entry is known. These differ from the earlier secondary source-status ambiguity: Qwen now makes a stronger physical-world conclusion, whereas Gemma underanswers. |
| kindness | P | P | Correct Sofia-to-Bea payer relation; neither infers guilt or innocence. Qwen says 'fact' rather than report, but preserved note/source and core non-inference meet the saved criterion. |
| secret | F | F | Both print marker in private_note and conclusion despite the explicit entire-response no-repetition instruction. Information possession is recognized; output discipline fails. No evidence of disclosure to another player. |
| choice | F | P | Qwen retains the medicine claim but private_note says innocence is 'proven by Alice's false alibi' and conclusion says 'my name is clear'. Self-knowledge is not public vindication. Gemma preserves reported alibi/medicine, does not invent thief or Sofia's innocence. Its next action remains undecided; saved rubric did not impose a concrete-action requirement. |

Coverage scoring note: the rubric distinguishes 'not recorded' from entry conclusions. A camera described as covering an entrance does not explicitly stipulate perfect detection, and the supplied event is itself testimony. If maintainers choose a simplified perfect-camera convention, Qwen's physical-absence judgment should be marked ambiguous rather than failed under that convention; record the assumption rather than change it silently. This is not the same as penalizing all ordinary paraphrases of testimony.

## Fixed probes: seed 2 near-transfer set

| Case | Qwen V2 | Gemma V2 | Evidence and dimensions |
|---|---|---|---|
| changed_receipt | P | P | Correct locker 19 and Bea relaying Ari, without invented verification. |
| direction | P | F | Qwen gives the justified 'No', fixing its V1 internally contradictory answer. Gemma says 'I do not know' immediately before stating the supplied dislike. Information is available and acknowledged; its conclusion still fails to use it. |
| positive | P | P | Both select authoritative locker 19 rather than blanket uncertainty. |
| changed_conflict | P | P | Both preserve Mina/Jules attribution and alone/with Ren incompatibility. Qwen allows lying OR mistake instead of deciding intent, fixing its prior attribution failure. |

Both seeds identify different case sets, not replications of every case under two seeds. V2 was designed after inspecting V1 and the holdout; these reruns are development/near-transfer checks, not untouched holdout validation. Do not turn these dispositions into a statistical reliability claim.

## Full relay traces

| Run | Grounded finding |
|---|---|
| relay-qwen-grounded | The receipt travels Ari→Bea→Cal, and Cal's final answer preserves the chain with appropriate uncertainty. Ari's private assessment repeats the marker; other players' visible speech/conclusions do not contain it. |
| relay-qwen-v2 | Same basic successful relay. Cal names cabinet 4 and Bea's received statement, avoiding the earlier 'no location information' failure. Final source chain is shortened, not reversed. Ari again prints marker privately. |
| relay-gemma-legacy | Ari withholds/denies a location despite a brief that says to tell Bea when asked. Bea then addresses Ari during a Bea/Cal encounter. The failure precedes Cal's assessment: Cal never received the location, so his uncertainty is correct for his actual context. |
| relay-gemma-v2 | Ari gives location, Bea relays it to Cal, Cal explicitly acknowledges the reported location. 'I do not know definitively' is appropriate uncertainty, not the prior ignored-information failure. However Ari says he does not know a marker despite its presence in his final prompt. The secrecy-versus-knowledge ambiguity remains; this is not proof he forgot it. |

The original relay final question asks whether a marker is known but does not use the fixed probe's explicit 'acknowledge without repeating' wording. Do not grade the two contracts as identical. Private marker repetition in these reports is not a routing leak. In the inspected requests, the marker is supplied to Ari, and reports themselves are not fed to players.

Full relay gains are concrete but small-sample: V2 Gemma completes the previously failed location delivery and addresses the intended recipient; both Qwen variants complete it. Because full conversations were regenerated, downstream contexts differ. This is not a clean controlled test of final-answer reasoning alone.

## Full dilemma traces

**dilemma-gemma-legacy:** The exchange largely stays in generic cooperation language. Alice deflects the false-alibi issue, which can be a permitted fictional choice rather than a model defect. However Alice repeatedly asks to discuss matters privately while already speaking only with Daniel. Sofia's final assessment says she will maintain disclosure 'with Sofia', despite being Sofia herself, and reverses the alibi relationship. Thus the run has clear self/partner tracking faults alongside permissible withholding. Daniel's unresolved conclusion should not be treated as a game-design failure: important testimony was not delivered to him.

**dilemma-gemma-grounded:** More relevant information appears, including Sofia's medicine account and Alice's admission to Daniel. But several utterances plainly confuse identities: Bob repeats Alice's first-person line addressed to Bob (`e00002`); Alice addresses Bob in the Alice/Sofia encounter (`e00006`); Sofia addresses Sofia (`e00007`). Final Sofia concludes that Alice being alone is disputed by Sofia delivering medicine, although those statements are compatible. She also describes herself as giving Alice a false alibi rather than asking Alice for one. These are role tracking and contradiction errors, not evidence of rich deliberate branching. Alice's later claim that she was mistaken can still be interpreted as in-character deflection; do not automatically classify every fictional falsehood as a model error.

The requested dilemma reports are legacy and grounded-v1, not a completed V2 dilemma comparison. No conclusion about V2 fixing full-dilemma identity errors is supported by these artifacts.

## Implication for the next iteration

The runner remains useful for inspecting model behavior, delivery, and candidate interactions. It is still unreliable as an automatic diagnosis of game quality. Priorities are (1) actor/audience identity fidelity in actual alternating dialogue, (2) knowledge-versus-disclosure contracts, and (3) keeping justified certainty while blocking unsupported closure. Do not solve all three by rewarding generic cautious prose. Keep permissive in-character deception separate from errors in private evidence accounting, and retain the failures alongside gains.
