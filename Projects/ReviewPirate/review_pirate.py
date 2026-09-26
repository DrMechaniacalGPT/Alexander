#!/usr/bin/env python3

import argparse
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
    question_ids = set()

    for index, claim in enumerate(data.get("claims", []), start=1):
        if claim.get("product_id") not in product_ids:
            errors.append(f"claim {index}: unknown product_id {claim.get('product_id')!r}")
        if claim.get("source_id") not in source_ids:
            errors.append(f"claim {index}: unknown source_id {claim.get('source_id')!r}")

    for q_index, question in enumerate(data.get("decision_questions", []), start=1):
        qid = question.get("id")
        if not qid:
            errors.append(f"decision question {q_index}: missing id")
        elif qid in question_ids:
            errors.append(f"decision question {q_index}: duplicate id {qid!r}")
        else:
            question_ids.add(qid)

        for o_index, outcome in enumerate(question.get("outcomes", []), start=1):
            if outcome.get("product_id") not in product_ids:
                errors.append(
                    f"decision question {q_index}, outcome {o_index}: "
                    f"unknown product_id {outcome.get('product_id')!r}"
                )
            if "answer" not in outcome:
                errors.append(
                    f"decision question {q_index}, outcome {o_index}: missing answer"
                )

    return errors


def validate_profile(data, profile):
    known = {q.get("id") for q in data.get("decision_questions", [])}
    return [
        f"profile: unknown question id {key!r}"
        for key in profile
        if key not in known
    ]


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
            answer = outcome.get("label", str(outcome.get("answer")).lower())
            reason = outcome.get("reason", "")
            lines.append(f"- **{answer}** -> **{product}** — {reason}")
        lines.append("")

    return lines


def render_profile(data, products, profile):
    if profile is None:
        return []

    questions = {q.get("id"): q for q in data.get("decision_questions", [])}
    matches = []

    for qid, answer in profile.items():
        question = questions.get(qid)
        if not question:
            continue

        for outcome in question.get("outcomes", []):
            if outcome.get("answer") == answer:
                matches.append(
                    (
                        question.get("prompt", qid),
                        products.get(outcome.get("product_id"), outcome.get("product_id")),
                        outcome.get("reason", ""),
                    )
                )

    lines = ["## For this buyer", ""]

    if not matches:
        lines += [
            "none of the current decision rules fire",
            "",
            "that is useful information too",
            "",
        ]
        return lines

    for prompt, product, reason in matches:
        lines.append(f"- **{product}** — {reason}")
        lines.append(f"  - because: {prompt}")

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


def render(data, profile=None):
    errors = validate(data)
    if profile is not None:
        errors += validate_profile(data, profile)
    if errors:
        raise ValueError("\n".join(errors))

    products = {p["id"]: p["name"] for p in data.get("products", [])}
    sources = {s["id"]: s for s in data.get("sources", [])}

    grouped = defaultdict(lambda: defaultdict(list))
    for claim in data.get("claims", []):
        grouped[claim["product_id"]][claim["topic"]].append(claim)

    lines = [f"# {data.get('comparison', 'Review Pirate report')}", ""]
    lines += render_profile(data, products, profile)
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


def parse_args():
    parser = argparse.ArgumentParser(
        description="turn structured review evidence into a readable map"
    )
    parser.add_argument("data", help="comparison JSON")
    parser.add_argument(
        "--profile",
        help="optional buyer profile JSON keyed by decision-question id",
    )
    return parser.parse_args()


def main():
    args = parse_args()

    try:
        data = load(args.data)
        profile = load(args.profile) if args.profile else None
        output = render(data, profile)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"review pirate sank: {exc}", file=sys.stderr)
        raise SystemExit(1)

    print(output, end="")


if __name__ == "__main__":
    main()
