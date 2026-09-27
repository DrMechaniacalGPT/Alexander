# Local mystery simulator

A small Python runner that calls installed Ollama models with a separate context for each participant. Start with the [dialogue-format checkpoint](DIALOGUE.md), then the [strict-output and reasoning-budget checkpoint](REASONING-BUDGET.md), then the [earlier reasoning comparison](REASONING.md) for the latest comparison, and [RESULTS.md](RESULTS.md) for the initial implementation and failures. This is a working experimental instrument, not a calibrated model of party guests.

## Run it

Python 3.10+ on Linux/macOS and an already-running local Ollama service are sufficient. An OS file lock prevents two writers from using the same run directory. No pip dependencies, model downloads, paid API or cloud service are used.

```bash
cd Projects/MurderMystery/simulation
python3 -m unittest discover -s tests -v
python3 -m dojo.runner fixtures/01_exchange.json --out runs/my-first-run --backend stub
python3 -m dojo.runner fixtures/02_private_relay.json --out runs/my-relay --backend ollama --model qwen3.5:9b --context 8192 --max-calls 8 --max-seconds 300
```

A new run directory is required when the scenario, seed or configuration changes. The installed models used in our experiments are recorded in [local-environment.json](local-environment.json); your machine must have the selected model installed. The program does not install it for you.

Each run writes `report.md`, `summary.json`, immutable per-turn request/response journals, events, private per-player inspection files and a budget record. **`complete` means the configured phases executed and outputs passed structural checks. It does not mean the players reasoned correctly or the game worked.** Read the conversations and conclusions.

Repeat the exact command to resume an interrupted run. Accepted turns are reconstructed without further inference. A journaled successful raw response is validated without regenerating it. A failed/invalid attempt is retained; explicit resume may retry, within the original cumulative call/time caps. No automatic semantic repair or silent retries occur. Changing a cap requires a new run directory. To avoid repeating accepted conversations, pass `--continue-from OLD_RUN` with the same case, engine, backend, model and seed. Use `--reuse-turns N` to explicitly reuse a shorter prefix when revising later prompts. This copies only the selected contiguous accepted prefix, revalidates its player messages/actions, and records parent provenance. The old failed run is preserved. Call caps include inherited attempts; wall-time caps apply to the new branch. Reports distinguish inherited turns and new requests. A continuation is not an independent repeat. Repeat the complete continuation command when resuming/replaying that branch.

Add `--replay` to reconstruct a completed compatible run using recorded responses, without contacting Ollama. Replay checks that the current player messages match the recorded ones and revalidates actions; it is not a rerun with the same seed. Schemas may become stricter while recorded messages/actions remain compatible. Historical `0.1.0` trials predate the final-answer contract; some intermediate `0.2.0` trials also predate the current final prompt. They are preserved for audit, not promised compatible with current replay. The latest relay and completed external trajectories were replay-checked. Exact-message validation deliberately rejects incompatible prompt revisions.

## Experimental reasoning profiles

`--prompt-profile grounded-v2` adds evidence guidance and explicit public speaker/audience names. It is an experimental candidate, not a claim of generally better reasoning. `legacy` remains the default; `grounded-v1` is retained for the first recorded comparison and should not be preferred for new public dialogue because its secret-possession guidance is too broad. See [the comparison and limits](REASONING.md).

Use `python3 -m dojo.benchmark --help` for frozen single-turn comparisons and `python3 -m dojo.audit --help` for recorded output-contract checks. Offline rubrics never enter player prompts. Contract checks validate format and citation availability, not the truth or support of a conclusion. Private assessments do not deliver a model's stray `say` field to other players; the audit flags it as a contract failure.

`--strict-output` adds phase-specific schema constraints and independent validation; rejected text stays in the journal. `--thinking` enables supported local model reasoning and needs an explicit output budget. Both are opt-in so historical default payloads and manifests remain compatible. The latest 2,048-token thinking configuration failed during a fresh conversation; see [the budget results](REASONING-BUDGET.md) before running expensive sweeps. Thinking controls are model-specific; our tested installed models report boolean support.

Benchmark calls accept `--context`, `--tokens`, `--thinking` and `--strict-output`. They retain all generated results, mark contract violations, count failures and return a nonzero exit status after a batch with violations. Structural validity is still separate from reasoning quality.

`python3 -m dojo.export PRIVATE_SOURCE NEW_EXPORT` publishes an inspectable copy of original synthetic evidence with model-returned reasoning text omitted and hashed. It retains prompts, speech and private notes; it is not a privacy or copyright sanitizer. Full local journals remain available separately. Export never overwrites its source or an existing destination.

## Incremental fixtures

1. `01_exchange.json`: two players locate an envelope.
2. `02_private_relay.json`: a third player learns through an intermediary, while an unrelated private marker should remain undisclosed.
3. `03_dilemma.json`: Alice can decide how to respond to a challenged alibi and then talk to people affected by it. It is deliberately incomplete as a mystery.
4. `04_selective_disclosure.json`: three volunteers choose what to reveal across changing audiences; an offline rubric distinguishes withholding, self-knowledge, testimony and unsupported discoveries.
5. A private external adaptation exercises a longer sequence. See [external-run.md](external-run.md). Source-owned role/clue materials and reconstructive traces are not in the public repository.

## The model boundary

The context builder supplies only the assigned brief, shared orientation, public cast names, participant policy, and events delivered to that participant. Every request is independent; there is no shared chat history. Case truth and other roles are excluded. Private intention notes are recorded for analysis and **not fed back as persistent plans** in this version. This is an explicit limitation, not a claim to model durable private beliefs.

A speech is a claim. The engine does not treat it as established truth. It validates audience/attendance, schema and evidence IDs, and permits only the current encounter's symbolic actions. Those actions can unlock a phase; there is no general physical-world simulator, inventory trading, combat or automatic promise enforcement. The private external clue hunt tracks unique copies in its adapter and delivers text to discoverers; it does not simulate walking or searching a room.

A participant may have `policy.memory_events` to bound the recent delivered events included in context. The raw history remains inspectable. Other policy text can guide the model but is not a measured personality scale. Initiative-directed approach selection, natural moving groups, persistent intentions and learned behavioral parameters are not implemented.

Context safety uses a conservative UTF-8 byte bound plus template/schema reserve and generation headroom. It rejects oversized requests rather than silently dropping history. This is a capacity guard, not an exact tokenizer count. Actual prompt/output tokens, elapsed time, raw responses and truncation are logged. Local models can still ignore facts, invent claims, or reason badly inside correctly isolated contexts.

## Encounters and transitions

There is **no six-window default**. A fixture declares finite encounters or a random-pair schedule with an explicit window budget. A pair can get several alternating turns; predeclared groups can have explicit speakers. Random matching is a baseline, not a claim about real mingling. Dynamic joins, interruptions and initiative-driven targeting await a useful empirical model.

An optional `transition_after_contacts` trigger ends a scene after a named player has encountered a declared number of distinct partners **in that scene**, or the finite schedule budget ends first. The report records which condition ended it, including an unmet contact target. Being in the audience counts as an encounter; attention and understanding are not inferred. Call/time caps limit computation separately from fictional party time.

Future tests can compare clock-like budgets, coverage thresholds or narrative triggers. Limited coverage might create interesting pressure, but neither its desirability nor a particular threshold has been established.

## External data adapter

`tools/import_movie.py SOURCE_JSON PRIVATE_OUTPUT_JSON` converts checked local data into the first external text adaptation. The JSON input fields are `source`, `public_rules`, `roles` (eight entries with `id`, `name`, `brief`), `clues` (sixteen entries with `id`, `text`, `copies: 3`), `culprit_id`, `host_signal`, and `death_notice`. Original role text must be checked against the source; the generic adapter does not download or redistribute it.

The locally retained extraction script and source hash make our private input inspectable. A third-party user must obtain permitted materials themselves and verify the extraction; free access does not grant a blanket republishing license. Keep outputs under `local-private/` or outside Git. Private reports may reconstruct source material.

## Verification and scope

Tests cover private routing, exact group audiences, absence/late arrival, bounded memory, private final answers, immutable history, invalid actions, visible evidence references, truncation, replay/resume, capped calls, manifest mismatch, scene-specific requirements and transition accounting. They test software contracts; model behavior is checked separately in recorded experiments.

The first implementation intentionally omits an optimizer, scoring model for fun, graphical interface, automatic hypothesis verification and full character editor. Start by inspecting one trace and improving one clear failure at a time.

## Fixed-context diagnostic

`PYTHONPATH=. python3 tools/compare_contexts.py evidence/02_relay_final/turns/t00006.json runs/context-checks.json` makes four bounded calls across two already-installed models. It compares the delivered-report view with a counterfactual that removes other-player reports. Output is preserved without overwriting an existing result. Its protocol check is not a semantic grade; read whether the answer actually states the learned location and attributes the source. No multi-call sample establishes a model ranking.


## Dialogue history and distinct partners

`--prompt-profile dialogue-v1` is an opt-in party-player framing and role-aware history renderer. It includes only that player's delivered observations, makes prior own speech assistant history, labels other speech/actions/deliveries, and supplies the current audience separately. Private intentions and earlier private assessments are not memory. The default legacy payload is unchanged. See [DIALOGUE.md](DIALOGUE.md) for selected improvements and residual failures; do not equate better turn-taking with correct evidence reasoning.

`python3 -m tools.probe_dialogue` compares saved frozen requests with bounded local calls and retained outputs. Its source-derived records must remain private. `python3 -m tools.import_movie PRIVATE_SOURCE PRIVATE_OUTPUT --partners 4` creates an experimental schedule with four distinct partners for every guest; omitting the option preserves the original adapter. `python3 -m dojo.metrics EVENTS --out NEW_REPORT` measures exact same-speaker repeats and conversation opportunities, not factual correctness.
