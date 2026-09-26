# Experiments that help us design

This is the design-stage proposed protocol, not the execution record. The owner subsequently approved a smaller incremental sequence through an existing scenario; see [actual results and deviations](../simulation/RESULTS.md). The objective is to explore coherent, consequential alternatives and improve material, not to maximize branch count or certify a human behavioral model.

## Separate the things we change

Track case text, character commitments, participant policy, scheduler, memory treatment and model/configuration independently. A changed prompt is a treatment, not another seed. Replaying recorded outputs verifies software; regenerating is a stochastic repeat. Repeated runs of the same model are not independent samples of humans.

## Bounded sequence

| Stage | Question | Proposed scope | What we inspect |
|---|---|---|---|
| E0: integrity | Do private views and event routing work? | Stub/recorded responses, no inference | Private/group/absence/rumor/gesture cases; invalid IDs; retry/resume |
| E1: local capability | Can the installed model follow a role at realistic context size? | At most 12 short calls; 4,096 context tokens and 256 generated tokens as starting caps, configurable and logged | Completion, truncation, unsupported facts, role separation, latency and resource use |
| E2: one encounter | Can a dilemma create understandable action and reaction? | Four roles, one scene, two windows on a predeclared hand-authored schedule; at most 32 calls | Short actual dialogue; downstream response; stalled or impossible actions |
| E3: information treatments | Does relevant information alter the space of plausible choices? | Six snapshot treatments × three repeats = 18 bounded continuations, at most 12 calls each | Actions, cited observations, consequences and persistent alternatives |
| E4: role/profile stress | Which opportunities depend on a particular participant? | Low/high initiative on focal role; withheld/early disclosure; temporary absence; full/bounded recall, one variable at a time initially | What remains for every participant to do; delivery vs inference failures |
| E5: interaction format | Does pairing or grouping change the experience? | Random pairs, initiative-led pairs, then one explicit group-mode variant | Meeting access, speaking concentration, public spillover and quieter roles |

E2 deliberately controls who meets whom. It tests dialogue and response under that schedule, not spontaneous targeting or natural information discovery; the initiative scheduler is implemented later in W06.

These are starting limits, not instructions to run everything now. Stop each stage for inspection before spending the next batch. Add a wall-clock cap of 30 minutes to the first live batch; save progress rather than discard slow/failed runs. No paid provider fallback or automatic model download. Read-only local capability checks precede model choice; do not infer full-sweep performance from the earlier nine-token reply.

At E1 ensure the supplied packet fits the configured context, including output headroom; record a token estimate and truncation behavior. If it does not fit, shorten deliberately or explicitly increase the cap, rather than silently losing role instructions. Benchmark larger contexts before applying them broadly. Resource defaults may be changed with logged reasons within the agreed local experiment budget.

## Information treatments around Alice

Freeze the same immediate decision situation and prior views. Change only the focal information made legitimately available to Alice:

1. No additional account.
2. A credible account of Sofia helping someone.
3. A credible account of Sofia exploiting someone.
4. Evidence that Daniel faces a serious consequence.
5. Competing accounts that give both people sympathetic and troubling aspects.
6. Irrelevant information of roughly similar length as a control.

Do not tell the player which moral conclusion the treatment is supposed to produce. Avoid spoiler-bearing labels. Match source credibility and timing where possible; otherwise report those as additional changed factors. Do not demand that kindness always causes protection or that each branch appears one third of the time. An unchanged choice can be coherent when another commitment dominates.

Record the first decision and subsequent reactions separately. Immediate snapshot comparisons make the intervention inspectable; full reruns later test whether such information reaches Alice naturally. Artificially delivering information is not evidence that the scheduling/discovery design delivers it. Divergent continuations are expected, so shared seeds do not ensure identical downstream experiences.

Choices may be classified afterward as confession, negotiation, concealment or other, but do not force those categories as the only actions. A short stated reason and event references help review; they are not proof of the model's internal cause. Preserve unexpected constructive options and genuinely incompatible choices.

## What robustness means here

Test silence, absence, missed notes, overdisclosure, conflicting interpretations and deliberate deception. Add improvisation/faction treatments from [SOCIAL_DEDUCTION.md](SOCIAL_DEDUCTION.md) after the basic exchange is interpretable. Distinguish:

- **Accidental stall:** a missed cue leaves nobody with a meaningful next move.
- **Chosen consequence:** players knowingly protect someone at a cost, change an alliance or fail to establish the truth.
- **Model/engine failure:** hidden information leaks, an impossible action is accepted, a reply is truncated, or canonical evidence is invented.

Do not “fix” every chosen consequence into the intended answer. A missed solution may coexist with a strong evening; a correct accusation may coexist with empty participation. Conversely, repeatedly blocking all investigation by accident is actionable design trouble. Independent evidence routes must bypass a missing/uncooperative person, not merely funnel everyone toward them.

## Report shape

One-page run summary links to exact per-player traces. Include configuration, elapsed/model time, calls/tokens, incomplete runs, and the actual denominator for any frequency. Separate protocol errors from interpretive judgments.

| Lens | Record | Do not claim |
|---|---|---|
| Information | Delivered, retrieved and cited events per player | Heard = understood = believed |
| Decisions | Available opportunity, chosen action, supported context, effect on others | Many branches = meaningful agency |
| Participation | Approaches, received approaches, unfulfilled requests, inactivity and useful actions after disclosure | Equal word counts = equal experience |
| Investigation | Hypotheses, challenged claims, independently supported accusations | Omniscient solvability = personal solvability |
| Relationships | Promises, bargains, refusals and changed cooperation with evidence | Generated emotion = measured human emotion |
| Robustness | What survives each perturbation; failures and recovery costs | Success under assumed policies = population probability |

The most valuable output is a design revision with a traceable reason: e.g., a quiet participant had nobody seeking them after their first disclosure, so another role gains a legitimate reason to consult them. Preserve the prior version and compare. Do not optimize an opaque aggregate “fun” score.

## Later human correction

Small reader checks can test comprehension before recruiting full parties. Later observe a few real sessions, ask what choices felt available and consequential, and compare surprises with simulated traces. Volunteers recruited through public content may be unusually AI-enthusiastic; record that bias. No recruitment or outreach occurs in this pass. Human evidence can improve the model without becoming a prerequisite for all creative exploration.
