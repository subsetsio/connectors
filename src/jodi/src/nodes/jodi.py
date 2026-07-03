"""Joint Organisations Data Initiative (JODI) — Oil World Database.

Monthly country-level oil balances (~100 reporting economies, >90% of world
oil) from January 2002 to roughly one month before present: production, demand,
refinery intake/output, imports, exports and stock levels/changes, for crude &
upstream products plus refined products.

The source publishes two whole-database CSV zips that share one long-format
schema (REF_AREA, TIME_PERIOD, ENERGY_PRODUCT, FLOW_BREAKDOWN, UNIT_MEASURE,
OBS_VALUE, ASSESSMENT_CODE):
  - world_primary_csv.zip   crude & upstream products (CRUDEOIL/TOTCRUDE/NGL/...)
  - world_secondary_csv.zip refined products (GASOLINE/JETKERO/LPG/RESFUEL/...)
Because the two tiers are identical in schema and differ only in the value of
ENERGY_PRODUCT, they are unioned into ONE published table; the product code is a
column. The combined corpus is ~920MB of CSV / ~18M rows, so raw is streamed
batch-by-batch into one parquet asset rather than built in memory.

Stateless full re-pull: both zips are re-fetched and overwritten every refresh
(no incremental query is offered upstream, and revisions to historical months
are picked up for free). JODI-Gas is excluded — its CSV export is a stalled 2018
beta; current gas data is only in proprietary .ivt (see research_gaps).

License: free re-use with attribution per JODI terms of use.
"""

import io
import zipfile

import pyarrow as pa
import pyarrow.csv as pacsv

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    raw_parquet_writer,
    transient_retry,
)

# Stable whole-database CSV zips (verified live 2026-06; legacy
# /_resources/files/data/csv/ paths are dead). One CSV member per zip.
TIER_URLS = {
    "primary": "https://www.jodidata.org/_resources/files/downloads/oil-data/world_primary_csv.zip",
    "secondary": "https://www.jodidata.org/_resources/files/downloads/oil-data/world_secondary_csv.zip",
}

# Long-format columns, in source header order. Everything is read as string and
# left untyped in raw; the transform casts OBS_VALUE and drops suppressed cells.
COLUMNS = [
    "REF_AREA",
    "TIME_PERIOD",
    "ENERGY_PRODUCT",
    "FLOW_BREAKDOWN",
    "UNIT_MEASURE",
    "OBS_VALUE",
    "ASSESSMENT_CODE",
]
SCHEMA = pa.schema([(c, pa.string()) for c in COLUMNS])


@transient_retry()
def _download(url: str) -> bytes:
    resp = get(url, timeout=(10.0, 300.0))
    resp.raise_for_status()
    return resp.content


def fetch_oil(node_id: str) -> None:
    """Stream both tier zips into one parquet asset (bounded memory)."""
    asset = node_id
    convert = pacsv.ConvertOptions(column_types={c: pa.string() for c in COLUMNS})
    read = pacsv.ReadOptions(block_size=16 << 20)

    with raw_parquet_writer(asset, SCHEMA) as writer:
        for tier, url in TIER_URLS.items():
            print(f"Fetching {tier} from {url}")
            blob = _download(url)
            print(f"  downloaded {len(blob):,} bytes")
            with zipfile.ZipFile(io.BytesIO(blob)) as zf:
                members = [n for n in zf.namelist() if n.lower().endswith(".csv")]
                if not members:
                    raise RuntimeError(
                        f"{tier}: no CSV member in zip — found {zf.namelist()}"
                    )
                with zf.open(members[0]) as f:
                    reader = pacsv.open_csv(
                        f, read_options=read, convert_options=convert
                    )
                    n = 0
                    for batch in reader:
                        if batch.schema != SCHEMA:
                            raise RuntimeError(
                                f"{tier}: unexpected columns {batch.schema.names}"
                            )
                        writer.write_batch(batch)
                        n += batch.num_rows
                    print(f"  {tier}: wrote {n:,} rows from {members[0]}")


DOWNLOAD_SPECS = [
    NodeSpec(id="jodi-oil-world-monthly", fn=fetch_oil, kind="download"),
]


TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="jodi-oil-world-monthly-transform",
        deps=["jodi-oil-world-monthly"],
        key=("month", "country_code", "product", "flow", "unit"),
        temporal="month",
        sql='''
            SELECT
                CAST(TIME_PERIOD || '-01' AS DATE) AS month,
                REF_AREA                       AS country_code,
                ENERGY_PRODUCT                 AS product,
                FLOW_BREAKDOWN                 AS flow,
                UNIT_MEASURE                   AS unit,
                ASSESSMENT_CODE                AS assessment_code,
                TRY_CAST(OBS_VALUE AS DOUBLE)  AS value
            FROM "jodi-oil-world-monthly"
            WHERE TIME_PERIOD    IS NOT NULL
              AND REF_AREA       IS NOT NULL
              AND ENERGY_PRODUCT IS NOT NULL
              AND FLOW_BREAKDOWN IS NOT NULL
              AND TRY_CAST(OBS_VALUE AS DOUBLE) IS NOT NULL
        ''',
    ),
]
