# Independent open-book diagnostic review

Reviewed structured answers and visible requests in `iteration-openbook/{gemma4,qwen3.5}.json` and `iteration-openbook-thinking/gemma4.json`, under the private movie simulation directory. Native thinking was not inspected.

## Input integrity

All three requests contain the same reference: exactly 73 attributes matching the frozen inventory, plus 11 distinct collected clue types. Each request has only system/user messages and an empty observations list: earlier conversational history is absent. The participant's own original brief remains, including its own nonculprit information; other players' private briefs and culprit assignments are not supplied. No explicit answer label or answer-bearing confession was found. This is intentional authoritative access to all listed personality attributes, not a test of what an individual actually learned through play.

The normalized inventory is not perfectly literal source text. In particular, one history paraphrase can blur avoidance of an event with departure after it occurred. That ambiguity is inherited from the frozen inventory and should not be mistaken for a new model error. Another relationship description strongly suggests an unmarried status but does not explicitly state it. These limits matter when evaluating absolute claims that every constraint has been independently verified.

## Results

- **Gemma without thinking: abstention with a concrete reasoning error.** It invents a negative family attribute for a candidate whose family status is unspecified. Its examples of exclusions do not demonstrate that every candidate fails. It does not meaningfully evaluate the most strongly supported candidate despite the compact board.
- **Qwen: correct best-supported name, overclaimed completeness.** The listed positive matches and specific negative-possession deductions are supported by the board. The marital-status match is an inference from the relationship description, not an explicit board fact. It also reports 12 clues when the reference contains 11. A best-supported selection is defensible; claiming that all constraints explicitly verify one unique candidate is too strong. At least one alternative has substantial unknown attributes, so missing information must not be treated as exclusion.
- **Gemma with thinking: correct best-supported name, similarly overstated universal match.** Its concrete listed positive traits and broad absence-of-pets claim are supported. Its blanket claim to match all constraints silently inherits the marital-status inference and does not establish exhaustive exclusion of every incompletely described alternative. The stated matches are substantially better than the non-thinking answer, but this one comparison does not establish a general improvement.

Empty evidence arrays are appropriate to this board format: the request has no observed event IDs to cite. They are not evidence of ignoring the board.

## Adjacent targeted checks

The `iteration-notebook/t00150.json` answer selects the correct best-supported candidate using three publicly disclosed, source-consistent positive traits. This supports a local improvement in retrieving useful facts. Its exclusion summary is terse; keep its strongest-candidate framing distinct from an exhaustive proof.

The `iteration-qwen-final-fast/qwen3.5-ownership.json` answer also selects the correct candidate using delivered positive/status reports. However, it claims every other player has been eliminated, which the visible history does not establish for candidates with remaining unknown facts. Its named matches are supported; its uniqueness claim is not.

The board removes much of the memory and conversational contamination burden. The remaining mistakes therefore include constraint interpretation and calibration, not merely absent information or long-history retrieval. These selected probes support further diagnosis, not a general solve-rate or model-ranking conclusion.
