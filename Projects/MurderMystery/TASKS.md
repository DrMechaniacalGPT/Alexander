# Task board

Status: `[ ]` not started, `[~]` in progress, `[x]` completed. A task is complete only when its evidence and synthesis are committed, with limitations visible.

## Discovery

- [~] **M01 — Seller and product map.** Follow `research/market/METHOD.md`; catalog a broad, reproducibly found set across independent sites, marketplaces, print kits, and app formats. Record title, seller, player range, duration, mechanics, host role, delivery, price/date, review volume, and comparable theme. Target at least 20 distinct sellers or document why coverage stops sooner. Output: `research/market/sellers.csv`, `research/market/sellers.md`, and search log.
- [ ] **M02 — Buyer feedback sample.** Sample positive, mixed, and critical reviews for representative products across sources. Separate buyer setup/shipping complaints from player experience; capture exact product/version, date, review selection, repeated themes, and counterexamples. Output: `research/experience/reviews.md` with source ledger IDs.
- [ ] **M03 — Community and video research.** Search Reddit, forums, YouTube hosts, playthroughs, tutorials, and comments using recorded queries and dates. Note what can be observed in play versus merely asserted by a creator. Seek strong counterexamples to our format preferences. Output: `research/experience/community.md`.
- [ ] **M04 — Genre mechanics.** Compare at least the scripted, freeform/objective, staged clue, app-guided, and host-optional patterns using inspectable rules/previews and player reports. Map failure modes and what evidence supports each. Output: `research/experience/mechanics.md`.
- [ ] **M05 — Delivery and economics.** Verify current download prices, print quantities and assembly, fulfillment quotes, platform fees, refunds, video/tool costs, and app maintenance assumptions. Build low/base/high scenarios with explicit units, gross, variable costs, labor, acquisition, and contribution; keep lifetime observations separate from annual forecasts. Output: `research/market/economics.md` and reproducible model.
- [ ] **M06 — Synthesis.** Reconcile conflicting evidence from M01–M05, state what is known and unknown, and update the one-minute README. Gate 1 decision: proceed, revise scope, or stop. Output: `research/DECISION.md`.

## Concept and game

- [ ] **C01 — Broad concepts.** Generate divergent settings and mechanics, screen for obvious comparables, and select finalists by recorded criteria. Include *The Immortality Club* without privileging it. Output: `concepts/longlist.md`.
- [ ] **C02 — Persona challenge.** Have independent perspectives attack each finalist; record concrete objections and the evidence that would resolve them. Interview actual potential hosts/players where possible. Output: `concepts/personas.md`.
- [ ] **C03 — Concept decision.** Pitch the winning concept and alternatives with a falsifiable reason for choosing it. Output: `concepts/decision.md`; Gate 2 review.
- [ ] **D01 — Paper game.** Solution, role and information graph, act timing, host instructions, clue inventory, cancellation handling, and accusation/reveal. Output: playable `game/` packet.
- [ ] **D02 — Simulation dojo.** Encode the game state and heterogeneous encounter/communication policies. Run robustness sweeps, report assumptions and failures, fix brittle clue paths. Output: `simulation/` code and report.
- [ ] **D03 — Human tests.** Recruit varied groups, observe nights, gather anonymous individual responses, revise the packet, and document unresolved problems. Output: `playtests/` logs and Gate 4 decision.
- [ ] **L01 — Commercial experiment.** Produce the chosen format, test listing/discovery, record actual conversion and contribution, and decide whether to expand. Output: `launch/` report.

Tasks may be split into smaller PRs. A task ID is a stable pointer to evidence, not a claim that an agent ran in the background.
