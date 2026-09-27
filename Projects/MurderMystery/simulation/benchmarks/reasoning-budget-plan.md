# Second checkpoint: strict output and reasoning budget

The previous checkpoint found two private assessments with nonempty speech fields and persistent unsupported reasoning despite longer evidence prompts. Fix the structural gap independently of semantics, then test a different inference configuration instead of adding more instructions.

Implementation: opt-in strict output schemas and validation; optional local thinking mode; all selected settings recorded in manifests/payloads. Defaults remain byte-compatible for legacy replay. Reject invalid output without editing its text. Keep model internal reasoning out of player speech and subsequent context.

First paired experiment, frozen before execution: Qwen3.5:9b, grounded-v2, strict output, context 16384, max output 2048, seed 1. Same cases/settings with thinking false versus true. Four existing cases: moral choice, private secret diagnostic, changed-name contradiction, authoritative positive evidence. Eight calls maximum, timeout 120 seconds each. Compare all final fields against the existing rubrics, record truncations and runtime; do not treat longer reasoning as proof of better reasoning. If output cap is inadequate, retain failures and explicitly predeclare a bounded follow-up rather than silently increasing it.

If there is a useful result, confirm on fresh multi-turn situations and a complete small fixture before another external scenario. No downloads, paid inference, source-scenario edits or broad personality sweeps.
