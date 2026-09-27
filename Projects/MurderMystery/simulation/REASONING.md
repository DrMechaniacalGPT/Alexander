# Factual recall and evidence reasoning

**Follow-up:** [Strict output and reasoning budget](REASONING-BUDGET.md) adds output enforcement and records the next bounded experiment, including its truncation failure.

**We improved the small relay, but have not solved full mystery reasoning.** Explicit evidence and speaker cues let both local models carry a receipt location through a complete conversation chain. In the longer existing-game adaptation, the revised Qwen configuration still produced **0 correct accusations out of 7 nonculprit players**. Keep using this as an experimental instrument; do not use its outcomes to rank game quality yet.

This checkpoint adds reproducible probes, opt-in context profiles and stronger audit/review tools. It records **218 new local generation calls**: 84 single-turn probes (including four excluded pilot outputs), 92 turns across eight original synthetic trajectories, and 42 turns in one private external trajectory. **40 software tests pass; all nine complete trajectories replay without inference.** No model was downloaded, paid API used, or third-party packet published.

## What changed

- `legacy` preserves the previous prompt and remains the default for compatibility.
- `grounded-v1` adds evidence guidance. Retained for reproducing the first comparison; its universal instruction to acknowledge secret possession is too broad for public play.
- `grounded-v2` protects the player's choice over acknowledging secrets in public and adds redundant public identity cues. It does not expose hidden roles, truth, evaluator answers, other people's private notes, or undelivered events. V2 bundles these changes; results cannot identify which component helped.

The benchmark freezes explicit role knowledge, received observations, the question and an offline rubric. It uses the actual runner prompt and output schema. Human-readable judgments distinguish information use, provenance, inference restraint and instruction compliance. No automatic semantic score claims that a syntactically valid citation supports its conclusion.

## Findings already established

| Check | Observation | What it supports |
| --- | --- | --- |
| Exact previously failing relay context | Qwen legacy denies knowing the location; V1 names cabinet 4 and its source chain in the conclusion. But its forbidden, unused `say` field invents having found it. Removing the incoming report leaves both uncertain. | Better recall in one field, **not an overall passing response**. |
| Eight small cases, two profiles, two models | No profile uniformly wins. Qwen V1 improves one secondhand report but still invents exoneration; both models mishandle a private instruction not to repeat a marker. | Keep negative results; do not promote the prompt as a general reasoning fix. |
| Four changed/new cases with a different seed | All baseline/V1 configurations accept an explicitly authoritative inventory rather than defaulting to uncertainty. Qwen V1 introduces a contradictory yes/no answer and speaker confusion. | Some justified certainty is retained, but extra guidance can regress. |
| Full original relay | Qwen V1 and V2 convey cabinet 4 through Ari → Bea → Cal. Gemma legacy does not disclose the known location; Gemma V2 does relay it. | Improvement transfers beyond a supplied final-question snapshot in these single trajectories. |
| Full Gemma dilemma, legacy/V1 | Legacy has polite but unproductive exchanges. V1 includes speaker copying, wrong addressees and an invalid inference that medicine delivery contradicts someone else's being alone. | Fixed-question competence does not establish interactive competence. |

V2's full dilemmas still fail in ways the receipt task cannot reveal. Qwen rationalizes kindness into a changed history, confuses Bob with Daniel, and asks about a delivery its own role performed. Gemma keeps the donation unresolved and permits withholding, but Alice once addresses an absent Bob. Explicit names help some samples; they do not solve identity or social reasoning.

The automated audit of the 176 public generation attempts found two final responses with nonempty `say` fields. The runner recorded their private conclusions and **did not deliver those strings as public speech**, so this is not a routing leak. It is a gap between the instructed output contract and the runner's structural acceptance. Both occurred with V1; one also invented a search in the unused field. Inspecting only the final conclusion would overstate improvement. A future change should constrain these fields at generation and validation, retaining old failures rather than silently repairing them.

A model may reasonably report hearing a location while remaining unsure whether it is true. Conversely, saying nothing was heard when a report is present is a recall failure. We do not require all testimony to be trusted or all secrets to be disclosed.

The synthetic marker never reaching another participant is a routing property. Repeating it in a private diagnostic despite “do not repeat its value” is an instruction failure, not cross-player disclosure. Denying possessing it in an ordinary roleplay assessment can also be ambiguous between concealment and failed self-knowledge; the explicit private diagnostic is needed to separate these interpretations.

## Transfer to the existing scenario

The unchanged private adaptation ran from scratch with Qwen, V2, seed 17, context 16384 and output cap 768. All 42 turns completed in 289.755 seconds of recorded model wall time. Nonculprit outcomes: **0 correct, 5 wrong, 2 abstentions**. The culprit's self-accusation is excluded because its own card contains privileged solution knowledge. There were no output-contract failures; one private-note field reached its schema limit.

The earlier concise run had 0 correct, 6 wrong and 1 abstention; the earlier reminder variant had 1 correct and 6 wrong. These are single trajectories, not a success-rate estimate. The new full run changes the prompt throughout, which changes conversations and therefore later information; earlier historical speech also used different output bounds. It is not a clean final-reasoning-only intervention. The case and schedule stayed fixed, and all original/private source materials stayed outside Git. See [aggregate metadata](evidence/reasoning/external-transfer.json) and [adaptation limitations](external-run.md).

Failures include inferring personal traits from a profession, confusing related but different preferences, treating unknown attributes as absent, and inventing supporting statements. These are simulator/inference failures, not evidence that the source game is poor. Better receipt recall is insufficient for the richer task.

## Method and limitations

All generation is local, using already-installed models. Fixed probes use context 8192, output cap 768, temperature 0.7, seed 1 for the eight development cases and seed 2 for four changed/new cases. Model digests and server version are recorded in `evidence/reasoning/environment.json`. Full runs record their own configuration. Matched profiles share the same supplied case but prompt changes can alter random-number consumption; equal seeds do not produce matched stochastic paths.

Two pilot cases had inconsistent cast names. Their original four outputs remain in `qwen-seed1` but are excluded from the main comparison, replaced by `qwen-corrected-seed1`. Six unaffected cases are unchanged. Gemma uses the corrected specification throughout. The original and corrected JSON files are retained. The first probe collector recorded payloads but lacked a separate evaluator manifest; later runs freeze the complete offline specification too and reject rubric-only changes. Existing pilot records are not retroactively presented as having that protection.

V1 guidance was informed by the known failures and closely states desired development behavior. The four additional cases were written before inspecting their outputs. Once inspected, those cases became development evidence for V2, not an untouched validation set. One result per configuration is not a calibrated success rate. Independent qualitative reviews retain ambiguous judgments and examine private notes as well as conclusions.

The frozen relay control removes the one final incoming report while retaining the player's preceding question. The reusable tool rejects multiple incoming events or later self-echoes. Removing a report does not in general erase all knowledge: retained earlier speech must still be inspected. This particular retained question contains no receipt location.

## Reproduce

```bash
python3 -m unittest discover -s tests -v
python3 -m dojo.benchmark benchmarks/evidence-v2.json --out runs/probes --model qwen3.5:9b --profiles legacy grounded-v2
python3 -m dojo.benchmark benchmarks/holdout-v1.json --out runs/changed-probes --model qwen3.5:9b --seed 2 --profiles legacy grounded-v2
python3 -m dojo.runner fixtures/02_private_relay.json --out runs/relay-v2 --backend ollama --model qwen3.5:9b --context 8192 --tokens 768 --max-calls 8 --max-seconds 300 --prompt-profile grounded-v2
python3 -m dojo.audit evidence/reasoning --out runs/contract-audit.json
```

Use a fresh output directory for changed settings. Probe collection locks its output directory, saves the evaluator specification outside model input, reserves each request before generation and retains exceptions. It skips completed identical requests but refuses to silently retry an interrupted or failed reservation. A recorded response still needs contract and semantic review.

## Next evidence gates

1. Constrain private/final output fields in the generation schema and validate them without silently repairing responses. Preserve old journals and explicit compatibility rules.
2. Test whether the installed model's reasoning mode helps on the difficult frozen cases, with matched settings and explicit local call/time/token caps. More prompt instructions alone have not solved the problem.
3. Before personality or scheduler sweeps, use fresh multi-turn cases that distinguish voluntary withholding from forgetting, and require pursuing an unanswered question rather than polite repetition. Test whether conclusions cite supporting statements, not merely visible event IDs.
4. Keep human playtesting separate. These traces can expose simulator failures and possible design vulnerabilities; they cannot diagnose the source game's quality or predict player enjoyment.

## Inspect the evidence

- [Original Qwen review](benchmarks/reviews/qwen-review.md), [second-model/changed-case review](benchmarks/reviews/confirmation-review.md), [V2 review](benchmarks/reviews/v2-review.md), [full-transfer review](benchmarks/reviews/transfer-review.md).
- [Probe specifications and provenance](benchmarks/README.md), [public output-contract audit](evidence/reasoning/contract-audit.json), [recorded local environment](evidence/reasoning/environment.json).
- Complete original synthetic request/response journals are under `evidence/reasoning/`; private external traces remain in `local-private/movie/reasoning-v2-seed17/`.
