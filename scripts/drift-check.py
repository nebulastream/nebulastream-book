#!/usr/bin/env python3
"""Drift check for the NebulaStream book.

Walks every .qmd file under chapters/ and appendices/ and verifies that:

  1. Every monospace-quoted file path under nes-* still exists in the
     pinned NebulaStream tree.
  2. Every code-listing comment of the form
     `// <relative-path>:<start>-<end>` references a file that exists
     and a line range that is within the file's actual length.

A miss is reported as a warning (exit 1 only if --strict is passed).

The pinned tree is configured by the NES_TREE environment variable;
otherwise it defaults to /Users/zeuchste/git/nebulastream. In CI, this
should point at a checked-out submodule pinned to PINNED_COMMIT.
"""

from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
from pathlib import Path

DEFAULT_TREE = Path(os.environ.get("NES_TREE", "/Users/zeuchste/git/nebulastream"))
DEFAULT_REF = os.environ.get("NES_REF", "origin/main")

# A path must contain at least one '/' (to distinguish e.g. "nes-repl"
# the binary name from "nes-repl/something" the directory) OR end with
# a recognised file extension. Single-segment module names like
# "nes-common" still match because they end with the implicit "/".
PATH_RE = re.compile(
    r"`(nes-[a-zA-Z0-9_-]+"
    r"(?:/[a-zA-Z0-9_./-]+)?"
    r"(?:\.(?:hpp|cpp|h|md|test|cmake|inc|g4))?"
    r")`"
)


def looks_like_path(ref: str, view: GitRefView) -> bool:
    """Heuristic: a bare 'nes-foo' is a path only if it exists as a directory."""
    if "/" in ref or "." in ref:
        return True
    return view.path_exists(ref)
LISTING_RE = re.compile(
    r"//\s*(nes-[a-zA-Z0-9_/.-]+\.(?:hpp|cpp|h|inc)):(\d+)-(\d+)"
)


def find_qmd_files(root: Path):
    for d in ("chapters", "appendices", "."):
        for p in (root / d).glob("*.qmd"):
            yield p


class GitRefView:
    """Lookup paths against a git ref (e.g. 'origin/main') instead of the working tree.

    Falls back to working-tree lookup if the ref isn't available.
    """

    def __init__(self, tree: Path, ref: str | None) -> None:
        self.tree = tree
        self.ref = ref
        self.available = ref is not None and self._ref_exists()

    def _ref_exists(self) -> bool:
        try:
            subprocess.run(
                ["git", "-C", str(self.tree), "rev-parse", "--verify", self.ref],
                check=True, capture_output=True,
            )
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False

    def path_exists(self, path: str) -> bool:
        if self.available:
            try:
                subprocess.run(
                    ["git", "-C", str(self.tree), "cat-file", "-e", f"{self.ref}:{path}"],
                    check=True, capture_output=True,
                )
                return True
            except subprocess.CalledProcessError:
                # cat-file -e fails for non-existent or directory entries; try ls-tree for dirs
                try:
                    out = subprocess.run(
                        ["git", "-C", str(self.tree), "ls-tree", "--name-only",
                         self.ref, path],
                        check=True, capture_output=True, text=True,
                    )
                    return bool(out.stdout.strip())
                except subprocess.CalledProcessError:
                    return False
        return (self.tree / path).exists()

    def line_count(self, path: str) -> int | None:
        if self.available:
            try:
                out = subprocess.run(
                    ["git", "-C", str(self.tree), "show", f"{self.ref}:{path}"],
                    check=True, capture_output=True, text=True,
                )
                return out.stdout.count("\n") + (0 if out.stdout.endswith("\n") else 1)
            except subprocess.CalledProcessError:
                return None
        full = self.tree / path
        if not full.exists():
            return None
        try:
            with full.open("r", encoding="utf-8", errors="replace") as f:
                return sum(1 for _ in f)
        except OSError:
            return None


def check_path_reference(view: GitRefView, ref: str) -> str | None:
    if view.path_exists(ref):
        return None
    return f"missing path: {ref}"


def check_listing(view: GitRefView, ref: str, start: int, end: int) -> str | None:
    if not view.path_exists(ref):
        return f"listing references missing file: {ref}:{start}-{end}"
    lines = view.line_count(ref)
    if lines is None:
        return f"could not read {ref}"
    if start < 1 or end < start or end > lines:
        return f"listing range out of bounds: {ref}:{start}-{end} (file has {lines} lines)"
    return None


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--book-root",
        type=Path,
        default=Path(__file__).resolve().parent.parent,
        help="Path to the book repo root (default: parent of scripts/).",
    )
    parser.add_argument(
        "--tree",
        type=Path,
        default=DEFAULT_TREE,
        help="Path to the pinned NebulaStream tree (the git repo).",
    )
    parser.add_argument(
        "--ref",
        type=str,
        default=DEFAULT_REF,
        help=("Git ref (branch, tag, or sha) to validate paths against. "
              "Defaults to origin/main. Use --ref '' to use the working "
              "tree instead."),
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Exit non-zero if any warnings are emitted.",
    )
    args = parser.parse_args(argv)

    if not args.tree.exists():
        print(f"error: NebulaStream tree not found at {args.tree}", file=sys.stderr)
        return 2

    ref = args.ref or None
    view = GitRefView(args.tree, ref)
    if ref and not view.available:
        print(f"warning: git ref {ref!r} not found at {args.tree}; "
              f"falling back to working tree.", file=sys.stderr)

    warnings: list[str] = []
    files_checked = 0

    for qmd in find_qmd_files(args.book_root):
        files_checked += 1
        text = qmd.read_text(encoding="utf-8", errors="replace")

        for ref_path in set(PATH_RE.findall(text)):
            cleaned = ref_path.rstrip("/")
            if not looks_like_path(cleaned, view):
                continue
            err = check_path_reference(view, cleaned)
            if err:
                warnings.append(f"{qmd.name}: {err}")

        for m in LISTING_RE.finditer(text):
            listing_ref, start, end = m.group(1), int(m.group(2)), int(m.group(3))
            err = check_listing(view, listing_ref, start, end)
            if err:
                warnings.append(f"{qmd.name}: {err}")

    where = f"{args.tree} @ {ref}" if view.available else f"{args.tree} (working tree)"
    print(f"drift-check: scanned {files_checked} chapter/appendix files against {where}")
    if not warnings:
        print("drift-check: ok")
        return 0

    print(f"drift-check: {len(warnings)} warning(s):")
    for w in warnings:
        print(f"  - {w}")
    return 1 if args.strict else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
