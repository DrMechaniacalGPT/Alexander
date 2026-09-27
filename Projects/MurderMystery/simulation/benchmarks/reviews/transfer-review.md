# Independent transfer review

Reviewed the two original synthetic V2 dilemma reports, the private external run summary, and five relevant private accusation requests. No model calls or implementation changes. External findings below are aggregate only: no source-owned role text, clue wording, character names, solution identity, or reconstructive accusation transcript is reproduced.

## Main conclusion

The improved fixed probes do not yet transfer reliably to ongoing dialogue or the external adaptation. Both synthetic dilemma traces contain useful interactions, but also identity or evidence-handling failures. The external run completes mechanically while producing no correct nonculprit accusation. These results support continued instrument development, not automatic diagnosis of the source game's quality or human playability.

## Original synthetic dilemma: Gemma V2

The trace more often preserves the actual actor and information than the earlier Gemma grounded-v1 run. Bob's final assessment treats Alice's statement as testimony rather than proof of theft. Sofia correctly says she gave Alice her medicine-delivery account. Daniel correctly leaves the situation unresolved because his own conversation supplies no corroborating detail. These are concrete improvements over the earlier self-addressing and logically incompatible final accounts.

An audience error remains: Alice addresses Bob at event e00004 while the encounter is Alice/Sofia. The request routing can be correct while the generated dialogue addresses the wrong person. Merely including explicit names in context has not eliminated that problem.

Alice chooses not to expose her promise to Sofia; that can be an authorized character choice. Her deflection should not automatically be counted as an inference failure. Nor should Daniel's lack of resolution count as a game defect when he was never given the relevant account. The final assessment of withheld information is an observable generated explanation, not verified access to the model's underlying motives.

## Original synthetic dilemma: Qwen V2

Some final judgments are more cautious than the earlier Qwen run: Daniel says Sofia's innocence remains unproven, and Bob says the donation is unresolved. Alice initially admits the false alibi, producing an interpretable social decision.

The conversation nevertheless becomes materially unreliable:

- Alice addresses Bob during the Alice/Sofia encounter (e00004).
- Sofia asks Alice whether Sofia's own medicine delivery happened (e00005/e00007), despite her supplied role establishing that activity as her account. This confuses uncertainty about proving a fact to others with possessing one's own backstory.
- Later dialogue invents Sofia assisting Alice at the specified time; that differs from Alice initially being alone. Because public deception is allowed, the changed statement alone is not necessarily a model error. However Alice's final private explanation also redescribes the promised false alibi as an omission rather than a lie, showing unstable evidence accounting rather than a cleanly tracked public/private distinction.
- Several utterances and Sofia's final assessment aim to clear Bob, although Daniel is the character whose unfair suspicion is established in the scenario. This is a concrete transfer of stakes to the wrong person.

The two models produce different disclosure paths, but those differences cannot yet be credited as successful personality variation. Some arise from permitted withholding; others demonstrably arise from role confusion, changed facts, and unsupported reinterpretation. No evidence here establishes human fidelity or meaningful branch probabilities.

## Private external adaptation: independently checked aggregates

The recorded run is structurally complete: 42 requests, approximately 290 seconds of recorded model time, and private accusations before the prescribed confession. Excluding the culprit, the seven assessments divide into:

| Assessment outcome | Count |
|---|---:|
| Correct accusation | 0 |
| Wrong accusation | 5 |
| Explicit insufficient-evidence response | 2 |
| Total nonculprit participants | 7 |

Thus **0/7 nonculprits accused correctly**, with **5 wrong and 2 abstaining**. The culprit's self-accusation is excluded because the private role provides privileged solution knowledge; it is not an independent deduction success. Its accompanying reasoning also should not be credited merely because the selected identity is correct.

The summary and inspected accusation contexts show several failure patterns without requiring source details:

- Unstated personal attributes are inferred from occupation or unrelated interests.
- A direction-sensitive activity preference is replaced with an occupational stereotype.
- A participant's own private trait is treated as though it were a clue about somebody else.
- A candidate's observed contradiction is used inside an argument for accusing that candidate rather than as a reason to question the match.
- Matching one attribute is treated as satisfying several unobserved requirements, followed by an unsupported uniqueness claim.
- Dialogue repeats another character's first-person introduction or traits, polluting later evidence with actor confusion even when the engine's event actor remains correct.

Wrongness alone does not identify a reasoning error: a participant can rationally choose an incorrect suspect from incomplete or deceptive information. Here, the source-to-inference mismatches in inspected requests supply stronger evidence of model failure than the accuracy count itself. Conversely the two abstentions can be appropriate under limited information and must not be lumped into five unsupported accusations.

No blanket conclusion about the original game follows. This is one seed, one selected cast, a shortened text adaptation, a particular allocation of discovered evidence, and no additional post-discovery discussion. Those assumptions constrain what participants can know. The experiment does not show that humans would fail, that all necessary evidence reached a suitable player, or that the source mystery is unsolvable.

## Recommended interpretation

Retain the runner for inspecting traces and diagnosing simulator failures. Do not optimize a mystery to compensate for these failures yet: changing the game because a model swaps identities or invents missing traits risks repairing the instrument's errors through the content. Prioritize actor/audience continuity, separation of self-knowledge from corroboration, and explicit handling of unknown candidate attributes in multi-turn contexts. Preserve open-ended character choices while separately checking whether each model's factual account remains grounded.
