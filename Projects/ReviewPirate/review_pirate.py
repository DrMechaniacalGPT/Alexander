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


def render(data):
    products = {p["id"]: p["name"] for p in data.get("products", [])}
    sources = {s["id"]: s for s in data.get("sources", [])}

    grouped = defaultdict(lambda: defaultdict(list))
    for claim in data.get("claims", []):
        grouped[claim["product_id"]][claim["topic"]].append(claim)

    lines = [f"# {data.get('comparison', 'Review Pirate report')}", ""]

    for product_id, topics in grouped.items():
        lines += [f"## {products.get(product_id, product_id)}", ""]

        for topic, claims in sorted(topics.items()):
            lines += [f"### {topic}", ""]

            support = sum(c.get("stance") == "support" for c in claims)
            oppose = sum(c.get("stance") == "oppose" for c in claims)
            qualify = sum(c.get("stance") == "qualify" for c in claims)

            lines.append(
                f"evidence map: {support} support / {oppose} oppose / {qualify} qualify"
            )

            if support and oppose:
                lines.append("")
                lines.append("**conflict detected**")

            lines.append("")

            for claim in claims:
                source = sources.get(claim.get("source_id"), {})
                title = source.get("title", claim.get("source_id", "unknown source"))
                url = source.get("url")
                if url:
                    title = f"[{title}]({url})"

                lines.append(
                    f"- **{claim.get('stance', 'unknown')}** — {claim.get('claim', '')} "
                    f"({claim.get('evidence_type', 'unknown')}, "
                    f"confidence {fmt_confidence(claim.get('confidence'))}) — {title}"
                )

                if claim.get("note"):
                    lines.append(f"  - note: {claim['note']}")

            lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def main():
    if len(sys.argv) != 2:
        print("usage: python3 review_pirate.py path/to/data.json", file=sys.stderr)
        raise SystemExit(2)

    data = load(sys.argv[1])
    print(render(data), end="")


if __name__ == "__main__":
    main()
