#!/usr/bin/env bash
# Publish the rendered book to GitHub Pages via the gh-pages branch.
#
# This is the manual-deploy path that exists because the
# `nebulastream` GitHub organisation currently has Actions disabled
# at the org level, so .github/workflows/publish.yml cannot run.
# Once an org admin enables Actions for this repo, this script
# becomes redundant — the workflow takes over — but it remains
# safe to use as a fallback.
#
# What this does:
#   1. Renders the book to HTML via Quarto.
#   2. Stages the rendered output in a temp directory with a
#      `.nojekyll` marker (so GitHub doesn't try to Jekyll-process it).
#   3. Initialises a fresh git repo in that temp dir and force-pushes
#      it to origin/gh-pages.
#   4. Triggers a Pages build via the GitHub API (if `gh` is available).
#
# Force-push is intentional: gh-pages is a build artefact branch with
# no human-meaningful history.
#
# Usage:  make publish
#   or    ./scripts/publish.sh

set -euo pipefail

# Resolve the book root from this script's location.
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BOOK_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

cd "$BOOK_ROOT"

# 1. Render
echo "→ rendering to HTML"
if command -v quarto >/dev/null 2>&1; then
    QUARTO=quarto
elif [[ -x /Applications/quarto/bin/quarto ]]; then
    QUARTO=/Applications/quarto/bin/quarto
else
    echo "error: quarto not found in PATH or /Applications/quarto/bin" >&2
    exit 1
fi
"$QUARTO" render --to html >/dev/null

if [[ ! -d _book ]]; then
    echo "error: _book/ not produced by quarto render" >&2
    exit 1
fi

# 2. Stage in a temp dir
PUBLISH_DIR="$(mktemp -d)"
trap 'rm -rf "$PUBLISH_DIR"' EXIT

cp -R _book/. "$PUBLISH_DIR/"
touch "$PUBLISH_DIR/.nojekyll"
echo "→ staged $(find "$PUBLISH_DIR" -type f | wc -l | tr -d ' ') files"

# 3. Force-push to gh-pages
USER_EMAIL="$(git config user.email || echo 'pages-publish@nebulastream.local')"
USER_NAME="$(git config user.name  || echo 'Pages Publish')"
ORIGIN_URL="$(git remote get-url origin)"
HEAD_SHA="$(git rev-parse --short HEAD)"
TIMESTAMP="$(date -u +%Y-%m-%dT%H:%M:%SZ)"

(
    cd "$PUBLISH_DIR"
    git init -q -b gh-pages
    git add -A
    git -c user.email="$USER_EMAIL" -c user.name="$USER_NAME" \
        commit -q -m "Pages deploy ${TIMESTAMP} from main@${HEAD_SHA}"
    git remote add origin "$ORIGIN_URL"
    git push -f -q origin gh-pages
)
echo "→ pushed to origin/gh-pages"

# 4. Nudge GitHub to build (otherwise it may delay)
REPO_SLUG="$(echo "$ORIGIN_URL" | sed -E 's#.*github\.com[:/]([^/]+/[^/.]+)(\.git)?#\1#')"
if command -v gh >/dev/null 2>&1; then
    gh api -X POST "/repos/${REPO_SLUG}/pages/builds" >/dev/null 2>&1 \
        && echo "→ triggered Pages build" \
        || echo "  (could not trigger Pages build via gh; site will rebuild on its own)"
fi

echo
echo "✓ published"
echo "  https://$(echo "$REPO_SLUG" | cut -d/ -f1).github.io/$(echo "$REPO_SLUG" | cut -d/ -f2)/"
