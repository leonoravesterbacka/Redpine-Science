r"""Quadrant four Precision@5 and mean DCG@5, side by side in one figure.

Two panels, one script, one PDF -- the standard way to put two related bar
charts side by side in a LaTeX figure without breaking the "author at the
true rendered width, never let LaTeX rescale the font sizes out from under
you" rule this report's figures otherwise follow: a single wide image split
into two subplots keeps the whole-figure-to-\linewidth scale factor the same
as every other figure here, where two independently-authored half-width
images placed side by side would not (each would need re-authoring at half
TEXT_WIDTH_IN to keep its point sizes correct at the smaller display size).
Replaces the report's earlier single-panel quadrant4_precision.pdf; a DCG
panel was briefly a separate figure of its own (fig_quadrant4_dcg.py, removed
2026-09-23 -- "I just want the precision at 5 plot") and is reinstated here,
now as a second panel of the same figure rather than a second standalone one.

Data provenance, all three panelists now included (2026-09-25 -- the third
panelist's 30 questions landed, superseding an earlier two-judge, n=85 version
of this figure): three PhD-level domain experts each blind-score their own
batch of 30 subspecialty questions (neurology-mostly, cardiology,
rheumatology), plus 25 further questions cross-judged by two of the three for
an inter-rater agreement check (see quadrant four's Method section) --
115 questions in all. Top 5 results per system, 0-4 relevance scale,
single-shot retrieval (no agent loop), "relevant" = score >= 3 of 4. Read
directly from connect-eval-fresh's run outputs, each domain batch's own
summary.json/raw_scores.json plus the cross-judged 25's pooled per-item
average (judges' scores on a shared item averaged before pooling, so a
cross-judged question contributes one data point, not two).

Precision@5: relevant counts derived directly from the pooled item-level
scores (>= 2 of 4 counts as relevant -- one point looser than the >= 3
threshold the published relevance evaluation this report's Method section
cites uses; a deliberate choice for this report, not a match to their own
cutoff -- see main.tex's Method section for the same note). Pooled: Redpine
430/572 = 75.2%, PubMed 227/571 = 39.8%. Error bars are a Wald 95% CI for a
binomial proportion, from these exact pooled counts.

Mean DCG@5: per-query DCG@5 values from all three domain batches (90 values)
plus the 25 cross-judged questions' own pooled per-query DCG (each already an
average across whichever judges scored it) -- 115 values per system in query
order (Jin's 30, Zihan's 30, Nora's 30, then the 25 cross-judged). Error bars
are a two-sided t 95% CI of the mean over the 115 pooled per-query values
(114 df).

Run:  uv run --with matplotlib python figures/fig_quadrant4_combined.py
"""

import math
import statistics
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from redpine_style import (  # noqa: E402
    ARM_COLORS, DARK_GREY, TEXT_WIDTH_IN, apply_style, bar_style, label_bars, save,
)

import matplotlib.pyplot as plt  # noqa: E402

OUT = Path(__file__).resolve().parent / "quadrant4_metrics"

ORDER = ["redpine", "pubmed"]
LABELS = {"redpine": "Redpine Science", "pubmed": "PubMed"}

# --- Panel 1: Precision@5 ---------------------------------------------------
# Threshold >= 2 of 4 (not the >= 3 a published relevance evaluation's own
# threshold uses) -- a deliberate choice for this report, see docstring above.
PRECISION_COUNTS = {  # (relevant, n_scored), pooled across all three panelists' domain
    "redpine": (430, 572),  # batches plus the two-judge cross-judged 25
    "pubmed": (227, 571),
}
Z_95 = 1.959963984540054  # two-sided normal critical value at 95%


def proportion_and_ci(k, n):
    """Wald 95% CI for a binomial proportion, in percentage points."""
    p = k / n
    half_width = Z_95 * math.sqrt(p * (1 - p) / n)
    return p * 100, half_width * 100


# --- Panel 2: mean DCG@5 -----------------------------------------------------
# Per-query DCG@5, all three domain batches (90 values) plus the 25
# cross-judged questions' own pooled per-query value (115 per system), in
# query order: Jin's 30, Zihan's 30, Nora's 30, then the 25 cross-judged.
PER_QUERY_DCG = {
    "redpine": [
        7.202601495740551, 8.801553605799326, 5.0716717421690936, 9.976307110209634,
        6.879135676952785, 9.914700798564784, 7.152841291421868, 5.148712314377457,
        2.6350587306158695, 10.793836475517569, 4.02371901428583, 7.765988484187327,
        6.510065430524243, 7.010065430524243, 2.0616063116448506, 5.827594795832177,
        8.21444760306672, 4.510065430524243, 7.658777744901699, 6.823465818787765,
        6.948459118879392, 6.841248379593765, 10.50180680129739, 4.966241679685392,
        6.127341600334113, 4.870877047725932, 9.432483359370783, 10.77605391471157,
        9.27605391471157, 9.906983668283027, 7.385072130432616, 4.966241679685392,
        10.531976968374654, 4.765988484187327, 10.293836475517569, 8.271924937667158,
        8.845377356638176, 10.045630552136242, 6.432483359370782, 5.202601495740551,
        9.101300410301262, 8.371418546671029, 10.793836475517569, 6.892789260714372,
        8.896918237758785, 6.845377356638177, 8.406983668283027, 10.732230163872718,
        10.232230163872718, 10.345377356638176, 9.793836475517569, 10.906983668283027,
        8.020130861048486, 9.732230163872718, 9.476307110209634, 5.3969182377587845,
        7.652841291421868, 8.845377356638176, 10.363159917444175, 9.732230163872718,
        4.879135676952785, 7.845377356638177, 5.8969182377587845, 7.0716717421690936,
        2.7227062322935724, 5.0, 8.458524549403634, 3.335311926113934,
        10.793836475517569, 8.527847991330242, 8.75827135390557, 2.748205923381328,
        4.948459118879392, 3.922959427791637, 7.77605391471157, 8.670623852227868,
        7.6409951840957, 7.614953994062848, 4.908764345084952, 7.901047214803196,
        5.448459118879392, 4.0, 6.510065430524243, 2.3868528072345416,
        6.52371901428583, 3.692536065216308, 5.2719249376671575, 8.097171433256849,
        2.9484591188793923, 6.692536065216308, 7.7251329600883905, 7.033771044993326,
        8.63893035800448, 6.244076608767902, 7.477197448610597, 7.553347682417997,
        6.586486076235177, 4.562509712293545, 7.427721393581209, 2.6329942420936634,
        7.606333463132397, 6.196394630357187, 8.126180512460602, 5.488153555104817,
        8.529912479852449, 8.3237362306913, 9.069606916077873, 7.717415829806635,
        7.88003907760148, 9.976307110209634, 7.910842233423906, 7.271021199449448,
        6.488424304577365, 8.473338883469719, 8.258000604433022,
    ],
    "pubmed": [
        0.0, 0.0, 0.8868528072345416, 3.922959427791637,
        1.9922828697182435, 8.583517849495262, 1.1309297535714575, 0.0,
        1.5177825608059992, 2.7541423768611586, 0.6309297535714575, 4.166494875183456,
        2.0616063116448506, 6.714447603066719, 1.5, 2.922959427791637,
        4.239947294154475, 3.1487123143774567, 4.809812235026179, 6.353635985865029,
        4.958524549403635, 5.4525880959238044, 5.740488793099571, 0.43067655807339306,
        3.4484591188793923, 1.1309297535714575, 8.133278053813944, 4.184818934934552,
        0.0, 8.845377356638176, 2.5616063116448506, 5.265988484187327,
        9.901047214803196, 0.8613531161467861, 0.9306765580733931, 0.0,
        9.662906721946111, 2.6309297535714578, 5.892789260714372, 0.0,
        11.793836475517569, 9.089454302975092, 2.8613531161467862, 11.793836475517569,
        6.827594795832177, 8.1587777449017, 6.361353116146786, 9.793836475517569,
        7.510065430524243, 6.77605391471157, 9.00180680129739, 11.363159917444175,
        5.702601495740551, 5.8969182377587845, 7.589454302975093, 2.9484591188793923,
        4.809812235026179, 6.335311926113934, 10.793836475517569, 6.827594795832177,
        0.0, 5.2221647333484755, 0.0, 6.783771044993326,
        0.5, 0.0, 9.531976968374654, 4.52371901428583,
        3.510065430524243, 0.0, 5.07938887245085, 3.0177825608059994,
        4.966241679685392, 6.017782560805999, 5.8969182377587845, 2.3868528072345416,
        0.38685280723454163, 3.678882481454721, 3.4964118467626557, 3.335311926113934,
        2.379135676952785, 0.0, 1.761859507142915, 2.6309297535714578,
        0.0, 1.2737056144690833, 0.0, 2.6309297535714578,
        1.8868528072345416, 3.4484591188793923, 2.6110823666742378, 4.812780461766094,
        1.842409467467276, 6.87114779719848, 5.10722380153336, 0.0,
        3.7292622747018176, 7.564574200815751, 5.290868586346668, 0.0,
        0.5308031558224253, 0.31546487678572877, 6.420894601700416, 4.638026957355785,
        0.19342640361727081, 6.41883011317821, 0.8957440876375412, 5.344203206516934,
        6.914700798564783, 1.742012120245695, 3.837647164108688, 6.458524549403635,
        1.261859507142915, 0.0, 5.431579958722088,
    ],
}
T_CRIT_114DF = 1.9809922979375063  # two-sided t, 95%, 114 df


def mean_and_ci(values):
    mean = statistics.mean(values)
    half_width = T_CRIT_114DF * statistics.stdev(values) / len(values) ** 0.5
    return mean, half_width


def _draw_panel(ax, values, errors, *, ylabel, ylim, yticks, value_fmt):
    x = range(len(ORDER))
    bars = ax.bar(
        x, values, width=0.5,
        **bar_style([ARM_COLORS[s] for s in ORDER]), zorder=2,
    )
    ax.errorbar(
        x, values, yerr=errors, fmt="none",
        ecolor=DARK_GREY, elinewidth=0.9, capsize=3.5, capthick=0.9, zorder=3,
    )
    label_bars(ax, bars, values, fmt=value_fmt, offset=max(errors) + ylim[1] * 0.025)

    # A bar chart is read by comparing heights, so the axis starts at zero.
    ax.set_ylim(*ylim)
    ax.set_yticks(yticks)
    ax.set_ylabel(ylabel)
    ax.set_xticks(list(x))
    ax.set_xticklabels([LABELS[s] for s in ORDER])
    ax.tick_params(axis="x", length=0)
    ax.grid(axis="x", visible=False)


def main():
    apply_style()
    fig, (ax_precision, ax_dcg) = plt.subplots(
        1, 2, figsize=(TEXT_WIDTH_IN, 3.1),
    )

    precision_values, precision_errors = [], []
    for system in ORDER:
        k, n = PRECISION_COUNTS[system]
        value, half_width = proportion_and_ci(k, n)
        precision_values.append(value)
        precision_errors.append(half_width)
    _draw_panel(
        ax_precision, precision_values, precision_errors,
        ylabel="Precision@5 (%)", ylim=(0, 100), yticks=[0, 20, 40, 60, 80, 100],
        value_fmt="{:.1f}",
    )

    dcg_means, dcg_errors = [], []
    for system in ORDER:
        mean, half_width = mean_and_ci(PER_QUERY_DCG[system])
        dcg_means.append(mean)
        dcg_errors.append(half_width)
    _draw_panel(
        ax_dcg, dcg_means, dcg_errors,
        ylabel="Mean DCG@5", ylim=(0, 10), yticks=[0, 2, 4, 6, 8, 10],
        value_fmt="{:.2f}",
    )

    fig.tight_layout(w_pad=3.0)

    out = save(fig, OUT)
    print("Precision@5:")
    for system, value, half_width in zip(ORDER, precision_values, precision_errors):
        k, n = PRECISION_COUNTS[system]
        print(f"  {LABELS[system]:16s} {value:5.1f}% +/- {half_width:.1f}  ({k:.0f}/{n})")
    print("Mean DCG@5:")
    for system, mean, half_width in zip(ORDER, dcg_means, dcg_errors):
        print(f"  {LABELS[system]:16s} {mean:.4f} +/- {half_width:.4f}")
    print("wrote", out)


if __name__ == "__main__":
    main()
