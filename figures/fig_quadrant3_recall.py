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

Exact found-counts at each rank cutoff, derived from each system's rank
distribution (1-10) and cross-checked against the percentages above:

    System    Recall@1 (k/n)   Recall@5 (k/n)   Recall@10 (k/n)
    Redpine   466/668          538/668          555/668
    Exa       420/668          505/668          518/668
    Tavily    263/668          353/668          366/668

Error bars are a Wald (normal-approximation) 95% confidence interval for a
binomial proportion, computed here from these exact counts -- the same
method fig_quadrant4_precision.py uses for its own Precision@5 bars.

nDCG is reported in the main text's table, not this figure, which covers only
the three recall cutoffs. MRR was dropped from the report entirely (2026-09-25,
"keep it simple and few metrics tracked") -- kept in the data-provenance table
above as a factual record of what was measured, not because it appears
anywhere in the paper. Do not mix in Gemini or Bing numbers from the same
project: those showed run-to-run flip rates of 10-13% on this benchmark, a
different reliability class, not a like-for-like point estimate with the
three systems plotted here.

Run:  uv run --with matplotlib python figures/fig_quadrant3_recall.py
"""

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from redpine_style import (  # noqa: E402
    ARM_COLORS, DARK_GREY, apply_style, bar_style, figure, label_bars, save,
)

OUT = Path(__file__).resolve().parent / "quadrant3_recall"

N_QUERIES = 668

# (found, n) at each rank cutoff, one tuple per rank, in RANKS order.
COUNTS = {
    "redpine": [(466, N_QUERIES), (538, N_QUERIES), (555, N_QUERIES)],
    "exa":     [(420, N_QUERIES), (505, N_QUERIES), (518, N_QUERIES)],
    "tavily":  [(263, N_QUERIES), (353, N_QUERIES), (366, N_QUERIES)],
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

Z_95 = 1.959963984540054  # two-sided normal critical value at 95%


def proportion_and_ci(k, n):
    """Wald 95% CI for a binomial proportion, in percentage points."""
    p = k / n
    half_width = Z_95 * math.sqrt(p * (1 - p) / n)
    return p * 100, half_width * 100


def main():
    apply_style()
    fig, ax = figure()

    centers = range(len(RANKS))
    n_systems = len(ORDER)

    for i, system in enumerate(ORDER):
        values, errors = [], []
        for k, n in COUNTS[system]:
            value, half_width = proportion_and_ci(k, n)
            values.append(value)
            errors.append(half_width)

        offset = (i - (n_systems - 1) / 2) * BAR_WIDTH
        x = [c + offset for c in centers]
        bars = ax.bar(
            x, values, width=BAR_WIDTH,
            **bar_style(ARM_COLORS[system]), label=LABELS[system], zorder=2,
        )
        ax.errorbar(
            x, values, yerr=errors, fmt="none",
            ecolor=DARK_GREY, elinewidth=0.8, capsize=2.5, capthick=0.8, zorder=3,
        )
        label_bars(ax, bars, values, offset=max(errors) + 1.0)

    # A bar chart is read by comparing heights, so the axis starts at zero.
    ax.set_ylim(0, 100)
    ax.set_yticks([0, 20, 40, 60, 80, 100])
    ax.set_ylabel("Recall (%)")
    ax.set_xticks(list(centers))
    ax.set_xticklabels(RANKS)
    ax.tick_params(axis="x", length=0)
    ax.grid(axis="x", visible=False)
    # Above the axes entirely, not "upper left" inside them -- inside, the
    # legend box sat directly over the Recall@1 group's value labels.
    ax.legend(loc="lower left", bbox_to_anchor=(0.0, 1.0), ncol=3, borderaxespad=0.3)

    out = save(fig, OUT)
    for system in ORDER:
        for rank_label, (k, n) in zip(RANKS, COUNTS[system]):
            value, half_width = proportion_and_ci(k, n)
            print(f"{LABELS[system]:16s} {rank_label:10s} "
                  f"{value:5.1f}% +/- {half_width:.1f}  ({k}/{n})")
    print("wrote", out)


if __name__ == "__main__":
    main()
