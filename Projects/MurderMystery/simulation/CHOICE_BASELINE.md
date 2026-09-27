# Can the current game work in our simulator?

## Current answer

**The eight-character adaptation supports a clear best guess; we do not have evidence that the game is fundamentally broken.** The intended culprit has the strongest complete-information support under every tested encoding. Formal uniqueness depends on ordinary-language interpretations of a few career descriptions. Players need not produce a proof to enjoy guessing.

**Local use of long conversation histories remains a material limitation.** Required votes remove abstentions but do not consistently improve accuracy or eliminate confused attribution and self-accusations. Three independently isolated Codex reviewers choose the intended culprit on selected player contexts where Gemma chose incorrectly. This is evidence that missing information alone does not explain those particular failures, not a general model ranking.

A deterministic fact-sharing simulator is now implemented and tested. It separates received information from global facts, makes unknowns explicit, and can reproduce information-flow experiments without language-model calls. Gemma selects the intended culprit in all seven player assessments on one preselected, favorable packet-sharing trace. Three anonymous-label and shuffled-presentation controls also succeed. These results change information quality and presentation together, so they do not isolate history retrieval as the cause of earlier failures.

## What the experiments say

### Require a guess

These are repeated final assessments of the same saved player contexts—not newly played parties. Seven nonculprits are scored; the culprit's privileged answer is excluded.

| Final-answer format | Before clarification | After clarification | Limitation |
| --- | ---: | ---: | --- |
| Earlier optional accusation | 1/7 | 4/7 | Six and two abstentions respectively; correct names are not all sound arguments |
| Required suspect plus explanation | 2/7 | 3/7 | One choice disagrees with its explanation; one self-vote |
| One-field required vote | 3/7 | 4/7 | One and two self-votes respectively; no explanation to evaluate |

Removing the player's own explicitly innocent character from the three self-vote contexts produces legal votes but **zero correct replacements out of three**. It is a useful rule constraint, not a deduction fix. These small, selected comparisons do not establish stable percentage improvements. [Required-guess records](evidence/choice/required-guess-metadata.json), [vote-only records](evidence/choice/choice-only-metadata.json).

### Is the available information usable?

Three fresh-context reviewers separately receive the same serialized messages and schema as three failed local required-guess assessments. All three select the intended culprit with relevant received evidence and acknowledge missing facts. None sees another reviewer's private packet or the evaluator answer. The execution wrapper differs from an API call, and these are selected failures, so do not treat 3/3 as a party-wide benchmark. [Review provenance](evidence/choice/stronger-review.json).

A hosted API comparison was not run: no API key was present in the execution environment. The independent review is the qualitative alternative discussed with the owner. No paid API calls were made.

### Does complete information uniquely solve it?

| Interpretation of the eight selected roles | Candidates not excluded, sampled 11 clue types | Candidates not excluded, all 16 printed types | Highest match-count candidate |
| --- | ---: | ---: | --- |
| Strict explicit entailment | 4 | 4 | Intended culprit |
| Also recognize current acting plus previous modeling as different work | 3 | 3 | Intended culprit |
| Also interpret the former magician role as another career | 2 | 2 | Intended culprit |
| Also interpret band participation alongside acting as another occupation | 1 | 1 | Intended culprit |

The latter assumptions are progressively less explicit; the band assumption is especially debatable. They are sensitivity settings, not silent corrections to the source. Missing attributes stay unknown. One printed clue concerns the death mechanism and cannot eliminate a character without a relevant link. These results concern the selected eight-role adaptation, not all ten available role cards or a faithful physical clue hunt. [Corrected reference results](evidence/choice/complete-information-v2.json).

### Can information circulate without an LLM?

Yes. Each player starts with their own source-backed fact packets, meets distinct partners, receives their allocated clue types, and optionally shares with the group. All choices use only their received packets. Irrelevant background packets still consume conversational space.

For seven partners and four fact packets per exchange, across 100 seeds and 700 nonculprit decisions:

| Reference condition | Correct required votes |
| --- | ---: |
| Strict interpretation, no group exchange | 271/700 (38.7%) |
| Strict interpretation, two group rounds | 615/700 (87.9%) |
| Career interpretations, two group rounds | 669/700 (95.6%) |
| Strict interpretation, same two-round traces, rank by distinct supporting sources | 683/700 (97.6%) |

This is an idealized transport and decision baseline, not a human success forecast. It knows recipients' ledgers to avoid redundant delivery, transmits facts accurately, and uses a declared ranking heuristic. The outcomes within a party are correlated. More partners do not monotonically improve every setting, because random selection and group-sharing choices interact. [Strict study](evidence/choice/sharing-strict-v2.json), [interpretation sensitivity](evidence/choice/sharing-ordinary-v2.json), [weighting sensitivity](evidence/choice/source-weight-sensitivity.json).

## Recommendation and next step

**Stay with this game and build a small hybrid experiment.** Let agents choose which permitted facts to disclose while the simulator records those explicit disclosures accurately. Then give symbolic and local-model assessors the same resulting player knowledge. This tests a useful middle ground between random packet sharing and unrestricted, error-prone dialogue.

Packet delivery must be visible as an explicit factual disclosure, not an invisible transfer behind unrelated speech. Preserve background packets; do not give the choosing agent an omniscient view of another player's knowledge. Keep free speech separately attributed and do not automatically turn every claim into authoritative fact. Use a fresh predeclared seed and retain the existing free-dialogue and deterministic controls. No new commercial game selection is required.

The current conclusion is sufficient to motivate that direction: the encoded game is workable as a best-guess puzzle, local models can use clean partial evidence, and full conversation handling remains unreliable. We have not measured human enjoyment, realistic error rates, or general performance across games.

### Structured-evidence capability check

Gemma receives each of seven nonculprits' known authoritative predicate assertions and clues from the strict symbolic trace at seed 17, plus their own innocence. It sees no global facts, solver rankings, candidate eliminations or answer label. Irrelevant background is omitted. All seven votes are correct; the mean response time is about 31 seconds. Exact-knowledge boundary checks pass for every request.

On three preselected contexts, consistent anonymous character/source labels and shuffled fact, clue and candidate order also produce the correct three votes. This challenges fixed-name and ordering shortcuts. It remains one favorable, noiseless transport trace with several player views—not seven independent parties or a validation of natural dialogue. [Packet comparison](evidence/choice/packet-assessment-metadata.json), [label/order control](evidence/choice/alias-metadata.json), [self-vote follow-up](evidence/choice/self-vote-metadata.json).

## Engineering and review

83 tests pass, including information isolation, reproducibility, evaluator-answer independence, conflicting claims, duplicate evidence and source prerequisites. Review found and fixed a prematurely activated two-source inference and an overly strong career encoding before final comparisons. Superseded evidence is retained and labeled. Source packets, detailed source-derived traces and native model reasoning remain private.

This cycle completed 41 local inference calls plus three isolated Codex reviews. All local experiments are finished.

The standing workflow now requires a completion review and justified follow-up, rather than stopping when a task or PR is finished. An hourly follow-up is active to resume that loop between conversations while avoiding duplicate active work.

---

# Experiment record

## Current objective
Push the current game and available simulator approaches until evidence supports a next decision. A completed task is a checkpoint, not the finish line. Preserve uncertainty without making abstention the party outcome.

## Declared comparisons

1. Require guesses on seven nonculprit saved final contexts before and after clarification: same Gemma model, seed, thinking and evidence. Change final instruction and add an enumerated suspect field. Budget: 14 calls, 1,800 seconds, 180 seconds each.
2. Build seeded fact-packet exchange with explicit sources and conservative elimination. Compare limited sharing with complete access; unknown and conflicting reports cannot silently become false. Validate interpretations against full source cards before calling the game fundamentally ambiguous.
3. Fresh-context independent Codex review of one identical required-guess context. Read only that player packet, no scenario truth or other players’ private packets. This is a qualitative stronger-model counterpoint, not a hosted API benchmark; no API key was configured in the execution environment.

## Follow-up declared during first batch

The first batch produced a suspect field inconsistent with its explanation. Run a second comparison on the same original contexts and settings with a one-field required vote. No separate explanation or certainty score. Budget: 14 additional calls, 1,800 seconds, 180 seconds each. This measures votes, not sound supporting reasoning. Do not discard the contradictory first result.

## Provisional findings

The conservative source encoding leaves four candidates compatible with the eleven sampled clue types. The intended culprit has the most positive matches. This is not yet a conclusion about the complete published game: a second reviewer is checking ordinary interpretations, complete cards and uncollected clue types.

## Second follow-up declared before inference

A deterministic seven-partner, four-packet, two-group-round trace at seed 17 gives every nonculprit the intended culprit as its highest hard-match candidate, although several candidates remain formally possible. Give Gemma exactly each player's known authoritative predicate packets and collected/shared clue packets, plus their own innocence. Do not supply symbolic rankings, exclusions or answer labels. Use a frozen shuffled candidate order, seed 23, native thinking, 32,768 context, 8,192 output tokens. Maximum seven calls, 900 seconds, 180 seconds each. This changes communication and representation together; it tests whether the local model can make useful votes after reliable packet transport, not whether natural dialogue is faithful. Retain the simpler vote-only conversational comparison before this test.

## Review fixes and weighting sensitivity

Independent review found a derived career assertion could activate before both supporting packets arrived. The engine now enforces prerequisite packet exposure, covered by a test. It also flagged that lifelong work does not necessarily mean exclusive work; the strict source encoding now leaves that predicate unknown. Earlier sweep files are retained as superseded; use `*-v2.json` for conclusions. Current aggregates fingerprint their case and engine. The complete-information candidate sets are unchanged by these corrections.

A follow-up on the same 100 strict seeded parties reranks candidates by distinct matching fact sources instead of raw hard-clue matches. At seven partners, four packets and two group rounds, correct votes increase from 615/700 to 683/700. The finding does not depend on treating several consequences of one fact as independent support. Neither weighting is a calibrated player model.

The first suspect-only batch also repeats an impossible self-vote by a player whose private card explicitly says they are innocent. After both saved contexts complete, rerun those two contexts with only that known-ineligible choice removed and an explicit own-card reminder. Maximum two calls, 360 seconds, 180 seconds each. This is a legal-choice constraint grounded in the player's own knowledge, not hidden culprit information.


## Stronger-model follow-up

The first fresh-context reviewer selected the intended culprit from exactly the same messages and schema as the local p5 required-guess call; that local call chose incorrectly. Before seeing further review outputs, select two additional saved failures (p3 and p6, clarification required-guess contexts) for separate fresh-context reviewers. Each may read only its own evidence packet. This remains a selected-case qualitative comparison with a different execution wrapper, not a controlled API benchmark or a party-wide accuracy estimate.

The completed relevant vote-only contexts show three self-votes: p6 before and after clarification, and p5 after clarification. Extend the declared own-innocence follow-up to exactly these three contexts before running it; budget three calls, 540 seconds, 180 seconds each.

## Label/order robustness control declared before inference

The first three structured packet assessments select the intended culprit. Before declaring that capability result, preselect p2, p4 and p8 for a combined anonymous-label and presentation-order test once their original calls finish. Replace every character identity consistently, shuffle candidate, fact and clue lists, and verify inverse mapping preserves supplied evidence. Leave model settings unchanged. Maximum three calls, 540 seconds, 180 seconds each. This challenges fixed-name/order shortcuts; it is not a new game or an estimate of generalization to other plots.
