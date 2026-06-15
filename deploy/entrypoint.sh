#!/bin/sh
# Clone-or-pull the OKF bundle from the internal git server, then serve it over MCP.
set -e
: "${OKF_GIT_REMOTE:?set OKF_GIT_REMOTE to your internal repo URL}"
: "${OKF_REPO_DIR:=/data/repo}"

if [ ! -d "$OKF_REPO_DIR/.git" ]; then
  echo "[okf] cloning $OKF_GIT_REMOTE -> $OKF_REPO_DIR"
  git clone "$OKF_GIT_REMOTE" "$OKF_REPO_DIR"
else
  echo "[okf] pulling latest"
  git -C "$OKF_REPO_DIR" pull --ff-only || true
fi

git config --global --add safe.directory "$OKF_REPO_DIR"
# Build the search index, then run the server (server also rebuilds if missing).
python3 "$OKF_REPO_DIR/tools/okf-index.py" build "$OKF_BUNDLE" || true
exec python3 "$OKF_REPO_DIR/server/okf_mcp_server.py"
