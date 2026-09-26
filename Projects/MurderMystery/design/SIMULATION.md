# Local simulation design

The design-stage specification below is only partly implemented. See the [working runner and scope](../simulation/README.md) and [measured results](../simulation/RESULTS.md). The existing [Ollama probe](../research/feasibility/local_probe_results.json) proves tiny local calls work. It does not establish long-context performance, strategy or human realism. Use ordinary Python and the local Ollama HTTP endpoint; keep the adapter replaceable.

## Data separation

| Object | Contains | Who may receive it |
|---|---|---|
| Case truth | Fixed history, canonical artifacts, true relationships and rule constraints | Engine and post-run analysts; players only through explicit projections |
| Live world state | Current attendance, possessions, accepted actions and recorded commitments, with event provenance | Engine; players receive only observable consequences or their own state |
| Character | Own knowledge, commitments, relationships, disclosure guidance, portrayal cues | Assigned participant |
| Participant policy | Initiative, exploratory targeting, disclosure tendency, attention/retrieval policy | That participant and controller; separate from character identity |
| Exposure log | Events actually delivered to a participant | Controller; eligible input to that participant's memory |
| Accessible memory | Selected personal events/notes used this turn | That participant only |
| Belief/intent report | Stated suspects, uncertainties, intended approaches and supporting event IDs | Private unless deliberately spoken |
| Run manifest | Case/prompt versions, model settings, seeds, caps, treatment and scheduler | Analysis; never a spoiler-bearing player prompt |
| Evaluator annotation | Contradictions, route failures, choice classification, unsupported claims | Analysis only; never fed into a frozen run |

Shareable character background and room-wide public facts are separate fields. Never provide a player the analyst's global map of relationships. Never let an extraction or summary step use the omniscient transcript. Players have no file, browser or repository tools.

Historical facts remain immutable; live state changes only through validated events. A spoken promise is recorded as a commitment, not guaranteed compliance or automatic trust. Physical possession and attendance have explicit state transitions. The first fixture supports speech, recorded commitments, attendance and simple evidence delivery only; combat, murder, voting and other world-changing systems are deferred. Consequences include another participant receiving information, making a promise, refusing cooperation or taking an available follow-up action; do not represent every effect solely as an analyst’s prose.

Keep observations immutable. An exposure is not belief, understanding or current recall. Belief reports are outputs to inspect, not verified access to model cognition. Evidence IDs identify events the player actually received. A correct inference about something unseen is possible; distinguish it from leaking hidden prompt material.

## Minimal event contract

Each event has `id`, `scene`, `window`, `actor`, `kind`, explicit `recipients`, `content`, and optional `artifact_id`/`in_reply_to`. Identity keys are opaque; they must not encode hidden meaning such as `murderer_confession` or `real_alibi`. Engine records rule decisions separately from the text players hear.

| Event example | Recipient result |
|---|---|
| A whispers to B while C is elsewhere | Only A and B receive it |
| A speaks in a group containing B and C | A, B and C receive the utterance; later memory policy may omit it |
| D joins halfway through that conversation | D receives subsequent events, not the prior transcript automatically |
| C steps outside for two windows | No room speech delivered; return does not backfill missed events |
| A repeats “B says Sofia left” to C | C gets A's report with attribution, not B's original private conversation |
| A makes a gesture toward B | Only declared observers receive the action; recognition is separate and modeled explicitly |
| A asks the engine to show a card it does not possess | Mechanical action rejected and logged; no new artifact created |

Dialogue may include lies and unsupported claims. Only the engine creates canonical artifacts. Do not treat every false statement as a model error or every model error as intentional deception. Label uncertain cases for review.

## First participant settings

Use four adjustable dimensions initially: initiative, exploration versus goal-directed targeting, disclosure tendency, and attention/retrieval. These are experimental policies, not scientifically calibrated personality scales. Keep demographic labels out of them.

Initiative is controller-visible and affects the chance of attempting an approach. Target preferences come from the model using only its available information; exploratory selection sometimes substitutes a random eligible target. Low initiative does not reduce reasoning quality or willingness to answer. High initiative does not automatically imply rudeness, dominance or interruption.

Disclosure tendency influences interpretation and willingness to volunteer, with explicit stress variants for withholding or overdisclosure. The normal engine does not enforce all character instructions as mechanical barriers: early revelation is allowed to be observed. It does enforce visibility, attendance, artifact possession and irreversible world actions. A mandatory-disclosure instruction violation is reported, not silently repaired. The simulation must preserve a player's discretionary moral choice even when a confrontation condition is recognized.

For attention, compare full personal-log access, bounded retrieval and temporary absence as separate treatments. A bounded policy can prioritize recent events and explicitly saved notes; log what it omitted. Do not automatically save every important clue using the evaluator's knowledge. Players may retain access to their own printed role sheet; forgetting a newly heard claim and failing to reread the sheet are distinct conditions.

## Scheduling

There is no fixed player count or six-window default. The hypothesis is that limited opportunity may make encounters consequential. Compare a declared encounter/time budget, contact-based transition, or narrative event, and retain a finite safety cap. No condition is yet a validated model of human mingling. The first implementation offers fixed encounters and random-pair windows; initiative-directed approaches and naturally forming groups remain design work.

At each window, carry ongoing conversations forward, mark attendance/occupancy, sample initiative and randomize proposal order among initiators. Resolve target requests against remaining capacity. An unmatched player may wait or accept an incoming approach; do not silently force everyone into a helpful conversation. A declared duration policy sometimes reserves two windows. Record unfulfilled approaches and idle time. Compare against random pairing as a baseline; even that baseline should include missed windows in stress cases.

Group mode is a separate later treatment: membership, speaker selection, audience and turn budget must be explicit. Joining late does not grant prior knowledge. More recipients does not mean more attention or equal speaking opportunities. Do not implement groups as all-to-all private messages. Interruptions and free movement are deferred until simpler traces show a need.

## A model turn

Build a prompt from stable rules, that player's role and policy, current accessible observations, scene opportunities and legal action forms. Request a short utterance or action, plus compact private intent/evidence references where useful. Actual speech goes only to recipients; private fields do not. A schema helps parsing, but validation still checks IDs, recipients, capacities and possession.

One turn updates the event log and then permitted views. Replies in a conversation are sequential. Independent conversations may later run concurrently, but start serially for inspectability and limited local memory. Use snapshot IDs and idempotency keys so retries cannot double-apply an action. Checkpoint between completed actions; resume must not replay a disclosure twice. Bound timeouts/retries and preserve failed outputs.

Record model output for exact replay. Reissuing the same prompt or seed is a new generation, not guaranteed deterministic replay. Do not share one global conversation history between roles. The same loaded local model can serve all separate requests.

## Implementation shape and first stop

Proposed modules: `case_io`, `views`, `events`, `policies`, `scheduler`, `models/ollama`, `runner`, `report`. JSON data and JSONL traces are sufficient initially; no framework, training, database or 3D environment is assumed.

First runnable slice: four roles, one dilemma, one private exchange, stubbed responses and exact view tests; then a bounded local inference trial. E2 uses a predeclared hand-authored schedule for its two windows. The initiative scheduler arrives in W06; early encounters establish no claim about natural meeting or discovery probability. No full murder solution is needed for testing dilemma mechanics. The fixture must label itself synthetic and incomplete. Do not populate the rest of a commercial game simply to give the simulator more to do.

## Extension: factions and improvisation

Faction membership, knowledge of membership and shared objectives are separate character fields. Membership never grants automatic access to teammates' observations. Alliances may also emerge from explicit promises during play. The participant policy later adds improvisational latitude and deception tendency as distinct treatments; ordinary color, speculation, false testimony and invented artifacts are not the same action. See [social-deduction comparison](SOCIAL_DEDUCTION.md). Defer these axes until the first dialogue is interpretable rather than introducing every trait into a single opaque persona prompt.
