# Contributing to the NebulaStream Book

Thanks for considering a contribution. The book is a draft and
benefits enormously from corrections, especially from people who
work on the parts of NebulaStream the chapters describe.

## Quick start

```bash
git clone https://github.com/nebulastream/nebulastream-book
cd nebulastream-book
make preview        # live HTML preview while you edit
```

You will need:
- [Quarto](https://quarto.org) >= 1.5
- A clone of [nebulastream/nebulastream](https://github.com/nebulastream/nebulastream)
  available locally so the drift-check can validate cited paths
- Optional: TeX Live (any recent distribution) for rebuilding the
  TikZ diagrams under `figures/tikz/`

## What kinds of contribution help most

Roughly in order of priority:

1. **Technical corrections.** Where prose diverges from current
   code behaviour, either fix the prose or open an issue describing
   the divergence. The chapters most likely to be wrong are flagged
   in `WRITING_PLAN.md` under the per-chapter review table.

2. **Worked examples.** The book follows a Garcia-Molina/Ullman/Widom
   convention of numbered "Example X.Y" callouts every few pages.
   Adding a worked example to a thinly-illustrated section is
   always welcome.

3. **Reading exercises** that point at real systests. Each chapter
   ships with 3–5 exercises pointing at `nes-systests/*.test`. Pull
   requests adding more are very welcome — see `STYLE_GUIDE.md` for
   the format.

4. **Diagrams.** The book uses TikZ rendered to SVG. New diagrams
   go under `figures/tikz/chXX-name.tex`; see existing diagrams
   for the pattern. Run `cd figures/tikz && ./build.sh` to compile.

5. **Bibliography.** If you cite a paper that isn't in
   `references.bib`, please add the BibTeX entry.

## Style

See `STYLE_GUIDE.md`. Short version: Kleppmann voice (first-person
plural, opinionated, willing to articulate trade-offs), Petrov
structure (curated tour, real-system reference sidebars under half
a page), Garcia-Molina/Ullman/Widom worked examples every few
pages. Reading exercises instead of traditional problem sets.

## What needs review

Every chapter PR requires review from a maintainer who knows the
relevant module. The current reviewer assignments live in
`WRITING_PLAN.md`'s per-chapter status table and in `.github/CODEOWNERS`.
The CODEOWNERS handles are placeholders today; we will replace them
with real team handles as the book moves through Phase 7 review.

## Drift check

Every cited file path and line range must resolve against the
pinned NebulaStream commit (recorded in `PINNED_COMMIT`).
The CI runs `scripts/drift-check.py --strict` against
`nebulastream/nebulastream@main` on every PR. Locally:

```bash
NES_TREE=/path/to/your/nebulastream NES_REF=origin/main \
    python3 scripts/drift-check.py
```

If your PR cites a file that doesn't exist on `main`, the check
will fail. Either correct the path or wait for the cited code
to land upstream.

## Licence

Prose is CC BY-SA 4.0 (see `LICENSE`). Code excerpts are inherited
from upstream NebulaStream under Apache 2.0 (see `LICENSE-CODE`).
By submitting a PR you agree your contribution is under CC BY-SA 4.0.
