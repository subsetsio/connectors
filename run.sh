#!/usr/bin/env bash
# Run a connector against the shared venv.
#
# Usage:
#   ./run.sh <slug>              run a connector (builds the shared venv if absent)
#   ./run.sh --rebuild <slug>    force-rebuild the shared venv first, then run
#   RUN_ID=20260702-101918 ./run.sh cbs   resume a specific run
#
# The shared venv is self-healing: first use (or use after a wipe) builds it via
# setup-shared-venv.sh, so there's no separate setup step to remember. Rebuild
# with --rebuild when the dependency union changes (a connector adds a package).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
VENV="$ROOT/.venv-shared"

rebuild=0
if [[ "${1:-}" == "--rebuild" ]]; then rebuild=1; shift; fi

slug="${1:-}"
[[ -n "$slug" ]] || { echo "usage: ./run.sh [--rebuild] <slug>" >&2; exit 2; }

CONNECTOR_DIR="$ROOT/src/$slug"
[[ -d "$CONNECTOR_DIR" ]] || { echo "no such connector: src/$slug" >&2; exit 2; }

if [[ "$rebuild" == 1 || ! -x "$VENV/bin/python" ]]; then
  "$ROOT/setup-shared-venv.sh"
fi

# cwd = connector dir so get_connector_name() resolves to the slug and the
# runner puts src/ on the child's PYTHONPATH. The runner spawns the connector
# with sys.executable, which is this shared interpreter.
cd "$CONNECTOR_DIR"
exec "$VENV/bin/python" -m subsets_utils.runner
