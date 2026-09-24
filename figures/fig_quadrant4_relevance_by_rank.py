"""Quadrant four: average relevance by rank, pooled across both judges.

Presented in the same shape as Consensus's own published relevance
evaluation -- see https://consensus.app/home/blog/consensus-outperforms-
google-scholar-for-academic-search-retrieval/, which reports "Average
Relevance by Rank" as its third headline metric alongside Precision and
DCG (both already charted in fig_quadrant4_combined.py). This is that same
metric for this report's panel: mean relevance (0-4 scale) at each of the
top 5 ranks, so a reader can see whether a system's advantage holds at
every position or is concentrated near the top.

Data provenance. Both judges' relevance_by_rank.csv (connect-eval-fresh),
pooled by rank across the two 30-query batches, weighted by each rank's n
(29 or 30, since one query per batch returned fewer than 5 results):

    runs/relevance_judging_jin_30/relevance_by_rank.csv
    runs/relevance_judging_zihan_30/relevance_by_rank.csv

    System   Rank   Jin (mean, n)     Zihan (mean, n)   Pooled mean   n
    Redpine  1      2.5333, 30        2.8667, 30        2.7000        60
    Redpine  2      2.5667, 30        3.1000, 30        2.8334        60
    Redpine  3      2.5000, 30        2.9000, 30        2.7000        60
    Redpine  4      2.1333, 30        2.8333, 30        2.4833        60
    Redpine  5      2.1379, 29        2.8000, 30        2.4746        59
    PubMed   1      0.9333, 30        2.1724, 29        1.5423        59
    PubMed   2      1.2667, 30        2.1333, 30        1.7000        60
    PubMed   3      1.1333, 30        2.4000, 30        1.7666        60
    PubMed   4      1.5667, 30        2.2667, 30        1.9167        60
    PubMed   5      0.9310, 29        1.8333, 30        1.3898        59

No error bars, matching Consensus's own choice not to show an uncertainty
band for this breakdown: they report it as a described pattern ("higher
average relevance at every position"), not a chart with intervals, and this
figure reports the same aggregate mean per rank they do.

Run:  uv run --with matplotlib python figures/fig_quadrant4_relevance_by_rank.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from redpine_style import (  # noqa: E402
    ARM_COLORS, apply_style, bar_style, figure, label_bars, save,
)

OUT = Path(__file__).resolve().parent / "quadrant4_relevance_by_rank"

# Pooled mean relevance (0-4 scale) at each rank, one list per system, in
# RANKS order.
RELEVANCE = {
    "redpine": [2.7000, 2.8334, 2.7000, 2.4833, 2.4746],
    "pubmed":  [1.5423, 1.7000, 1.7666, 1.9167, 1.3898],
}

ORDER = ["redpine", "pubmed"]
RANKS = ["Rank 1", "Rank 2", "Rank 3", "Rank 4", "Rank 5"]

LABELS = {"redpine": "Redpine Science", "pubmed": "PubMed"}

BAR_WIDTH = 0.36


def main():
    apply_style()
    fig, ax = figure()

    centers = range(len(RANKS))
    n_systems = len(ORDER)

    for i, system in enumerate(ORDER):
        offset = (i - (n_systems - 1) / 2) * BAR_WIDTH
        x = [c + offset for c in centers]
        bars = ax.bar(
            x, RELEVANCE[system], width=BAR_WIDTH,
            **bar_style(ARM_COLORS[system]), label=LABELS[system], zorder=2,
        )
        label_bars(ax, bars, RELEVANCE[system], fmt="{:.2f}", offset=0.08)

    # A bar chart is read by comparing heights, so the axis starts at zero.
    ax.set_ylim(0, 4)
    ax.set_yticks([0, 1, 2, 3, 4])
    ax.set_ylabel("Mean relevance (0-4 scale)")
    ax.set_xticks(list(centers))
    ax.set_xticklabels(RANKS)
    ax.tick_params(axis="x", length=0)
    ax.grid(axis="x", visible=False)
    ax.legend(loc="upper right")

    out = save(fig, OUT)
    for system in ORDER:
        values = "  ".join(f"{v:.2f}" for v in RELEVANCE[system])
        print(f"{LABELS[system]:16s} {values}")
    print("wrote", out)


if __name__ == "__main__":
    main()
