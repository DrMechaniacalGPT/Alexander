# V2 development decision, before execution

V1 fixes the exact old Qwen relay assessment and a fresh relay, but neither profile dominates the small tests. Gemma answers the fixed-context cases more consistently but fails to disclose its known receipt in a live relay; dilemma conversations include parroting another speaker, addressing self, and addressing absent people. V1's universal secret-possession instruction also overreaches into legitimate public concealment.

V2 is a bundled candidate: preserve the evidence guidance, explicitly protect public choice over acknowledging secret possession, and add redundant public self/speaker/audience names with a speaker-boundary reminder. No evaluator answer, hidden role or new memory is added. This does not isolate which component helps. V1 stays byte-compatible for recorded experiments; defaults remain legacy.

Run V2 on all eight corrected development probes plus four already-written holdouts for both models (24 calls), then the original relay (7 calls each). Select further full-run tests based on the results. These are reused development/confirmation cases, not fresh independent validation after seeing V1 outputs. Inspect information, provenance, restraint, output contract, and new regressions. Do not count private diagnostic marker repetition as cross-player leakage.
