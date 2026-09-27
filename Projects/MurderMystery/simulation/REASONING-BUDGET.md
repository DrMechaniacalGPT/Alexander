# Strict output and local reasoning budget

**Strict output checking is ready; reasoning mode remains an experiment.** It fixes one private-secret response and avoids one unsupported exoneration in small paired probes, but still invents a favorable motive. In a fresh three-player conversation it exhausts the 2,048-token cap on turn three without answering. The earlier no-reasoning run completes but reasons poorly. Neither result warrants promoting this configuration as a reliable simulator.

This checkpoint contains **24 new local generation attempts**, including one retained truncation; **49 tests pass**. No scenario was rewritten to manufacture success, no model downloaded, and no paid inference used.

## Changes

`--strict-output` constrains phase-specific fields in the generation schema and independently rejects violating responses before the runner applies them. Private assessments require empty speech, no public action and a nonempty conclusion; ordinary speech requires an empty conclusion. Invalid raw output is retained, not rewritten. The deterministic stub renders its scripted fields for each phase; that is fixture generation, not repair of an LLM response.

`--thinking` asks the installed local model to use its reasoning mode. Context and output budgets remain explicit. The thinking flag and strict schema are present in recorded payloads; selected runner options are in manifests. Defaults preserve historical payloads and omit false options from old-style manifests. A continuation cannot silently switch reasoning mode. Internal model reasoning never becomes a player observation, speech, private intention or persistent memory.

The benchmark now records contract violations and reports failure counts even when generation returns successfully. Invalid responses remain in the denominator and are not automatically retried. Identical completed requests are skipped on resume; changed request settings or evaluator specifications require a new directory. The initial eight paired probes predate embedded per-record validation status; a separate contract audit covers them.

## First paired check

Four fixed cases, one model, same `grounded-v2` prompt, strict schema, seed 1, context 16384 and output cap 2048. Only the thinking flag changes. Eight calls, all structurally valid and none truncated. The existing offline rubrics are in `benchmarks/reasoning-budget-v1.json`.

| Case | Reasoning off | Reasoning on |
| --- | --- | --- |
| Private possession without repeating marker | Repeats marker in private note and conclusion | Acknowledges possession without repeating it in any action field |
| Moral choice under incomplete evidence | Declares another person innocent without proof | Avoids that exoneration, but still overstates what the plea reveals about the person's motives |
| Conflicting reports | Identifies contradiction; does not choose a liar | Identifies contradiction and explicitly separates reports from truth |
| Authoritative positive evidence | Gives the justified location | Gives the justified location |

Recorded wall time for these four calls: 35.641 seconds off, 101.068 seconds on. These totals include model loading/cache effects and are not a stable performance benchmark. Greater inference cost must earn its keep through better complete interactions, not merely longer answers.

Evaluate the structured action fields consistently across both arms. The separately returned internal reasoning trace is not player output or proof that a model's explanation is faithful. Raw local traces retain it for debugging; public exports omit that text while retaining its hash/length and the complete action response. Never feed it into another player's context.

## Fresh interaction gate

An independent bounded author froze `fixtures/04_selective_disclosure.json` and its offline rubric before execution. Three music-hall volunteers have different knowledge and reasons to choose limited disclosure. The case has ten speech turns and three private assessments, with changing audiences; it does not hide a solvable culprit or require maximum disclosure to pass.

Run reasoning off/on with the same model, profile, strict schema, seed 1, context 16384, output cap 2048, maximum 14 calls and maximum 900 seconds per trajectory. No scenario changes between conditions. The rubric distinguishes private self-knowledge from legitimate public withholding, testimony from observation, booking from attendance, proposed actions from completed discoveries, and factual fidelity from merely polite conversation.


## Fresh interaction results

- **Reasoning off:** all 13 turns complete, 82.790 seconds of recorded model wall time. Neri publicly names the confidential person but later claims to have withheld that identity. Players confuse the booking interval, actual occupancy, water observation and damage; several address an absent interlocutor. Public evasion was explicitly permitted, but erroneous private accounting and unsupported causal conclusions are separate failures.
- **Reasoning on:** two speech turns accepted, then the third request uses all 2,048 generated tokens in model reasoning and returns no action content. The runner stops with the original failure retained: 3 requests, 186.652 seconds, zero private assessments. The partial prefix cannot establish improved full interaction quality. No automatic retry or enlarged budget was used.
- The original shell command chain ended after the completed off arm, before an on directory or request existed. The on arm was started separately with the predeclared settings; no generation was repeated because of that interruption.

An offline audit covers all 24 attempts: one contract failure, the empty truncated response. Model reasoning never enters a later player's context. Public exports retain exact structured action text and request payloads, but omit the separately returned reasoning field with a hash/length marker. Complete local journals remain under `local-private/reasoning-budget/`. This omission does not redact prompts or private character notes; only original synthetic evidence is exported.

## Supported controls and limits

The installed `/api/show` metadata reports boolean thinking controls for both local models, not named effort levels. We did not invent a numeric reasoning-budget parameter. Ollama documents separate reasoning and final-content fields and model-specific supported values: [thinking controls](https://docs.ollama.com/capabilities/thinking), [chat API](https://docs.ollama.com/api/chat). Our token cap bounded the entire generated response and could therefore leave no final answer; this is directly observed in the failed turn.

## Next useful comparisons

1. Test a declared larger output/per-call budget or the other installed model on the exact failed context before paying for a whole long trajectory. Preserve this failure; an explicit continuation is not an independent rerun.
2. If a small configuration completes reliably, repeat a fresh interaction with alternative profiles/seeds and inspect factual boundaries, meaningful questions and voluntary disclosure separately.
3. Diagnose information coverage independently of inference. The external adaptation goes directly from clue delivery to accusations. An independently reviewed proposal is to preserve the pre-clue trajectory and compare immediate assessment with one additional discussion window. The source does not explicitly require that extra window, so it is an experimental variation, not a claimed correction to the game. See [adaptation review](benchmarks/reviews/adaptation-review.md).

The next milestone is interpretable, sustained conversations under a known local compute budget. It is not merely structural completion or a higher count of correct accusations when required information was never available.

## Run and inspect

```bash
python3 -m unittest discover -s tests -v
python3 -m dojo.benchmark benchmarks/reasoning-budget-v1.json --out runs/budget-probes --model qwen3.5:9b --profiles grounded-v2 --context 16384 --tokens 2048 --strict-output --thinking
python3 -m dojo.runner fixtures/04_selective_disclosure.json --out runs/selective --backend ollama --model qwen3.5:9b --context 16384 --tokens 2048 --max-calls 14 --max-seconds 900 --prompt-profile grounded-v2 --strict-output --thinking
```

The last command reproduces a configuration that failed here; it is not a recommended production setting. Use a new directory for changed settings. Read [the frozen interaction rubric](fixtures/04_selective_disclosure.md), [probe review](benchmarks/reviews/reasoning-budget-review.md), [interaction review](benchmarks/reviews/fresh-review.md), and [contract audit](evidence/reasoning-budget/contract-audit.json). Public original traces are under `evidence/reasoning-budget/`; their export manifest records original and published file hashes.

Verification also replays all eight earlier public trajectories, the new completed trajectory, and the failed run’s accepted prefix (in a disposable copy), without inference. Export hashes remain intact after replay.
