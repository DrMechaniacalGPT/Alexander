# Evidence-reasoning probes

These are original synthetic diagnostic situations, not party scenarios or a standardized measure of human behavior. Rubrics stay outside model contexts. A pass means only that a specific output satisfies a narrow criterion; models can fail complete conversations despite passing isolated questions.

- `evidence-v1.json`: original eight-case specification. Two cases had inconsistent cast names.
- `evidence-v2.json`: corrected cast names for conflict and choice. The other six cases are unchanged.
- `cast-correction.json`: just those two cases, for four replacement Qwen generations. Original pilot outputs remain recorded and are excluded from the corrected comparison.
- `holdout-v1.json`: four changed/new cases written before their first execution. They are no longer untouched holdouts for V2 development.
- `PLAN.md`: initial bounded plan, including the intended comparison rather than a retrospectively rewritten success story.
- `v2-plan.md`: rationale recorded before running the bundled identity/secrecy-scope candidate.
- `reviews/`: independent qualitative readings, including ambiguities and negative results. Temporary absolute paths in the original reviews identify the working copies; committed traces live under `../evidence/reasoning/`.

The first collector did not persist a separate rubric manifest; input files and raw payloads are retained. The revised collector writes an immutable `evaluation.json` containing the complete offline cases and selected profiles, rejects changed rubrics, reserves requests before inference, and does not silently retry failed reservations. Do not relabel old records as having protections added later.

Inspect the entire response, not only `conclusion`: a private note can reverse the source and beneficiary of a fact, or a stray `say` can invent an action even though the engine never speaks it. Citation availability is a software property; whether a cited statement actually supports the conclusion requires a separate reading. See `../REASONING.md` for decisions, caveats and commands.
