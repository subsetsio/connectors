"""EEA Bathing Water Quality (WISE_BWD) — connector node module.

Access mechanism: EEA Discodata, a public REST-over-SQL gateway
(https://discodata.eea.europa.eu/sql). We snapshot the nine publishable views
of the [WISE_BWD].[latest] schema, one download node per view.

Fetch shape: **stateless full re-pull** (shape 1). Every refresh re-pulls each
whole table and overwrites its raw asset. BWD is an annual reporting programme
and late corrections/revisions rewrite historical rows in place, so a stored
watermark would silently skip revised rows — full re-pull picks them up for
free. The largest table (timeseries_MonitoringResult, ~2.85M rows) is paginated
at 100k rows/page and streamed to parquet row-group by row-group, so no whole
table is held in memory.

Raw format: **parquet with an explicit per-column schema** derived from the
WISE_BWD view definitions (constants.TABLE_COLUMNS). The views have fixed,
documented column types, so an explicit schema is the strongest contract:
type drift raises at table-construction time. Date/datetime values arrive as
ISO strings and are kept as strings in raw (lossless), then CAST to DATE /
TIMESTAMP in the transform. Storing dates as strings rather than letting a JSON
reader guess avoids the read_json_auto type-inference ambiguity entirely.
"""

import pyarrow as pa

from constants import ENTITY_IDS, TABLE_COLUMNS
from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    transient_retry,
    raw_parquet_writer,
)

SLUG = "eea-bathing-water"
BASE_URL = "https://discodata.eea.europa.eu/sql"
DATABASE = "WISE_BWD"
SCHEMA = "latest"          # [latest] is the alias for the newest BWD release
PAGE_SIZE = 100_000        # docs: a single page > ~100k truncates; keep at 100k
MAX_PAGES = 1_000          # safety ceiling — raises (never silently truncates)

# WISE_BWD source dataType -> pyarrow type for RAW storage. date/datetime are
# stored as their ISO strings and re-typed in the transform; every other type
# maps to its native arrow type so the parquet schema is the exact contract.
_PA_TYPE = {
    "bit": pa.bool_(),
    "int": pa.int64(),
    "float": pa.float64(),
    "decimal": pa.float64(),
    "date": pa.string(),
    "datetime": pa.string(),
    "nvarchar": pa.string(),
    "varchar": pa.string(),
}


def _node_id(entity_id: str) -> str:
    return f"{SLUG}-{entity_id.lower().replace('_', '-')}"


# Pure lookups built from constants (no I/O). The node id lowercases and
# dash-folds the table name, which is lossy, so the original casing cannot be
# recovered from the id alone — keep the map explicit.
NODE_TO_TABLE = {_node_id(e): e for e in ENTITY_IDS}


def _schema_for(table: str) -> pa.Schema:
    return pa.schema([(col, _PA_TYPE[dtype]) for col, dtype in TABLE_COLUMNS[table]])


@transient_retry()  # 6 attempts, exponential backoff over transient net errors / 429 / 5xx
def _fetch_page(table: str, page: int) -> list[dict]:
    """Fetch one page of a [WISE_BWD].[latest] table. Raises on non-2xx."""
    query = f"SELECT * FROM [{DATABASE}].[{SCHEMA}].[{table}]"
    resp = get(
        BASE_URL,
        params={"query": query, "p": page, "nrOfHits": PAGE_SIZE},
        timeout=(10.0, 300.0),
    )
    resp.raise_for_status()
    # Response envelope is {"results": [ {row}, ... ]}; there is no total/row-count
    # field, so end-of-data is detected by a short page.
    return resp.json()["results"]


def fetch_one(node_id: str) -> None:
    """Stateless full re-pull of one WISE_BWD table to parquet.

    Paginate p=1.. with nrOfHits=100000, writing each page as a row group, and
    stop when a page returns fewer than PAGE_SIZE rows (the documented
    end-of-data signal — there is no total count).
    """
    table = NODE_TO_TABLE[node_id]
    asset = node_id  # the spec id IS the asset name
    schema = _schema_for(table)

    total = 0
    with raw_parquet_writer(asset, schema) as writer:
        for page in range(1, MAX_PAGES + 1):
            rows = _fetch_page(table, page)
            if rows:
                writer.write_table(pa.Table.from_pylist(rows, schema=schema))
                total += len(rows)
            if len(rows) < PAGE_SIZE:
                break
        else:
            # Loop ran to MAX_PAGES without a short page: the table grew past our
            # safety ceiling. Raise rather than publish a truncated snapshot.
            raise RuntimeError(
                f"{asset}: hit MAX_PAGES={MAX_PAGES} for table {table} without a "
                f"short page; source larger than expected — raise the ceiling."
            )
    print(f"{asset}: wrote {total} rows from {table} across {page} page(s)")


DOWNLOAD_SPECS = [
    NodeSpec(id=_node_id(e), fn=fetch_one, kind="download")
    for e in ENTITY_IDS
]


# --- Transform: one published Delta table per subset --------------------------
#
# Thin parse-and-type pass over the raw parquet view. Every column already
# carries its native type from the explicit parquet schema, so the only work is
# re-typing the date/datetime columns that were stored as ISO strings. The full
# re-pull overwrites raw each run, so there are no accumulated duplicates.
_SQL_CAST = {"date": "DATE", "datetime": "TIMESTAMP"}


def _select_sql(node_id: str) -> str:
    table = NODE_TO_TABLE[node_id]
    projections = []
    for col, dtype in TABLE_COLUMNS[table]:
        ident = f'"{col}"'
        target = _SQL_CAST.get(dtype)
        if target:
            projections.append(f"CAST({ident} AS {target}) AS {ident}")
        else:
            projections.append(ident)
    cols = ",\n        ".join(projections)
    return f'SELECT\n        {cols}\n    FROM "{node_id}"'


TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{s.id}-transform",
        deps=[s.id],
        sql=_select_sql(s.id),
    )
    for s in DOWNLOAD_SPECS
]
