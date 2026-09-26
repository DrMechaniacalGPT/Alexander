# Task board

Status: `[ ]` not started, `[~]` in progress, `[x]` completed. A task is complete only when its evidence and synthesis are committed, with limitations visible.

## Current design and simulation work packages

**Current gate: review this blueprint, then choose an execution slice.** These are proposed implementation tasks, not processes already running. The owner's latest instruction makes this pass planning/research, before building the simulator. IDs W01–W12 refine D01/D02/D03 rather than creating a second task system. The integrating agent owns implementation/integration; the owner supplies taste, people access and spending decisions when needed. A separate reviewer may audit outputs, but no reviewer or persona substitutes for a customer.

- [x] **P01 — Refine intent and research the design.** Read collaboration guidance; integrate primary agency/design sources and independent critique. Output: `design/DESIGN.md`, `design/RESEARCH.md`, `design/DECISIONS.md`. Done: coherent proposal distinguishes established practice, empirical transfer limits and our hypotheses.
- [x] **P02 — Expand experience and benchmark evidence.** Add six coded first-person accounts and compare five free/external candidates with actual access and terms. Output: `design/EXPERIENCE.md`, `design/BENCHMARKS.md`, `design/SOCIAL_DEDUCTION.md`. Done: contradictory preferences and free-versus-open distinction visible; no prevalence or human-behavior claim.
- [x] **P03 — Make design reviewable.** Character structure, two-page HTML sketch, simulation/event contracts, experiment protocol and work breakdown. Output: remaining `design/` files. Done: layout rendered and inspected; links checked; no full game or simulator built.

### First execution slice: W01–W04

- [ ] **W01 — Author one controlled social situation.** Depends on blueprint review. Owner: integrating agent, owner reviews tone.
  - Write four reciprocal role briefs around one dilemma, plus fixed facts and at least two independent ways to encounter relevant information. Use Alice only if still useful; no obligation to preserve names or plot details.
  - Separate shareable background, private facts, conflicting commitments, optional portrayal, openings and disclosure authority. At least two responses must be understandable; permit unanticipated actions.
  - Define downstream consequences and meaningful activity after disclosure. Add a clean variant and deliberately brittle variant; do not author a full murder merely for completeness.
  - Output: `simulation/fixtures/dilemma-v1/` with README, data and rights/provenance. Acceptance: independent review can identify what each role knows, wants and may choose, and can trace who else can respond. Stop for conflicting facts or a choice whose consequences are entirely cosmetic.
- [ ] **W02 — Implement state, events and private views.** Depends on W01's explicit inputs. Owner: integrating agent; independent isolation review.
  - Implement the objects/contracts in `design/SIMULATION.md`; append-only event log, opaque IDs, immutable history, separate live state and player-specific context construction. Keep evaluator truth outside player data.
  - Test private delivery, group membership, late join, temporary absence, repeated rumor attribution, gesture visibility, invalid artifact possession and hidden marker leakage. No inference needed.
  - Output: core modules/tests and fixture projection snapshots. Acceptance: exact recipients and permissible facts match expectations; hearing never silently becomes belief. Stop if a summary/extraction step needs omniscient context.
- [ ] **W03 — Build a deterministic dialogue runner.** Depends on W02. Owner: integrating agent.
  - Use stub/recorded responses for a complete short exchange; validate action schema, IDs and timing. Preserve rejected actions.
  - Add request caps, checkpoint/resume and idempotency; test a retry and interruption so effects are not duplicated. Produce per-player transcript plus an analyst view.
  - Output: CLI runner and a reproducible no-model demonstration. Acceptance: replay reproduces the accepted event sequence; private intention does not appear as public speech. Stop for silent repair, skipped failures or unreproducible state.
- [ ] **W04 — Connect and benchmark local inference.** Depends on W03. Owner: integrating agent.
  - Implement a replaceable Ollama adapter with local endpoint only, explicit settings, bounded generation/timeouts and raw usage/error capture. Inspect installed model metadata and server behavior before selecting context settings.
  - Run E1 then E2 from `design/EXPERIMENTS.md` within their separate caps, using a predeclared hand-authored encounter schedule until W06 exists; inspect results between stages. No downloads, paid fallback or broad unattended sweep.
  - Output: model manifest, raw calls and concise capability report. Acceptance: role context fits, outputs parse, facts/visibility remain auditable, and a short encounter completes with intelligible consequences. Report model errors rather than pretending this validates human behavior. Stop/revise if truncation, latency or unsupported inventions dominate.

### Explore the design: W05–W08

- [ ] **W05 — Compare information-shaped choices.** Depends on W04. Owner: integrating agent, independent trace reviewer.
  - Freeze a decision snapshot; prepare relevant positive/adverse/competing information, consequence-to-other-person information, no-addition and irrelevant controls. Keep provenance/timing comparable and identify confounds.
  - Run the bounded E3 continuations. Classify actions afterward; retain “other,” ambiguous and failed cases. Inspect supporting observations and effects on others.
  - Output: paired trace report and proposed writing revisions. Acceptance: distinguishes random variety, context-sensitive choice and mechanical failure. Do not require equal branches or infer internal causation from generated rationales. Stop automated expansion if the traces are not interpretable.
- [ ] **W06 — Add encounter scheduling.** Depends on W04; informed by W05. Owner: integrating agent.
  - Implement random-pair baseline and initiative-led matching with explicit attendance, occupancy, continuation length and unmatched approaches. Vary windows rather than hardcode six as human truth.
  - Test no double-booking and no information from future or missed windows. Add group membership/speaker routing only after pair mode passes; compare formats separately.
  - Output: schedule tests and visible encounter timeline. Acceptance: schedule assumptions and idle opportunities are explicit; forced pairing is not presented as spontaneous mingling.
- [ ] **W07 — Stress roles and imperfect play.** Depends on W05–W06. Owner: integrating agent and reviewer.
  - Swap initiative profiles across roles. Compare withholding, early full disclosure, one-role absence and full/bounded attention one at a time; retain contextual memory omissions.
  - Add small faction and improvisation treatments only after initial patterns are understandable. Separate portrayal, speculation, deception, unsupported testimony and fabricated artifacts.
  - Output: per-role opportunity/decision report and versioned revisions. Acceptance: separates accidental stalls, chosen consequences and model failures; evaluates useful play after secrets emerge. Stop rather than optimize an aggregate “fun” score.
- [ ] **W08 — Map and conditionally adapt an external scenario.** Mapping can start after W02; live runs depend on W04 and a resolved use scope. Owner: integrating agent; owner involved only if permission/contact/spending is needed.
  - Start with the small Élysée reference, or select a better candidate with a recorded reason. Inventory original rules, roles, moderation, actions and unmodeled behavior without copying packets into the MIT repo.
  - Resolve permitted intended use before adaptation/publication; if unclear, keep only the mapping or use an original substitute. Maintain rights/provenance and adaptation assumptions separately.
  - If appropriate, run a few frozen adapted traces. Output: compatibility report, not a claim that original players behave this way. Acceptance: external structure challenges our assumptions; borrowed materials are not silently relicensed. Model familiarity and absent human ground truth remain limitations.

### From research fixture to product: W09–W12

- [ ] **W09 — Observe existing play and improve the vocabulary.** Parallel research, not a prerequisite for every creative experiment. Owner: bounded research agent/integrator.
  - Locate an accessible full playthrough or consented session with usable dialogue. Code selected contiguous windows: approaches, lies/speculation, corrections, disclosure, quiet participation and coalitions; record missing audio/edits and vendor influence.
  - Compare observed behaviors with our policy labels; retire labels that obscure more than they explain. Output: dated coding guide/source records. Acceptance: no inference of frequencies from selectively edited clips and no claim that strategy advice is observation. If access fails, record the gap rather than inventing it.
- [ ] **W10 — Select a theme and write one original scene.** Depends on usable W05/W07 findings; owner taste decision. Refines C03 and starts D01.
  - Revisit audience, tone and Immortality/Lot 13/other candidates. Decide which relationships and dilemmas fit; do not pick a theme from simulated branch counts.
  - Expand toward eight reciprocal roles and one scene, with optional shared orientation beats. Review each player's workload and post-disclosure opportunities. Full three-act writing follows only when this slice is worth extending.
  - Output: concept decision and one playable scene, with versioned cards. Acceptance: fixed history coherent, quieter roles consequential, no required acting trick or endless rule burden. Human comprehension remains unmeasured until W11.
- [ ] **W11 — Arrange reader checks and human sessions.** Reader checks can begin once W01 exists; parties depend on playable W10 material. Refines D03. Owner helps access people; outreach requires authorization.
  - Ask readers what is fixed, private and optional and what they would do first. Later gather actual host preparation, misunderstandings, choices, enjoyment and solvability separately.
  - Plan recruitment, consent/logging and questions before contacting volunteers. The owner may host one session; later public-content volunteers are a biased but potentially useful source.
  - Output: human feedback and comparison with predictions/surprises. Acceptance: direct participant voices and negative cases retained. No claim of calibrated population behavior from a handful of groups.
- [ ] **W12 — Decide public experiment and commercial scope.** Depends on real material/results worth showing; refines L01. Owner approves public positioning and spending.
  - Storyboard an honest process account, including failures and human differences when available. Decide standalone branding, asset/license boundaries, free sample versus finished paid convenience, and recruitment versus purchase goals.
  - Rebuild economics including simulator maintenance, video production and acquisition labor. Measure qualified hosts and transactions separately from views/developer interest.
  - Output: launch/recruitment proposal and bounded measurement plan. Acceptance: no unsupported perfect-game claim, no assumption of virality, no third-party NC content silently used in commercial materials. No publication implied by this task list.

**Next proposed action after review:** execute W01–W04 only, inspect the concrete output, then select the next experiments. Research W09 may proceed independently if authorized. This avoids building a full game and full simulator simultaneously while still co-designing a meaningful situation.


## Historical discovery scope

- [~] **M01 — Seller and product map.** Follow `research/market/METHOD.md`; catalog a broad, reproducibly found set across independent sites, marketplaces, print kits, and app formats. Record title, seller, player range, duration, mechanics, host role, delivery, price/date, review volume, and comparable theme. Target at least 20 distinct sellers or document why coverage stops sooner. Output: `research/market/sellers.csv`, `research/market/sellers.md`, and search log.
- [~] **M02 — Buyer feedback sample.** Sample positive, mixed, and critical reviews for representative products across sources. Separate buyer setup/shipping complaints from player experience; capture exact product/version, date, review selection, repeated themes, and counterexamples. Output: `research/experience/reviews.md` with source ledger IDs.
- [~] **M03 — Community and video research.** Search Reddit, forums, YouTube hosts, playthroughs, tutorials, and comments using recorded queries and dates. Note what can be observed in play versus merely asserted by a creator. Seek strong counterexamples to our format preferences. Output: `research/experience/community.md`.
- [~] **M04 — Genre mechanics.** Compare at least the scripted, freeform/objective, staged clue, app-guided, and host-optional patterns using inspectable rules/previews and player reports. Map failure modes and what evidence supports each. Output: `research/experience/mechanics.md`.
- [~] **M05 — Delivery and economics.** Verify current download prices, print quantities and assembly, fulfillment quotes, platform fees, refunds, video/tool costs, and app maintenance assumptions. Build low/base/high scenarios with explicit units, gross, variable costs, labor, acquisition, and contribution; keep lifetime observations separate from annual forecasts. Output: `research/market/economics.md` and reproducible model.
- [x] **M06 — Synthesis.** Reconcile conflicting evidence from M01–M05, state what is known and unknown, and update the one-minute README. Gate 1 decision: proceed, revise scope, or stop. Output: `research/DECISION.md`.

## Historical concept and game scope

- [~] **C01 — Broad concepts.** Generate divergent settings and mechanics, screen for obvious comparables, and select finalists by recorded criteria. Include *The Immortality Club* without privileging it. Output: `concepts/longlist.md`.
- [~] **C02 — Persona challenge.** Have independent perspectives attack each finalist; record concrete objections and the evidence that would resolve them. Interview actual potential hosts/players where possible. Output: `concepts/personas.md`.
- [~] **C03 — Concept decision.** Pitch the winning concept and alternatives with a falsifiable reason for choosing it. Output: `concepts/decision.md`; Gate 2 review.
- [ ] **D01 — Paper game.** Solution, role and information graph, act timing, host instructions, clue inventory, cancellation handling, and accusation/reveal. Output: playable `game/` packet.
- [ ] **D02 — Simulation dojo.** Encode the game state and heterogeneous encounter/communication policies. Run robustness sweeps, report assumptions and failures, fix brittle clue paths. Output: `simulation/` code and report.
- [ ] **D03 — Human tests.** Recruit varied groups, observe nights, gather anonymous individual responses, revise the packet, and document unresolved problems. Output: `playtests/` logs and Gate 4 decision.
- [ ] **L01 — Commercial experiment.** Produce the chosen format, test listing/discovery, record actual conversion and contribution, and decide whether to expand. Output: `launch/` report.

Tasks may be split into smaller PRs. A task ID is a stable pointer to evidence, not a claim that an agent ran in the background.

## Earlier September 26 discovery audit (historical snapshot)

The [bounded execution amendment](research/EXECUTION.md) permits a discovery recommendation with gaps visible. Checkboxes retain the original broader completion tests.

| Task | Delivered | Remaining |
|---|---|---|
| M01 | Inherited 32-seller pilot plus fresh format/price probes and two broad query windows | No census or saturation; purposive title selection |
| M02 | 15 coded written accounts with contradictory experiences | Exact versions/purchase verification missing for many; negative app coverage limited |
| M03 | Community synthesis, two transcripts and video discovery window | No full video/comment comparison; no live observation |
| M04 | Six overlapping patterns compared, primary rules/previews | App operation and some host-blind flows are seller claims, not hands-on audits |
| M05 | Reproducible digital economics with tested arithmetic and sensitivity | Actual costs/CAC, specified fulfillment quotes, app/video estimates absent |
| M06 | Bounded recommendation, countercase, uncertainty and proposed next experiments | Owner discussion required before further phase |
| C01 | Twelve concepts, five scored finalists, limited comparable screening | Broad independent novelty screening not completed |
| C02 | One-researcher adversarial perspectives, explicitly hypothetical | Independent perspectives and real host/player interviews not obtained |
| C03 | Provisional Immortality/Lot 13 pitch and falsifiable selection logic | No owner selection or validated winner |
| D01–L01 | None | Deliberately beyond the requested pre-build discussion gate |

No task status implies an agent is continuing in the background.

## Feasibility follow-up — September 26

- [x] **F01 — Decision-stage technical assessment.** Document separate engineering, design-validation and distribution bets; alternatives, isolation architecture, costs, effort and stop rules. Output: `research/FEASIBILITY.md`, `research/DOJO_SKETCH.md`, `research/FEASIBILITY_SOURCES.md`.
- [x] **F02 — User-requested local connectivity probe.** Three short Python/Ollama calls and separate-input marker checks passed; timings and exact prompts saved. This is not a game simulation or a privacy proof.
- [~] **F03 — Agree next scope.** Direction clarified through the owner’s discussion: co-design a creative local experiment and small original situation. The blueprint and W01–W04 now specify the proposed investment; execution review remains open. The former narrow defect-detection gate is superseded.

The discovery checkpoint remains open for product discussion. The proposed dojo is not evidence of human enjoyment or an established acquisition channel.
