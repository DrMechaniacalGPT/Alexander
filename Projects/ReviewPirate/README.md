# Review Pirate

save people from opening seventeen tabs
then use the loot to fund more builds

Review Pirate turns a pile of reviews into a source-linked map of agreement, disagreement, and uncertainty.

it is not the philosophy project wearing a fake moustache

it is a product

## user problem

buying something expensive or complicated often means

- watching long videos
- reading repetitive reviews
- decoding affiliate incentives
- comparing different versions
- discovering too late that reviewers disagree about the one thing you care about

the useful output is not

8.7 out of 10

it is

- what changes the answer
- what people consistently agree on
- what people consistently dislike
- where experiences diverge
- which claims are measured
- which claims are vibes
- where the evidence came from

## product rule

every important claim should lead back to evidence

the pirate may summarize the map
but does not get to invent the islands

## v0

v0 is intentionally stupid

input

a JSON file containing

- products
- buyer questions
- sources
- claims

output

a markdown report containing

- questions that change the answer
- product-by-topic evidence
- visible conflicts
- confidence labels
- source links
- source type and financial relationship

the first goal is to learn whether the structure is useful

not to build a crawler
that consumes the internet before breakfast

## first live comparison

Rapsodo MLM2PRO
vs
Square Golf Home Edition

why

the sticker prices are similar
but the purchase changes with

- indoor room depth
- outdoor use
- subscription tolerance
- practice priorities
- simulator software

that makes it a good test
for conditional recommendations

data

`data/mlm2pro-vs-square.json`

research notes

`research/mlm2pro-vs-square.md`

## run

sample

```bash
python3 review_pirate.py data/sample.json
```

live comparison

```bash
python3 review_pirate.py data/mlm2pro-vs-square.json
```

tests

```bash
python3 -m unittest -v
```

## eventual pipeline

1 collect sources
2 extract atomic claims
3 normalize claims that mean the same thing
4 label evidence type
5 detect support contradiction and qualification
6 estimate confidence
7 ask what changes the answer for the buyer
8 render the evidence map
9 send traffic back to original reviewers

## money

the product needs to make money

because the point is to fund more work

possible models

- affiliate links with ranking isolated from payout
- paid subscription
- paid deep-dive reports
- fixed referral fees

hard rule

payment cannot buy the conclusion

if the money can secretly move the ranking
we have invented
a more literate ad

## status

live hand-built dataset
working report generator
tests
CI definition

still missing the important part

users
