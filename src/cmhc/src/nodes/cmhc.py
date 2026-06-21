"""CMHC (Canada Mortgage and Housing Corporation) housing statistics.

CMHC's open data is published as Statistics Canada tables in the 34-10-xxxx
housing product family. Each subset is one StatCan table, fetched as a stable
bulk-CSV zip (https://www150.statcan.gc.ca/n1/tbl/csv/<PID8>-eng.zip) — no auth,
no pagination, full table in one shot. The entity id IS the 8-digit StatCan
product id.

Fetch shape: stateless full re-pull. Each table is a few MB and StatCan rewrites
the whole CSV on each release (revisions included), so there is no usable
incremental filter — we re-fetch the full table every run and overwrite.

Each StatCan CSV shares a fixed long-format frame (REF_DATE, GEO, DGUID,
<table-specific dimension columns>, UOM, UOM_ID, SCALAR_FACTOR, SCALAR_ID,
VECTOR, COORDINATE, VALUE, STATUS, SYMBOL, TERMINATED, DECIMALS). The dimension
columns differ per table, so raw is saved per-table with its own inferred schema
and the transform keeps them generically via `* EXCLUDE`.
"""

import io
import zipfile

import pyarrow as pa
import pyarrow.csv as pacsv

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    save_raw_parquet,
    transient_retry,
)

# entity union — copied from data/sources/cmhc/work/entity_union.json
from constants import ENTITY_IDS

CSV_URL = "https://www150.statcan.gc.ca/n1/tbl/csv/{pid}-eng.zip"

# Fixed StatCan frame columns dropped at publish — the same on every table.
# Whatever sits between DGUID and UOM (the table-specific dimension columns)
# is kept by the `* EXCLUDE` projection in the transform.
_DROP_COLS = [
    "DGUID", "UOM_ID", "SCALAR_FACTOR", "SCALAR_ID", "VECTOR",
    "COORDINATE", "SYMBOL", "TERMINATED", "DECIMALS",
]


@transient_retry()
def _fetch_zip(url: str) -> bytes:
    resp = get(url, timeout=(10.0, 120.0))
    resp.raise_for_status()
    return resp.content


def fetch_one(node_id: str) -> None:
    asset = node_id  # the runtime passes the spec id; it IS the asset name
    pid = node_id[len("cmhc-"):]
    payload = _fetch_zip(CSV_URL.format(pid=pid))

    zf = zipfile.ZipFile(io.BytesIO(payload))
    data_name = f"{pid}.csv"
    if data_name not in zf.namelist():
        raise AssertionError(
            f"{asset}: expected {data_name} in zip, got {zf.namelist()}"
        )
    raw = zf.read(data_name)

    # Per-table schema inferred from the CSV header. Each table is written once
    # (not batched), so inference is safe; the StatCan long format is stable
    # within a table. Force fully-null columns (e.g. SYMBOL/TERMINATED) to
    # string so the parquet has a concrete type rather than the null type.
    table = pacsv.read_csv(io.BytesIO(raw))
    fixed = []
    for field in table.schema:
        if pa.types.is_null(field.type):
            fixed.append(table.schema.get_field_index(field.name))
    if fixed:
        cols = []
        schema_fields = []
        for i, field in enumerate(table.schema):
            col = table.column(i)
            if pa.types.is_null(field.type):
                col = col.cast(pa.string())
                field = pa.field(field.name, pa.string())
            cols.append(col)
            schema_fields.append(field)
        table = pa.table(cols, schema=pa.schema(schema_fields))

    save_raw_parquet(table, asset)


DOWNLOAD_SPECS = [
    NodeSpec(
        id=f"cmhc-{eid.lower().replace('_', '-')}",
        fn=fetch_one,
        kind="download",
    )
    for eid in ENTITY_IDS
]


def _transform_sql(asset_id: str) -> str:
    drop = ",".join(f'"{c}"' for c in _DROP_COLS)
    return f'''
        SELECT
            CAST("REF_DATE" AS VARCHAR) AS ref_date,
            "GEO"      AS geo,
            * EXCLUDE ("REF_DATE", "GEO", "UOM", "STATUS", "VALUE", {drop}),
            "UOM"      AS uom,
            "STATUS"   AS status,
            TRY_CAST("VALUE" AS DOUBLE) AS value
        FROM "{asset_id}"
        WHERE TRY_CAST("VALUE" AS DOUBLE) IS NOT NULL
          -- -999 is a StatCan missing-value sentinel (e.g. vacancy "Rate" = -999,
          -- which is impossible), not a real observation; drop it.
          AND TRY_CAST("VALUE" AS DOUBLE) <> -999
    '''


TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{s.id}-transform",
        deps=[s.id],
        sql=_transform_sql(s.id),
    )
    for s in DOWNLOAD_SPECS
]
