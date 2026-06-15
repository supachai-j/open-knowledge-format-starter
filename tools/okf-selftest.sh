#!/usr/bin/env bash
# okf-selftest.sh — exercise the whole OKF toolchain end-to-end in a temp project.
# Pure-stdlib tools are required; embeddings/hybrid are tested only if a local Ollama
# is reachable (otherwise skipped). Exits non-zero if any check fails. Run: bash tools/okf-selftest.sh
set -uo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
PY="${PYTHON:-python3}"
TMP="$(mktemp -d)"; trap 'rm -rf "$TMP"' EXIT
pass=0; fail=0
ok()  { echo "  ✓ $1"; pass=$((pass+1)); }
bad() { echo "  ✗ $1"; fail=$((fail+1)); }

echo "OKF self-test  (tools: $HERE)"

# 1. init
$PY "$HERE/okf-init.py" "$TMP/proj" --date 2026-01-01 >/dev/null 2>&1 && [ -f "$TMP/proj/wiki/index.md" ] \
  && ok "okf-init scaffolds a bundle" || bad "okf-init"
W="$TMP/proj/wiki"

# 2. validate — conformant
$PY "$HERE/okf-validate.py" "$W" >/dev/null 2>&1 && ok "okf-validate passes a clean bundle" || bad "okf-validate (clean)"

# 3. validate — negative (missing type must fail)
printf '%s\n' '---' 'title: x' '---' 'no type here' > "$W/broken.md"
if $PY "$HERE/okf-validate.py" "$W" >/dev/null 2>&1; then bad "okf-validate should FAIL on missing type"; else ok "okf-validate catches missing type"; fi
rm -f "$W/broken.md"

# 4. index + search (BM25)
$PY "$HERE/okf-index.py" build "$W" >/dev/null 2>&1 && ok "okf-index builds" || bad "okf-index build"
$PY "$HERE/okf-search.py" "how this knowledge base is organized" --bundle "$W" -k 1 2>/dev/null | grep -q "getting-started" \
  && ok "okf-search (BM25) returns expected hit" || bad "okf-search (BM25)"

# 5. viz — air-gap single file
$PY "$HERE/okf-viz.py" "$W" --name selftest >/dev/null 2>&1 \
  && [ -f "$W/viz.html" ] && ! grep -q "cdn.jsdelivr" "$W/viz.html" \
  && ok "okf-viz emits a self-contained (no-CDN) viewer" || bad "okf-viz (air-gap)"

# 6. lease lifecycle
export OKF_LEASE_DIR="$TMP/leases"
TOK=$($PY "$HERE/okf-lease.py" acquire t/x --owner A --ttl 60 2>/dev/null | $PY -c "import sys,json;print(json.load(sys.stdin).get('token',''))" 2>/dev/null)
[ -n "$TOK" ] && ok "okf-lease acquire" || bad "okf-lease acquire"
if $PY "$HERE/okf-lease.py" acquire t/x --owner B >/dev/null 2>&1; then bad "okf-lease should block a 2nd owner"; else ok "okf-lease blocks contending owner"; fi
$PY "$HERE/okf-lease.py" release t/x --owner A --token "$TOK" >/dev/null 2>&1 && ok "okf-lease release" || bad "okf-lease release"

# 7. embeddings + hybrid (optional — only if Ollama is up)
if curl -s -m 2 http://localhost:11434/api/tags >/dev/null 2>&1; then
  if $PY "$HERE/okf-embed.py" build "$W" >/dev/null 2>&1 \
     && $PY "$HERE/okf-search.py" "organize knowledge" --bundle "$W" 2>/dev/null | grep -q "hybrid"; then
    ok "okf-embed + hybrid search (Ollama)"
  else bad "okf-embed/hybrid (Ollama reachable but failed)"; fi
else
  echo "  – skipped embeddings/hybrid (no Ollama on :11434)"
fi

echo "──────────────────────────────"
echo "  $pass passed, $fail failed"
[ "$fail" -eq 0 ]
