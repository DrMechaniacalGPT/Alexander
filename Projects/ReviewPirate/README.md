# Review Pirate

save people from opening seventeen tabs
then use the loot to fund more builds

Review Pirate turns a pile of reviews into a source-linked map of agreement, disagreement, and uncertainty.

It is not the philosophy project wearing a fake moustache.
It is a product.

## user problem

buying something expensive or complicated often means

- watching long videos
- reading repetitive reviews
- decoding affiliate incentives
- comparing different versions
- discovering too late that reviewers disagree about the one thing you care about

the useful output is not
"8.7 out of 10"

it is

- what people consistently agree on
- what people consistently dislike
- where experiences diverge
- which claims are measured
- which claims are vibes
- what matters for this particular buyer
- where the evidence came from

## product rule

every important claim should lead back to evidence

the pirate may summarize the map
but does not get to invent the islands

## v0

v0 is intentionally stupid

input:
a small JSON file containing products, sources, and claims

output:
a markdown report showing

- claim
- stance
- evidence type
- source
- confidence
- conflicts

the first goal is to learn whether the structure is useful
not to build a crawler that consumes the internet before breakfast

## eventual pipeline

1. collect sources
2. extract atomic claims
3. normalize claims that mean the same thing
4. label evidence type
5. detect support and contradiction
6. estimate confidence
7. condition the summary on the buyer
8. render the evidence map
9. send traffic back to original reviewers

## money

the product needs to make money
because the point is to fund more work

acceptable candidates:

- affiliate links with ranking isolated from payout
- paid subscription
- paid deep-dive reports
- referral fees that are fixed rather than bid for placement

hard rule:

payment cannot buy the conclusion

if the money can secretly move the ranking
we have simply invented a more literate ad

## first category

not chosen yet

good candidates have

- meaningful purchase price
- lots of conflicting reviews
- repeat questions
- measurable attributes
- enough reviewer depth to make synthesis useful

## run the prototype

```bash
python3 review_pirate.py data/sample.json
```

the report prints to stdout

redirect it if you want a file

```bash
python3 review_pirate.py data/sample.json > report.md
```

## status

prototype skeleton
not product
not treasure
yet
