r"""Quadrant two: the three judge metrics by arm, under two judges, in one figure.

Three panels, one per metric (claim coverage, contradiction rate, correctness),
each with the two arms under each of two judges. One wide image split into
subplots, for the same reason as fig_quadrant4_combined.py: the figure is
authored at the true text width so LaTeX never rescales the type.

Data provenance. The 179 expert-validated questions, both arms answered by
Claude Opus 5 (web search only; web search plus Redpine Science), judged per
gold claim. Two judges over the same stored answers:

    Sonnet 5 on Bedrock, pass A          the pre-registered judge
    TypeSafe Jev 1.13 via OpenRouter,    exploratory second judge,
    mean of passes J1 and J2             PREREGISTRATION.md amendment 2026-09-23

Numbers read off connect-eval on 2026-09-25, from the repo root:

    uv run python -m deepeval_pipeline.agreement.evidence.margins A
    uv run python -m deepeval_pipeline.agreement.evidence.margins J1,J2

for the per-arm means, and a per-arm 95 percent t interval of the mean
(n = 179, t = 1.973) computed over the same per-question scores that
margins.py loads. Correctness is the F1 of coverage and one minus the
contradiction rate, per question, as the report's methods define it.

Run:  uv run --with matplotlib python figures/fig_quadrant2_metrics.py
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt

sys.path.insert(0, str(Path(__file__).resolve().parent))

from redpine_style import (  # noqa: E402
    ARM_COLORS, DARK_GREY, TEXT_WIDTH_IN, apply_style, bar_style, save,
)

OUT = Path(__file__).resolve().parent / "quadrant2_metrics"

# Per judge, per metric, per arm: (mean, 95 percent t half-width), n = 179.
DATA = {
    "sonnet": {
        "claim_coverage":     {"web": (0.7016, 0.0444), "redpine": (0.8012, 0.0393)},
        "contradiction_rate": {"web": (0.0694, 0.0241), "redpine": (0.0382, 0.0167)},
        "correctness":        {"web": (0.7591, 0.0426), "redpine": (0.8467, 0.0346)},
    },
    "jev": {
        "claim_coverage":     {"web": (0.6962, 0.0446), "redpine": (0.7912, 0.0396)},
        "contradiction_rate": {"web": (0.1068, 0.0265), "redpine": (0.0775, 0.0230)},
        "correctness":        {"web": (0.7436, 0.0427), "redpine": (0.8277, 0.0361)},
    },
}

JUDGES = ["sonnet", "jev"]
JUDGE_LABELS = {"sonnet": "Sonnet 5", "jev": "Jev"}

# Web search only is the comparison arm; web search plus Redpine Science is
# Redpine's own result and takes the Crimson role, the only red in the chart.
ARMS = ["web", "redpine"]
ARM_LABELS = {"web": "Web search only", "redpine": "Web search plus Redpine Science"}

METRICS = [
    ("claim_coverage", "Claim coverage", (0, 1.0), [0, 0.2, 0.4, 0.6, 0.8, 1.0]),
    ("contradiction_rate", "Contradiction rate", (0, 0.2), [0, 0.05, 0.10, 0.15, 0.20]),
    ("correctness", "Correctness (F1)", (0, 1.0), [0, 0.2, 0.4, 0.6, 0.8, 1.0]),
]

BAR_WIDTH = 0.46
GROUP_GAP = 1.25    # distance between the two judges' pairs


def _draw_panel(ax, metric, ylabel, ylim, yticks):
    xs, means, errors, colors = [], [], [], []
    for j, judge in enumerate(JUDGES):
        for k, arm in enumerate(ARMS):
            mean, half = DATA[judge][metric][arm]
            xs.append(j * GROUP_GAP + (k - 0.5) * BAR_WIDTH)
            means.append(mean)
            errors.append(half)
            colors.append(ARM_COLORS[arm])
    bars = ax.bar(xs, means, width=BAR_WIDTH, **bar_style(colors), zorder=2)
    ax.errorbar(xs, means, yerr=errors, fmt="none", ecolor=DARK_GREY,
                elinewidth=0.9, capsize=3.0, capthick=0.9, zorder=3)
    # Value above each bar, clear of its error bar.
    for bar, mean, half in zip(bars, means, errors):
        ax.text(bar.get_x() + bar.get_width() / 2, mean + half + 0.012 * ylim[1],
                f"{mean:.2f}", ha="center", va="bottom", color=DARK_GREY, fontsize=7.5)
    # A bar chart is read by comparing heights, so every panel starts at zero.
    ax.set_ylim(*ylim)
    ax.set_yticks(yticks)
    ax.set_ylabel(ylabel)
    ax.set_xticks([j * GROUP_GAP for j in range(len(JUDGES))])
    ax.set_xticklabels([JUDGE_LABELS[j] for j in JUDGES])
    ax.set_xlim(-0.7, (len(JUDGES) - 1) * GROUP_GAP + 0.7)
    ax.tick_params(axis="x", length=0)
    ax.grid(axis="x", visible=False)
    return bars


def main():
    apply_style()
    fig, axes = plt.subplots(1, 3, figsize=(TEXT_WIDTH_IN, 2.7))
    first = None
    for ax, (metric, ylabel, ylim, yticks) in zip(axes, METRICS):
        bars = _draw_panel(ax, metric, ylabel, ylim, yticks)
        first = first or bars
    fig.legend(first[:2], [ARM_LABELS[a] for a in ARMS], loc="lower center",
               ncol=2, bbox_to_anchor=(0.5, -0.04), frameon=False)
    fig.tight_layout(w_pad=2.0, rect=(0, 0.06, 1, 1))

    out = save(fig, OUT)
    for judge in JUDGES:
        print(JUDGE_LABELS[judge])
        for metric, _, _, _ in METRICS:
            web, rp = DATA[judge][metric]["web"], DATA[judge][metric]["redpine"]
            print(f"  {metric:18} web {web[0]:.3f} +/- {web[1]:.3f}   redpine {rp[0]:.3f} +/- {rp[1]:.3f}"
                  f"   gap {rp[0] - web[0]:+.3f}")
    print("wrote", out)


if __name__ == "__main__":
    main()
