# Discovery and build plan

## Decision gates

| Gate | Question | Evidence needed | Output |
| --- | --- | --- | --- |
| 1. Market and experience | Is there a real buyer problem worth solving? | Seller map, format comparison, sampled buyer/player feedback, grounded revenue scenarios | Short business and experience brief; proceed, revise, or stop |
| 2. Concept | Which setting and mechanics best fit that problem? | Broad concept set, comparable titles, persona critique, feasibility scores, counterarguments | One concept pitch plus rejected alternatives |
| 3. Paper prototype | Does the mystery work as a game? | Causal solution, clue graph, role objectives, timing, cancellation variants, simulation stress tests | Complete playable packet |
| 4. Human playtest | Is the night fun and fair for different players? | Multiple independent groups, host preparation logs, player surveys and debriefs, observed interaction paths | Revised game and decision to produce |
| 5. Commercial test | Will strangers find and buy it at viable cost? | Real listing traffic, conversion, refunds, production time, paid unit economics | Launch, change offer, or stop |

No gate is satisfied by a polished narrative about how the game *ought* to work.

## Gate 1: research in parallel, synthesis afterward

Start with the tasks in [TASKS.md](TASKS.md). Search seller catalogs and prices; independently study YouTube demonstrations and discussion, Reddit/other community accounts, retailer and marketplace reviews, published game rules or previews, and delivery economics. Preserve search strings and sampled material. Each task produces a short finding and a source trail. Then compare the evidence across tasks, especially when hosts and players disagree.

Use breadth targets to avoid anchoring on the first few sellers, then continue until new passes stop changing the taxonomy or leading objections. Record uncovered channels and inaccessible data. A search result count is not a market size.

The commercial model must distinguish lifetime shop sales from annual demand, gross sales from contribution, games from adjacent products, and observed data from scenarios. For example, 14,456 sales at $40 would be $578,240 gross **if** every sale were that product at that price; the earlier Etsy number cannot support that assumption or an annual revenue claim. Model a range of title-level units and acquisition costs with traceable inputs. Report what cannot be estimated.

## Gate 2: concept selection

Generate a broad candidate set before scoring favorites. For each finalist, define the premise, who wants to attend, what guests do during the evening, distinctive physical evidence, comparable products, production burden, and likely objections. Evaluate from at least these perspectives: first-time host, experienced host, enthusiastic actor, reluctant actor, puzzle solver, social guest, player with a peripheral role, and a group with a late cancellation. Persona reviews generate questions; customer feedback adjudicates them.

Keep *The Immortality Club* in the set, not at the top by default. Revisit the download/box/app/video mix only after the format research and host workflow are clear.

## Gate 3: design and model

Write the true event timeline and unique solution first. Map what each role knows, wants, can reveal, and can infer by act. State what evidence reaches everyone and what depends on conversation. Test the distinction between **individually solvable**, **collectively solvable**, and **only solvable after the reveal**. The last is a failure unless deliberately chosen and honestly sold.

Build a simulation dojo only when the paper design supplies precise inputs. Give agents private dossiers and varied policies for disclosure, deception, attention, trust, and off-topic time. Vary encounter graphs, talk duration, cancellations, and willingness to follow prompts. Measure information reach, role participation, accusation paths, and solution robustness across many runs. Include an oracle check that the clue set logically distinguishes the culprit. Models can expose brittle paths; they cannot measure delight, embarrassment, chemistry, or perceived fairness. Human playtests decide those.

## Gate 4: observe actual people

Run distinct groups with different hosting experience and mixes of acting/puzzle interest. Log preparation time, stalls, clue circulation, who was left out, accusations before and after the reveal, and whether players felt their actions mattered. Ask separately whether the solution felt earned and whether they enjoyed the evening. Revise and repeat until the serious failure modes stop recurring; do not declare success by counting playtests alone.

## Gate 5: sell carefully

Prototype the lowest-friction delivery that preserves the party experience. Test invitation/onboarding video and shared audiovisual cues as optional treatments, with a paper path. Compare print-at-home assembly burden with a fulfilled kit before investing in inventory or an app. A YouTube explainer can be tested as discovery content, but its views are not purchases.

## Working rhythm

Use small PRs: plan; research task or coherent group of tasks; market/experience synthesis; concept decision; paper prototype; simulation; playtest revisions. The PR description states scope, evidence added, conclusion changed, and open questions. The project README stays short and current. This plan can change when the evidence demands it; record the reason in the diff.
