"""EEA Bathing Water Quality (WISE_BWD) — connector node module.

Access mechanism: EEA Discodata, a public REST-over-SQL gateway
(https://discodata.eea.europa.eu/sql). We snapshot the nine publishable views
of the [WISE_BWD].[latest] schema, one download node per view.

Fetch shape: **stateless full re-pull** (shape 1). Every refresh re-pulls each
whole table and overwrites its raw asset. BWD is an annual reporting programme
and late corrections/revisions rewrite historical rows in place, so a stored
watermark would silently skip revised rows — full re-pull picks them up for
free. The largest table (timeseries_MonitoringResult, ~2.85M rows) is paginated
at 100k rows/page and streamed to gzipped NDJSON so no full table is ever held
in memory.

Raw format: NDJSON. The views carry drifty/nullable columns and ISO
date/datetime strings of varying precision (e.g. "...:25.210"); NDJSON keeps the
raw untyped and the transform SQL casts on read, which is sturdier than forcing
a parquet schema over heterogeneous JSON.
"""

import json

from constants import ENTITY_IDS, TABLE_COLUMNS
from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    transient_retry,
    raw_writer,
)

SLUG = "eea-bathing-water"
BASE_URL = "https://discodata.eea.europa.eu/sql"
SCHEMA = "latest"          # [latest] is the alias for the newest BWD release
DATABASE = "WISE_BWD"
PAGE_SIZE = 100_000        # docs: a single page > ~100k truncates; keep at 100k
MAX_PAGES = 1_000          # safety ceiling — raises (never silently truncates)


def _node_id(entity_id: str) -> str:
    return f"{SLUG}-{entity_id.lower().replace('_', '-')}"


# Pure lookup built from a constant (no I/O): node id -> source table name.
# The node id lowercases and dash-folds the table name, which is lossy, so we
# cannot recover the original casing from the id alone — keep the map explicit.
NODE_TO_TABLE = {_node_id(e): e for e in ENTITY_IDS}


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
    payload = resp.json()
    # Response envelope is {"results": [ {row}, ... ]}; no total/row-count field,
    # so end-of-data is detected by a short page.
    return payload["results"]


def fetch_one(node_id: str) -> None:
    """Stateless full re-pull of one WISE_BWD table to gzipped NDJSON.

    Paginate p=1.. with nrOfHits=100000, writing each page as it arrives, and
    stop when a page returns fewer than PAGE_SIZE rows (the documented
    end-of-data signal — there is no total count).
    """
    table = NODE_TO_TABLE[node_id]
    asset = node_id  # the spec id IS the asset name

    total = 0
    with raw_writer(asset, "ndjson.gz", mode="wt", compression="gzip") as f:
        for page in range(1, MAX_PAGES + 1):
            rows = _fetch_page(table, page)
            for row in rows:
                f.write(json.dumps(row, separators=(",", ":")))
                f.write("\n")
            total += len(rows)
            if len(rows) < PAGE_SIZE:
                break
        else:
            # Loop exhausted without a short page: the table grew past our
            # safety ceiling. Raise loudly rather than publish a truncated snapshot.
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
# Each transform is a thin parse-and-type pass over the raw NDJSON view: rename
# nothing, cast every column to its declared WISE_BWD type. Source dataType ->
# DuckDB cast target. nvarchar/varchar stay VARCHAR (no cast). The full re-pull
# overwrites raw each run, so there are no accumulated duplicates to dedup.
_CAST = {
    "bit": "BOOLEAN",
    "int": "BIGINT",
    "float": "DOUBLE",
    "decimal": "DOUBLE",
    "date": "DATE",
    "datetime": "TIMESTAMP",
}


def _select_sql(node_id: str) -> str:
    table = NODE_TO_TABLE[node_id]
    projections = []
    for col, dtype in TABLE_COLUMNS[table]:
        ident = f'"{col}"'
        target = _CAST.get(dtype)
        if target:
            projections.append(f"CAST({ident} AS {target}) AS {ident}")
        else:  # nvarchar / varchar — already text
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
