r"""Quadrant three MRR and nDCG, side by side in one figure.

Two panels, one script, one PDF -- same reason fig_quadrant4_combined.py uses
this layout: a single wide image split into two subplots keeps the whole-
figure-to-\linewidth scale factor the same as every other figure in this
report, where two independently authored half-width images would not (each
would need re-authoring at half TEXT_WIDTH_IN to keep its point sizes correct
at the smaller display size).

Data provenance -- same single-shot retrieval eval as fig_quadrant3_recall.py
(see that script's docstring for the full experimental setup: n=668 queries,
Exa publication-retrieval benchmark, DOI-exact-else-title-substring
matching). MRR and nDCG are the two metrics already in the main text's table
that this figure adds a chart for:

    System    MRR      nDCG
    Redpine   0.7440   0.7651
    Exa       0.6865   0.7086
    Tavily    0.4521   0.4758

No error bars: MRR and nDCG here are single aggregate values per system, not
averages over a per-query list this script has access to, so there is no
real per-query dispersion to compute a confidence interval from. Per this
report's own rule (figures/README.md: "an error bar with no stated
definition is worse than none"), both panels are plain point estimates.

Run:  uv run --with matplotlib python figures/fig_quadrant3_mrr_ndcg.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from redpine_style import (  # noqa: E402
    ARM_COLORS, TEXT_WIDTH_IN, apply_style, bar_style, label_bars, save,
)

import matplotlib.pyplot as plt  # noqa: E402

OUT = Path(__file__).resolve().parent / "quadrant3_mrr_ndcg"

ORDER = ["redpine", "exa", "tavily"]
LABELS = {"redpine": "Redpine Science", "exa": "Exa", "tavily": "Tavily"}

MRR = {"redpine": 0.7440, "exa": 0.6865, "tavily": 0.4521}
NDCG = {"redpine": 0.7651, "exa": 0.7086, "tavily": 0.4758}


def _draw_panel(ax, values, *, ylabel):
    x = range(len(ORDER))
    bars = ax.bar(
        x, values, width=0.5,
        **bar_style([ARM_COLORS[s] for s in ORDER]), zorder=2,
    )
    label_bars(ax, bars, values, fmt="{:.3f}", offset=0.02)

    # A bar chart is read by comparing heights, so the axis starts at zero.
    ax.set_ylim(0, 1)
    ax.set_yticks([0, 0.2, 0.4, 0.6, 0.8, 1.0])
    ax.set_ylabel(ylabel)
    ax.set_xticks(list(x))
    ax.set_xticklabels([LABELS[s] for s in ORDER])
    ax.tick_params(axis="x", length=0)
    ax.grid(axis="x", visible=False)


def main():
    apply_style()
    fig, (ax_mrr, ax_ndcg) = plt.subplots(1, 2, figsize=(TEXT_WIDTH_IN, 3.1))

    mrr_values = [MRR[s] for s in ORDER]
    ndcg_values = [NDCG[s] for s in ORDER]
    _draw_panel(ax_mrr, mrr_values, ylabel="MRR")
    _draw_panel(ax_ndcg, ndcg_values, ylabel="nDCG")

    fig.tight_layout(w_pad=3.0)

    out = save(fig, OUT)
    print("MRR:")
    for system, value in zip(ORDER, mrr_values):
        print(f"  {LABELS[system]:16s} {value:.4f}")
    print("nDCG:")
    for system, value in zip(ORDER, ndcg_values):
        print(f"  {LABELS[system]:16s} {value:.4f}")
    print("wrote", out)


if __name__ == "__main__":
    main()
