# Style Guide for Chapter Authors

The book is written in one coherent style — Kleppmann's narrative
voice, Petrov's structure, and Garcia-Molina/Ullman/Widom's worked
examples. Read Chapter 15 first; it is the canonical reference for
voice and conventions.

## Voice

- **First-person plural.** "We will see…" not "you will see."
- **Opinionated.** Articulate the trade-off behind every design
  choice. If you say "NebulaStream chose X", say *why*, and what was
  given up by not choosing Y.
- **Honest about gaps.** Where the live code differs from a published
  design document, name the difference and explain it. The
  caveat-callout (`.callout-warning`) is built for this.
- **No marketing language.** "Efficient", "robust", "scalable" are
  banned unless quantified.

## Structure of a chapter

1. Opening (1–2 paragraphs). Motivation, not summary.
2. Numbered sections (`## 15.1 ...`). 6–10 per chapter.
3. Mermaid or TikZ diagram per major concept.
4. Worked examples (`callout-note title="Example X.Y"`) every 3–8
   pages.
5. At most three Real-system reference sidebars
   (`callout-tip title="Real-system reference: ..."`), each ≤ ½ page.
6. Summary section.
7. Reading exercises (3–5, `callout-important`). Each must point at a
   real test in `nes-systests/`, a real flag in `cmake-build-debug/`,
   or a real subprocess command. **No problem-set-style exercises.**
8. References. BibTeX keys go in `references.bib` and are cited via
   `[@key]`.

## Code listings

- Always cite the source file and line range as a comment on the
  listing's first line: `// nes-query-engine/TaskQueue.hpp:34-44`.
- Maximum 25 lines per listing. Split or elide rather than going
  longer.
- The `include-code-files` Quarto filter can pull listings directly
  from `vendor/nebulastream/`. Prefer that over copy-pasting once the
  submodule is wired up; copy-paste rots.

## File paths

- Use full repository-relative paths in monospace:
  `nes-query-engine/TaskQueue.hpp`.
- For the absolute path on the author's machine, use only when
  motivating "go look at this": `/Users/zeuchste/git/nebulastream/...`.
- Do not invent paths. If you are not sure a path exists, grep for it.

## Diagrams

- **Mermaid** for sequence/state/flow. Renders in HTML; uses
  `mermaid-diagram` codeblocks.
- **TikZ** for print-quality figures going into the PDF. Source lives
  next to the chapter.
- **draw.io** (`.drawio.svg`) for figures a non-LaTeX contributor
  needs to edit.

Figure style guide (colors, arrow conventions) lives in
`figures/STYLE.md` once we have one. Lock it before Phase 2.

## Real-system references — what counts

Acceptable comparisons:

- Apache Flink
- Apache Spark Streaming / Structured Streaming
- Materialize / Differential / Timely
- Hyper / Umbra
- Arroyo
- Kafka Streams (sparingly)

Hard limit: ≤ ½ page each. The book is about NebulaStream; sidebars
illuminate, they do not survey.

## Status callout at the top of every chapter

Every chapter (and stub) opens with a `callout-warning` or
`callout-note` indicating its status:

- **stub** — placeholder only
- **outline** — section headings drafted, no prose
- **first draft** — prose drafted, awaiting review
- **maintainer review** — under review by a DIMA/BIFOLD maintainer
- **complete** — reviewed and accepted

## Pinning

Every claim that names a specific commit, line range, or numeric
constant must be true at the pinned commit (`PINNED_COMMIT` file at
repo root). The nightly drift check is your safety net but not your
correctness proof — verify manually before submitting a chapter.
