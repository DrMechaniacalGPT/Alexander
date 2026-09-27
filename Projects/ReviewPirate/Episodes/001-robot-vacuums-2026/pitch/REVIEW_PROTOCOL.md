# Fresh-context editorial review gate

Adopted September 27, 2026 after the owner and author independently found the delivered B pitch inadequate. Playback validation did not establish editorial readiness. No draft is owner-review-ready merely because its files exist or its audio plays.

## Objective

Produce a short, engaging, source-led account that helps a first-time robot-vacuum shopper understand consequential patterns across reviews, understand how those findings change the options, and know which original reviews deserve their attention. The matrix must help the viewer reason. The ending must follow from the evidence actually presented. Runtime and the number of products or beats are flexible.

## Isolated review packet

Freeze a version before evaluation. Record the version, artifact hashes, scene order and timing. Give a fresh reviewer only a short neutral audience/purpose brief, the thumbnail, the exact audience-visible scene images in order and the exact spoken transcript, with timing. Include audio or video only when the review actually evaluates those media. Do not supply this conversation, author rationale, staging promises, preferred option labels, research notes, previous reviews, or a description calling the work successful. Crop the listening-page chrome and internal notes out of scene captures. Do not substitute planned shots for actual images.

Use a new reviewer call with no inherited conversation (a subagent with fork_turns="none" where available). The reviewer must not browse the workspace, research or other chats to repair missing viewer context. Record exactly which media it inspected. A text-only review cannot pass the visual gate. A scene-image/transcript review cannot pass final voice, motion or audiovisual timing.

## Two-pass review

First pass: before showing the detailed rubric, ask the reviewer to describe the experience in its own words: what the opening promised; what each scene added or changed; the main takeaway; why the ending follows; where it became confused, lost interest, or needed information not supplied. Require specific scene references. This is a comprehension check, not a request to praise or rewrite the draft.

Second pass: provide the criteria below in the same isolated review conversation. Ask for PASS, REVISE or CANNOT ASSESS for each, concrete evidence, severity and the smallest substantive change that would address each failure. Invite important failures the rubric missed. Preserve its independent account from pass one.

## Criteria across the whole experience

1. **Promise and payoff:** The first seconds establish what the video will answer. The ending answers that question. Changing scope is explained. A striking eight-winner grid cannot silently turn into an unrelated two-product recommendation.
2. **Orientation:** A first-time viewer can tell which products and specific reviews matter, what the marks mean, and how the current scene relates to the landscape. Names, dates, images and readable cells support rather than overload comprehension.
3. **Useful progress:** Each major beat changes understanding or the candidate comparison for a stated reason. Adding a product, retaining uncertainty or branching can be legitimate progress. Arbitrary elimination, cosmetic highlighting and repeated caveats are not substitutes for progress.
4. **Earned conclusions:** The visible evidence supports the stated recommendation, shortlist or referral. Relevant price/category context is supplied. No unexplained leap from two favorable reviews to a market-wide winner; no implication that an untested alternative fixes another model's problem.
5. **Source-led substance and credibility:** Concrete findings support the account early and throughout. The audience can distinguish another reviewer's test, that reviewer's recommendation, and our inference. We never imply firsthand testing. Referrals explain what the viewer will gain from the original source, at the relevant moment.
6. **Visual explanation:** The actual images make the information easier to understand. Important comparisons are legible without pausing to decode a tiny grid. Relevant findings, exceptions and accumulated progress remain visible. A beautiful background and repeated decorative character pose do not establish a visual story.
7. **Coherent, engaging sequence:** The next question grows from the previous finding. The language sounds natural to a shopper rather than like internal research notes. Detail, caveats, character action and visual changes support attention; they do not repeatedly interrupt it. Shortness alone is not success.
8. **Practical payoff:** The viewer can explain what they learned, why it matters to their next decision, and which original review to consult for deeper evidence. A list of model names or generic links is insufficient.

Evaluate the opening, every transition and the ending; do not give one average score that hides a fatal gap. The reviewer is a simulated fresh viewer, not a substitute for real audience testing.

## Separate evidence check

A different verification pass may read the claim ledger and original sources. It checks product identity, dates, prices/eligibility, scoring scales, source dependence, disclosures, representativeness and whether each scripted inference follows. The audience reviewer cannot establish factual truth by finding the story persuasive. Both checks must pass for the artifact's declared stage.

## Revision loop and exit rule

1. Build the complete audience artifact; inspect it sequentially without relying on notes.
2. Freeze it and run the two-pass isolated review plus the separate evidence check.
3. Save verbatim reviewer output in a local review record, then make an issue ledger linking each substantive finding to scenes and a proposed fix. Do not count the review as completed if the reviewer did not receive the actual media.
4. Revise research, story structure or visuals as necessary. Fix causes, not just wording. Do not defend the draft by giving the viewer reviewer missing backstory.
5. Review the revised complete sequence, then send the new frozen version to another fresh reviewer. Do not show it earlier praise, failures or desired verdicts. Compare findings for regressions; do not keep sampling unchanged drafts until one approves.
6. The fresh-review gate passes only when the reviewer explicitly reports **no remaining issues under the review criteria**, can independently reconstruct the reasoning, and has actually inspected the required audience materials. Do not silently weaken this to “no major issues,” dismiss remaining minor findings, or interpret CANNOT ASSESS as PASS. This is a bounded review judgment, not a guarantee that no flaw exists.
7. After that pass, perform the full-conversation alignment review below on the **same frozen artifact version**. Fresh-review success is an intermediate gate, not readiness.
8. Mark **ready for owner review** only when that exact version passes the fresh review, the separate evidence check, and the conversation-context check. Any revision after a pass invalidates readiness for the new version: run the revised complete artifact through the fresh review again, followed by another context check.

When failures remain and useful work is available, continue. If repeated revisions stall, change the approach and inspect the missing research rather than polish the same structure. If access, time or another concrete constraint prevents progress, report an unfinished checkpoint and the blocker; do not relabel it ready. Passing this gate is permission to show the owner a stronger draft, not permission to publish or purchase anything.

## Final conversation-context gate

Added at the owner's explicit request September 27, 2026. The author now reviews the passed artifact against the full available conversation record, including earlier corrections and rejected approaches. Retrieve older conversation logs where available; do not claim a full-history check if only a compacted summary was accessible. Record the reviewed history scope and any material gaps. Keep that history out of the fresh reviewer's packet.

Build a traceable alignment record: owner intent or correction; its underlying purpose; applicable artifact scene(s); observed fulfillment or failure; and the resulting revision. Resolve evolving preferences using later explicit corrections while preserving durable earlier goals. Do not turn tentative examples (eight products, seven beats, a one-minute limit, a particular mascot or elimination scheme) into mandatory requirements unless the owner actually adopted them.

Inspect the artifact sequentially, not only against a checklist. In particular, revisit the agreed review-of-reviews premise; thumbnail-to-opening continuity; useful synthesis and original-source referrals; scientific substance without claiming our own tests; understandable accumulated progress on the grid; credibility and visual interest throughout; character/house integration appropriate to the declared production stage; and the requirement that conclusions be earned. Ask what the fresh reviewer missed because it did not know the conversation. Also ask whether the rubric itself omitted an important aspect of the intended experience.

The context review may reject a draft even when the fresh reviewer found no issues. It cannot excuse confusing audience-facing material by appealing to explanations elsewhere in the conversation. Record concrete failures and revise the artifact, evidence or review criteria as appropriate. Then return to a fresh-context review of the complete new version, followed by the evidence check and another conversation-context check. Do not reuse an earlier passing verdict after edits or waive the fresh gate because the context-informed author now likes the result.

Keep each frozen version's fresh-review report, evidence-check result and context-alignment record together. Only a version with all three passing can be presented as ready. Unfinished work or inaccessible history is reported honestly; it is not converted into a pass.

## Current baseline

Option B in listening-v2 fails promise/payoff, orientation, earned shortlist, sequence and visual explanation based on September 27 owner/author review. Preserve it as the failed baseline; do not animate it. A and C have not received this fresh review in the current discussion. The earlier recommendation to advance B is withdrawn.

Isolated reviews now run under this protocol; see `review-loop/ISSUES.md` and each frozen version’s reports. Rejected revisions are retained, and a pass is never inferred from artifact creation. For the listening-pitch stage, evaluate the actual scene images and transcript; final motion and voice remain separate later gates.
