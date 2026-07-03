"""NCHS connector — CDC Socrata open-data portal (data.cdc.gov).

Catalog connector: every NCHS dataset is a flat tabular resource on CDC's
Socrata portal, grouped under domain_category "National Center for Health
Statistics". One DOWNLOAD_SPEC per dataset id (the entity union), all fetched
the same way via the per-dataset full CSV export
(/api/views/<id>/rows.csv?accessType=DOWNLOAD), which returns the entire table
in one request (no pagination).

Fetch shape: stateless full re-pull. Each dataset is a small-to-medium
aggregate table (tens of thousands of rows at most); re-fetching the whole
table every run is cheap and picks up revisions for free. No watermark, no
cursor. Socrata supports $where on :updated_at but we do not use incremental.

Raw is saved as parquet with pyarrow-inferred types (single write per asset,
so inference is safe). Column names are sanitized to snake_case so the
published Delta tables have valid identifiers; all-null columns are cast to
string so they survive the parquet/Delta round-trip. The transform is a thin
SELECT * republish of the typed raw.
"""
import io
import re
import csv as _csv

import pyarrow as pa
import pyarrow.csv as pacsv

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    save_raw_parquet,
    transient_retry,
)

EXPORT_URL = "https://data.cdc.gov/api/views/{ds}/rows.csv?accessType=DOWNLOAD"

from constants import ENTITY_IDS


@transient_retry()
def _download_csv(url: str) -> bytes:
    resp = get(url, timeout=(10.0, 300.0))
    resp.raise_for_status()
    return resp.content


def _sanitize(names: list[str]) -> list[str]:
    """Map source CSV headers to unique snake_case identifiers safe for
    parquet/Delta column names."""
    out: list[str] = []
    seen: dict[str, int] = {}
    for n in names:
        s = re.sub(r"[^0-9a-z]+", "_", n.strip().lower()).strip("_")
        if not s:
            s = "col"
        if s in seen:
            seen[s] += 1
            s = f"{s}_{seen[s]}"
        else:
            seen[s] = 0
        out.append(s)
    return out


def _read_csv(content: bytes) -> pa.Table:
    """Parse CSV with pyarrow type inference; fall back to all-string parsing
    if inference trips over a column whose type drifts past the sample block."""
    try:
        return pacsv.read_csv(io.BytesIO(content))
    except pa.lib.ArrowInvalid:
        header = next(_csv.reader(io.StringIO(content.decode("utf-8", "replace"))))
        col_types = {name: pa.string() for name in header}
        return pacsv.read_csv(
            io.BytesIO(content),
            convert_options=pacsv.ConvertOptions(column_types=col_types),
        )


def fetch_one(node_id: str) -> None:
    asset = node_id  # the runtime passes the spec id; it IS the asset name
    dataset_id = node_id[len("nchs-"):]
    content = _download_csv(EXPORT_URL.format(ds=dataset_id))
    table = _read_csv(content)

    # All-null columns infer as pyarrow null type; cast to string so they
    # survive the parquet/Delta round-trip with a concrete type.
    arrays = []
    for i, field in enumerate(table.schema):
        col = table.column(i)
        if pa.types.is_null(field.type):
            col = col.cast(pa.string())
        arrays.append(col)
    table = pa.Table.from_arrays(arrays, names=_sanitize(table.schema.names))

    save_raw_parquet(table, asset)


DOWNLOAD_SPECS = [
    NodeSpec(
        id=f"nchs-{eid.lower().replace('_', '-')}",
        fn=fetch_one,
        kind="download",
    )
    for eid in ENTITY_IDS
]

# Per-dataset primary observation-period column (published/sanitized names).
# These Socrata tables have heterogeneous grains; only freshness (temporal) is
# declared, for the datasets that expose a clear period column in their profile.
TEMPORAL_BY_ID = {
    "nchs-489q-934x": "year_and_quarter",
    "nchs-4bc2-bbpq": "week_end",
    "nchs-53g5-jf7x": "end_date",
    "nchs-76vv-a7x8": "year_and_quarter",
    "nchs-9cpv-whbv": "week_ending_date",
    "nchs-jqwm-z2g9": "year_and_quarter",
    "nchs-muzy-jte6": "week_ending_date",
    "nchs-pj7m-y5uh": "year",
    "nchs-r8kw-7aab": "year",
    "nchs-tpcp-uiv5": "year",
    "nchs-v2g4-wqg2": "analysisdate",
    "nchs-xkkf-xrst": "week_ending_date",
}

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{s.id}-transform",
        deps=[s.id],
        sql=f'SELECT * FROM "{s.id}"',
        temporal=TEMPORAL_BY_ID.get(s.id),
    )
    for s in DOWNLOAD_SPECS
]
