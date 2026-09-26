# Design proposal: a mystery with choices worth making

September 26, 2026. **Recommendation: develop a small local simulation and an experimental social situation together, then expand toward a complete party game.** The immediate deliverable is a design laboratory: inspectable conversations and consequential choices, with understandable variation between runs. Human predictive accuracy is a later question; it is not a prerequisite for exploring the design.

This supersedes the earlier feasibility memo's narrower requirement that dialogue must first beat static checks at defect detection. Simpler checks remain useful diagnostics. The owner values the creative experiment itself, alongside the eventual game and possible public account of the work. No commercial theme, complete game, simulator implementation or public launch is selected by this document.

## The experience we are aiming for

A guest understands who they are, has a few natural ways to begin, and encounters information that changes what they suspect or care about. Their choices affect other people. They can make mistakes, miss a clue, protect the wrong person or disclose too soon without necessarily losing every useful thing to do. The eventual explanation should remain grounded in a fixed case, while loyalties, discoveries and consequences can vary.

Alice is an illustrative design lens, not a selected cast member. She values honesty, has lied to protect Sofia, and sees someone else harmed by her lie. Learning something generous or troubling about either person may change her response. Confession, negotiation and continued concealment can each be understandable; none should be chosen only to satisfy an author's expected sequence.

**Five commitments:**

1. **Information gives choices context.** Testimony, relationships, interpretation and moral stakes accompany factual clues. Being unpleasant is not proof of guilt; acting skill is not required evidence.
2. **Choices create further play.** Revealing a secret can open a negotiation, damage trust or create an obligation. A character remains useful after disclosing everything.
3. **Routes are resilient, consequences are real.** Offer independent ways to discover important facts, without making every deliberate choice immediately irrelevant through an automatic fallback. Protect against accidental stalls; preserve chosen costs.
4. **Characters and participants are distinct.** The fictional role has commitments and knowledge; the person playing it has initiative, attention and disclosure habits. Swap participant profiles across roles without rewriting the case.
5. **The simulation is inspectable.** Trace who encountered information, what was available in their context, what they said and what changed. Interesting transcripts are material for design, not proof of human enjoyment.

## What the research adds

Primary research on interactive stories supports investigating distinguishable consequences and perceived agency. Video-game research links autonomy and competence with enjoyment. Neither establishes that morally ambiguous dinner mysteries are superior. Practitioner methods add actionable tools: relationships with both attachment and conflict, optional first moves, and playable inner tensions. Experienced designers also warn that too many relationships can leave important connections unused. [Evidence and limitations](RESEARCH.md)

Six additional first-person accounts also support keeping a hybrid of short shared beats and free interaction open. They warn against assuming more freedom suits every group or equal secret counts produce equally worthwhile roles. [Review supplement](EXPERIENCE.md)

This points toward **fewer, richer, reachable opportunities**, not maximizing the number of possible interactions. The prior market evidence still applies: established sellers already combine goals, secrets and freeform conversation. Our proposed contribution is how we explore and refine the resulting experience, not a claim to have invented it.

## Defaults to test, not requirements to worship

| Working default | Why start here | When to change it |
|---|---|---|
| Eight roles eventually; four in the first experimental fixture | Makes local perspectives inspectable | Expand after one dilemma produces coherent downstream effects |
| Up to two highlighted disclosures per role | Keeps important guidance findable | Change when the role needs fewer/more, not to force symmetry |
| Two possible opening approaches | Reduces the blank-start problem | Remove redundancy or add an alternative for missing players |
| Optional portrayal cue | Helps a guest start acting without demanding performance | Replace anything tiring, embarrassing or necessary to solve the case |
| Six conversation windows per scene in the later scheduler | A bounded time model | Vary windows and duration; do not equate them with real minutes |
| Short actual dialogue, then per-player summaries | Preserves misunderstanding, persuasion and evasion | Use summaries for cheap broad sweeps only after comparing information loss |
| Ollama first | Local Python/model calls already work | Change model/backend if realistic-context tests expose limits |

## Concrete artifacts

- [Character sheet specification and Alice example](CHARACTER_CARD.md); [printable layout sketch](character-card.html).
- [Simulation architecture](SIMULATION.md): separate truth, observations, attention and player policies; event examples and scheduling rules.
- [Experiment design](EXPERIMENTS.md): context-sensitive choices, profile swaps, imperfect play and report format.
- [Free-game comparison](BENCHMARKS.md): what is accessible, what can be reused, and why to compare an existing game after a small original fixture.
- [Additional experience evidence](EXPERIENCE.md) and [teams/improvisation](SOCIAL_DEDUCTION.md).
- [Implementation work packages](../TASKS.md#current-design-and-simulation-work-packages): small dependent slices with acceptance checks.
- [Decisions and open hypotheses](DECISIONS.md): what was retained, changed and deferred from the voice discussion.

## The first implementation slice

A local command-line runner loads a four-role experimental situation, constructs private contexts, records a short exchange and shows each participant's view. Begin with recorded responses to verify routing, then use Ollama. One encounter should include an opportunity to choose, not an automatically triggered confession. A later paired comparison supplies different relevant information before the same dilemma. Then map a freely available external scenario, subject to its terms, before investing in a complete original game. The game and simulator should develop together at the level of small situations first.

That slice can demonstrate machinery and produce design material. It cannot demonstrate an enjoyable three-hour mystery. Expand only when the traces are coherent enough to learn from; if they expose a flawed scheduler or confused instructions, simplify before adding more features. The prior 16–36-hour harness estimate excludes the richer card authoring, group-mode work and human testing; re-estimate after the first realistic-context benchmark.

## Boundaries and next decision

This pass delivers the blueprint, researched rationale, layout sketch and task breakdown. It does not draft a full murder, run new simulations, recruit people or start a campaign. The owner need not choose every parameter. Before actual implementation, the concrete proposal to review is the first local slice above and the experiment limits in EXPERIMENTS.md. A full setting and commercial scope can remain open while that small research fixture is developed.

Later human sessions should be scarce, valuable corrections: capture surprises, misunderstandings and meaningful choices rather than demand statistical validation before any creative work. A public video may help explain the experiment and eventually recruit volunteers; that remains an untested route. Public presentation stays independent of Alexander branding, and the free/paid asset boundary still needs a deliberate decision.
