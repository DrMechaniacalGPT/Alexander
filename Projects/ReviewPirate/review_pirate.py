#!/usr/bin/env python3

import json
import sys
from collections import defaultdict
from pathlib import Path


def load(path):
    with Path(path).open("r", encoding="utf-8") as handle:
        return json.load(handle)


def fmt_confidence(value):
    if value is None:
        return "unknown"
    return f"{round(float(value) * 100)}%"


def validate(data):
    errors = []
    product_ids = {p.get("id") for p in data.get("products", [])}
    source_ids = {s.get("id") for s in data.get("sources", [])}

    for index, claim in enumerate(data.get("claims", []), start=1):
        if claim.get("product_id") not in product_ids:
            errors.append(f"claim {index}: unknown product_id {claim.get('product_id')!r}")
        if claim.get("source_id") not in source_ids:
            errors.append(f"claim {index}: unknown source_id {claim.get('source_id')!r}")

    for q_index, question in enumerate(data.get("decision_questions", []), start=1):
        for o_index, outcome in enumerate(question.get("outcomes", []), start=1):
            if outcome.get("product_id") not in product_ids:
                errors.append(
                    f"decision question {q_index}, outcome {o_index}: "
                    f"unknown product_id {outcome.get('product_id')!r}"
                )

    return errors


def source_label(source):
    title = source.get("title", source.get("id", "unknown source"))
    url = source.get("url")
    if url:
        return f"[{title}]({url})"
    return title


def render_decision_questions(data, products):
    questions = data.get("decision_questions", [])
    if not questions:
        return []

    lines = ["## Questions that change the answer", ""]

    for question in questions:
        lines.append(f"### {question.get('prompt', 'question')}")
        lines.append("")
        for outcome in question.get("outcomes", []):
            product = products.get(outcome.get("product_id"), outcome.get("product_id"))
            when = outcome.get("when", "if this matters")
            reason = outcome.get("reason", "")
            lines.append(f"- **{when}** → **{product}** — {reason}")
        lines.append("")

    return lines


def render_sources(data):
    sources = data.get("sources", [])
    if not sources:
        return []

    lines = ["## Source ledger", ""]

    for source in sources:
        relationship = source.get("financial_relationship", "unknown")
        first_hand = source.get("first_hand", "unknown")
        kind = source.get("kind", "unknown")
        lines.append(
            f"- {source_label(source)} — {kind}; "
            f"first hand: {first_hand}; financial relationship: {relationship}"
        )

    lines.append("")
    return lines


def render(data):
    errors = validate(data)
    if errors:
        raise ValueError("\n".join(errors))

    products = {p["id"]: p["name"] for p in data.get("products", [])}
    sources = {s["id"]: s for s in data.get("sources", [])}

    grouped = defaultdict(lambda: defaultdict(list))
    for claim in data.get("claims", []):
        grouped[claim["product_id"]][claim["topic"]].append(claim)

    lines = [f"# {data.get('comparison', 'Review Pirate report')}", ""]
    lines += render_decision_questions(data, products)
    lines += ["## Evidence map", ""]

    for product_id, topics in grouped.items():
        lines += [f"### {products.get(product_id, product_id)}", ""]

        for topic, claims in sorted(topics.items()):
            lines += [f"#### {topic}", ""]

            support = sum(c.get("stance") == "support" for c in claims)
            oppose = sum(c.get("stance") == "oppose" for c in claims)
            qualify = sum(c.get("stance") == "qualify" for c in claims)

            lines.append(
                f"{support} positive / {oppose} negative / {qualify} qualifying signals"
            )

            if support and oppose:
                lines.append("")
                lines.append("**conflict detected — do not flatten this**")

            lines.append("")

            for claim in claims:
                source = sources[claim["source_id"]]
                lines.append(
                    f"- **{claim.get('stance', 'unknown')}** — {claim.get('claim', '')} "
                    f"({claim.get('evidence_type', 'unknown')}, "
                    f"confidence {fmt_confidence(claim.get('confidence'))}) — "
                    f"{source_label(source)}"
                )

                if claim.get("note"):
                    lines.append(f"  - note: {claim['note']}")

            lines.append("")

    lines += render_sources(data)
    return "\n".join(lines).rstrip() + "\n"


def main():
    if len(sys.argv) != 2:
        print("usage: python3 review_pirate.py path/to/data.json", file=sys.stderr)
        raise SystemExit(2)

    try:
        data = load(sys.argv[1])
        output = render(data)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"review pirate sank: {exc}", file=sys.stderr)
        raise SystemExit(1)

    print(output, end="")


if __name__ == "__main__":
    main()
