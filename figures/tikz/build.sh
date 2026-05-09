#!/usr/bin/env bash
# Compile every chXX-*.tex in this directory to an SVG via LaTeX → DVI → SVG.
#
# Why DVI → SVG? `dvisvgm` reads DVI directly and produces clean, scalable
# SVG output. Compared to pdflatex → pdf2svg, the DVI route preserves text
# as actual SVG text (not curves), so headings and labels stay searchable
# and re-styleable from CSS.
#
# Each .tex starts with `\input{_preamble.tex}` which sets `\documentclass{standalone}`,
# so the output crops to the diagram's bounding box automatically.

set -euo pipefail

cd "$(dirname "$0")"

# Use latex (not pdflatex) so we get a DVI that dvisvgm can consume directly.
# `--no-fonts` would emit text as paths; we want real text so we omit it.
TEXLIVE_BIN="$HOME/texlive/2024/bin/universal-darwin"
LATEX="$TEXLIVE_BIN/latex"
DVISVGM="$TEXLIVE_BIN/dvisvgm"

if [[ ! -x "$LATEX" || ! -x "$DVISVGM" ]]; then
    LATEX="$(command -v latex || true)"
    DVISVGM="$(command -v dvisvgm || true)"
fi

if [[ -z "$LATEX" || -z "$DVISVGM" ]]; then
    echo "error: need latex and dvisvgm in PATH or at $TEXLIVE_BIN" >&2
    exit 1
fi

# dvisvgm needs --libgs or a working ghostscript in some configs;
# for our standalone TikZ documents (no PostScript specials) the default works.
COMPILED=0
for tex in ch*-*.tex; do
    [[ -e "$tex" ]] || continue
    base="${tex%.tex}"
    echo "→ $tex"
    "$LATEX" -interaction=nonstopmode -halt-on-error "$tex" > "$base.compile.log" 2>&1 || {
        echo "  latex failed; see $base.compile.log"
        continue
    }
    "$DVISVGM" --no-fonts=0 --exact-bbox --bbox=papersize \
        "$base.dvi" -o "$base.svg" >> "$base.compile.log" 2>&1 || {
        echo "  dvisvgm failed; see $base.compile.log"
        continue
    }
    # Cleanup intermediates; keep the SVG and the log
    rm -f "$base.dvi" "$base.aux"
    COMPILED=$((COMPILED + 1))
    echo "  → $base.svg"
done

echo "build.sh: $COMPILED diagram(s) compiled"
