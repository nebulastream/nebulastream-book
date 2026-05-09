# Writing Plan

This is the operational plan for drafting the book. The full strategic
plan (positioning, audience, risks) lives at
`/Users/zeuchste/.claude/plans/ok-my-plan-is-rustling-conway.md`.

## Currency audit (2026-05-09)

A live-tree-vs-draft audit found that the original first drafts were
anchored on time-stamped 2024 design documents and on a feature
branch (`cd3ef68c73`), both of which lagged `origin/main`. Findings:

| Claim | Status | Action |
|---|---|---|
| Distribution single-node only | **OUTDATED** — `nes-distributed` and `nes-network` are on `main`; ILP planner has landed | Rewrote Ch 19; updated Ch 1, 2, 14, 18, 22 |
| 16 nes-* modules | **OUTDATED** — main has 23 | Updated Ch 2 module table |
| FunctionRegistry is future work | **OUTDATED** — `LogicalFunctionRegistry` exists | Updated Ch 13 |
| No execution-state checkpointing | TRUE, but CLI metadata persistence exists at `~/.local/state/nebucli/` | Clarified in Ch 16 |
| All other audited claims | TRUE | No change |

**Re-pin:** `PINNED_COMMIT` was changed from the user's local feature
branch `cd3ef68c73` to `origin/main @ 1a61e63d54`. The chapters now
target `main`, not the feature branch.

**Methodological lesson** (added to preface): design docs are
historical context, not descriptions of current state. The
drift-check verifies path/line resolution but cannot verify
narrative match. Maintainer review (Phase 7) is the only defence.

## Phase status

| Phase | Duration | Status | Notes |
|-------|----------|--------|-------|
| 0 — Scoping & Greenlight | 4 wk | **complete (drafts)** | Repo bootstrapped; Ch 15 sample written; drift-check working. Pending: maintainer/DIMA greenlight, publisher conversation. |
| 1 — Skeleton + Reference Architecture | 6 wk | **complete (drafts)** | Ch 1 + Ch 2 drafted. |
| 2 — Foundations | 3 mo | **complete (drafts)** | Ch 3, 4, 5, 6 drafted. |
| 3 — Time and Connectors | 2 mo | **complete (drafts)** | Ch 7, 8 drafted. |
| 4 — Optimization & Compilation | 3 mo | **complete (drafts)** | Ch 9–13 drafted; Ch 12 (Nautilus) flagged for co-author review. |
| 5 — Runtime | 2 mo | **complete (drafts)** | Ch 14, 16, 17, 18 drafted. |
| 6 — Operations + Tail | 1.5 mo | **complete (drafts)** | Ch 19–22 + appendices A/B/C drafted. |
| 7 — Review & Copyedit | 2 mo | **not started** | Awaits maintainer review of all chapters; external technical review by 2-3 outside experts; copyedit pass. |
| 8 (optional) — Exercise Manual | 3 mo | **optional** | Companion problem book. |

## What "draft" means

All 22 chapters and 3 appendices have a first-pass draft written
against pinned NebulaStream commit `cd3ef68c73`. Drafts include:

- Status callout, intro paragraph, numbered sections.
- Worked examples (`callout-note title="Example X.Y"`).
- "Real-system reference" sidebars for major chapters (Ch 1-2,
  6-8, 10-13, 15-18, 21).
- Reading exercises (3-5 per chapter) pointing at real systests.
- Summary, References sections.
- Code listings cited by file path; drift-check passes.

What drafts do NOT include yet:

- Maintainer-validated technical accuracy (the book's biggest
  risk). Each chapter requires DIMA/BIFOLD review before merge.
- External technical review (Phase 7).
- Copyediting (Phase 7).
- TikZ figures for print quality (mermaid only at this stage).
- Final cross-references and index.
- The optional Companion Exercise Manual (Phase 8).

## Per-chapter status

| # | Title | Status | Reviewer needed |
|---|---|---|---|
| 1 | Why Stream Processing? | first draft | any DIMA member |
| 2 | System Tour | first draft | engine architect |
| 3 | Data Model | first draft | nes-data-types maintainer |
| 4 | Buffer Management | first draft | nes-memory maintainer |
| 5 | Query Language | first draft | nes-sql-parser maintainer |
| 6 | Logical Algebra | first draft | nes-logical-operators maintainer |
| 7 | Watermarks | first draft | watermark-doc author |
| 8 | Sources & Sinks | first draft | nes-sources/nes-sinks maintainer |
| 9 | Logical Optimisation | first draft | nes-query-optimizer maintainer |
| 10 | Physical Lowering | first draft | nes-physical-operators maintainer |
| 11 | Pipelining | first draft | nes-query-compiler maintainer |
| 12 | Nautilus / MLIR | first draft, **highest risk** | Nautilus co-author needed |
| 13 | Plugins | first draft | static-plugin-registry-doc author |
| 14 | Task Execution | first draft | nes-query-engine maintainer |
| 15 | Two-Queue Scheduler | first draft | nes-query-engine maintainer (smoke test) |
| 16 | Stateful Operators | first draft | nes-physical-operators maintainer |
| 17 | Error Handling | first draft | error-handling-doc author |
| 18 | Frontends | first draft | nes-frontend maintainer |
| 19 | Distributed Deployment | first draft | research lead (BIFOLD) |
| 20 | Testing | first draft | systest-doc author |
| 21 | Benchmarking | first draft | performance team |
| 22 | Open Problems | first draft | research lead |
| A | Build | first draft | any contributor |
| B | Conventions | first draft | tech lead |
| C | Glossary | first draft | tech lead |

## Phase 0 deliverables

- [x] Quarto book repo bootstrapped at `nebulastream-book/`
- [x] Chapter skeleton committed (22 chapters + 3 appendices)
- [x] Style guide drafted (`STYLE_GUIDE.md`)
- [x] Sample chapter Ch 15 first draft complete
- [x] Drift-check tooling working against pinned commit
- [x] All 21 remaining chapters + 3 appendices drafted
- [ ] Pin commit confirmed by maintainer
- [ ] DIMA/BIFOLD greenlight on positioning + outline
- [ ] Publisher conversation initiated (O'Reilly, MK, or Leanpub)
- [ ] Book repo migrated to `nebulastream/nebulastream-book` on GitHub

## Ordering rules for review (Phase 7)

- Each chapter requires ≥1 DIMA/BIFOLD maintainer review before
  merge to a "complete" status.
- Co-author chapters with deep-expertise dependencies:
  - **Ch 7** (Watermarks) — co-author with whoever owns the
    watermark code.
  - **Ch 12** (Nautilus / MLIR) — co-author with a Nautilus
    maintainer. **Highest priority for co-authoring.**
  - **Ch 15** (Two-Queue Scheduler) — review request to whoever
    owns `nes-query-engine/`.
  - **Ch 19** (Distributed Deployment) — review with research
    lead to ensure vision-vs-implementation line is drawn
    accurately.
- Cross-references between chapters are now possible (all chapters
  drafted). Forward references that target stub status should now
  resolve to drafted status everywhere.

## Drift management

- The drift-check (`scripts/drift-check.py`) runs against
  `/Users/zeuchste/git/nebulastream` and verifies every cited path
  and line range. Currently passes (0 warnings).
- For CI, wire the drift-check to a pinned NebulaStream submodule;
  fail the build only if the cited line range goes out of bounds,
  warn otherwise.
- An "edition refresh" at +12 months from v1 ship walks every
  drift warning and updates the prose.

## Schedule discipline

- Phase 7 (review and copyedit) is the next concrete step.
- Suggested order:
  1. Ch 12 (Nautilus) — highest accuracy risk; recruit co-author
     first.
  2. Ch 15 (sample chapter) — already drafted; quickest review.
  3. Ch 7 (watermarks) — second-highest risk; recruit co-author.
  4. Foundations (Ch 1-6) — broad-strokes review; small
     factual corrections.
  5. Remaining chapters in numerical order.
- Each review cycle: maintainer reads, leaves comments, primary
  author iterates, second pass.

-----
 Before "submittable to a publisher"                                                                                                                             
                                                                  
  Technical accuracy (the big one):                                                                                                                               
  - Per-chapter maintainer review by DIMA/BIFOLD. The per-chapter table in WRITING_PLAN.md lists who should review what. Ch 12 (Nautilus/MLIR) is highest risk and
   explicitly needs a co-author, not just a reviewer.                                                                                                             
  - External technical review by 2–3 outside experts (one Flink, one Materialize/Arroyo, one academic).
  - Pin NebulaStream as a vendor/ git submodule at a release tag, switch the drift-check to run against it, and re-add the include-code-files filter so listings  
  pull from the pinned tree instead of being copy-pasted inline.                                                                                                  
                                                                                                                                                                  
  Polish:                                                                                                                                                         
  - Bibliography. references.bib has 9 entries; chapters cite ~80 sources by author/title instead of [@key]. Every citation needs a real BibTeX entry.            
  - Acknowledgements section in index.qmd is still a placeholder.                                                                                                 
  - Authors field in _quarto.yml is "TBD".                       
  - Copyedit pass by a professional copy editor (consistency, voice, typos at scale).                                                                             
  - Back-of-book index — no index exists yet.                                        
  - TikZ figures for print quality. Right now everything is mermaid (fine for HTML, mediocre for print).                                                          
  - Cross-references between chapters are partial — @sec-foo works in some places, prose-form (see Chapter 12) in others. Make uniform.
  - Status callouts at the top of each chapter need to advance from "first draft" → "maintainer review" → "complete" as reviewers approve.                        
                                                                                                                                                                  
  Infrastructure:                                                                                                                                                 
  - CI for the book repo — GitHub Actions running drift-check + Quarto render on every PR. Currently only manual.                                                 
  - Publisher conversation — O'Reilly, MK Publishers, or self-publish via Leanpub.                                                                                
  - Migration to a real GitHub repo at nebulastream/nebulastream-book (currently lives only in your Downloads folder).
                                                                                                                                                                  
  Realistic remaining timeline                                                                                                                                    
                                                                                                                                                                  
  Per the original plan: Phase 7 (review + copyedit) is ~2 months, contingent on getting maintainer reviewers lined up. Phase 8 (a companion exercise manual with 
  traditional problems and solutions) is optional and adds ~3 months.                                                                                             
                                                                                                                                                                  
  The book has gone from zero to a complete-coverage first draft in this session, but the next mile — turning a first draft into a publishable manuscript — is    
  mostly humans-doing-careful-reading, which I cannot substitute for. The good news is the structural work is done: outline locked, drift-check working, voice
  consistent across 22 chapters.                                                                                                                                  
                                                                  
  Want me to fix the ieee.csl issue right now so HTML renders?     