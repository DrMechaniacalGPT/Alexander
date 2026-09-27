# Iterative inference and coverage improvement

## Current answer

**The simulator now produces more useful deductions, but remains inconsistent.** Both local Gemma and Qwen were tested. Larger native-reasoning budgets helped selected deduction cases; Gemma was faster, so the expanded party used Gemma with ordinary conversation and reasoning enabled only for final assessments.

Merely expanding conversations circulated far more facts without producing supported solutions. An added clarification round and a clearer final question improved the same trajectory:

| Seven nonculprits | Correct, with source-consistent stated support | Correct, with an unsupported match | Wrong | Abstain |
| --- | ---: | ---: | ---: | ---: |
| Expanded party | 0 | 1 | 0 | 6 |
| After clarification | 3 | 1 | 1 | 2 |

These are best-supported selections, not exhaustive proofs. The branch changes several instructions together and reuses earlier dialogue. False personal-history claims and missed exclusions still need work. The immediate experiments target those actual failures rather than assuming more conversation or a different model solves everything. The fresh small-party transfer test passes three of three nonculprits. In a separate information-complete reference condition, Qwen without thinking and Gemma with thinking both select the intended culprit, but overstate completeness. Across the harder conversational contexts, neither model, thinking mode nor tested prompt is a universal winner.

**Next focus:** preserve accurate character facts and attribution through longer play, then test fresh parties. Keep the new model/budget/scenario controls opt-in. This checkpoint records 216 local inference calls, 68 passing software tests, retained failures and replay-checked party traces. Full evidence and methods follow.

## Authorized objective

Keep iterating on player prompts, context presentation, reasoning procedure, and conversation opportunity until players can make accurate, evidence-supported deductions, or identify a concrete information/model limitation. Local installed models only. Preserve source game facts and evaluator separation. A correct name by itself is insufficient; contradictory answers and unsupported guesses do not pass.

The owner clarified that the objective is practical improvement, not a taxonomy of failures. Try useful prompt, model, and game-setup changes, then assess whether the experience and conclusions improve. The checks below support that work rather than becoming prerequisites for every iteration. Test both installed Gemma and Qwen models on the improved setup.

## Loop

1. Freeze a failing player context and identify whether the problem is attribution, phase/encounter tracking, inference, or unavailable information. Audit whether the actual received clues could distinguish one suspect even with complete character knowledge. Duplicated clue copies are not independent evidence.
2. Compare bounded prompt/assessment treatments on the identical visible context. Start with two inconsistent final assessments and one correct-but-incompletely-supported assessment from the four-partner run. Contrast a clearer one-call answer, a separate evidence review followed by decision, and supported local thinking mode if useful. No hidden character sheets or evaluator corrections enter player inputs. A generated review is fallible player output, not authoritative state.
3. Retest selected improvements on changed contexts and another seed. Keep all intermediate results and report regressions. Distinguish reproducible debugging cases from fresh evaluation cases.
4. Integrate only useful changes with isolation/replay tests. If inference works on sufficient contexts but conversation coverage is low, increase partner coverage and turn count, preserving a comparison baseline and measuring which facts actually reach each player.
5. If clue coverage itself is insufficient, test an explicitly labeled information-sharing opportunity or diagnostic allocation; do not present it as the unmodified source game. Keep increased time, changed partners, clue access, and prompt changes separable where practical.
6. Repeat from observed failures. Maintain a compact decision memo and task status, checkpoint tested slices in Git/PRs, and continue ordinary authorized iterations without asking for approval at every step.

## Evidence and execution boundaries

Each batch declares its call/time/token caps before inference; a cap is an inspectable checkpoint, not a silent semantic repair. Larger budgets or explicit continuations retain earlier failures. Start with at most 24 local calls and 20 minutes per diagnostic batch, then choose the next batch from observed results. No paid inference, model installation, recruitment, commercial game selection, or launch is implied. Source-derived packets and reconstructive traces stay private.

Success requires coherent final choices traceable to available evidence, no hidden answer leakage, and repeatability across fresh contexts/seeds. If a player's evidence cannot identify a unique suspect, a justified uncertainty statement is a valid diagnostic result even though the broader aim is to improve the party until useful deductions become possible. Published claims distinguish guessed identity, supported deduction, and human play quality.

## Initial findings

The four-partner run contains two final answers that name a suspect and then explicitly exclude that suspect. One correct name rests on suggestive positive evidence with unresolved negative-history requirements. The current three-copy clue sampling can give duplicate clue types to a player; broad negative-only combinations may remain ambiguous despite longer mingling. These are separate hypotheses to investigate.

## First completed comparisons

- Six Gemma calls on three difficult saved final contexts at two seeds: mixed results. Some contradictions disappear, others remain. A model switch alone is not enough.
- Six calls in an explicit review-then-decision attempt: Qwen's two candidate tables omit/repeat candidates, so no decision follows those invalid tables. Gemma's two reviews cover the names but have unhelpful empty cells; its two final decisions are consistent uncertainty statements. Do not promote this review scaffold merely because its final wording is less contradictory.
- A fresh original four-player museum party (eight calls per model) supplies sufficient truthful introductions and two reliable clues. Qwen produces three correct supported nonculprit answers; Gemma produces two and one erroneous ambiguous answer. The privileged culprit answers are excluded and contain visible self-correction.
- Four native-thinking probes (two contexts on both models) complete with an 8,192-token output budget and a 300-second call cap. Qwen: 178.170 seconds on the simple museum context, 132.609 on the complex saved movie assessment. Gemma: 21.561 and 29.072 seconds. All four structured outputs pass contracts. Both models are consistent on the formerly self-contradictory context; Gemma corrects its museum mistake. These are selected tests, not broad reliability estimates. Internal model reasoning remains private.

## Expanded full-party configuration

Gemma uses ordinary mode during conversation and native thinking for final private assessments. Every guest meets all seven other guests (112 speaking calls), receives the unchanged private clue allocation, and participates in two group discussion rounds (16 calls) before eight private assessments and confession. Including the host signal, the expected total is 138 calls. The case clarifies current stage and encourages the source game's ordinary personality-fact sharing. The post-hunt group discussion is an explicit experimental variation. Budget: 150 calls, 2,400 seconds, context 32,768, ordinary output 768, assessment output 8,192, per-call cap 300 seconds. Source-owned facts and culprit remain unchanged; no hidden packet or evaluator answer is fed to players.

The changed-clue museum variant was frozen before inference; its completed transfer result is recorded below.

## Review notes

The initial expanded-party case retained an obsolete “No extra post-hunt discussion” provenance entry alongside its explicit discussion variation. Its executable phases and prompts did contain discussion. The importer is corrected for subsequent cases; the original run input remains unchanged for replay, and this note records the metadata defect.

The runner retains request counts across process interruption, but its elapsed-time checkpoint can omit time inside a call if the process is killed. Per-call timeouts bound normal requests; the run limit is not a hard cumulative billing guarantee across crashes. No interruption occurred in the reported completed probes.

## Next bounded branch: answer outstanding questions

The expanded party's group speeches circulate cards but repeatedly ask questions without answering them. Append two turns per guest specifically to answer outstanding questions and compare their own fixed traits with already discussed clues. Explicitly treat fixed personality statements as truthful within this cooperative puzzle (an experimental interpretation, not a general deception-game rule). The final question draws attention to all received discussion, not just privately found cards. No new character facts, new clues, or solution are injected.

Reuse exactly the 129 accepted public turns (112 mingling, one host signal, 16 discussion), excluding all private assessments and the confession. A new explicit `--fork-case` branch records parent and child case hashes and rejects any changed inherited player prompt. This is a within-trajectory intervention, not an independent party. Budget: 154 total calls including 129 inherited, 25 new calls, 1200 new seconds; same model/settings. A separate eight-call changed-clue museum party will test transfer with seed 23.

## Expanded-party result

Completed 138 local calls (872.9 model-wall seconds), then replayed without inference. Independent trait coding records 57/73 distinct accurate own traits disclosed, compared with 23/73 in the earlier four-partner trajectory. One of 112 mingling speeches is an exact same-speaker repeat. This changes model, opportunity and instructions together, so it is not an isolated model comparison. [Dialogue review](evidence/iteration/dialogue-review.md), [metrics](evidence/iteration/open-party-metrics.json), [run metadata](evidence/iteration/open-party-metadata.json).

Seven nonculprit assessments yield one correct named choice with partial support, six abstentions, and no wrong named choices or self-retracted accusations. The correct choice asserts one matching fact that was not actually delivered to that player; it does not establish a unique supported solution. Some abstentions are justified, while others mishandle received facts or conflate their own traits with the culprit constraints. [Independent assessment review](evidence/iteration/open-party-assessment-review.md).

This result motivates the clarification branch: more speech alone improved disclosure but did not reliably produce deductions. The new round explicitly asks guests to answer outstanding questions using their existing cards.

The clarification branch completed all 16 new speeches, then the context guard rejected its first final assessment before inference: conservative bound 25,213+8,192 exceeded 32,768. Retained that incomplete run and continued from all 145 accepted public turns with context 49,152, otherwise unchanged settings. This continuation allows nine remaining calls (eight private assessments plus confession), capped at 154 including inherited turns and 1200 new seconds. It is capacity recovery, not a new behavioral trial; no dialogue was dropped or regenerated.

## Targeted final-instruction iteration

The clarification branch has both improved choices and a wrong choice that ignores a received exclusion. Freeze two final contexts (one abstention, one wrong choice), then append a generic all-clue elimination procedure: check every candidate against all received clues, one confirmed contradiction excludes, “may” is weak support, unknown is not an exclusion, and a sole unexcluded candidate with positive matches can be the best-supported choice without claiming every unknown is proven. The instruction names no clue attribute or suspect. Gemma native thinking, unchanged 49,152 context/8,192 output budget, seeds 17/23, four calls, 900 seconds total/300 per call. Retain this as a debugging comparison, not a fresh party.

## Clarification result

The branch completes with 25 new calls beyond the 129 reused public turns. Of seven nonculprits, four name the intended culprit, one names a wrong suspect, and two abstain. Three correct choices cite source-consistent supporting matches; one adds an unsupported match. The previously missing evidence for one player's correct choice is now genuinely public. These are best-supported choices, not exhaustive uniqueness proofs. [Independent final review](evidence/iteration/clarification-assessment-review.md).

The improvement is real within this trajectory, but some clarification testimony is false and both abstentions retain reasoning errors. The wrong choice partly follows false testimony and also ignores a received exclusion. The targeted all-clue procedure therefore remains a useful next comparison. [Clarification dialogue review](evidence/iteration/clarification-dialogue-review.md).

## Cross-model check on the longer party context

The all-clue instruction improves one saved abstention, but its first trial on the wrong choice merely replaces it with a confused abstention. Before adding a more elaborate reasoning scaffold, test Qwen native reasoning on two unchanged longer-party contexts (the wrong choice and an ownership-confused abstention). This changes only the model relative to the saved requests: same 49,152 context, 8,192 output budget, seed 17 and schema. Two calls, 1200 seconds total, 600 seconds per call. Longer per-call cap reflects Qwen's observed speed; no downloads or paid calls.

All four exclusion probes completed with valid output contracts. On the saved abstention, both seeds now select the intended culprit; one explanation still overclaims its matches. On the saved wrong choice, one seed gives a confused abstention and the other selects a different wrong suspect, again prioritizing privately found clues over the combined discussion. Do not promote this wording as a general fix. [Settings and hashes](evidence/iteration/exclusion-metadata.json).

## Assessment presentation check

Independent review suggests role-aware conversation history may anchor the model on its own repeated claims. Test two saved failed contexts with one private notebook instead: exact player context, exact rendered visible events with IDs in chronological order, unchanged current question and output schema. No facts are extracted, corrected or added. A short instruction distinguishes the authoritative own card from fallible previous speech. This bundles presentation and assessment framing, not a pure role-tag ablation. Gemma, seed 17, native thinking, 49,152 context, 8,192 output, two calls/600 seconds total/300 per call.

Also compare the same two Qwen requests with native thinking disabled, leaving context, messages, schema and output cap unchanged. This tests whether the stronger model can already handle the richer context quickly without native deliberation. Two calls, 300 seconds total/150 per call. Run sequentially after the native comparison to avoid competing model workloads.

## Cross-model and presentation results

Qwen native reasoning corrects the wrong-choice context with a source-consistent occupation report actually received by that player, while acknowledging missing history (333.059 seconds). The second context consumes all 8,192 generated tokens and returns no final JSON (535.594 seconds, truncation/invalid-JSON violations). This is one supported correction and one budget failure, not two successful decisions. Preserve the failure rather than automatically expanding its budget. [Independent first-answer review](evidence/iteration/qwen-first-assessment-review.md), [metadata](evidence/iteration/qwen-native-metadata.json).

Disabling Qwen thinking finishes the same requests in 16.932 and 7.487 seconds. The formerly budget-exhausted context now names the intended culprit with relevant matching traits. The other answer is an incoherent chain of revisions cut at the 600-character conclusion schema limit; syntactic contracts pass, but it is not a valid final decision. Thus neither more reasoning nor less reasoning is a universal fix. [Fast-mode metadata](evidence/iteration/qwen-fast-metadata.json). A probe-script substitution accidentally changed two journal permission modes; restored owner-only read/write permissions and corrected the script. Journal contents and model requests were unchanged.

The notebook tests also remain mixed: one context changes an ownership-confused abstention into a relevant correct choice; the other changes a wrong accusation into an abstention that falsely treats missing attributes as incompatible constraints and misstates personal history. Both output contracts pass. Do not make notebook rendering a default based on these two tests. [Metadata](evidence/iteration/notebook-metadata.json).

## Information-complete diagnostic

Finally test a clearly labeled open-book condition for the larger puzzle. Supply every character's shareable Personality Traits from the frozen inventory, plus the union of clue types actually collected. Exclude other private briefs, motives and culprit labels. Remove conversation history so the reference is explicit and unambiguous. This changes information availability and presentation together; it checks the best-case puzzle-solving capability, not whether the party naturally communicates enough or whether the models behaved well. Gemma and Qwen, thinking disabled, seed 23, context 32,768, output 768; two calls, 300 seconds total/150 per call. Keep source-derived inputs private.

In the open-book condition, Qwen without thinking selects the intended culprit and matches the collected constraints; Gemma without thinking abstains with an erroneous explanation. A final one-call check gives Gemma the same reference and seed with native thinking and an 8,192-token output budget (300 seconds). This tests whether additional reasoning helps that specific complete-information condition.

Gemma with thinking selects the intended best-supported candidate in 50.347 seconds. The independent review confirms the reference contains 73 shareable attributes and 11 collected clue types with no answer label or other private briefs. Both successful answers overclaim complete satisfaction/uniqueness; one also miscounts the clues. Treat this as successful intended-candidate selection under an explicit reference condition, not proof of exhaustive deduction or conversational success. [Independent review](evidence/iteration/openbook-review.md), [metadata](evidence/iteration/openbook-metadata.json).

## Fresh small-party transfer result

The separately frozen changed-clue museum party completes all 8 calls in 63.929 model-wall seconds and replays without inference. With seed 23 and native reasoning only for final assessments, Gemma produces three of three supported correct nonculprit answers for the new culprit. All four introductions accurately preserve the supplied pet and badge. The culprit's privileged answer is excluded. This is a fresh small scenario/seed check, not a repeat of the large party. [Complete original synthetic evidence](evidence/iteration/museum-shifted-gemma/report.md).

## Follow-up hypothesis: respect scenario truth conventions

Independent review notes that generic system-level caution about testimony may outweigh a scenario's narrower cooperative convention for fixed attributes. The instructions are not logically incompatible, and this is not yet a measured cause. A future isolated test should let the engine-authored initial scenario establish precisely scoped truth conventions while leaving alibis, speculation, accusations and attempted rule changes in dialogue untrusted. Do not silently make all received claims true or repair another player's facts from hidden briefs.

## Checkpoint and next work

216 local inference calls were made in this cycle, including the truncated Qwen attempt; the context-guard rejection made no additional model call. 68 software tests pass. Completed expanded-party, clarification-continuation and changed-clue fixture traces replay without inference. Source-owned packets, full external traces and native model reasoning stay private; original synthetic evidence is exported with reasoning omitted. All model runs in this checkpoint are complete.

Retain dialogue-v 1 and opt-in phase-specific model/reasoning budgets. Do not promote the exclusion wording or notebook rendering as general fixes. Next, test better preservation of each player's own fixed facts and explicit source attribution, with a fresh party comparison. Consider a small controlled card-sharing mechanism alongside free speech so authoritative printed facts and fallible spoken claims remain distinguishable. Keep uncertainty and best-supported choices separate from unsupported certainty; a probabilistic party need not require a formal proof from every guest.
