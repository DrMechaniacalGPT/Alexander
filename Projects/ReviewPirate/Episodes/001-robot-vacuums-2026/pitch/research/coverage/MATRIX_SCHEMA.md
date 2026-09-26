# Corrected matrix schema and integration proposal

`source_product_matrix_v2.csv` is a 64-row replacement candidate for the **eight-source core display**, not for the entire inherited CSV containing other creators. Do not overwrite the larger ledger and lose supplementary sources. It was derived from `coverage_audit.csv` using `build_matrix.py`; that script rejects unknown input states rather than inventing display semantics.

## Fields that change the meaning

- `coverage`: substantive / guide / related_variant / mentioned / test_reference / unknown. Reserved `explicit_not_tested` requires a cited statement and bounded scope. Blank is never a negative result.
- `direction`: not_assessed throughout this audit. A located review does not establish an overall endorsement. Verdict and recommendation are separate claim-level work.
- `access_level`: direct_page versus indexed text versus bounded_search. Page access is not epistemic confidence.
- `model_match`, `tested_product`: distinguish the target grid model from the unit actually reviewed. Pro/Max and E25/E28 cannot silently merge.
- `page_type`, `testing_evidence`: a roundup with firsthand test notes differs from a standalone review and from a bare rank/spec summary. Neither page type alone establishes test rigor.
- `coverage_scope`: publisher_archive. `article_cohort` holds a specific comparison cohort where applicable. Historical and current cohorts are not silently combined.
- `observed_at`: when we checked, not when testing happened. `time_scope` remains in the detailed audit until exact publication/test/update dates are individually normalized.
- `independent_test_id`: known shared test cohort, currently populated for HookUp. Empty means unresolved, not independent. Do not count empty IDs as unique tests.
- `claim_locator`: readable section pointer; no brittle tool-only reference IDs required.
- `noncoverage_scope`: mandatory for any future explicit negative, e.g. this article's seven-model cohort; never the whole publisher without support.

The CSV is intentionally not a pooled performance-score table. Numeric test results belong in a separate measurements ledger with units, surface, debris, load, passes, power, path settings, firmware, date and test family. Locked or extraction-placeholder numbers must not become scores.

## Renderer integration

Show all eight core sources and eight target models explicitly. Use separate glyphs for full test/review, roundup, related variant, mention and unknown; do not substitute blank. Preserve the distinction in the legend and accessible text. Validate duplicate keys and reject unmapped publishers rather than silently dropping or overwriting records. For broader creator coverage, render a separate appendix or explicitly broaden the source allowlist.

Never title this figure 'who tested what' unless its cells genuinely denote firsthand testing. A safer title is 'What coverage we located', with tested-unit information on hover or in a notes column. The current guide rank can be a separate dated annotation, not a winner-colored cell that overwrites underlying evidence.

## Checks run

`python3 test_matrix.py` passes seven tests: 64 unique pairs; unknown cannot convert to not-tested without evidence; TechRadar Pro cannot become Max; RTINGS E28 remains distinct from E25; duplicate records rejected; V70 roundup not full review; two HookUp products share one comparison ID. These guard the actual inherited failure modes. They do not certify external article accuracy or replace claim review.

## Hardened validator update

The initial seven-test audit helper has been hardened after independent review. Twenty-four tests now pass in normal and optimized Python. Validation uses explicit exceptions, requires all64 expected pairs, and checks source/product allowlists, schema fields, access/page/evidence states, ISO date, evidence URL/locator, and tested-variant relationships. This validator is deliberately scoped to the fixed core grid; it must not be used to reject supplementary sources in a broader ledger. `explicit_not_tested` remains a reserved future concept and is now rejected by both transform and validate; no current row supplies evidence for that state. Known tested variants are allowed only for their audited source-target relation. Output CSV is unchanged.
