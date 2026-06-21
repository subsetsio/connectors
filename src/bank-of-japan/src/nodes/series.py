"""Bank of Japan — series (catalog) subset.

``series`` is the catalog: one row per series_code (name, unit, frequency,
category, 5-level layer-tree position, recorded date range, last_update),
sourced from /getMetadata (one call per DB).

Fetch shape: a stateless full re-pull. Every refresh re-reads each DB's
metadata and overwrites the catalog. It is cheap (~50 small CSV calls) and
picks up catalog edits/revisions for free. Raw is written one parquet file per
DB (``bank-of-japan-series-<db>``); the transform glob-unions them.
"""
import httpx
import pyarrow as pa

from subsets_utils import NodeSpec, SqlNodeSpec, save_raw_parquet

from utils import DATABASES, _PermanentError, _fetch_metadata

# Catalog (series) raw schema — declared once, the contract for every per-DB
# parquet batch. Dates are kept as raw YYYYMMDD strings and parsed in the
# transform (some are empty for layer-header rows / undated series).
SERIES_SCHEMA = pa.schema([
    ("db", pa.string()),
    ("series_code", pa.string()),
    ("name", pa.string()),
    ("unit", pa.string()),
    ("frequency", pa.string()),
    ("category", pa.string()),
    ("layer1", pa.string()),
    ("layer2", pa.string()),
    ("layer3", pa.string()),
    ("layer4", pa.string()),
    ("layer5", pa.string()),
    ("start_date", pa.string()),
    ("end_date", pa.string()),
    ("last_update", pa.string()),
    ("notes", pa.string()),
])


def fetch_series(node_id: str) -> None:
    for db in sorted(DATABASES):
        try:
            series = _fetch_metadata(db)
        except _PermanentError as exc:
            print(f"  skip catalog db={db}: {exc}")
            continue
        except httpx.HTTPStatusError as exc:
            print(f"  skip catalog db={db}: HTTP {exc.response.status_code}")
            continue
        if not series:
            print(f"  catalog db={db}: 0 series")
            continue
        table = pa.Table.from_pylist(series, schema=SERIES_SCHEMA)
        save_raw_parquet(table, f"{node_id}-{db.lower()}")


DOWNLOAD_SPECS = [
    NodeSpec(id="bank-of-japan-series", fn=fetch_series, kind="download"),
]


TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="bank-of-japan-series-transform",
        deps=["bank-of-japan-series"],
        sql='''
            SELECT
                db,
                series_code,
                name,
                unit,
                frequency,
                category,
                layer1, layer2, layer3, layer4, layer5,
                -- Catalog dates arrive at mixed widths by frequency: YYYYMMDD
                -- (daily), YYYYMM (monthly/quarterly), YYYY (annual). strptime
                -- *raises* on a width mismatch and TRY_CAST does not catch a
                -- function error, so parse with try_strptime (NULL on miss) and
                -- coalesce widest-first, defaulting the missing parts to the 1st.
                COALESCE(
                    try_strptime(NULLIF(start_date, ''), '%Y%m%d'),
                    try_strptime(NULLIF(start_date, ''), '%Y%m'),
                    try_strptime(NULLIF(start_date, ''), '%Y')
                )::DATE AS start_date,
                COALESCE(
                    try_strptime(NULLIF(end_date, ''), '%Y%m%d'),
                    try_strptime(NULLIF(end_date, ''), '%Y%m'),
                    try_strptime(NULLIF(end_date, ''), '%Y')
                )::DATE AS end_date,
                COALESCE(
                    try_strptime(NULLIF(last_update, ''), '%Y%m%d'),
                    try_strptime(NULLIF(last_update, ''), '%Y%m'),
                    try_strptime(NULLIF(last_update, ''), '%Y')
                )::DATE AS last_update,
                notes
            FROM "bank-of-japan-series"
            WHERE series_code IS NOT NULL AND series_code <> ''
            QUALIFY row_number() OVER (
                PARTITION BY db, series_code
                ORDER BY last_update DESC NULLS LAST
            ) = 1
        ''',
    ),
]
