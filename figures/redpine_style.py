"""Shared Redpine figure style for the Redpine Science report.

Every figure in the report imports this module, so the whole document shares one
palette, one type scale, and one set of plotting conventions. Import it, call
`apply_style()`, build the axes, then call `save()`.

Brand rules enforced here (see the Redpine brand brief):
  * the seven-colour palette only, nothing mixed or tinted
  * square corners everywhere, no shadows, no bevels
  * ABC Diatype for labels, falling back to Inter or Helvetica Neue as the brief
    allows, since ABC Diatype is a licensed face that may not be installed
  * Crimson and Dark Red mark Redpine's own results; comparison systems are
    never red

Plotting conventions, which are not brand rules but are why the figures read well:
  * bar charts start at zero, always
  * no chart title: the caption belongs in LaTeX, where it is numbered and
    referenced
  * horizontal reference lines only, behind the data, in a light grey
  * every bar is labelled with its value, so the reader never measures against
    the axis
  * error bars are drawn only where they mean something, and the caption must
    say what they are
"""

from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt

# === Palette ================================================================
# The seven brand colours. Nothing outside this dict ships in a figure.
DARK_RED = "#BD0519"
CRIMSON = "#EB301F"
ORANGE = "#FB8520"
WARM_WHITE = "#FDFBF7"
DARK_GREY = "#171717"
LIGHT_GREEN = "#628F6B"
SKY_BLUE = "#8BBCE5"

# Role assignments, fixed across the report so a colour means the same thing on
# every page. Redpine configurations are the two reds, so the reader can see at
# a glance which bars are ours; everything we are compared against is a neutral
# or a cool colour and never red.
# The one colour in this file that is not from the brand palette. The palette's
# only grey is Dark Grey (#171717), which reads as solid black at bar size and
# overpowers every other bar. This is a warm mid grey chosen to sit at roughly
# the same lightness as Sky Blue and Orange, so the baseline recedes without
# disappearing. Off-palette by deliberate exception, for data marks only: it
# never touches type, rules, or anything carrying the brand.
BASELINE_GREY = "#9E9892"

ARM_COLORS = {
    "redpine": CRIMSON,           # Redpine Science
    "redpine_first": ORANGE,      # Redpine Science plus web search
    "web": SKY_BLUE,              # web search, or any third-party system
    "closed_book": BASELINE_GREY,  # the no-retrieval baseline
}
ANNOTATION = DARK_RED

# === Geometry ===============================================================
# Width of the text block in the Springer Nature sn-jnl class, in inches.
# CHECK THIS ONCE: put \the\textwidth in main.tex, compile, and read the value
# off the PDF (it prints in points; divide by 72.27 for inches). Then set it
# here and include figures at [width=\linewidth] so nothing is ever rescaled.
# A figure authored at the true text width keeps the font sizes below exact.
TEXT_WIDTH_IN = 5.3

# Golden-ratio-ish default. Wider than tall reads better in a single column and
# leaves room for value labels above the bars.
DEFAULT_HEIGHT_IN = 3.1

# === Type ===================================================================
# ABC Diatype is the brand sans. The brief permits Inter or Helvetica Neue as
# fallbacks; DejaVu Sans is matplotlib's own last resort so a machine without
# any of them still renders rather than failing.
SANS_STACK = ["ABC Diatype", "Inter", "Helvetica Neue", "Helvetica", "DejaVu Sans"]

BASE_PT = 9      # tick labels and value labels
LABEL_PT = 9.5   # axis labels
SMALL_PT = 8     # footnotes inside the axes, legend entries


def apply_style():
    """Set the rcParams for every figure in the report. Call once per script."""
    mpl.rcParams.update({
        # Type
        "font.family": "sans-serif",
        "font.sans-serif": SANS_STACK,
        "font.size": BASE_PT,
        "axes.labelsize": LABEL_PT,
        "axes.titlesize": LABEL_PT,
        "xtick.labelsize": BASE_PT,
        "ytick.labelsize": BASE_PT,
        "legend.fontsize": SMALL_PT,

        # Colour
        "text.color": DARK_GREY,
        "axes.labelcolor": DARK_GREY,
        "xtick.color": DARK_GREY,
        "ytick.color": DARK_GREY,
        "axes.edgecolor": DARK_GREY,
        "figure.facecolor": "none",
        "axes.facecolor": "none",
        "savefig.facecolor": "none",
        "savefig.edgecolor": "none",

        # Frame: two spines, not four. Less ink, and the eye reads the bars.
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.linewidth": 0.8,
        "xtick.major.width": 0.8,
        "ytick.major.width": 0.8,
        "xtick.direction": "out",
        "ytick.direction": "out",

        # Reference lines sit behind the data and stay quiet.
        "axes.grid": True,
        "axes.axisbelow": True,
        "grid.color": "#D8D4CC",
        "grid.linewidth": 0.6,
        "grid.alpha": 1.0,

        # No rounded corners, no shadows, anywhere.
        "legend.frameon": False,
        "patch.linewidth": 0.0,
        "legend.fancybox": False,

        # Vector text in the PDF, so the figure stays searchable and sharp.
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
        "savefig.bbox": "tight",
        "savefig.pad_inches": 0.02,
    })


def figure(width_in=TEXT_WIDTH_IN, height_in=DEFAULT_HEIGHT_IN):
    """A figure sized to the document's text block."""
    return plt.subplots(figsize=(width_in, height_in))


def label_bars(ax, bars, values, fmt="{:.1f}", offset=0.9, color=DARK_GREY):
    """Print each bar's value above it, so no one reads values off the axis."""
    for bar, value in zip(bars, values):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + offset,
            fmt.format(value),
            ha="center", va="bottom", color=color, fontsize=BASE_PT,
        )


def save(fig, path):
    """Write the figure as a PDF, and a PNG beside it for quick review.

    Overleaf takes the PDF. The PNG is a convenience for looking at the result
    without opening a viewer, and is not referenced by the document.
    """
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path.with_suffix(".pdf"), transparent=True)
    # 600 dpi so the review PNG holds up when zoomed. The PDF is vector and has
    # no resolution at all, so nothing in the document depends on this number.
    fig.savefig(path.with_suffix(".png"), dpi=600, transparent=False,
                facecolor="white")
    plt.close(fig)
    return path.with_suffix(".pdf")
