"""Quadrant four Precision@5 by system, pooled across both judges.

Data provenance. Two PhD-level domain experts each blind-score their own
batch of 30 subspecialty questions (one batch mostly neurology, the other
entirely cardiology), top 5 results per system, 0-4 relevance scale,
single-shot retrieval (no agent loop), matching a published relevance
evaluation's methodology (see quadrant four's Method section). "Relevant" is
score >= 3 of 4, the same threshold that evaluation uses. Read directly from
connect-eval-fresh's run outputs:

    runs/relevance_judging_jin_30/summary.json    n_scored=149 (connect), 149 (pubmed)
    runs/relevance_judging_zihan_30/summary.json  n_scored=150 (connect), 149 (pubmed)

Relevant counts, derived from each run's precision * n_scored (every one lands
on a whole number, confirming the arithmetic):

    System   Judge   n_scored   relevant
    Redpine  Jin       149         73
    Redpine  Zihan     150        103
    PubMed   Jin       149         31
    PubMed   Zihan     149         66

Pooled: Redpine 176/299 = 58.9%, PubMed 97/298 = 32.6%. Error bars are a
Wald (normal-approximation) 95% confidence interval for a binomial
proportion, computed here from the exact pooled counts -- not a repeated-run
CI like fig_scifact_arms.py's, since this is one pooled judging pass, not
five repeat runs.

Run:  uv run --with matplotlib python figures/fig_quadrant4_precision.py
"""

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from redpine_style import (  # noqa: E402
    ARM_COLORS, DARK_GREY, apply_style, bar_style, figure, label_bars, save,
)

OUT = Path(__file__).resolve().parent / "quadrant4_precision"

# (relevant, n_scored) per system, pooled across both judges' batches.
COUNTS = {
    "redpine": (176, 299),
    "pubmed": (97, 298),
}

ORDER = ["redpine", "pubmed"]
LABELS = {"redpine": "Redpine Science", "pubmed": "PubMed"}

Z_95 = 1.959963984540054  # two-sided normal critical value at 95%


def proportion_and_ci(k, n):
    """Wald 95% CI for a binomial proportion, in percentage points."""
    p = k / n
    half_width = Z_95 * math.sqrt(p * (1 - p) / n)
    return p * 100, half_width * 100


def main():
    apply_style()
    fig, ax = figure()

    values, errors = [], []
    for system in ORDER:
        k, n = COUNTS[system]
        value, half_width = proportion_and_ci(k, n)
        values.append(value)
        errors.append(half_width)

    x = range(len(ORDER))
    bars = ax.bar(
        x, values, width=0.5,
        **bar_style([ARM_COLORS[s] for s in ORDER]), zorder=2,
    )
    ax.errorbar(
        x, values, yerr=errors, fmt="none",
        ecolor=DARK_GREY, elinewidth=0.9, capsize=3.5, capthick=0.9, zorder=3,
    )
    label_bars(ax, bars, values, offset=max(errors) + 0.8)

    # A bar chart is read by comparing heights, so the axis starts at zero.
    ax.set_ylim(0, 100)
    ax.set_yticks([0, 20, 40, 60, 80, 100])
    ax.set_ylabel("Precision@5 (%)")
    ax.set_xticks(list(x))
    ax.set_xticklabels([LABELS[s] for s in ORDER])
    ax.tick_params(axis="x", length=0)
    ax.grid(axis="x", visible=False)

    out = save(fig, OUT)
    for system, value, half_width in zip(ORDER, values, errors):
        k, n = COUNTS[system]
        print(f"{LABELS[system]:16s} {value:5.1f}% +/- {half_width:.1f}  ({k:.0f}/{n})")
    print("wrote", out)


if __name__ == "__main__":
    main()
