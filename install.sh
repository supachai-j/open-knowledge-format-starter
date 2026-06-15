#!/usr/bin/env bash
# Install the OKF skill into a Claude Code skills directory.
#
# Usage:
#   ./install.sh                 # global  → ~/.claude/skills/okf   (all projects)
#   ./install.sh --project       # project → ./.claude/skills/okf   (current repo only)
#   ./install.sh --dir <path>    # custom  → <path>/okf
#   ./install.sh --uninstall [--project|--dir <path>]
#
# The skill is self-contained: SKILL.md + all pure-Python tools + vendored viewer
# libs. No external dependencies (semantic search optionally uses a local Ollama).
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")" && pwd)"
MODE="global"; DIR=""; UNINSTALL=0

while [ $# -gt 0 ]; do
  case "$1" in
    --project) MODE="project"; shift ;;
    --dir) MODE="dir"; DIR="${2:?--dir needs a path}"; shift 2 ;;
    --uninstall) UNINSTALL=1; shift ;;
    -h|--help) sed -n '2,12p' "$0"; exit 0 ;;
    *) echo "unknown arg: $1" >&2; exit 2 ;;
  esac
done

case "$MODE" in
  global)  BASE="$HOME/.claude/skills" ;;
  project) BASE="$(pwd)/.claude/skills" ;;
  dir)     BASE="$DIR" ;;
esac
SKILL_DIR="$BASE/okf"

if [ "$UNINSTALL" -eq 1 ]; then
  rm -rf "$SKILL_DIR"
  echo "✓ uninstalled $SKILL_DIR"
  exit 0
fi

echo "Installing OKF skill → $SKILL_DIR"
mkdir -p "$SKILL_DIR/scripts/vendor"
cp "$REPO_ROOT/skill/okf/SKILL.md"            "$SKILL_DIR/SKILL.md"
cp "$REPO_ROOT"/tools/okf-*.py                "$SKILL_DIR/scripts/"
cp "$REPO_ROOT/tools/concept-template.md"     "$SKILL_DIR/scripts/"
cp "$REPO_ROOT"/tools/vendor/*                "$SKILL_DIR/scripts/vendor/" 2>/dev/null || true
chmod +x "$SKILL_DIR/scripts/"*.py

echo "✓ installed:"
echo "    $SKILL_DIR/SKILL.md"
echo "    $SKILL_DIR/scripts/  ($(ls "$SKILL_DIR/scripts"/*.py | wc -l | tr -d ' ') scripts + vendor/)"
echo
echo "Use it: open Claude Code and say e.g. \"init an OKF knowledge base here\" or \"/okf\"."
if [ "$MODE" = "global" ]; then echo "Installed globally — available in every project."; fi
