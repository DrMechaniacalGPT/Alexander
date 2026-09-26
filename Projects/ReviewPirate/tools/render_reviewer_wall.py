#!/usr/bin/env python3

import csv
import html
import sys
from pathlib import Path

WIDTH = 1920
HEIGHT = 1080


def esc(value):
    return html.escape(str(value), quote=True)


def render(rows):
    margin = 120
    top = 230
    card_w = 800
    card_h = 150
    gap_x = 80
    gap_y = 38
    lefts = [margin, margin + card_w + gap_x]

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}">',
        '<rect width="100%" height="100%" fill="#f4f1ea"/>',
        '<text x="120" y="105" font-family="Arial, sans-serif" font-size="58" font-weight="700" fill="#141414">8 experts. 8 different “best” robot vacuums.</text>',
        '<text x="120" y="165" font-family="Arial, sans-serif" font-size="28" fill="#5d584f">Ranking snapshot observed September 25, 2026</text>',
    ]

    for i, row in enumerate(rows):
        col = i % 2
        r = i // 2
        x = lefts[col]
        y = top + r * (card_h + gap_y)
        parts.append(
            f'<rect x="{x}" y="{y}" width="{card_w}" height="{card_h}" '
            'rx="22" fill="#ffffff" stroke="#d9d3c6" stroke-width="2"/>'
        )
        parts.append(
            f'<text x="{x+30}" y="{y+45}" font-family="Arial, sans-serif" '
            f'font-size="24" font-weight="700" fill="#141414">{esc(row["source"])}</text>'
        )
        parts.append(
            f'<text x="{x+30}" y="{y+88}" font-family="Arial, sans-serif" '
            f'font-size="31" font-weight="700" fill="#141414">{esc(row["pick"])}</text>'
        )
        parts.append(
            f'<text x="{x+30}" y="{y+125}" font-family="Arial, sans-serif" '
            f'font-size="20" fill="#746e63">{esc(row["context"])}</text>'
        )

    parts.append(
        '<text x="120" y="1030" font-family="Arial, sans-serif" font-size="22" '
        'fill="#746e63">Review Pirate • “best” depends on candidate set, methodology, price, date, and buyer.</text>'
    )
    parts.append('</svg>')
    return "\n".join(parts)


def main():
    if len(sys.argv) != 3:
        raise SystemExit("usage: render_reviewer_wall.py rankings.csv output.svg")

    with Path(sys.argv[1]).open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))

    Path(sys.argv[2]).write_text(render(rows), encoding="utf-8")


if __name__ == "__main__":
    main()
