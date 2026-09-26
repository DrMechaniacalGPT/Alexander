# Readiness audit

September 26, 2026. Baseline: PR #7, commit `826cc404e93fa30e25b3d09c2c44b2d3e0a10e55`. Findings below inspect the repository; web checks are explicitly scoped separately. The legacy September 25 fact-check labels are historical claims of verification, not fresh verification by this pass.

## Context and working method

Read Alexander's `prime_directive.txt`, `policy.txt`, `soul.txt`, `craft.txt`, `Agents/Alexander/collaboration.txt`, `Path/path.txt`, `Path/steps.txt`, and the original review-synthesis idea in `Ministry/GeneratedSlop/generated_slop.txt`. The durable direction is useful software at mass adoption, openness, audience development, and resources for further work. Treat conversational examples as hypotheses and refine the idea rather than copying the transcript.

Reviewed the mystery project's shared `Projects/AGENTS.md`, `WORKFLOW.md`, and `PLAN.md` in its separate worktree, along with the relevant prior conversation. Adopt its evidence pyramid, bounded tasks, skeptical review, and distinction between PR checkpoints and outcomes. Those documents are currently in [the mystery PR stack](https://github.com/DrMechaniacalGPT/Alexander/pull/13), not PR #7's ancestry. This plan does not merge that unrelated stack or create a competing shared policy.

Read the Review Pirate business/research documents, episode script, synthesis, fact-check ledger, sources, matrix and incentive records; inspected production directions, economics, discovery, competitive analysis, CSV data and renderer. The pilot-series backlog does not need implementation in this cycle. No claim of an exhaustive review of external review content is made.

## Findings and required repairs

| Priority | Finding and repository evidence | Why it matters / task |
|---|---|---|
| High | `SCRIPT.md` says blank cells mean a product “wasn't in that source's evidence set”; `MATRIX.md` defines blank as not yet verified. The core matrix has 15 populated cells out of 64. | Missing research cannot establish non-coverage. Introduce unknown / mentioned / substantive / explicit exclusion states. Only verified candidate-set differences can explain a verdict. R1–R3. |
| High | TechRadar's matrix row identifies X60 **Max** but links `dreame-x60-pro-ultra-review`. The linked article's heading identifies X60 **Pro Ultra Complete**. | Could combine different regional products. Treat as unresolved, not proven equivalent or proven different. R1/R2. |
| High | The script says “mostly nobody” is wrong before demonstrating explanations. Synthesis says different tests, weights, prices and homes explain the result. | Plausible mechanisms are not established causes for every disagreement. Find matched cases, disconfirming evidence, and unresolved residual disagreements. R3/R6. |
| High | September 16 hub versus September 24 Top 20 is presented as a ranking change caused by a new candidate. | Two page types can differ concurrently. Need dated comparable snapshots and reason for change; otherwise describe page disagreement or remove the causal timeline. R2. |
| High | Several buyer shortlists extend beyond the eight matrix products; pet-hair section includes vague “current MOVA and Ecovacs leaders.” | Viewers need supported, specific decisions. Verify every named candidate, cost/market and limitation, or omit it. R3/R6. |
| Medium | `SOURCES.md`: 33 URL occurrences, 32 unique URLs; one T90 thread occurs twice. Multiple URLs also share publisher, test or discussion. | Count URLs, independent tests, creators and owner experiences separately. A “30+” boast is not a coverage result. R1. |
| Medium | Owner sources are purposive examples without recorded search order or inclusion/exclusion decisions; mature Saros evidence is much richer than some other products. | Can discover failure modes, not comparative reliability rates. Apply a bounded balanced search; preserve missing evidence. R4. |
| Medium | CSV has no observation date, source ID, claim locator, test-version or product-region fields; all professional rows in several source classes use `deep`. | Review cannot reconstruct every assertion or distinguish editorial endorsement from standardized testing. R1/R2. |
| Medium | `render_evidence_matrix.py` omits Chris Loh from its fixed `SOURCES`, despite a CSV row. A dictionary silently overwrites duplicate source/product keys. | Display can diverge from data. Validate duplicate keys and unmapped records; explicitly filter or render sources. R7. |
| Medium | Production opener rearranges script beats; 8 source/product names and a large grid compete for attention. | Read and time the exact voice track. Use a few illustrative sources first, then reveal scope. R6/R7. |
| Medium | Discovery has vendor estimates and title scores but no raw response/query archive. Economics specifies formulas and metrics, without a demonstrated repeatable cost or forecast. | Neither title score nor affiliate headline rate proves demand or profitability. Preserve estimates as hypotheses; measure actual cost and qualified behavior. R5/R9/R11. |
| Medium | Affiliate-rate discussion occupies scarce script time without establishing any influence on the verdict. | Keep disclosure; shorten the detour unless verified commercial context changes a specific interpretation. Never imply corruption from a public rate table. R6. |

## What to preserve

The editorial firewall, separation of anecdotes from failure rates, attention to source methods and evidence age, refusal to manufacture a universal winner, original chart approach, and promise to link the reviewers themselves are valuable. The draft has a recognizable dry voice. Repairing the evidence should sharpen that voice, not turn the video into a methods paper.

## External spot-check log

Directly opened September 26; these checks support limited observations, not the entire legacy packet:

| Page | Observation | Limit |
|---|---|---|
| [RTINGS buying guide](https://www.rtings.com/robot-vacuum/reviews/best/robot) | Names Saros 10R its overall pick; distinguishes hard-floor strengths and carpet pet-hair limits. | Extracted numeric score fields showed 0.0; do not interpret those placeholders as scores. Not all test pages re-audited. |
| [Vacuum Wars Top 20](https://vacuumwars.com/vacuum-wars-best-robot-vacuums/) | Names MOVA V70 Ultra Complete the highest overall scorer. | Does not verify historical ranking movement or its cause. |
| [TechRadar X60 review](https://www.techradar.com/home/robot-vacuums/dreame-x60-pro-ultra-review) | Heading says X60 Pro Ultra Complete. | Manufacturer-backed equivalence with Max remains unresolved. |
| [ElevenLabs pricing](https://elevenlabs.io/pricing) | Starter displayed $6 monthly and commercial license; credit limits are plan/model dependent. | No subscription, account access, API access or narration quality tested. |
| [Descript installation documentation](https://help.descript.com/hc/en-us/articles/10612575375501-Troubleshooting-issues-with-installing-Descript) | Desktop macOS/Windows and a web version. | No signed-in export tested. An attempted system-requirements URL returned an error. |
| [Descript pricing](https://www.descript.com/pricing) | Pricing page accessible. | Do not select a tier until the required export and voice features are checked in the actual account. |
| [FFmpeg](https://ffmpeg.org/about.html), [Shotcut](https://www.shotcut.org/) | Candidate render utility and cross-platform editor. | Neither installed on PATH in this shell; no production feasibility proof yet. |

Search used for access clarification: `site.help.descript.com supported browsers Linux web`. Only official Descript documentation is used for the resulting recommendation. No new keyword estimates were collected; the historical vidIQ outputs remain unverified snapshots. No paid generation, full transcript verification, complete ranking refresh, retailer sampling, or rights clearance occurred in this planning pass.

## Readiness conclusion

Enough material exists to justify a serious pilot, but the proposition that methodology explains the disagreement still needs case-level evidence. “Holistic” should mean accountable coverage of the decision, not an impossible promise to read the whole internet. The legacy TODO's research-complete statement is superseded by this audit. Research exits only through the explicit checks in [TASKS.md](TASKS.md).
