# NebulaStream: A Stream Processing Engine from the Inside Out

A book about NebulaStream's internals, modeled after Garcia-Molina /
Ullman / Widom's *Database Systems: The Complete Book*, Petrov's
*Database Internals*, and Kleppmann's *Designing Data-Intensive
Applications*.

**Status.** Draft. Phase 0 / Phase 1 of the writing plan
(see `WRITING_PLAN.md`). Chapter 15 is the first complete draft
("smoke test" chapter for voice and tooling). The remaining 21
chapters and 3 appendices are stubs.

## Building the book

This project uses [Quarto](https://quarto.org). With Quarto and a
LuaLaTeX distribution installed:

```bash
# Render to HTML (fast)
quarto render --to html

# Render to PDF (slow; requires LuaLaTeX)
quarto render --to pdf

# Live-preview while editing
quarto preview
```

The output goes into `_book/`.

## Repository layout

```
nebulastream-book/
├── _quarto.yml          # book configuration (parts, formats, filters)
├── index.qmd            # preface
├── references.qmd       # bibliography page
├── references.bib       # BibTeX entries
├── chapters/            # 22 chapter files
│   ├── 01-why-streaming.qmd
│   ├── ...
│   └── 22-open-problems.qmd
├── appendices/          # build, conventions, glossary
└── figures/             # TikZ, mermaid, draw.io
```

## Pinning NebulaStream

Code listings and file-path references in this book target
`origin/main` (currently HEAD `1a61e63d54`). The pinned reference
is recorded in `PINNED_COMMIT`. Drift is checked nightly by CI:
every cited file path and line range must still resolve in the
pinned tree.

**Earlier drafts pinned `cd3ef68c73`** — a feature branch
(`feat/scheduling-paper-latency-instrumentation`) of the user's
local checkout. That branch was *behind* `origin/main` on the
distribution layer (`nes-distributed/` and `nes-network/` had
landed on main but were absent on the feature branch). The
chapters affected by the re-pin (most visibly Chapter 19)
have been updated; see the `Status` callout at the top of each
chapter.

## License

Prose: CC BY-SA 4.0.
Code excerpts: Apache-2.0, inherited from upstream NebulaStream.
See `LICENSE` and `LICENSE-CODE`.

## Contributing

This book is a work in progress. Errata, corrections, and pull requests
welcome. Each chapter requires review from at least one DIMA / BIFOLD
maintainer before merge.
