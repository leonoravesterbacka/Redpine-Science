"""Quadrant four mean DCG@5 by system, pooled across both judges.

Data provenance. Same pooled judging pass as fig_quadrant4_precision.py (see
that script's docstring for the full experimental setup). Per-query DCG@5
values below are the two judges' 30-query batches concatenated into one list
of 60, read directly from connect-eval-fresh's raw_scores.json (added
alongside the summary aggregates specifically so a real, per-query-derived
confidence interval could be computed here, rather than a fabricated one or
none at all):

    runs/relevance_judging_jin_30/raw_scores.json    ["systems"][system]["per_query_dcg"]
    runs/relevance_judging_zihan_30/raw_scores.json  ["systems"][system]["per_query_dcg"]

The pooled mean matches the aggregate already reported in this report's prose
("7.85"/"4.83") to two decimal places -- the earlier version of this figure
carried no error bar at all, since only the pooled aggregate was available at
the time, not a per-query list to derive real dispersion from.

Run:  uv run --with matplotlib python figures/fig_quadrant4_dcg.py
"""

import statistics
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from redpine_style import (  # noqa: E402
    ARM_COLORS, DARK_GREY, apply_style, figure, label_bars, save,
)

OUT = Path(__file__).resolve().parent / "quadrant4_dcg"

# Per-query DCG@5, pooled across both judges' 30-query batches (60 values
# per system): relevance_judging_jin_30's 30 values followed by
# relevance_judging_zihan_30's 30 values, in query order within each batch.
PER_QUERY_DCG = {
    "redpine": [
        7.202601495740551, 8.801553605799326, 5.0716717421690936, 9.976307110209634,
        6.879135676952785, 9.914700798564784, 7.152841291421868, 5.148712314377457,
        2.6350587306158695, 10.793836475517569, 4.02371901428583, 7.765988484187327,
        6.510065430524243, 7.010065430524243, 2.0616063116448506, 5.827594795832177,
        8.21444760306672, 4.510065430524243, 7.658777744901699, 6.823465818787765,
        6.948459118879392, 6.841248379593765, 10.50180680129739, 4.966241679685392,
        6.127341600334113, 4.870877047725932, 9.432483359370783, 10.77605391471157,
        9.27605391471157, 9.906983668283027,
        7.385072130432616, 4.966241679685392, 10.531976968374654, 4.765988484187327,
        10.293836475517569, 8.271924937667158, 8.845377356638176, 10.045630552136242,
        6.432483359370782, 5.202601495740551, 9.101300410301262, 8.371418546671029,
        10.793836475517569, 6.892789260714372, 8.896918237758785, 6.845377356638177,
        8.406983668283027, 10.732230163872718, 10.232230163872718, 10.345377356638176,
        9.793836475517569, 10.906983668283027, 8.020130861048486, 9.732230163872718,
        9.476307110209634, 5.3969182377587845, 7.652841291421868, 8.845377356638176,
        10.363159917444175, 9.732230163872718,
    ],
    "pubmed": [
        0.0, 0.0, 0.8868528072345416, 3.922959427791637, 1.9922828697182435,
        8.583517849495262, 1.1309297535714575, 0.0, 1.5177825608059992,
        2.7541423768611586, 0.6309297535714575, 4.166494875183456, 2.0616063116448506,
        6.714447603066719, 1.5, 2.922959427791637, 4.239947294154475,
        3.1487123143774567, 4.809812235026179, 6.353635985865029, 4.958524549403635,
        5.4525880959238044, 5.740488793099571, 0.43067655807339306, 3.4484591188793923,
        1.1309297535714575, 8.133278053813944, 4.184818934934552, 0.0,
        8.845377356638176,
        2.5616063116448506, 5.265988484187327, 9.901047214803196, 0.8613531161467861,
        0.9306765580733931, 0.0, 9.662906721946111, 2.6309297535714578,
        5.892789260714372, 0.0, 11.793836475517569, 9.089454302975092,
        2.8613531161467862, 11.793836475517569, 6.827594795832177, 8.1587777449017,
        6.361353116146786, 9.793836475517569, 7.510065430524243, 6.77605391471157,
        9.00180680129739, 11.363159917444175, 5.702601495740551, 5.8969182377587845,
        7.589454302975093, 2.9484591188793923, 4.809812235026179, 6.335311926113934,
        10.793836475517569, 6.827594795832177,
    ],
}

ORDER = ["redpine", "pubmed"]
LABELS = {"redpine": "Redpine Science", "pubmed": "PubMed"}

# 95% CI of the mean over 60 pooled per-query values, two-sided t, 59 df.
T_CRIT_59DF = 2.0010


def mean_and_ci(values):
    mean = statistics.mean(values)
    half_width = T_CRIT_59DF * statistics.stdev(values) / len(values) ** 0.5
    return mean, half_width


def main():
    apply_style()
    fig, ax = figure()

    means, errors = [], []
    for system in ORDER:
        mean, half_width = mean_and_ci(PER_QUERY_DCG[system])
        means.append(mean)
        errors.append(half_width)

    x = range(len(ORDER))
    bars = ax.bar(
        x, means, width=0.5, color=[ARM_COLORS[s] for s in ORDER], zorder=2,
    )
    ax.errorbar(
        x, means, yerr=errors, fmt="none",
        ecolor=DARK_GREY, elinewidth=0.9, capsize=3.5, capthick=0.9, zorder=3,
    )
    label_bars(ax, bars, means, fmt="{:.2f}", offset=max(errors) + 0.15)

    # A bar chart is read by comparing heights, so the axis starts at zero.
    ax.set_ylim(0, 10)
    ax.set_yticks([0, 2, 4, 6, 8, 10])
    ax.set_ylabel("Mean DCG@5")
    ax.set_xticks(list(x))
    ax.set_xticklabels([LABELS[s] for s in ORDER])
    ax.tick_params(axis="x", length=0)
    ax.grid(axis="x", visible=False)

    out = save(fig, OUT)
    for system, mean, half_width in zip(ORDER, means, errors):
        print(f"{LABELS[system]:16s} {mean:.4f} +/- {half_width:.4f}")
    print("wrote", out)


if __name__ == "__main__":
    main()
