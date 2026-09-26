# Task board

Status: `[ ]` not started, `[~]` in progress, `[x]` completed. A task is complete only when its evidence and synthesis are committed, with limitations visible.

## Discovery

- [~] **M01 — Seller and product map.** Follow `research/market/METHOD.md`; catalog a broad, reproducibly found set across independent sites, marketplaces, print kits, and app formats. Record title, seller, player range, duration, mechanics, host role, delivery, price/date, review volume, and comparable theme. Target at least 20 distinct sellers or document why coverage stops sooner. Output: `research/market/sellers.csv`, `research/market/sellers.md`, and search log.
- [~] **M02 — Buyer feedback sample.** Sample positive, mixed, and critical reviews for representative products across sources. Separate buyer setup/shipping complaints from player experience; capture exact product/version, date, review selection, repeated themes, and counterexamples. Output: `research/experience/reviews.md` with source ledger IDs.
- [~] **M03 — Community and video research.** Search Reddit, forums, YouTube hosts, playthroughs, tutorials, and comments using recorded queries and dates. Note what can be observed in play versus merely asserted by a creator. Seek strong counterexamples to our format preferences. Output: `research/experience/community.md`.
- [~] **M04 — Genre mechanics.** Compare at least the scripted, freeform/objective, staged clue, app-guided, and host-optional patterns using inspectable rules/previews and player reports. Map failure modes and what evidence supports each. Output: `research/experience/mechanics.md`.
- [~] **M05 — Delivery and economics.** Verify current download prices, print quantities and assembly, fulfillment quotes, platform fees, refunds, video/tool costs, and app maintenance assumptions. Build low/base/high scenarios with explicit units, gross, variable costs, labor, acquisition, and contribution; keep lifetime observations separate from annual forecasts. Output: `research/market/economics.md` and reproducible model.
- [x] **M06 — Synthesis.** Reconcile conflicting evidence from M01–M05, state what is known and unknown, and update the one-minute README. Gate 1 decision: proceed, revise scope, or stop. Output: `research/DECISION.md`.

## Concept and game

- [~] **C01 — Broad concepts.** Generate divergent settings and mechanics, screen for obvious comparables, and select finalists by recorded criteria. Include *The Immortality Club* without privileging it. Output: `concepts/longlist.md`.
- [~] **C02 — Persona challenge.** Have independent perspectives attack each finalist; record concrete objections and the evidence that would resolve them. Interview actual potential hosts/players where possible. Output: `concepts/personas.md`.
- [~] **C03 — Concept decision.** Pitch the winning concept and alternatives with a falsifiable reason for choosing it. Output: `concepts/decision.md`; Gate 2 review.
- [ ] **D01 — Paper game.** Solution, role and information graph, act timing, host instructions, clue inventory, cancellation handling, and accusation/reveal. Output: playable `game/` packet.
- [ ] **D02 — Simulation dojo.** Encode the game state and heterogeneous encounter/communication policies. Run robustness sweeps, report assumptions and failures, fix brittle clue paths. Output: `simulation/` code and report.
- [ ] **D03 — Human tests.** Recruit varied groups, observe nights, gather anonymous individual responses, revise the packet, and document unresolved problems. Output: `playtests/` logs and Gate 4 decision.
- [ ] **L01 — Commercial experiment.** Produce the chosen format, test listing/discovery, record actual conversion and contribution, and decide whether to expand. Output: `launch/` report.

Tasks may be split into smaller PRs. A task ID is a stable pointer to evidence, not a claim that an agent ran in the background.

## September 26 discovery audit

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
- [ ] **F03 — Agree next scope.** Decide whether to pursue the narrow test bench, a game-first approach or a content/research-first approach, with a bounded investment. No build commitment yet.

The discovery checkpoint remains open for product discussion. The proposed dojo is not evidence of human enjoyment or an established acquisition channel.
