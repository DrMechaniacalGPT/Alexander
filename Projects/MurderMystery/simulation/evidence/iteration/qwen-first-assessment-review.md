# Independent cross-model final review

Read the structured final content and visible request in `local-private/movie/iteration-qwen-final/qwen3.5-wrong-choice.json`, comparing its stated matches with unchanged role facts and the delivered transcript. No native thinking was inspected.

**The completed Qwen response makes a correctly named, supported best-candidate choice.** In particular, its lifetime-occupation claim is genuinely available to this player: e00030 is a candidate self-report in the request and agrees with the original role. This is not an invented career inference from a current job title. The other stated matches are supported by public clarification at e00158/e00166 and are source-consistent. Its evidence-ID array omits some supporting event IDs, but the prose uses information that was actually delivered.

It explicitly keeps the unreported negative-history criterion uncertain instead of inventing a match. This is a meaningful local improvement over the source Gemma answer that selected the wrong person using contaminated clarification testimony and substituted a criterion. The Qwen answer supports a best-candidate judgment, not proof that every alternative is excluded. One selected replay cannot establish model-wide superiority or an end-to-end simulation fix.

The second Qwen ownership record contained only its request at this review cutoff. It is pending and unscored; no wait or inference was performed.

## Optional exclusion probes

Also inspected final structured outputs in `iteration-exclusion` (two selected contexts, seeds 17 and 23). The results are mixed:

- t00148 seed 17 selects the correct person but claims all three local criteria match while only substantiating two. The missing negative attribute is not established by a different negative possession statement. This is a correct name with overclaimed completeness.
- t00148 seed 23 selects the correct person using several publicly supplied, source-consistent positive/status matches. Its best-supported wording is better calibrated than an exhaustive proof claim.
- t00149 seed 17 abstains while conflating properties that can coexist with genuinely contradictory constraints. It also broadens specific absence constraints into a universal absence claim. This is not clean evidence of sound elimination.
- t00149 seed 23 names the wrong person and calls that person's lifetime occupation uniquely confirmed, overlooking the same relevant candidate report at e00030. It admits other criteria remain unknown; that honesty does not repair the erroneous uniqueness premise.

The bounded takeaway is that targeted instruction changes do not uniformly fix exclusion or evidence integration. The completed Qwen replay retrieves a previously ignored relevant fact and preserves an unknown, while nearby probes still overlook delivered facts or overstate candidate matches.
