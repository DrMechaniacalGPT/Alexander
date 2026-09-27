# Coverage audit — September 26, 2026

A bounded discovery audit of all 64 pairs in the inherited eight-publisher/eight-product grid. This is coverage discovery, not 64 complete review audits. Every pair received the exact query recorded in `coverage_audit.csv`; 64 queries ran in 16 groups of four. Additional shortened-name searches and direct page/link checks resolved several results. Search results were inspected, including irrelevant variants. No unsuccessful search establishes that a publisher did not test a product.

## Result

28 exact-product review/comparison pages located, one exact-product test table, three guide entries, two related-variant entries, two mentions, one retrospective assertion of testing, and 27 unknown cells. `indexed_review_text` means the search tool returned original-publisher review text, not a separate full-page audit. `direct_page` means that page was also opened. These are evidence-access levels, not quality scores. No cell is marked not tested.

The inherited 15/64 occupied grid substantially understated coverage. Several blank cells are readily discoverable reviews. It cannot support a narrative that reviewer disagreement largely comes from different tested candidate sets.

## Corrections that affect the video

1. **RTINGS does have an X60 Max review.** [Direct page](https://www.rtings.com/robot-vacuum/reviews/dreame/x60-max-ultra-complete) reviewed July24 2026, writing modified August12, methodology v1.0. Other model pages show v1.1; do not combine raw ratings as though test versions match. Public extraction shows locked/0.0 placeholder scores, which must not enter data.
2. **TechRadar's X60 Pro is not a verified Max test.** [The reviewed article](https://www.techradar.com/home/robot-vacuums/dreame-x60-pro-ultra-review), price/availability section, expressly describes the US Max as a somewhat different variant. The legacy Max row must be replaced by related-variant status, even though launch reporting on Max exists. Do not propagate the source's apparent suction-number typo.
3. **Vacuum Wars covers much more of this grid.** Newly located exact Curv2Flow, E25 and Shark UVReveal reviews, and a Qrevo Curv test table. [Curv2Flow](https://vacuumwars.com/roborock-qrevo-curv-2-flow-review/) is notably critical of mopping. This is a real opposing result worth case-level reconciliation, not a missing candidate. [E25](https://vacuumwars.com/eufy-e25-omni-robot-vacuum-review/) supplies another independent test family for the value option.
4. **HookUp's historical tests matter.** [2025 comparison](https://www.thesmarthomehookup.com/test_install/ultimate-robot-vacuum-and-mop-comparison-2025/) includes Saros10R; [2024 comparison](https://www.thesmarthomehookup.com/2024-ultimate-robot-vacuum-and-mop-comparison/) includes S8MaxV. Neither belongs to the 2026 seven-product cohort. Publisher-wide coverage and a particular comparison's candidate set are different fields.
5. **E25 versus E28 needs careful handling.** [RTINGS E28 review](https://www.rtings.com/robot-vacuum/reviews/eufy/omni-e28-robot-vacuum) says it bought E28 and describes E25 as effectively the same robot with a different dock feature. Preserve this as related-variant evidence, not a directly tested E25.
6. **Shark is not an isolated WIRED curiosity.** Exact Shark UVReveal reviews located at Vacuum Wars, TechRadar, Tom's Guide and Expert Reviews; Good Housekeeping also includes it in a mop guide. This supplies a much better route to adjudicating its strengths than framing WIRED's preference as inexplicable.
7. **Tom's Guide has Saros10R, Curv, Curv2Flow and Shark tests as well as X60.** Its Saros headline emphasizes pet hair, a useful challenge to RTINGS' carpet-pet-hair caveat. Do not assert a contradiction until surfaces, hair type, settings and methods are matched.

## Query and selection limits

Exact names can miss differently punctuated or shortened titles; even supplemental searches did not exhaust publisher archives or YouTube. Expert Reviews' first four exact queries returned no results; shortened-name searches remained inconclusive. This does not show non-coverage. A guide link found its E25 review successfully where a search did not. A guessed TechRadar Saros10R URL failed; following the actual review link resolved the correct URL. Both demonstrate why search absence is weak evidence.

Unknown cells remain unknown. Some searches returned Curv2Pro, Saros10, E28, MOVA V50 or other nearby models; none were silently upgraded to the requested model. Good Housekeeping Saros content is a feature with a `Created by` label whose creator was absent from extraction; independent lab testing is not established. Do not diagnose sponsorship solely from that incomplete label.

Current guide positions are current observations, while historical reviews retain their own dates/cohorts. A current guide and an old review headline can disagree without proving a dated ranking transition. No archive snapshots were located in this bounded pass. No full videos were watched, no transcripts timed, no manufacturer equivalence investigation completed, and no complete incentive audit was performed.

## Next content work

- Resolve shared-model disagreements first: Curv2Flow mopping across HookUp/VacuumWars; Saros10R pet hair across RTINGS/Tom's Guide; Shark across four sources.
- Keep two separate tables: publisher coverage and exact article/video cohort. Avoid counting a guide plus its linked review as two independent tests.
- For any buyer recommendation, finish claim-level methods, region, current price, firmware and maintenance checks. Discovery of a review is not endorsement.
- Replace the old winner-grid visual with a specific question-led case. A 64-cell grid can remain in the written appendix, with unknown and related-variant states visible.

## Direct-page follow-up

All 28 exact-model review/comparison pairs were subsequently directly opened (27 distinct URLs because two products share HookUp2026), along with all three guides and both variant reviews. Every requested page resolved. The CSV now marks 35 direct-page rows, including previously opened mention/test-table records. No access-blocked review was encountered. Several direct article-body sections were inspected to establish firsthand testing and distinguish related units; this remains a coverage audit, not a verification of every performance claim.

Additional findings:

- Vacuum Wars' current V70 guide links to a [September16 release story](https://vacuumwars.com/mova-v70-ultra-complete-release/). That article anticipates future testing rather than reporting it. A later guide could reflect later testing, but the linked story does not establish it. Keep the attributed current guide result while treating full test publication as unresolved.
- Good Housekeeping's S8MaxV roundup reports a course-test observation but warns that its tested unit is unavailable, with a purchase link to a plumbed variant. Its Shark mop roundup contains firsthand lab observations and a dock leak when moved. Both remain roundups with test summaries, not full standalone tests.
- Vacuum Wars E25 direct page now says updated September16, while search discovery said June10. The audit corrects that discrepancy rather than preserving the earlier snippet date as fact.
- RTINGS Curv2Flow is methodology v1.0; Saros10R/Curv show v1.1. Its own prose differs on relative Curv/Flow stain performance between the introductory comparison and lower side-by-side paragraph. Avoid a firm comparative stain claim until resolved.
- TechRadar Shark explicitly describes two weeks of tests; Tom's Guide Shark discloses reducing the Cheerios load after an overflowing bin. These methodological details can matter more than the verdict adjectives.

See `MATRIX_SCHEMA.md` for the proposed core-matrix replacement, limitations and regression checks. Broader supplementary creator rows must be preserved separately.
