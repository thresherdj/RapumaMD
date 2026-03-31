#!/usr/bin/env bash
# install.sh — Bootstrap rapumamd and all its dependencies on a fresh machine.
#
# NOTE FOR MAINTAINERS: Update this script if any of the following change:
#   - System packages (apt) required by the pipeline
#   - The pipx installation method or flags
#   - Python version requirements (pyproject.toml: requires-python)
#   - New external tool dependencies added to the pipeline
#
# Usage:
#   bash install.sh
#   bash install.sh --no-open    # skip opening a test PDF after install

set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
OPEN_TEST=true

for arg in "$@"; do
  [[ "$arg" == "--no-open" ]] && OPEN_TEST=false
done

info()  { echo "[rapumamd] $*"; }
warn()  { echo "[rapumamd] WARNING: $*" >&2; }
die()   { echo "[rapumamd] ERROR: $*" >&2; exit 1; }

# ── 1. System packages ────────────────────────────────────────────────────────
info "Installing system packages..."
sudo apt-get update -qq
sudo apt-get install -y \
  python3 \
  python3-pip \
  pipx \
  pandoc \
  texlive-xetex \
  texlive-latex-extra \
  texlive-fonts-recommended \
  texlive-plain-generic \
  git

# ── 2. Ensure pipx bin dir is on PATH ────────────────────────────────────────
pipx ensurepath --force
export PATH="$HOME/.local/bin:$PATH"

# ── 3. Install rapumamd via pipx (editable) ──────────────────────────────────
info "Installing rapumamd..."
if pipx list | grep -q rapumamd; then
  pipx install -e "$REPO_DIR" --force
else
  pipx install -e "$REPO_DIR"
fi

# ── 4. Smoke test ─────────────────────────────────────────────────────────────
info "Verifying installation..."
rapumamd --help > /dev/null || die "rapumamd not found after install — open a new shell and retry."

if [[ "$OPEN_TEST" == true ]] && ls "$REPO_DIR"/TestMDs/*.md 1>/dev/null 2>&1; then
  TEST_MD="$(ls "$REPO_DIR"/TestMDs/*.md | head -1)"
  info "Rendering test document: $TEST_MD"
  rapumamd render "$TEST_MD" && info "Done. PDF opened." || warn "Render test failed — install succeeded but check pandoc/xelatex."
else
  info "Install complete. Run: rapumamd render path/to/file.md"
fi
