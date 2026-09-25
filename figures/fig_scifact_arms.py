"""SciFact accuracy by arm, averaged over five Sonnet 5 runs.

Data provenance. Five repeat runs of the ScholarQABench SciFact subtask
(208 biomedical claims, true or false, scored by the source's own compute_match
rule) on claude-sonnet-5 via Bedrock. Per-run scores are read off the committed
logs in connect-external-benchmarks on branch results/scaled-study:

    scifact_20260911_110150   n=197
    scifact_20260915_132619   n=199
    scifact_20260915_140004   n=199
    scifact_20260915_145823   n=199
    scifact_20260915_150156   n=196

A claim is excluded from every arm of the run it falls in when the model refused
it with no answer in at least one arm, or when an arm call failed after retries.
Nine claims refuse deterministically on Sonnet 5 and a further one or two rows
per run were lost to Bedrock throttling, so runs differ in n. Run 1 was rescored
onto this rule on 2026-09-25, having first been scored with its refused claims
counted incorrect. Four further logs exist on disk and are superseded copies of
runs 2 to 5, not extra runs.
The arithmetic behind the published percentage is in that repo's
docs/CLAIM_MATH_2026-09-16.md.

Run:  uv run --with matplotlib python figures/fig_scifact_arms.py
"""

import statistics
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from redpine_style import (  # noqa: E402
    ARM_COLORS, DARK_GREY, apply_style, bar_style, figure, label_bars, save,
)

OUT = Path(__file__).resolve().parent / "scifact_arms"

# Per-run accuracy, in percent, one list per arm, five runs in order.
RUNS = {
    "closed_book":   [88.3, 86.9, 87.4, 87.4, 87.8],
    "web":           [92.4, 93.5, 94.0, 93.5, 92.3],
    "redpine":       [94.9, 93.5, 96.0, 94.5, 92.9],
    "redpine_first": [93.9, 93.0, 93.5, 94.5, 94.4],
}

# Plot order runs left to right from least to most tool access, so the bars
# tell the story in reading order rather than needing the caption to explain it.
ORDER = ["closed_book", "web", "redpine", "redpine_first"]

LABELS = {
    "closed_book": "No retrieval",
    "web": "Web search",
    "redpine": "Redpine Science",
    "redpine_first": "Redpine Science\nthen web",
}

# 95% CI of the mean over five runs, two-sided t with 4 degrees of freedom.
T_CRIT_4DF = 2.776


def mean_and_ci(values):
    mean = statistics.mean(values)
    half_width = T_CRIT_4DF * statistics.stdev(values) / len(values) ** 0.5
    return mean, half_width


def main():
    apply_style()
    fig, ax = figure()

    means, errors = [], []
    for arm in ORDER:
        mean, half_width = mean_and_ci(RUNS[arm])
        means.append(mean)
        errors.append(half_width)

    x = range(len(ORDER))
    bars = ax.bar(
        x, means, width=0.62,
        **bar_style([ARM_COLORS[arm] for arm in ORDER]),
        zorder=2,
    )
    ax.errorbar(
        x, means, yerr=errors, fmt="none",
        ecolor=DARK_GREY, elinewidth=0.9, capsize=3.5, capthick=0.9, zorder=3,
    )

    label_bars(ax, bars, means, offset=max(errors) + 0.5)

    # A bar chart is read by comparing heights, so the axis starts at zero.
    # Truncating it here would turn a 6.6 point gap into a visual doubling.
    ax.set_ylim(0, 105)
    ax.set_yticks([0, 20, 40, 60, 80, 100])
    ax.set_ylabel("Claims answered correctly (%)")
    ax.set_xticks(list(x))
    ax.set_xticklabels([LABELS[arm] for arm in ORDER])
    ax.tick_params(axis="x", length=0)
    ax.grid(axis="x", visible=False)

    # The headline gap is printed to stdout and belongs in the LaTeX caption,
    # not inside the axes: a number baked into the figure cannot be referenced,
    # cannot be corrected without regenerating the PDF, and competes with the
    # bars for attention.
    gap = means[ORDER.index("redpine")] - means[ORDER.index("closed_book")]
    print(f"headline gap: +{gap:.1f} points, "
          f"{100 * gap / means[0]:.1f}% relative")

    out = save(fig, OUT)
    for arm, mean, half_width in zip(ORDER, means, errors):
        print(f"{arm:14s} {mean:5.2f} +/- {half_width:.2f}")
    print("wrote", out)


if __name__ == "__main__":
    main()
