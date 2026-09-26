# Delivery and economics

**Conclusion:** a downloadable game can have a useful unit margin, but we have no acquisition, conversion or sales evidence for ours. It is not yet a credible war-chest forecast. All observations accessed September 26, 2026; [sources](../sources.csv).

## Evidence and assumptions

D023/D024 show one seller offering a $43.95 download and a $119.95 physical option; D025 shows a $65 small-group download. Those are asking prices, not our validated price or a median. D003 is a substantial free alternative. Price must reflect a reliably better or more convenient evening, not production effort alone.

The reproducible [model](model/economics.py) reads [inputs.json](model/inputs.json) and produces [results.md](model/results.md). It assumes US Etsy sales: 6.5% transaction, 3% processing, $0.20 listing plus $0.25 processing fixed per sold order (D026/D027). Listing renewals without sales, setup fees, currency conversion and jurisdiction-specific charges are not modeled; the fixed reserve is an assumption, not verification of these costs. Actual eligibility, listing terms and tax treatment need review before launch. Buyer-tax processing is a parameter; base excludes tax and a sensitivity includes 8%. Income taxes are excluded. No fee credits on refunds are assumed, conservatively.

Model equation per placed order:

`contribution = price × (1 − refund rate) − fees − delivery − CAC − support labor`

`full first-year result = orders × contribution − fixed cash − development labor`

CAC means total acquisition spend per order; it is not only ad spend. Organic acquisition is not inherently free. Development labor includes authoring, revisions and initial marketing preparation, but measured ongoing content/distribution work must also be included before judging profitability. Cash results assume founder labor is unpaid; full results value it. Support is $30/hour, development $35/hour × 120 hours, fixed cash $1,500. These are **scenario inputs**, not wage recommendations, a budget commitment or estimates derived from observed production.

| Scenario | Price / orders | Refund / CAC / support | Full first-year result |
|---|---|---|---:|
| Low | $39 / 100 | 8% / $20 / 15 min | −$5,302.50 |
| Base | $49 / 300 | 3% / $10 / 6 min | $3,052.50 |
| High | $59 / 1,000 | 2% / $5 / 4 min | $38,815.00 |

At base assumptions, full break-even is 196 orders. The $8,152.50 cash surplus at 300 orders is not profit after paying for all labor. $10,000 beyond costs requires 358 orders with unpaid founder labor or 539 with labor valued. No evidence currently supports any of these sales volumes, refund rates or CAC values. Bundling favorable assumptions into the high case does not establish that they can co-occur.

At hypothetical 2% conversion, 300 sales need 15,000 qualified visits. A $10 CAC would allow only $0.20 per paid click before other acquisition work. This exposes distribution as a major unknown rather than solving it. Sensitivities cover price, CAC, support, development time, tax processing and Etsy offsite fees. Offsite fees affect attributed orders; stressing every order at 15% is a boundary case, not the normal blended fee. Avoid double-counting the same offsite spend in measured CAC later.

## Delivery decisions

- **PDF first for validation:** negligible inventory; buyer printing/setup friction still real (D001/D003). An illustrative 40-page packet at D030's $0.34 starting copy price would cost $13.60 before finishing/tax. Page count is a scenario, not an authored packet specification; the New York store rate is not a local quote or guaranteed color price.
- **Physical kit later:** as an illustration only, 50 × $0.34 printing + $3 materials + $8 shipping + 20 minutes assembly at $30/hour = **$38 before platform fees, acquisition, refunds and support**. Those materials/shipping/time inputs are unquoted assumptions. At a $99 price they may be viable, but real specifications, geographic fulfillment and damage rates are missing. Do not claim a fulfillment quote was obtained.
- **App/video later:** no production quote or maintenance model was obtained. A new interface/cinematic treatment adds expense before core enjoyment is known. Their possible value remains open, not disproven.
- **Channel undecided:** Gumroad's opened pricing page lists 10% + $0.50 direct and 30% discovery (D029). An official help search excerpt adds card processing (D028), but its page body was inaccessible. Resolve the full fee schedule before modeling or choosing it; do not compare incomplete fee totals as if equivalent.

## Open-source fit

The repository has a root MIT license. We must discuss intended terms for the eventual story/pack before publishing it; this memo makes no legal determination about asset licensing. Selling tested, convenient packaging or service alongside accessible source may fit Alexander, but removes any assumption that exclusive text access alone sustains margins. The financial model does not include a proven moat, recurring revenue or repeat-customer benefit.

## Reproduce and verify

From `research/market/model/`:

```sh
python3 economics.py
python3 -m unittest discover -s . -v
```

Three tests check an independently hand-calculated base case and break-even boundary, zero-sales/negative-margin behavior, and fee/tax/acquisition sensitivity. No external dependencies. The narrower digital scenario is ready for inspection; original M05 remains partial because production quotes, video/app costs and measured demand are absent.
