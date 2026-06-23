"""IPSS (National Institute of Population and Social Security Research, Japan).

IPSS publishes no API — it is a static web tree of self-contained Excel tables
(one per statistical table). The chosen mechanism is per-entity bulk download of
.xlsx (population projections) and legacy .xls (social-security DB) files at
stable URLs; the file list per entity is fixed in `src/constants.ENTITY_PATHS`.

SQL transforms can only read parquet/ndjson/csv, so each fetch fn parses its
Excel file in Python and writes NDJSON. The tables are idiosyncratic bilingual
cross-tabs (a title row, a multi-row header band, then numeric data rows whose
leading column carries a year / age / category key). Rather than author 111
fragile bespoke parsers, we use ONE robust generic extractor: every numeric data
cell becomes one long-format record with its grid coordinates and best-effort
row/column labels reconstructed from the header band. This never misparses into
silence — any sheet with numbers yields rows — and stays faithful to the source;
a consumer pivots (sheet, row, col) -> value and reads the labels.

Stateless full re-pull: files are tiny (10-600 KB) and the corpus is ~111 files,
so we re-fetch everything each refresh and overwrite. No watermark/cursor — the
source exposes no incremental filter (revisions are republished wholesale).
"""

import io
import re

import pyarrow as pa
import pandas as pd

from subsets_utils import NodeSpec, SqlNodeSpec, get, transient_retry, save_raw_parquet
from constants import ENTITY_PATHS

BASE = "https://www.ipss.go.jp/"

# Cells that look numeric but are placeholders for "no data".
_NULL_TOKENS = {"", "*", "-", "–", "—", "―", "−", "…", "...", "‥", "nan", "NaN", "None", "x", "X"}

_YEAR_RE = re.compile(r"^(19|20|21)\d{2}$")

# Explicit schema — the contract for every NDJSON-equivalent record we emit.
SCHEMA = pa.schema([
    ("sheet", pa.string()),
    ("row", pa.int32()),
    ("col", pa.int32()),
    ("row_label", pa.string()),
    ("col_label", pa.string()),
    ("value", pa.float64()),
])


@transient_retry()
def _download(url: str) -> bytes:
    resp = get(url, timeout=(10.0, 120.0))
    resp.raise_for_status()
    return resp.content


def _to_num(x):
    """Parse a cell to float, or None if it isn't a real number."""
    if x is None:
        return None
    if isinstance(x, bool):
        return None
    if isinstance(x, (int, float)):
        f = float(x)
        return f if f == f else None  # drop NaN
    s = str(x).strip().replace(",", "").replace("　", "")
    if s in _NULL_TOKENS:
        return None
    s = s.replace("−", "-")  # unicode minus -> ascii
    try:
        return float(s)
    except ValueError:
        return None


def _txt(x):
    if x is None:
        return None
    s = str(x).strip()
    if s.lower() in {"nan", "none", ""}:
        return None
    return re.sub(r"\s+", " ", s.replace("　", " "))


def _parse_excel(content: bytes) -> list[dict]:
    """Extract every numeric data cell from every sheet as a long-format record
    with best-effort row/column labels. Robust across the source's varied
    cross-tab layouts; never returns silently-empty for a sheet that has data."""
    xl = pd.ExcelFile(io.BytesIO(content))
    out: list[dict] = []
    for sheet in xl.sheet_names:
        df = xl.parse(sheet, header=None, dtype=object)
        nrows, ncols = df.shape
        if nrows == 0 or ncols == 0:
            continue
        grid = df.values
        numeric = [[_to_num(grid[r][c]) for c in range(ncols)] for r in range(nrows)]

        # First data row: first row with >=2 numeric cells (header band sits
        # above). Fall back to >=1 so a single-column table still yields data.
        def first_data_row(threshold: int):
            for r in range(nrows):
                if sum(1 for c in range(ncols) if numeric[r][c] is not None) >= threshold:
                    return r
            return None

        first_data = first_data_row(2)
        if first_data is None:
            first_data = first_data_row(1)
        if first_data is None:
            continue  # no numeric content in this sheet

        # Column labels = header-band text joined per column (skip bare years).
        col_label = {}
        for c in range(ncols):
            parts = []
            for r in range(first_data):
                t = _txt(grid[r][c])
                if t and not _YEAR_RE.match(t):
                    parts.append(t)
            col_label[c] = " / ".join(parts) if parts else None

        for r in range(first_data, nrows):
            # Row label = first non-empty cell scanning left (year / age / category).
            rlabel = None
            for c in range(ncols):
                t = _txt(grid[r][c])
                if t:
                    rlabel = t
                    break
            for c in range(ncols):
                v = numeric[r][c]
                if v is None:
                    continue
                out.append({
                    "sheet": sheet,
                    "row": r,
                    "col": c,
                    "row_label": rlabel,
                    "col_label": col_label.get(c),
                    "value": v,
                })
    return out


def fetch_one(node_id: str) -> None:
    asset = node_id  # the runtime passes the spec id; it IS the asset name
    entity = node_id[len("ipss-"):]
    url = BASE + ENTITY_PATHS[entity]
    content = _download(url)
    rows = _parse_excel(content)
    table = pa.Table.from_pylist(rows, schema=SCHEMA)
    save_raw_parquet(table, asset)


DOWNLOAD_SPECS = [
    NodeSpec(
        id=f"ipss-{eid.lower().replace('_', '-')}",
        fn=fetch_one,
        kind="download",
    )
    for eid in ENTITY_PATHS
]

# One published Delta table per subset: a thin parse-and-type pass over the raw
# long-format extraction. value is non-null by construction; the filter keeps
# the 0-rows-is-failure contract honest if the upstream parse ever degrades.
TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{s.id}-transform",
        deps=[s.id],
        sql=f'''
            SELECT
                CAST(sheet AS VARCHAR)     AS sheet,
                CAST(row AS INTEGER)       AS row,
                CAST(col AS INTEGER)       AS col,
                CAST(row_label AS VARCHAR) AS row_label,
                CAST(col_label AS VARCHAR) AS col_label,
                CAST(value AS DOUBLE)      AS value
            FROM "{s.id}"
            WHERE value IS NOT NULL
        ''',
    )
    for s in DOWNLOAD_SPECS
]
