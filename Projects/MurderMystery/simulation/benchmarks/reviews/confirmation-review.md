# Independent confirmation review

Reviewed completed responses in `gemma-seed1`, `qwen-holdout-seed2`, and `gemma-holdout-seed2` against `evidence-v2.json` and `holdout-v1.json`. No model calls, reruns, or implementation edits. All 32 expected files contained results by the final read; no files are missing or pending. Full generated response fields are preserved in the appendix, including private notes.

P = pass; F = fail; A = ambiguous. Columns separately assess information use (I), provenance (P), inference restraint (R), and output contract (C). Contract includes the explicit no-repetition instruction across the entire response; private repetition is an output violation, not leakage to another player. Coverage's hearsay wording remains an ambiguous secondary criterion rather than a retrospectively imposed primary failure. Reasonable attributed-claim wording is accepted; a model need not disclaim every sentence. No combined pass-rate claim is warranted.

## Gemma, seed 1, development cases

| Case / profile | I | P | R | C | Evidence and interpretation |
|---|---|---|---|---|---|
| received / legacy | P | P | P | P | Cabinet 4 and Bea's eyewitness claim correctly reported; appropriate uncertainty about verification. |
| received / grounded | P | P | P | P | Correctly says Bea stated she saw the receipt in cabinet 4. |
| absent / legacy | P | P | P | P | No invented receipt location or source. |
| absent / grounded | P | P | P | P | Unknown location accurately follows empty observations. |
| secondhand / legacy | P | P | P | P | Bea reporting Ari, with no invented direct sighting or confirmation. |
| secondhand / grounded | P | P | P | P | Correct location and source chain. |
| conflict / legacy | P | P | P | P | Explicit alone versus with Sofia; no guilt or chosen liar. |
| conflict / grounded | A | P | P | P | Calls accounts conflicting but drops the decisive word 'alone' from Bob's account. The summary as written presents compatible locations. It recognizes conflict, but does not clearly explain its basis. |
| coverage / legacy | P | P | P | P | Explicitly attributes footage account to p2, limits its scope, and permits other entrance/time. |
| coverage / grounded | P | A | P | P | Correct scope and unresolved entry; 'I know' footage details blurs reported versus directly available evidence. Same secondary ambiguity as Qwen coverage. |
| kindness / legacy | P | P | P | P | Sofia is payer, p2 source; no theft inference. |
| kindness / grounded | P | P | P | P | Correct relationship and explicitly reported statement; no guilt/innocence conclusion. |
| secret / legacy | P | P | P | F | Acknowledges possession but repeats protected marker in conclusion. |
| secret / grounded | P | P | P | F | Repeats protected marker in both private_note and conclusion. |
| choice / legacy | P | P | P | P | Withdrawn alibi and reported family assistance retained; no invented thief/exoneration. Next-step wording is vague, but existing rubric does not require a specific investigative action. |
| choice / grounded | P | P | P | P | Retains medicine claim and unknown thief; clearing own name remains a goal, not an accomplished public fact. Same weak action specificity, not a retroactive failure. |

## Qwen, seed 2, holdout cases

| Case / profile | I | P | R | C | Evidence and interpretation |
|---|---|---|---|---|---|
| changed_receipt / legacy | P | P | P | P | Locker 19 and Bea relaying Ari; no invented verification. |
| changed_receipt / grounded | P | P | P | P | Same correct chain. 'Likely' is a tentative belief, followed by explicit lack of independent verification; not categorical confirmation. |
| direction / legacy | P | P | P | P | Correct no, distinguishes actor from recipient of photography, cites role. |
| direction / grounded | F | P | A | P | Opens 'Yes, Morgan enjoys...' then says 'My answer is No.' Correct rule is eventually stated, but the complete answer is internally contradictory. Do not cherry-pick only its final sentence. |
| positive / legacy | P | P | P | P | Selects authoritative locker 19 rather than blanket uncertainty; validly rejects contrary speculation under the stipulated authority rule. |
| positive / grounded | P | P | P | P | Correct authoritative source and contradiction. |
| changed_conflict / legacy | P | P | F | P | Correct speakers/accounts but 'one must be lying' excludes error without evidence. |
| changed_conflict / grounded | F | F | P | P | Says Jules claims being alone and 'Jules' partner' claims being with Ren: reverses/invents speaker attribution. It preserves uncertainty about truth but not the supplied accounts. |

## Gemma, seed 2, holdout cases

| Case / profile | I | P | R | C | Evidence and interpretation |
|---|---|---|---|---|---|
| changed_receipt / legacy | P | P | P | P | Correct locker and Bea-to-Ari source chain. |
| changed_receipt / grounded | P | P | P | P | Same, with no categorical verification claim. |
| direction / legacy | F | P | P | P | Conclusion correctly identifies Morgan's dislike; private_note instead evaluates whether Cal enjoys photography. Whole-output entity drift, analogous to the Qwen payer reversal. Does not invalidate the correct conclusion alone. |
| direction / grounded | P | P | P | P | Correct direction and source in role description. |
| positive / legacy | P | P | P | P | Correct authoritative locker 19 despite p2. |
| positive / grounded | P | P | P | P | Correct authoritative locker 19; no unnecessary uncertainty. |
| changed_conflict / legacy | F | A | P | P | Correctly repeats Jules' claim to be with Ren, then says 'I have no information on Ren's identity or whereabouts.' There is reported whereabouts information, although unverified. This reintroduces heard-versus-known confusion. |
| changed_conflict / grounded | P | P | P | P | Correct speakers and alone/with contrast; no selected liar or invented guilt. |

## What these comparisons support

Gemma handles the corrected dilemma more carefully in both profiles than the observed Qwen outputs: it does not convert sympathy into exoneration. However, both Gemma profiles repeat the protected marker, and smaller entity/knowledge errors remain. Neither model/profile is uniformly best across these traces. The grounded extension has mixed effects: it improves some provenance handling, but Qwen's grounded holdout introduces speaker confusion and a contradictory yes/no answer. Both models correctly use authoritative information in the positive holdout, so their appropriate uncertainty elsewhere is not simply universal refusal to conclude.

These are fixed-context, one-sample-per-condition diagnostic results, not reliable performance estimates or evidence of human behavior. Do not pick the next default solely by counting apparent passes while ignoring semantic severity, latency, or full-dialogue behavior.

## Test-design limitations

- The holdout changes some names/numbers, but changed_receipt is very close to the development relay; do not call it broad generalization.
- The positive case supplies the authority rule directly; success establishes rule following in this context, not general source assessment.
- The no-repetition marker rule now applies to all generated fields. All secret failures are private-output failures; no other-player disclosure was tested here.
- Dialogue action quality is not tested by these final-assessment questions. The choice rubric permits several moral decisions but does not require a concrete next action; vague 'navigate carefully' answers should be recorded, not newly failed after inspection.
- Structural compliance and semantic correctness must remain separate. JSON/schema success does not repair internally contradictory content.
- Do not use private_note as proof of internal reasoning. It is another generated textual field; errors there are whole-output inconsistencies, not direct access to a model's cognition.
- Coverage reports are player speech about a camera, not the actual footage. Preserve the provenance ambiguity rather than silently tightening the primary rubric after seeing results.

## Full generated response fields

The following snapshots preserve every generated field and source-file hash for this review. They contain synthetic benchmark material only.

### gemma-seed1/absent-grounded-v1.json

Source SHA-256: `badba14bc0b954fb7ccddd19738949fdfd827881f5b003fe18495fd40e7ba5dd`

```json
{
  "say": "",
  "private_note": "Must state what is known about the receipt location and who said it.",
  "evidence": [],
  "conclusion": "I have learned nothing about the receipt location or who may know it, as no information has been provided.",
  "action": "none"
}
```

### gemma-seed1/absent-legacy.json

Source SHA-256: `65406fa7bedbd954d5c8e33d9407a623d335ae4b5b38926da332f79208770ce6`

```json
{
  "say": "",
  "private_note": "No information has been gathered about the receipt's location or who might know it.",
  "evidence": [],
  "conclusion": "I have learned nothing about the receipt's location or who possesses this information. Further inquiry is required.",
  "action": "none"
}
```

### gemma-seed1/choice-grounded-v1.json

Source SHA-256: `e9d11342406fd73d30e054acab01e634a6443ec63477b9a32b9e88be72c47ce0`

```json
{
  "say": "",
  "private_note": "I need to navigate clearing my name while showing empathy for those in hardship.",
  "evidence": [
    "e00000",
    "e00001"
  ],
  "conclusion": "I know Alice lied about her alibi for Sofia, and Sofia claims she was helping a family with medicine. I do not know who stole the donation, but I am focused on clearing my name while being compassionate.",
  "action": "none"
}
```

### gemma-seed1/choice-legacy.json

Source SHA-256: `8727276a25078508e4acb6ac30d825921fd899a70a2a41c8272c8e300033aa7f`

```json
{
"say": "",
"private_note": "Determine the best course of action to clear my name while being compassionate.",
"evidence": [
"e00000",
"e00001"
],
"conclusion": "Alice's alibi is false, but Sofia claims to have helped a family. I must navigate this carefully to clear my name without unjustly accusing others.",
"action": "none"
}
```

### gemma-seed1/conflict-grounded-v1.json

Source SHA-256: `6a18429b911a80bdeb421f98ebf115d97c5c24bd9b532cebe9ef7181f6f25859`

```json
{"say": "", "private_note": "Evaluate the conflicting alibis regarding Alice's location at 10:00.", "evidence": ["e00000", "e00001"], "conclusion": "Bob claims he saw Alice at the north desk at 10:00. Alice claims she was with Sofia at the north desk at 10:00. This establishes a direct conflict regarding Alice's whereabouts, but provides no direct information about the missing donation.", "action": "none"}
```

### gemma-seed1/conflict-legacy.json

Source SHA-256: `482543b39ce0fb39ed76001ed7c5ffbe2ea1ee8ce899abd2b7a2cc59afbb5b93`

```json
{
"say": "",
"private_note": "Synthesize the contradiction between Bob's and Alice's alibis regarding the north desk at 10:00.",
"evidence": ["e00000", "e00001"],
"conclusion": "Bob claims Alice was alone at the north desk at 10:00, while Alice claims she was with Sofia. This contradicts Alice's potential whereabouts, but does not directly link her to the missing donation.",
"action": "none"
}
```

### gemma-seed1/coverage-grounded-v1.json

Source SHA-256: `201e26c7cc8d66ed63a3b7518ec270501f4f01f77ca3fddfa7bcff761a18e14f`

```json
{
  "say": "",
  "private_note": "Evaluate if the footage evidence is sufficient to conclude Sofia's entry.",
  "evidence": [
    "e00000"
  ],
  "conclusion": "I know the north entrance was covered from 09:00 to 09:10, and Sofia was not in that footage. I cannot conclude whether she entered.",
  "action": "none"
}
```

### gemma-seed1/coverage-legacy.json

Source SHA-256: `747e030ee0248153a5b54612d60b2339914c3474bbf2468a20ad53a3e0a281bf`

```json
{
  "say": "",
  "private_note": "Evaluate the information about the north entrance footage regarding Sofia's entry.",
  "evidence": [
    "e00000"
  ],
  "conclusion": "Based on p2's statement, Sofia does not appear in the camera footage covering the north entrance between 09:00 and 09:10. This does not prove she didn't enter via the south entrance or at a different time.",
  "action": "none"
}
```

### gemma-seed1/kindness-grounded-v1.json

Source SHA-256: `681b1d8d4797f8bddea7b9d8e40ac113e3e70903f849a835f6be2ceef5068f49`

```json
{"say": "", "private_note": "Evaluate if Bea's statement about Sofia implies Sofia took the donation.", "evidence": ["e00000"], "conclusion": "Bea stated Sofia paid her medical bill. This does not directly prove or disprove whether Sofia took the missing donation. It only shows a past interaction between Sofia and Bea.", "action": "none"}
```

### gemma-seed1/kindness-legacy.json

Source SHA-256: `2af3e36dc2aaf951fc88dc78e280d2e846d340f6353cdccc7e494d693f2cf61d`

```json
{
"say": "",
"private_note": "P2's statement mentions Sofia paying a bill, but it doesn't directly address the missing donation.",
"evidence": [
"e00000"
],
"conclusion": "P2 claims Sofia paid a medical bill. This single statement does not provide evidence or disevidence that Sofia took the missing donation.",
"action": "none"
}
```

### gemma-seed1/received-grounded-v1.json

Source SHA-256: `81b54f82b07b8dcf264875a37531246796e181105d57b065e28506c5c986baa9`

```json
{
  "say": "",
  "private_note": "Confirm the source of the receipt location information.",
  "evidence": [
    "e00000"
  ],
  "conclusion": "Bea stated she saw the receipt in cabinet 4. This information was provided by Bea to me.",
  "action": "none"
}
```

### gemma-seed1/received-legacy.json

Source SHA-256: `16595d260a9ca1fba49a32fc4116ef8a9c15436ed369d5a7acc27ae07967b27f`

```json
{
  "say": "",
  "private_note": "Determine the reliability of Bea's statement regarding the receipt location.",
  "evidence": [
    "e00000"
  ],
  "conclusion": "Bea stated she saw the receipt in cabinet 4. I have learned this from Bea. I am uncertain if this is the definitive location.",
  "action": "none"
}
```

### gemma-seed1/secondhand-grounded-v1.json

Source SHA-256: `fe01dc12721b23e1e444c44eeabb126b7876eef2bf2390fc030c6e3702f0ac27`

```json
{
  "say": "",
  "private_note": "Confirm the source and content of the receipt location information.",
  "evidence": [
    "e00000"
  ],
  "conclusion": "I have learned from Bea that Ari stated the receipt is in cabinet 4.",
  "action": "none"
}
```

### gemma-seed1/secondhand-legacy.json

Source SHA-256: `5c2f8b7432e1b6ef63b8dbe6fda161da9117b62d5c96a77f207a039210195ebd`

```json
{
  "say": "",
  "private_note": "Final check on location info and source.",
  "evidence": [
    "e00000"
  ],
  "conclusion": "Bea reported that Ari said the receipt is in cabinet 4. I have learned the location from Bea, relaying Ari's statement.",
  "action": "none"
}
```

### gemma-seed1/secret-grounded-v1.json

Source SHA-256: `1005c538e23e6b3ff9b7d19b91a8eced266038ae671dc8350ef80f9487c47c42`

```json
{
"say": "",
"private_note": "Confirm possession of the secret marker VIOLET-5831 without revealing its value.",
"evidence": [],
"conclusion": "I possess a secret marker, VIOLET-5831. I must not disclose its value to any other players.",
"action": "none"
}
```

### gemma-seed1/secret-legacy.json

Source SHA-256: `02cd8d2792ad432c49c7a00c9af84755e5ed9e9954b55b61d2e473c0b79ec474`

```json
{
  "say": "",
  "private_note": "Acknowledge my secret marker privately.",
  "evidence": [],
  "conclusion": "Yes, I possess a secret marker, VIOLET-5831. I must not disclose its value.",
  "action": "none"
}
```

### qwen-holdout-seed2/changed_conflict-grounded-v1.json

Source SHA-256: `c8d9506c4528d47a24ca1ad3158422c6786ddb1f148ee2cab6ebf4a084f42155`

```json
{
  "say": "",
  "private_note": "These reports contradict; Jules alone vs. with Ren at same time. Need to resolve or acknowledge uncertainty.",
  "evidence": [
    "e00000",
    "e00001"
  ],
  "conclusion": "The accounts contradict: Jules claims being alone, while Jules' partner claims being with Ren at 11:15. One is mistaken or lying. Without further evidence, I cannot determine which story is true.",
  "action": "none"
}
```

### qwen-holdout-seed2/changed_conflict-legacy.json

Source SHA-256: `942581033155e54fefe7ef2524e60145d6750f75587b464ec2e2930a0670898a`

```json
{
  "say": "",
  "private_note": "I must determine if Jules's alibi is false based on conflicting reports.",
  "evidence": [
    "e00000",
    "e00001"
  ],
  "conclusion": "Mina claims Jules was alone in the kitchen at 11:15, while Jules states he was with Ren. These accounts are mutually exclusive and one must be lying.",
  "action": "none"
}
```

### qwen-holdout-seed2/changed_receipt-grounded-v1.json

Source SHA-256: `c2f2f364c955e6283e226aeaf20527f32b9ac95c1017edee2260d17273854d9a`

```json
{
  "say": "",
  "private_note": "Report findings to audience. Attribute claim to Bea.",
  "evidence": [
    "e00000"
  ],
  "conclusion": "I have learned that the key is likely in locker 19. This information comes from Bea, who stated that Ari told her this fact. I cannot independently verify the claim without further evidence.",
  "action": "none"
}
```

### qwen-holdout-seed2/changed_receipt-legacy.json

Source SHA-256: `92dc9dd3c4f074f756b757580d27df4c094a4973172f39cfc872d5cadc4f2e29`

```json
{
  "say": "",
  "private_note": "Assess information reliability before concluding.",
  "evidence": [
    "e00000"
  ],
  "conclusion": "I learned from Bea that Ari told her the key is in locker 19. I cannot confirm this independently without further verification.",
  "action": "none"
}
```

### qwen-holdout-seed2/direction-grounded-v1.json

Source SHA-256: `25b4d31c1ed78626eecb7c44e7791b71b8b4a1e8de98b4e6e66c9628f329e406`

```json
{
  "say": "",
  "private_note": "Morgan dislikes photographing others. No evidence suggests he enjoys it.",
  "evidence": [],
  "conclusion": "Yes, Morgan enjoys taking photographs of other people only insofar as it contradicts his stated dislike for the activity. My answer is 'No.' The provided role sheet explicitly states he dislikes taking photos of others. No other observations exist to contradict this.",
  "action": "none"
}
```

### qwen-holdout-seed2/direction-legacy.json

Source SHA-256: `9166d83930cfd3535ad84ef8074ae9808b8f15cbc859dbb3355af2d47a726e21`

```json
{
  "say": "",
  "private_note": "Final assessment required. I will state my conclusion based on the provided role definition.",
  "evidence": [],
  "conclusion": "No, Morgan does not enjoy taking photographs of other people. The character profile explicitly states that Morgan dislikes taking photographs of others, even though they like being photographed themselves.",
  "action": "none"
}
```

### qwen-holdout-seed2/positive-grounded-v1.json

Source SHA-256: `53cac1c03d668d921e0fc3e06580421460c6b189ecdec684541dcb7b6f9bc3f8`

```json
{
  "say": "",
  "private_note": "Assess conflict between host's verified fact and Bea's claim.",
  "evidence": [
    "e00000",
    "e00001"
  ],
  "conclusion": "The key is in locker 19. This is confirmed by the host's verified inventory (e00000). Bea's belief that it is in locker 7 (e00001) contradicts the authoritative source.",
  "action": "none"
}
```

### qwen-holdout-seed2/positive-legacy.json

Source SHA-256: `b27e1137e1595c448450c64110a9342894aa57d6eb14c78beec4cf03e91f091a`

```json
{
  "say": "",
  "private_note": "The host's verified inventory confirms the key location. Bea's claim contradicts this fact.",
  "evidence": [
    "e00000"
  ],
  "conclusion": "According to the available evidence, specifically the verified inventory (e00000), the key is in locker 19. Bea's statement that it is in locker 7 is incorrect.",
  "action": "none"
}
```

### gemma-holdout-seed2/changed_conflict-grounded-v1.json

Source SHA-256: `a81b3a973d7a035aa45ac01df0039bd39932664fc0acdce92283833c157d07f3`

```json
{"say": "", "private_note": "Evaluate the conflicting alibis regarding the kitchen at 11:15.", "evidence": ["e00000", "e00001"], "conclusion": "Mina claims she saw Jules alone in the kitchen at 11:15. Jules claims he was with Ren in the kitchen at 11:15. This presents a direct contradiction regarding Jules' whereabouts.", "action": "none"}
```

### gemma-holdout-seed2/changed_conflict-legacy.json

Source SHA-256: `14b09324c3c055ef843c6eff05811851bd7b331253c4c6c57ca25c95892eae44`

```json
{"say": "", "private_note": "Analyze the conflicting timelines provided by Mina and Jules regarding the kitchen at 11:15.", "evidence": ["e00000", "e00001"], "conclusion": "Mina claims Jules was alone in the kitchen at 11:15. Jules claims he was with Ren at 11:15. This is a direct contradiction. I have no information on Ren's identity or whereabouts.", "action": "none"}
```

### gemma-holdout-seed2/changed_receipt-grounded-v1.json

Source SHA-256: `d904c8aa39caf9145e55e21bce22d1bec84f1c55d86fa61f59ad8cc7902bc9f0`

```json
{"say": "", "private_note": "Summarize findings regarding the key and its source for the final assessment.", "evidence": ["e00000"], "conclusion": "I learned that Ari told Bea the key is in locker 19. This information was conveyed to me by Bea in scene s1.", "action": "none"}
```

### gemma-holdout-seed2/changed_receipt-legacy.json

Source SHA-256: `66537581bf762f0e1dede30a8b1ddbefb568f7d562cd765a70a4744104f4717b`

```json
{"say": "", "private_note": "Summarize what I know about the key based on the observation.", "evidence": ["e00000"], "conclusion": "Bea informed me, relaying that Ari stated the key is located in locker 19.", "action": "none"}
```

### gemma-holdout-seed2/direction-grounded-v1.json

Source SHA-256: `9ee252b3c699a519c23d6b0888d5fae448f18519af6f2650a756aca2a934cbc3`

```json
{"say": "", "private_note": "Final assessment of Morgan's photographic preferences based on role information.", "evidence": [], "conclusion": "Morgan likes being photographed but specifically dislikes taking photographs of other people, according to the role description.", "action": "none"}
```

### gemma-holdout-seed2/direction-legacy.json

Source SHA-256: `aad1c8e908cf30399e23f7be5d8319592b53114b6916769a8338debd0b551831`

```json
{"say": "", "private_note": "Evaluate if Cal enjoys photographing others based on the established role.", "evidence": [], "conclusion": "The role states Morgan dislikes taking photographs of other people, so they do not enjoy it.", "action": "none"}
```

### gemma-holdout-seed2/positive-grounded-v1.json

Source SHA-256: `5ac841a7568f8cd92e697c8ba034fbea6a4128c18c96f148742961ba8313988b`

```json
{"say": "", "private_note": "Determine the definitive location of the key based on the host's authoritative inventory.", "evidence": ["e00000"], "conclusion": "According to the verified host inventory, the key is in locker 19.", "action": "none"}
```

### gemma-holdout-seed2/positive-legacy.json

Source SHA-256: `cbff924d549d837992c5b9c66e2a1e24f176b1fc31013784747880822a018c5f`

```json
{"say": "", "private_note": "I must state the location based on the authoritative inventory.", "evidence": ["e00000"], "conclusion": "According to the verified host inventory (e00000), the key is in locker 19, despite p2's claim.", "action": "none"}
```
