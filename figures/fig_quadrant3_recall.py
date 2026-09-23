"""Quadrant three retrieval results: Recall@1/5/10 by system.

Data provenance. Single-shot retrieval eval (one call per system per query, no
agent loop, Consensus-style methodology) against the Exa publication-retrieval
benchmark, restricted to the 671 queries whose gold paper is confirmed present
in Redpine Science's corpus (publication_search_in_corpus_v3.jsonl). Three of
the 671 queries failed on a transient API error during the run and are
excluded rather than scored as misses, leaving n=668 actually scored. Matching
is exact DOI where a system returns one (only Redpine does), else a
normalized title substring match.

    System    n    Found   Recall@1   Recall@5   Recall@10   MRR      nDCG
    Redpine   668  555     69.76%     80.54%     83.08%      0.7440   0.7651
    Exa       668  518     62.87%     75.60%     77.54%      0.6865   0.7086
    Tavily    668  366     39.37%     52.84%     54.79%      0.4521   0.4758

MRR and nDCG are reported in the main text's table, not this figure, which
covers only the three recall cutoffs. Do not mix in Gemini or Bing numbers
from the same project: those showed run-to-run flip rates of 10-13% on this
benchmark, a different reliability class, not a like-for-like point estimate
with the three systems plotted here.

Run:  uv run --with matplotlib python figures/fig_quadrant3_recall.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from redpine_style import (  # noqa: E402
    ARM_COLORS, apply_style, figure, label_bars, save,
)

OUT = Path(__file__).resolve().parent / "quadrant3_recall"

# Recall at each rank cutoff, in percent, one list per system, in RANKS order.
RECALL = {
    "redpine": [69.76, 80.54, 83.08],
    "exa":     [62.87, 75.60, 77.54],
    "tavily":  [39.37, 52.84, 54.79],
}

# Plot order left to right within each rank group: Redpine first since it is
# the system this report is about, then the two comparison systems.
ORDER = ["redpine", "exa", "tavily"]
RANKS = ["Recall@1", "Recall@5", "Recall@10"]

LABELS = {
    "redpine": "Redpine Science",
    "exa": "Exa",
    "tavily": "Tavily",
}

BAR_WIDTH = 0.24


def main():
    apply_style()
    fig, ax = figure()

    centers = range(len(RANKS))
    n_systems = len(ORDER)

    for i, system in enumerate(ORDER):
        offset = (i - (n_systems - 1) / 2) * BAR_WIDTH
        x = [c + offset for c in centers]
        bars = ax.bar(
            x, RECALL[system], width=BAR_WIDTH,
            color=ARM_COLORS[system], label=LABELS[system], zorder=2,
        )
        label_bars(ax, bars, RECALL[system], offset=1.0)

    # A bar chart is read by comparing heights, so the axis starts at zero.
    ax.set_ylim(0, 100)
    ax.set_yticks([0, 20, 40, 60, 80, 100])
    ax.set_ylabel("Recall (%)")
    ax.set_xticks(list(centers))
    ax.set_xticklabels(RANKS)
    ax.tick_params(axis="x", length=0)
    ax.grid(axis="x", visible=False)
    ax.legend(loc="upper left")

    out = save(fig, OUT)
    for system in ORDER:
        values = "  ".join(f"{v:.1f}" for v in RECALL[system])
        print(f"{LABELS[system]:16s} {values}")
    print("wrote", out)


if __name__ == "__main__":
    main()
