# Can an AI playtesting dojo make this a better project?

September 26, 2026. **Decision-stage analysis, not permission to build.** The owner clarified that the present objective is market understanding, player problems, a product direction and a concrete napkin sketch. This memo updates the [earlier discovery decision](DECISION.md); it does not claim a simulator or new game has been tested.

**My recommendation: consider a narrowly scoped game-design test bench, with a simulator as one tool. Do not yet commit to an autonomous society, an “optimal game,” or a video-led business.** The software is feasible. Its incremental value over ordinary editing and simple information-flow checks is unproven. That is the first worthwhile uncertainty to resolve.

## The three bets

| Bet | Assessment now | Evidence needed to advance |
|---|---|---|
| Can we run separate AI players, each with restricted information? | Technically feasible; known architecture and suitable local programming environment | A small run with inspectable inputs, correct routing and reliable action validation |
| Would doing so improve a human party? | Plausible for finding brittle clue paths and confusing incentives; unvalidated for enjoyment or realistic social behavior | Useful findings beyond simpler baselines, followed by human confirmation |
| Would a public account of the work bring paying hosts? | A coherent creative premise, not an evidenced acquisition channel | Audience response, qualified host interest, then actual conversion with content cost counted |

These bets can fail independently. A working simulator can produce a weak game; a good video can attract programmers who never host parties; a good game can sell without simulation. “Do you think it will work?” needs these separate answers.

## What we would actually be building

There are three artifacts: **a human party game**, **a developer tool for testing that game**, and **a public account of the experiment**. The buyer initially needs only the finished party materials. Eight friends would play without eight AI accounts or a live AI host. AI is part of the design process unless we later choose a different product.

The tool would be a Python program on this machine. A rules engine holds the true case, releases clues, controls who meets whom, and records events. Each AI player receives only its role brief and permitted observations. Model calls generate that player's next proposed speech/action. The program routes the speech, checks mechanical actions, and updates the relevant players' records. A separate analysis step looks for problems in the resulting trace. There is no need for eight open ChatGPT windows or eight permanently running models.

**My capability assessment:** I can implement and test that orchestration, isolation, logging, replay and measurement code here. Python 3.12.3 runs in this workspace. Ollama lists three installed local models. A three-call Python probe of `qwen3:8b` succeeded: a separate conversation did not report an undisclosed test marker, then recognized it after explicit delivery. The cold call took 13.036 seconds, including 12.584 seconds loading; warm tiny calls took 0.140 and 0.385 seconds. This demonstrates local inference and basic supplied-context behavior, not realistic player quality or full isolation guarantees. This shell has neither the OpenAI Python package nor an `OPENAI_API_KEY` environment value. That does not establish whether another account/key exists. A hosted-model experiment needs configured access and a spending limit. Local inference is now a demonstrated execution path and my preferred first backend to benchmark, not a proven substitute for every hosted model. No models were downloaded or paid API calls made. [Probe code and results](FEASIBILITY_SOURCES.md) are preserved.

See the [technical sketch](DOJO_SKETCH.md) for a concrete exchange, isolation rules, scheduling choices, model alternatives, costs and effort estimates.

## Does this address actual player problems?

The [review sample](experience/reviews.md) supports investigating preparation, information flow, confusing objectives and different levels of acting comfort. It does **not** establish that interaction complexity is the cause of existing weaknesses. Some problems may be proofreading, instruction design or insufficient human testing. Eight players create many possible histories, but a human designer need not plan each history individually: resilient rules, redundancy and clear goals can simplify the problem.

| Observed or proposed problem | Best first tool | What simulation might add |
|---|---|---|
| A crucial clue has one route | Clue/dependency graph and missing-player checks | Find conversational reasons a route is not used |
| A role has little agency | Role/objective review | Trace whether other agents ever have a reason to approach it |
| A secret destroys an objective too early | Release/goal compatibility check | Explore incentives to disclose early |
| Reading and setup are burdensome | Timed real-host walkthrough | Little; synthetic reading speed is not a human measurement |
| Shy guests feel uncomfortable | Low-pressure design and human feedback | Suggest situations to inspect, not measure discomfort |
| People enjoy the evening | Human playtests | Generate hypotheses, not satisfaction estimates |

Our proposed fixed-solution, guided-mingle format already has close competitors ([Mischief, D036](sources.csv)). The dojo does not remove this commercial objection. It might help us execute better, and it might make the work more interesting to share. Neither is established yet.

## Stronger and weaker versions of the idea

**Strongest version:** a transparent test bench that finds specific, reproducible failure cases, compares fixes and publishes where its predictions fail. That is useful even if the agents are imperfect people. A shared corpus of failure cases, tests and human outcomes could become a reusable asset across games.

**Weakest version:** elaborate personas converse, the same family of models scores their enjoyment, and an optimizer selects the version with the highest synthetic score. That can reward behavior peculiar to the models, especially if they are eager to solve the case or cooperate. More runs would make the wrong model look precise.

A mystery also has competing objectives: fair deduction, suspense, freedom, social participation, low preparation and a satisfying reveal. Maximizing solve rate can make it trivial; maximizing interaction count can produce tedious obligations. “Every interaction matters” should mean players have worthwhile opportunities, not that all 28 pairs must exchange a mandatory clue. We need owner taste and human observations to set those tradeoffs.

## Alternatives worth keeping alive

1. **Game first, ordinary playtests:** most direct route to an enjoyable product, but less distinctive as an AI learning project. Prefer if near-term revenue dominates.
2. **Static checks plus simple simulated information flow:** cheap, interpretable and a strong baseline. It may solve most reliability problems without conversational AI. That would be a useful discovery, not a defeat.
3. **A small hybrid test bench:** use explicit rules for truth/permissions and AI for dialogue choices. Best fit to the owner's learning interests, provided it must demonstrate additional value.
4. **Research/content first:** openly explore agent behavior with a free example; treat audience learning as the immediate output and postpone product income assumptions. Fits the interest in public experiments, but changes the short-term business objective.
5. **A general simulation platform:** premature. Many existing agent systems already cover the basic architecture. Reusable infrastructure should emerge from demonstrated game-specific needs.

I favor option 3 with option 2 as its control, rather than treating “full dojo” as the starting commitment.

## The distribution hypothesis needs its own test

A video can show a comprehensible failure, an attempted fix and what humans actually did. That is a stronger demonstration than claiming a perfect game because artificial players liked it. Research systems and AI mystery projects already exist; the combination is not a verified novelty claim. Our potential distinction is clear explanation and credible evidence of improvement.

The first public experiment would need to be worthwhile even without virality. An illustrative funnel makes the risk visible: 10,000 views × 1% site visits × 2% purchase conversion is **two orders**, not 200. Those rates are invented sensitivity inputs, not benchmarks. A narrower host audience could convert better; a broad AI audience could convert worse. Production/editing time belongs in acquisition cost. The previous $10 CAC assumption does not become valid because distribution is organic.

Opening the method can invite contribution and trust. Buying must still offer convenience and quality: a checked, attractive, ready-to-host package, or later physical fulfillment. We have not selected a license or free/paid content boundary. A code enthusiast and a party host are different audiences; track each separately. Public branding should stand alone, without Alexander positioning, as the owner requested. Public repository/link choices would need to reflect that before a campaign.

## Proposed next decision, before construction

Agree on this bounded research question: **Does isolated-agent dialogue reveal actionable game-design failures that cheaper static checks and rule-based agents miss?** A planted failure alone would only test the plumbing. A useful evaluation also needs clean controls, withheld failure cases, more than one behavior policy and explicit false-positive counts. The [sketch](DOJO_SKETCH.md) specifies a staged experiment and stop rules.

A demo might take roughly 4–8 focused engineering hours after access is ready; a usable eight-player research harness is more plausibly 16–36 hours total, before a finished game. These are low-confidence planning estimates with a work breakdown, not measured Codex completion times. Human calibration and a finished, saleable game require further iterations and scheduling. Do not reuse the old 120-hour commercial scenario as an estimate for this larger scope.

At this gate we need not settle every persona, model or theme. The remaining owner choices are whether the near-term deliverable is primarily a game or a public research experiment; whether this narrower test bench captures the interesting part; and what bounded investment would be worth making. Model quality, predictive usefulness and audience conversion are empirical questions. Further confident prose cannot answer them.
