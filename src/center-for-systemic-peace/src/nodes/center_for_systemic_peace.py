"""Center for Systemic Peace (CSP) — INSCR data page connector.

The source is a flat static-file host: one stable .xls per dataset under
https://www.systemicpeace.org/inscr/<file>.xls (see research mechanism
'bulk_xls'). The whole corpus is ~15 small Excel workbooks totalling <20 MB,
so the fetch shape is the simplest one: a **stateless full re-pull** — every
run downloads each file in full and overwrites. There is no incremental query
API and no bulk archive; each file is a complete replacement.

Each dataset has its own schema, so there is one download spec + one transform
per entity (no shared schema). Raw is written as parquet: numeric columns are
preserved with their native types, but `object`-dtype columns are coerced to
nullable strings because several source columns are dirty (European
comma-decimals like '3,5', blank cells, mixed int/str codes) and would
otherwise break parquet construction. The transform republishes each table
faithfully.
"""

import io
import math
import urllib.parse

import pandas as pd
import pyarrow as pa

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    save_raw_parquet,
    transient_retry,
)
from constants import FILES

SLUG = "center-for-systemic-peace"
BASE_URL = "https://www.systemicpeace.org/inscr/"


@transient_retry()  # 6 attempts, exponential backoff over transient net/5xx/429
def _download_xls(url: str) -> bytes:
    resp = get(url, timeout=(10.0, 120.0))
    resp.raise_for_status()
    return resp.content


def _normalize_columns(cols) -> list[str]:
    """Lowercase, strip, and slugify column names; de-duplicate collisions."""
    out: list[str] = []
    seen: dict[str, int] = {}
    for c in cols:
        base = "".join(
            ch if (ch.isalnum() or ch == "_") else "_" for ch in str(c).strip().lower()
        ).strip("_")
        base = base or "col"
        if base in seen:
            seen[base] += 1
            base = f"{base}_{seen[base]}"
        else:
            seen[base] = 0
        out.append(base)
    return out


def _to_arrow(df: pd.DataFrame) -> pa.Table:
    """Build a parquet-safe table: native numeric columns, object -> string.

    Object columns in these workbooks carry dirty values (comma-decimals, blank
    cells, mixed int/str). Coercing them to nullable strings makes the parquet
    write deterministic; the transform casts what it needs downstream.
    """
    df = df.copy()
    df.columns = _normalize_columns(df.columns)
    for col in df.columns:
        if df[col].dtype == object:
            df[col] = df[col].map(
                lambda v: None
                if v is None or (isinstance(v, float) and math.isnan(v))
                else str(v).strip()
            )
    return pa.Table.from_pandas(df, preserve_index=False)


def fetch_one(node_id: str) -> None:
    asset = node_id  # the spec id IS the asset name
    entity = node_id[len(SLUG) + 1 :]  # strip "center-for-systemic-peace-"
    filename = FILES[entity]
    url = BASE_URL + urllib.parse.quote(filename)
    content = _download_xls(url)
    df = pd.read_excel(io.BytesIO(content))
    table = _to_arrow(df)
    save_raw_parquet(table, asset)


DOWNLOAD_SPECS = [
    NodeSpec(
        id=f"{SLUG}-{eid.lower().replace('_', '-')}",
        fn=fetch_one,
        kind="download",
    )
    for eid in FILES
]


# One published Delta table per dataset. Each raw asset is already a clean,
# typed parquet, so the transform is a faithful republish (the SQL is the
# correctness gate: it fails loudly if a raw asset is empty or unreadable).
TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{s.id}-transform",
        deps=[s.id],
        sql=f'SELECT * FROM "{s.id}"',
    )
    for s in DOWNLOAD_SPECS
]
