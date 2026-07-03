#!/usr/bin/env bash
# Build ONE shared venv that serves every connector under src/.
#
# Why this works: connectors are launched as `python -m src.main` from their
# own directory (subsets_utils.runner spawns with sys.executable + cwd), so the
# connector package is never installed — a venv only needs the third-party deps
# plus the editable subsets_utils. Those are identical across 612/639 connectors,
# and the handful of extras (curl-cffi, odfpy, pyreadstat, …) are unioned in
# below, so this single env satisfies all 639.
#
# Usage: ./setup-shared-venv.sh
set -euo pipefail
cd "$(dirname "$0")"

VENV=".venv-shared"

# Common runtime shared by every connector (src/aaa/pyproject.toml).
COMMON=(
  s3fs fsspec httpx requests pandas pyarrow boto3 backoff ratelimit tenacity
  duckdb 'deltalake>=1.3.1' 'psutil>=7.2.1' tqdm 'openpyxl>=3.1' 'xlrd>=2.0'
  'py7zr>=0.20' 'lxml>=4.9'
)

# Union of every extra any connector declares beyond the common set.
EXTRAS=(
  'curl-cffi>=0.15.0' 'odfpy>=1.4.1' 'python-calamine>=0.7.0' 'pyreadstat>=1.3.5'
  'html5lib>=1.1' 'beautifulsoup4>=4.15.0' 'truststore>=0.10.4'
  'tableauhyperapi>=0.0.18825' 'msoffcrypto-tool>=6.0.0' 'h2>=4.3.0'
  'cloudscraper>=1.2.71' 'certifi>=2026.6.17'
)

echo "==> Creating $VENV (python 3.11)"
uv venv "$VENV" --python 3.11

echo "==> Installing subsets_utils (editable) + common + extras"
UV_PROJECT_ENVIRONMENT="$VENV" uv pip install --python "$VENV/bin/python" \
  -e lib/subsets_utils \
  "${COMMON[@]}" "${EXTRAS[@]}"

echo
echo "Done. Shared venv: $(pwd)/$VENV"
echo "Run a connector with:  ./run.sh <slug>"
