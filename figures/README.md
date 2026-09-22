# Figures

One script per figure, one shared style module. Every figure in the report is
generated here so the palette, type, and conventions stay identical across the
document.

## Running

```bash
uv run --with matplotlib python figures/fig_scifact_arms.py
```

Each script writes two files beside itself: a `.pdf` for the document and a
`.png` for quick review. Overleaf takes the PDF; the PNG is never referenced.

## Including a figure

```latex
\begin{figure}[h]
  \centering
  \includegraphics[width=\linewidth]{figures/scifact_arms.pdf}
  \caption{ScholarQABench SciFact accuracy by tool access, claude-sonnet-5,
  mean of five repeat runs. Error bars are 95\% confidence intervals of the
  mean over the five runs, so they show run-to-run variation rather than
  sampling error within a run. An agent with Redpine Science access answers
  6.6 points more claims correctly than the same agent with no retrieval, a
  relative gain of 7.6\%.}
  \label{fig:scifact-arms}
\end{figure}
```

## Before the first compile

Set `TEXT_WIDTH_IN` in `redpine_style.py` to the document's real text width.
Put `\the\textwidth` anywhere in `main.tex`, compile, and read the value off
the page; it prints in points, so divide by 72.27 for inches. Authoring the
figure at the true text width and including it at `width=\linewidth` means the
PDF is never rescaled, which keeps the label sizes exactly as set here. If the
figure is authored too narrow, LaTeX stretches it and every label grows with
it, which is how a document ends up with a different font size in every figure.

## Conventions

These are deliberate, and a new figure should not quietly break them.

- **Palette.** Brand colours for every system: Redpine Science is Crimson,
  Redpine Science plus web search is Orange, web search alone is Sky Blue. A
  colour means the same thing on every page.
- **One deliberate exception.** The no-retrieval baseline uses `BASELINE_GREY`
  (`#9E9892`), which is not a brand colour. The palette's only grey is
  `#171717`, which reads as black at bar size and drowns the other bars. The
  exception is for data marks only and never touches type or rules. Do not
  extend it: a second off-palette colour is how a palette stops being one.
- **Bars start at zero.** A truncated axis turns a 6.6 point gap into a visual
  doubling, and this report's whole argument is that the numbers are modest and
  real.
- **No title inside the figure.** The caption is the title, and it is numbered,
  referenced, and editable without regenerating a PDF.
- **No headline number inside the figure**, for the same reason.
- **Value labels on every bar**, so no one measures against the gridlines.
- **Error bars only where they mean something**, and the caption says what they
  are. An error bar with no stated definition is worse than none.
- **Two spines, light horizontal gridlines behind the data**, no box, no
  shadows, no rounded corners, per the brand brief.
- **Transparent background**, so the figure sits on the page's own paper rather
  than carrying a slightly different white.
- Fonts are embedded as Type 42, so the PDF stays vector and searchable.

## Adding a figure

Copy `fig_scifact_arms.py`, keep the module-level docstring naming where the
numbers came from (log filenames, branch, and what was excluded), and import
the style module rather than setting any rcParam locally.
