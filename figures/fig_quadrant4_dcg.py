"""Quadrant four mean DCG@5 by system, pooled across both judges.

Data provenance: same pooled judging pass as fig_quadrant4_precision.py (see
that script's docstring for the full provenance and run files). Read directly
from connect-eval-fresh's runs/relevance_judging_{jin,zihan}_30/summary.json,
weighted by each run's n_scored:

    System   Jin (n=149)   Zihan (n=150)   Pooled (n=299/298, connect/pubmed)
    Redpine     7.121          8.576              7.851
    PubMed      3.322          6.331              4.827

No error bar: the judging pipeline's summary.json carries only the pooled
mean DCG@5, not a per-query DCG list, so there is no real per-query
dispersion to compute a confidence interval from. Per this report's own rule
(figures/README.md: "an error bar with no stated definition is worse than
none"), this figure is a plain point estimate rather than a fabricated one.

Run:  uv run --with matplotlib python figures/fig_quadrant4_dcg.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from redpine_style import ARM_COLORS, apply_style, figure, label_bars, save  # noqa: E402

OUT = Path(__file__).resolve().parent / "quadrant4_dcg"

MEAN_DCG = {
    "redpine": 7.850922687029957,
    "pubmed": 4.826742820599355,
}

ORDER = ["redpine", "pubmed"]
LABELS = {"redpine": "Redpine Science", "pubmed": "PubMed"}


def main():
    apply_style()
    fig, ax = figure()

    values = [MEAN_DCG[s] for s in ORDER]
    x = range(len(ORDER))
    bars = ax.bar(
        x, values, width=0.5, color=[ARM_COLORS[s] for s in ORDER], zorder=2,
    )
    label_bars(ax, bars, values, fmt="{:.2f}", offset=0.15)

    # A bar chart is read by comparing heights, so the axis starts at zero.
    ax.set_ylim(0, 10)
    ax.set_yticks([0, 2, 4, 6, 8, 10])
    ax.set_ylabel("Mean DCG@5")
    ax.set_xticks(list(x))
    ax.set_xticklabels([LABELS[s] for s in ORDER])
    ax.tick_params(axis="x", length=0)
    ax.grid(axis="x", visible=False)

    out = save(fig, OUT)
    for system, value in zip(ORDER, values):
        print(f"{LABELS[system]:16s} {value:.3f}")
    print("wrote", out)


if __name__ == "__main__":
    main()
