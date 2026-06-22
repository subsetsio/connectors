"""Federal Reserve Bank of Chicago — economic data connector.

Mechanism (from research): the chicagofed.org "FedRelease" widgets are backed by
a public, no-auth JSON discovery endpoint per data provider, and every release
artifact is a stable CSV at https://api.data.chicagofed.org/<PROVIDER>/<file>.csv.
Each accepted subset is one such CSV.

Fetch shape: stateless full re-pull. Every CSV is the complete history in one
request (a few KB to ~MB), so we re-fetch the whole file each run and overwrite —
no watermark, no cursor. Revisions are picked up for free.

Raw shape: the source CSVs are heterogeneous wide tables — column 1 is a
period/date key, the remaining columns are numeric series (with blanks / NaN for
missing). We normalise every file to a uniform LONG form at fetch time:

    {period: str, series: str, value: str}   # value kept as raw numeric text

so the SQL transform is a thin, uniform cast-and-filter pass that publishes
(period, series, value) for every subset. Non-numeric cells (text categorical
columns, blanks, NaN) are dropped during parsing.
"""

import csv
import io
import math

import pyarrow as pa  # noqa: F401  (kept available; ndjson path doesn't need it)
from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    save_raw_ndjson,
    transient_retry,
)
from constants import ENTITY_IDS, PERIOD_COL_OVERRIDES

SLUG = "chicagofed"
DATA_BASE = "https://api.data.chicagofed.org"

# spec id -> original entity id (lowercasing is lossy, so map it explicitly)
ID_TO_ENTITY = {
    f"{SLUG}-{eid.lower().replace('_', '-')}": eid for eid in ENTITY_IDS
}


def _clean_number(raw):
    """Return a finite float if `raw` is a numeric cell, else None.

    Handles blanks, NaN markers, thousands separators, trailing footnote
    asterisks and leading '+' that the source occasionally uses.
    """
    if raw is None:
        return None
    s = raw.strip().strip('"').strip()
    if not s:
        return None
    if s.lower() in ("nan", "na", "n/a", "null", "-", "."):
        return None
    s = s.replace(",", "").rstrip("*").lstrip("+").strip()
    try:
        v = float(s)
    except ValueError:
        return None
    if not math.isfinite(v):
        return None
    return v


def _parse_long(text, period_col):
    """Melt a wide CSV string into long rows {period, series, value}.

    `period_col` names the key column; when None the first column is used.
    Only cells that parse as finite numbers are emitted.
    """
    reader = csv.reader(io.StringIO(text))
    rows = list(reader)
    if not rows:
        return []
    header = [h.strip().strip('"') for h in rows[0]]
    if period_col is not None and period_col in header:
        period_idx = header.index(period_col)
    else:
        period_idx = 0
    out = []
    for row in rows[1:]:
        if not row or len(row) <= period_idx:
            continue
        period = (row[period_idx] or "").strip().strip('"')
        if not period:
            continue
        for j, cell in enumerate(row):
            if j == period_idx or j >= len(header):
                continue
            value = _clean_number(cell)
            if value is None:
                continue
            out.append(
                {
                    "period": period,
                    "series": header[j],
                    "value": repr(value),
                }
            )
    return out


@transient_retry()
def _fetch_csv(url):
    resp = get(url, timeout=(10.0, 120.0))
    resp.raise_for_status()
    return resp.text


def fetch_one(node_id):
    asset = node_id  # the runtime passes the spec id; it IS the asset name
    entity_id = ID_TO_ENTITY[node_id]
    provider, stem = entity_id.split("/", 1)
    url = f"{DATA_BASE}/{provider}/{stem}.csv"
    period_col = PERIOD_COL_OVERRIDES.get(entity_id)
    text = _fetch_csv(url)
    rows = _parse_long(text, period_col)
    save_raw_ndjson(rows, asset)


DOWNLOAD_SPECS = [
    NodeSpec(
        id=f"{SLUG}-{eid.lower().replace('_', '-')}",
        fn=fetch_one,
        kind="download",
    )
    for eid in ENTITY_IDS
]

# Uniform thin transform: one published Delta table per subset, long format.
# value is cast in SQL (the correctness gate); 0 rows fails the node.
TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{s.id}-transform",
        deps=[s.id],
        sql=f'''
            SELECT
                CAST(period AS VARCHAR) AS period,
                CAST(series AS VARCHAR) AS series,
                CAST(value  AS DOUBLE)  AS value
            FROM "{s.id}"
            WHERE value IS NOT NULL
              AND TRY_CAST(value AS DOUBLE) IS NOT NULL
              AND NOT isnan(TRY_CAST(value AS DOUBLE))
        ''',
    )
    for s in DOWNLOAD_SPECS
]
