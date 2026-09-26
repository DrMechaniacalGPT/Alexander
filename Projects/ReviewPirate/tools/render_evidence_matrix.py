#!/usr/bin/env python3

import csv
import html
import sys
from pathlib import Path

PRODUCTS = [
    ("Saros 10R", "Roborock Saros 10R"),
    ("MOVA V70", "MOVA V70 Ultra Complete"),
    ("Curv 2 Flow", "Roborock Qrevo Curv 2 Flow"),
    ("Qrevo Curv", "Roborock Qrevo Curv"),
    ("Dreame X60", "Dreame X60 Max Ultra Complete"),
    ("Eufy E25", "Eufy Omni E25"),
    ("Shark PD", "Shark PowerDetect UV Reveal"),
    ("S8 MaxV", "Roborock S8 MaxV Ultra"),
]

SOURCES = [
    "RTINGS",
    "Vacuum Wars",
    "The Hook Up",
    "TechRadar",
    "Tom's Guide",
    "Expert Reviews",
    "WIRED",
    "Good Housekeeping",
    "Reddit owners",
    "Amazon owners",
]

FILL = {
    "winner": "#2f7d4a",
    "positive": "#8fbd76",
    "mixed": "#e6b85c",
    "critical": "#b85450",
    "neutral": "#a9a49a",
}

TEXT = "#171717"
BG = "#f4f1ea"
GRID = "#d5cfc3"


def esc(value):
    return html.escape(str(value), quote=True)


def load(path):
    rows = {}
    with Path(path).open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            rows[(row["source"], row["product"])] = row
    return rows


def render(rows):
    width = 1920
    height = 1080
    left = 330
    top = 230
    cell_w = 180
    cell_h = 70

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        f'<rect width="100%" height="100%" fill="{BG}"/>',
        f'<text x="90" y="90" font-family="Arial,sans-serif" font-size="56" font-weight="700" fill="{TEXT}">Same category. Different evidence maps.</text>',
        f'<text x="90" y="145" font-family="Arial,sans-serif" font-size="26" fill="#6f695f">Blank = no verified substantive coverage in the current research packet</text>',
    ]

    for c, (short, full) in enumerate(PRODUCTS):
        x = left + c * cell_w + cell_w / 2
        parts.append(
            f'<text x="{x}" y="{top-34}" text-anchor="middle" font-family="Arial,sans-serif" '
            f'font-size="19" font-weight="700" fill="{TEXT}">{esc(short)}</text>'
        )

    for r, source in enumerate(SOURCES):
        y = top + r * cell_h
        parts.append(
            f'<text x="{left-24}" y="{y+44}" text-anchor="end" font-family="Arial,sans-serif" '
            f'font-size="22" font-weight="700" fill="{TEXT}">{esc(source)}</text>'
        )

        for c, (_, product) in enumerate(PRODUCTS):
            x = left + c * cell_w
            row = rows.get((source, product))
            fill = "#ffffff"
            stroke = GRID
            stroke_w = 2
            label = ""

            if row:
                fill = FILL.get(row["direction"], FILL["neutral"])
                stroke_w = 5 if row["depth"] in {"deep", "owner_long_term"} else 2
                label = "★" if row["direction"] == "winner" else "●"

            parts.append(
                f'<rect x="{x+5}" y="{y+5}" width="{cell_w-10}" height="{cell_h-10}" '
                f'rx="12" fill="{fill}" stroke="{stroke}" stroke-width="{stroke_w}"/>'
            )
            if label:
                parts.append(
                    f'<text x="{x+cell_w/2}" y="{y+46}" text-anchor="middle" '
                    f'font-family="Arial,sans-serif" font-size="27" font-weight="700" fill="#ffffff">{label}</text>'
                )

    legend_y = 985
    legend = [
        ("winner", "winner / top pick"),
        ("positive", "positive"),
        ("mixed", "mixed / conditional"),
        ("critical", "critical"),
    ]
    x = 350
    for key, label in legend:
        parts.append(f'<rect x="{x}" y="{legend_y}" width="28" height="28" rx="6" fill="{FILL[key]}"/>')
        parts.append(
            f'<text x="{x+40}" y="{legend_y+22}" font-family="Arial,sans-serif" '
            f'font-size="20" fill="{TEXT}">{esc(label)}</text>'
        )
        x += 300

    parts.append(
        f'<text x="90" y="1045" font-family="Arial,sans-serif" font-size="20" fill="#6f695f">Review Pirate • coverage is not consensus • commercial context is tracked separately</text>'
    )
    parts.append("</svg>")
    return "\n".join(parts)


def main():
    if len(sys.argv) != 3:
        raise SystemExit("usage: render_evidence_matrix.py source_product_matrix.csv output.svg")
    Path(sys.argv[2]).write_text(render(load(sys.argv[1])), encoding="utf-8")


if __name__ == "__main__":
    main()
