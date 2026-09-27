# Dialogue history diagnosis

**The repeated introduction was reproducible, and changing how history is presented improves selected dialogue failures. This is not yet a general reasoning fix.** The owner asked us to investigate prompt construction before blaming local model capability, explicitly frame small cases as murder mystery party play, then compare the original party schedule with four distinct partners per guest.

## Executive comparison

| Run | Mingling speeches | Exact repeated speeches | Distinct own traits clearly disclosed | Nonculprit accusations: correct / wrong / abstain |
| --- | ---: | ---: | ---: | --- |
| Earlier JSON-observation baseline | 32 | 16 | 5 / 73 | 0 / 5 / 2 |
| Dialogue history, original schedule | 32 | 1 | 16 / 73 | 0 / 1 / 6 |
| Dialogue history, four distinct partners | 64 | 2 | 23 / 73 | 1* / 1 / 3, plus 2 inconsistent answers |

*The correct name uses a genuinely received but only suggestive positive report. Other needed facts remain unknown, so this is not a demonstrated unique solution. The two inconsistent answers name someone and then explicitly rule that person out. See the [independent assessment review](benchmarks/reviews/accusation-review.md).

The denominator is a frozen manual inventory of independently assertable personality facts, not word count or every detail on a character card. It excludes motives, role background, and performance instructions. Clear paraphrases count; vague implications and borrowed false claims do not. One broad preference paraphrase is flagged but treated consistently. Coverage is global disclosure by the owner of a fact, not proof every listener received it or understood it. Runs are single correlated trajectories, not human estimates.

## What was actually wrong?

The saved second-turn request contained both earlier lines, with correct speaker labels. It was a new model generation, not a replayed stored action: other response fields differed. Source newlines were also correctly decoded; the escaped appearance in inspection output was not evidence of double encoding. We have not established a transport or history-delivery bug.

The original prompt presented all prior speech inside a single JSON observation list. The candidate `dialogue-v1` instead places visible self-authored speech in assistant history and other players' speech, host deliveries, and actions in labeled user observations. It ends with an explicit current-player/current-audience envelope. These are transcript excerpts, not the full original action objects. Private intentions, prior private assessments, hidden roles, and evaluator answers are not inserted into chat history.

The candidate also explicitly describes a person playing a character at a murder mystery party and asks for the next reply. Therefore the comparison tests a **format-and-framing treatment**, not proof that role tags alone cause improvement. Legacy profiles and their replay payloads remain unchanged; the candidate is opt-in.

## Bounded frozen comparisons

Three pre-existing failures: repeated opening, adopting another character's pet/claims, and addressing a former partner. Two seeds per case. The initial 18 calls compare original input, a readable transcript inside one message, and alternating chat messages. The original repeated opening reproduced at both seeds. Alternating chat changed that behavior and avoided the selected role-adoption failure, but still carried an old question into a new encounter.

Six integration calls used JSON-wrapped event messages. One response still adopted another character's pet. A second six-call integration trial uses readable attributed lines and an explicit partner-change reminder. It improves the selected opening/role-adoption outputs, but does not fully reset conversational context: replies still sometimes answer the former partner's question. One private intention contradicts fixed character history. All versions and failures are retained.

The initial pilot's old auditor expected a final JSON player envelope and raised parser errors for the text-based treatments **after successful generation**. An offline re-audit using each unchanged original output schema and phase finds zero contract violations in those 18 responses. Those diagnostic errors are not counted as failed model generations, and no model call was repeated to repair them. The integrated profile preserves the machine-readable phase/citation envelope and works with the normal auditor.

## Small complete scenarios

A seven-call relay and thirteen-call selective-disclosure exercise ran under explicit party-player framing. The original fixture facts and encounter schedules are unchanged. These are small side-interaction exercises, not complete murder mysteries. Compare them qualitatively with earlier runs: seed/budget/profile differ, so do not assign a causal effect size.

The relay passes the location through two speakers with a recognizable source chain. The selective-disclosure conversation is more responsive, but invents protective actions, confuses a past booking interval with current time, and inaccurately accounts for some disclosures in private assessments. Fluent continuation is not reliable factual reasoning.

## Party comparison

The original-schedule rerun completed 42 calls in 285.350 seconds of recorded model wall time. Manual trait coding with a frozen 73-fact inventory improved from 5 clearly disclosed traits to 16, and same-speaker exact repeats fell from 16/32 to 1/32. Nonculprit accusations were 0 correct, 1 wrong, 6 abstentions (previously 0/5/2). This run uses the candidate profile and strict phase schema; it is not a pure role-tag ablation. More abstentions are not proof of better reasoning. Same seed and clue allocation are preserved. The completed expanded comparison gives each of eight players four distinct partners through a content-independent round-robin schedule: sixteen encounters, two turns per speaker, sixty-four dialogue calls. The original used thirty-two dialogue calls. The totals including the signal, private accusations and confession are 42 and 74 generations. The expanded run took 527.133 seconds of recorded model wall time. Every guest had exactly four distinct mingling partners; all 74 turns passed structural checks and replayed without inference.

The expanded round-robin also changes pair identity/order; it does not preserve the original two-window prefix. Treat it as a schedule intervention, not an isolated estimate of conversation count.

Our assessment question permits an insufficient-evidence answer, whereas the source party asks people to point to a suspect. We preserve this evaluation choice across these runs and report abstentions separately; it limits comparisons with human party solve rates.

The printed clue inventory, selected briefs, private allocation of three clue copies per guest, and immediate accusation sequence remain unchanged. We are varying conversation opportunity as well as compute; neither simulation recreates physical search, free movement, or human play.

Measure distinct accurate own traits disclosed, delivery to other players, repeated speech, role/audience errors, and accusation evidence separately. An unknown answer can be appropriate when relevant facts never arrived. Exclude the culprit from the accusation inference score. No game quality or human enjoyment conclusion follows from synthetic success or failure.

## Reproduction and evidence boundaries

Use `python3 -m tools.probe_dialogue SOURCE_RUN --out NEW_PRIVATE_DIRECTORY --cases t00002 t00013 t00020 --variants original integrated --seeds 17 23` for frozen comparisons. The tool reserves each request before local inference, keeps raw failures, refuses an existing output directory, and caps calls/time. `--variants readable chat` reproduces exploratory renderings; only `integrated` uses the production candidate. Source-derived inputs and detailed outputs must remain private.

Use `--prompt-profile dialogue-v1 --strict-output` with the runner for the integrated profile. The current schema remains the five-field action contract. Use `python3 -m tools.import_movie PRIVATE_SOURCE PRIVATE_OUTPUT --seed 17 --partners 4` to build the expanded schedule. The default adapter remains unchanged.

Raw external records stay under `local-private/movie/`; only non-reconstructive results and original synthetic exercises may be published. Source-derived facts are not silently relicensed. See the [task board](../TASKS.md) for the agreed sequence.

The independent frozen-case review is in [dialogue review](benchmarks/reviews/dialogue-review.md). Complete original exercise traces: [relay](evidence/dialogue/dialogue-relay/report.md), [selective disclosure](evidence/dialogue/dialogue-selective/report.md). Nine previously published complete original trajectories replay with no inference.

## What to do next

The repeated-opening failure is substantially reduced in these selected runs, and broader mingling increases distinct accurate disclosure. That is a useful implementation milestone. We have not reached reliable deductions or robust role fidelity. The four-partner run still transfers personal facts between people and anticipates a later-stage artifact. Some final answers name a suspect and then rule that same suspect out.

The next bounded diagnosis should separate two issues: explicit encounter/scene boundaries (who is here, what has actually happened) and the final decision protocol (consistent accusation or abstention after weighing the received clues). Test frozen failed contexts before another whole party. Also review whether generic permission to withhold is undercutting this particular game's stated disclosure rules. Do not replace unavailable facts with the full hidden packet to manufacture success.

## Verification and scope

This follow-up made **166 new local generation calls**: 30 frozen probes, 20 calls across two original exercises, and 116 calls across the two external party trajectories. No model download, paid API, silent repair, or repeated generation after failure was used. **58 tests pass**. Nine previously published complete original trajectories, both new original exercises, and both new external trajectories replay without inference. Original export hashes remain unchanged after replay. No inference job remains running at this checkpoint.
