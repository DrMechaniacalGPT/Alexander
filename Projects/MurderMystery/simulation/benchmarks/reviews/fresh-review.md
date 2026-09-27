# Fresh selective-disclosure comparison: independent review

Reviewed the frozen `/tmp/mystery-budget/fixtures/04_selective_disclosure.md` rubric against `evidence/reasoning-budget/fresh-off/report.md` and all accepted structured actions in both arms. Paths here are relative to `/tmp/mystery-budget` unless absolute. Evaluated `say`, `private_note`, `evidence`, `conclusion`, and `action`; separate internal reasoning was not evaluated or reproduced. This is an original small interaction fixture, not a human-behavior test.

## Completed thinking-off arm

The 13 accepted turns provide a complete trace with substantial semantic failures despite useful opening questions and correctly delivered testimony. Those failures are not explained solely by legitimate withholding.

| Dimension | Disposition and concrete evidence |
| --- | --- |
| Self-knowledge and disclosure accounting | **Fail.** Neri explicitly names Dax to Omar at t00001, then claims in both final `private_note` and `conclusion` at t00010 to have withheld Dax's identity from Omar. Naming Dax is a permitted choice; misreporting that choice is the error. Neri retains some booking knowledge in the final assessment, so this is not blanket forgetting. |
| Factual precision | **Fail.** Neri's t00010 conclusion upgrades Leena's water observation to water damage and associates it with 16:20 rather than the reported 16:25. Omar's t00011 also says water existed “then” after specifying 16:20. No inspection or damage finding was delivered. |
| Inference restraint | **Fail.** Omar treats water at 16:25 as confirmation that no late session occurred (t00005, t00007, t00011). Water is compatible with both attendance and no attendance. At t00007, he also converts Neri's alleged silence into evidence that no official booking existed, despite having heard Neri describe discretionary authorization. Attribution to Neri does not justify either inference. |
| Received testimony and provenance | **Mixed.** Omar hears and initially paraphrases Neri's discretionary answer, and Leena supplies her own correctly timed observation at t00004. Both subsequently circulate an unsupported no-session conclusion. Leena's final t00012 is a real partial recovery: she preserves her firsthand water observation at 16:25 and explicitly separates Omar's unverifiable inference from it. Do not mark that final assessment wrong merely because earlier speech was wrong. |
| Audience fidelity | **Fail.** In the final Neri/Leena encounter, both t00008 and t00009 address absent Omar; their private notes also describe communicating with him. This is actor/audience confusion, not a character choosing to withhold. The engine's delivery audience remains the prescribed pair; generated mistaken address does not establish an engine routing leak. |
| Prospective action | **Mostly sound.** Players repeatedly propose checking the instrument, and final assessments keep that inspection prospective. They do not report a completed caretaker inspection. However, Neri's unsupported “empty and safe” claim at t00008 must not be treated as a real check or game-world fact. |
| Structured contract and evidence fields | All 13 turns were accepted. Final turns use empty `say`, assessments in `conclusion`, and `action: none`. Listed event references do not make an inference true: Omar's citations to the water exchange do not support absence of use. No separate structural defect is established by this review. |

### Deception and ambiguity boundaries

Neri's public assertion that the room was free at 16:20 is not automatically a benchmark failure. Public evasion is permitted, and t00003's generated private note explicitly calls this a lie about the booking. That same note nevertheless asserts Omar knows it was a lie without delivered evidence of that knowledge, and incorrectly says Omar does not know the piano risk despite the public framing and Omar's opening concern. A generated note is output evidence, not privileged access to intent.

“Free” can mean unbooked or physically unoccupied. Neither sense warrants certifying attendance or absence; the trace should preserve the ambiguity instead of scoring all uses as equivalent. Neri's final reference to the room being open for Dax may refer to permission, so it need not be penalized as confirmed attendance. The separate errors about disclosure, damage, and timing are unambiguous.

Leena's final claim to have withheld a promise is not clearly invented: she heard Neri mention a promise in t00008. Her final account's omission of other details is not a failure under the 60-word constraint. Her earlier agreement with Omar remains an unsupported inference; her later restraint should receive credit.

### Opportunity and progress

Omar asks the scheduling question immediately. Leena shares the relevant observation; the trace reaches a reasonable next-step proposal to inspect the instrument. No one is required to identify the cause or confess. The final pair could have combined Neri's scheduling knowledge with Leena's observation, but instead continues speaking to absent Omar and repeats the no-session story. This missed opportunity has concrete identity and inference errors behind it, rather than merely failing to follow a preferred plot. Repeated inspection proposals do not establish investigation progress beyond choosing a next action.

## Incomplete thinking-on arm

Only t00000 and t00001 are accepted. Omar asks about a schedule exception; Neri reports private booking until 16:30 while keeping identity/reason out of public speech. That is a useful, more direct limited disclosure than the off arm's corresponding answer. The private note names Dax, which is allowed analyst-only output and is not public disclosure or a routing leak.

The same answer also says “No extension granted.” Relative to the old 16:00 closing, this conflicts with the supplied approved exception; relative to the newly stated 16:30 endpoint, it could mean no further extension. Deliberate public evasion is allowed, and there is no later assessment to resolve intent. Mark this **ambiguous**, not a clean factual success. “The caretaker will inspect” also strengthens the public fact that the caretaker can inspect; it is not evidence the inspection has already happened.

At t00002 generation exhausted the 2048-token cap with empty final content and no accepted action. This is a bounded execution failure, not a third conversational response. The arm never reaches the audience switch, Leena's observation, the final encounter, or any private assessment. It therefore cannot establish better interactive recall, provenance, restraint, or disclosure accounting. The accepted prefix supports a local observation about one answer, not a full-run improvement.

Recorded runtime is 82.79 seconds for 13 completed off turns versus 186.652 seconds for three on requests producing two accepted turns. These are unequal completed workloads; do not report their ratio as a full-run thinking slowdown. Under this tested cap, the on configuration did not complete the interaction.

## Next bounded decision

Preserve the off trace as evidence of self-report, actor/audience, and unsupported-negative-inference failures. Preserve the on trace as a promising limited-disclosure prefix followed by a budget failure. Any increased-budget rerun is a new resource setting and should retain this failed run. A completed on trace is needed before comparing downstream semantic behavior; neither additional time alone nor its more cautious opening guarantees improvement.
