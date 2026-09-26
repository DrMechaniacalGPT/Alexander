# Independent fact/promise review

September 26, 2026. Reviewed `NARRATION_DRAFT.txt`, `ART_DIRECTION.md`, supporting editorial ledgers, and `build_matrix.py`. This review identifies actionable issues; it does not replace the research or rewrite shared files.

## Narration

### High — the 92% statistic has an ambiguous model referent

`NARRATION_DRAFT.txt:1–3`: the last named model is Q7 M5, followed immediately by Vacuum Wars' 92% statistic and “Same model.” That statistic belongs to **Saros 10R**, as editorial E03 and the original review establish. A listener can reasonably assign it to Q7 M5. Begin the second paragraph with “Take the Saros 10R…” or another explicit model identifier. An on-screen model name helps, but the spoken sentence should survive audio-only listening.

### Medium — opening recommendation sounds broader than the research

Line1 says “Mostly hard floors? Start with the Saros 10R.” Supporting evidence is a conditional premium shortlist based on RTINGS and other tests, not a market-wide finding that every mainly-hard-floor household should start there. Price, space for the dock and the user's priorities matter. Add a brief qualifier such as “For a premium option on mostly hard floors…” and present it as a starting point, not the uniquely best match. Keep the immediate recommendation; do not bury it in caveats.

The Q7 M5 opening is better bounded (“basic cleaning”, clear clutter, manual emptying), and its support extends beyond the 64-cell grid via editorial E11/E12/E21. It is not unsupported merely because the grid omitted it. However, “for less” is relative and time-sensitive; refreshed owner-facing price observations support it today, not indefinitely.

### Medium — dated cohort needs a visible date, preferably a spoken one

Line7 correctly identifies seven robots and double weighting, but “It wins” can sound like an ongoing current crown. “In The Hook Up's April comparison…” would establish that scope without adding a methods lecture. At minimum put April2026 next to the attribution. The observed current-market guide is a different object from the fixed April cohort.

### Medium — caller-directed source retrieval underdelivers the synthesis promise

Lines15 and19 ask the viewer to find a maintenance video/open the linked test. The episode's value proposition includes reducing that burden. Supply model-specific source destinations in the final description and ideally a short “watch this section” cue; if exact timecodes have not been checked, do not invent them. This is an execution requirement, not a reason to remove source referrals. Avoid making an audience do the unresolved research on which the recommendation itself depends.

### Low — promise of three checks is not clearly signposted

Line1 promises three checks, while the rest moves through test disagreement, weighting/obstacles, disputed mopping, maintenance and a budget return. The intended three are recoverable, but the viewer has to assemble them. Use light verbal or visual labels for test relevance / tradeoffs / upkeep. This improves clarity without turning the video into three static slides.

### Claims that appropriately survive scrutiny

- The script does not average incompatible tests.
- Mopping conflict is acknowledged rather than explained away; dates/messes are explicitly hypotheses.
- Curv2Flow 2/6 is attributed to the same comparison as its overall result, avoiding a universal obstacle score.
- The maintenance discussion is model-specific, and the Q7 base/Plus distinction is retained.
- “The evidence is less settled” remains an editorial synthesis, not a proven causal explanation. Its proximity to the later specific conflict keeps it defensible.
- The script avoids the inherited V70 full-review/ranking-history problem and TechRadar Pro-to-Max error.

## Art direction

### Medium — source attribution over a generated macro can still look like test footage

`ART_DIRECTION.md:47,65` requires credit near claims and labels illustration, but the production rule is not precise enough for the numerical hair example. A photoreal carpet macro plus “Vacuum Wars 92%” can imply the generated scene illustrates that actual measured setup/result. At each such shot, visibly label **Illustration** and keep it separate from the source-result graphic. Show no generated before/after pickup, moving measured debris, or named robot completing the claimed test. The direct source clip, if used, needs separate provenance/usage review. A disclaimer hidden in the description is inadequate to clarify the on-screen scene.

### Low — opening product identity must remain clear when the prop is unbranded

The visual bible intentionally uses an unbranded graphite robot, but the voice immediately recommends a named model. Do not frame that prop as a product beauty shot under the Saros name. Use exact approved product imagery for product identification or make the unbranded illustrative status unambiguous. Otherwise the film can imply appearance/features it has not preserved.

The remaining art-direction promises are appropriately bounded: stills do not prove motion; otter preference is creative judgment; optical language is composition guidance; the liked thumbnail remains unrecovered rather than falsely replaced; the maintenance joke excludes plumbed docks. No unsupported audience-success claim found.

## Matrix code

The current code is an audit helper with useful semantic tests, not yet production validation. No current CSV corruption was found. The following failures were reproduced against the helper without modifying shared files:

1. **High if reused in production — assertions disappear under optimization.** `build_matrix.py:24–37` uses `assert` for all validation. Running under `python3 -O` accepted a made-up coverage state and winner direction. Replace with explicit exceptions for production, preserving asserts only in tests.
2. **Medium — partial/empty matrices accepted.** `validate([])` and `validate(rows[:1])` return true. The test suite checks the current fixture length, but the production function does not require the expected publisher/product cross-product. Add expected-set validation at the core-matrix entry point; keep a separate validator for a broader ledger.
3. **Medium — related variant can omit the actual tested model.** Line31 only checks inequality. Empty `tested_product` is different from E25 and therefore passes. Require a nonempty tested-model identifier plus recorded relation, and keep the exact-vs-related restriction.
4. **Medium — unrecognized publisher/access values accepted.** An invented source name and `access_level='fabricated'` pass. Validate enumerations and configured source/product identities before a renderer can drop or mislabel them. Do not infer direct access or testing from arbitrary strings.
5. **Low — explicit negative is reserved but not transformable.** `validate` accepts `explicit_not_tested`, while `transform` has no matching input state. This is currently safe because no row claims it, but future integration should either implement the state with evidence/scope requirements or remove it from the accepted enum until supported.
6. **Low — independent-test identity is deliberately incomplete.** Empty IDs must not be counted as independent tests. No current function does this, but a dashboard must not equate 28 located reviews with 28 independent test systems. Most grouping remains unresolved outside HookUp cohorts.

Recommended report phrasing: “Seven regression checks pass for the current audit dataset; production validation remains to be hardened.” Do not say the pipeline prevents every variant/coverage mistake or that these tests verify article truth.

## Validator repair completed

The integrating agent authorized repair after this review. `build_matrix.py` now uses explicit `ValueError`s, requires the exact64-pair Cartesian product, validates fields/enums/dates/URLs, and requires nonempty known tested products plus an audited variant relation. Unsupported explicit negatives are rejected by both transformation and validation until an evidence-backed implementation is added. Twenty-four tests pass under both ordinary Python and `python3 -O`; the existing CSV matches the validated derivation and was not changed. The preceding code findings describe the reviewed pre-repair version, not outstanding failures. External article truth and unresolved test independence still require editorial review.
