"""EEA Bathing Water Quality (WISE_BWD) — connector node module.

Access mechanism: EEA Discodata, a public REST-over-SQL gateway
(https://discodata.eea.europa.eu/sql). We snapshot the eleven publishable views
of the [WISE_BWD].[latest] schema, one download node per view.

Fetch shape: **stateless full re-pull** (shape 1). Every refresh re-pulls each
whole table and overwrites its raw asset. BWD is an annual reporting programme
and late corrections/revisions rewrite historical rows in place, so a stored
watermark would silently skip revised rows — full re-pull picks them up for free.

Pagination: the gateway uses `p` (1-based page) + `nrOfHits` (page size). A deep
OFFSET on a multi-million-row table makes the *server-side* query time out (the
gateway then answers HTTP 200 with `{"errors":[{"error":"Query timed out"}]}`),
so we never paginate a huge table by raw offset. Every table that carries a
`season` (reporting year) is fetched **partitioned by season**: we discover the
distinct seasons, then pull each season's rows separately. The biggest table
(timeseries_MonitoringResult, ~2.85M rows) tops out around ~185k rows in a single
season, so per-partition offsets stay ≤ one page and the timeout never triggers.
Pages within a partition are ordered by the row id so OFFSET paging is stable.
The one table without a season (spatial_ProtectedArea, ~31k rows) is small enough
to page by plain offset. Each table streams to parquet row-group by row-group, so
no whole table is held in memory.

Raw format: **parquet with an explicit per-column schema** derived from the
WISE_BWD view definitions (constants.TABLE_COLUMNS). The views have fixed,
documented column types, so an explicit schema is the strongest contract: type
drift raises at table-construction time. Date/datetime values arrive as ISO
strings and are kept as strings in raw (lossless), then CAST to DATE / TIMESTAMP
in the transform — sidestepping JSON reader type-inference ambiguity.
"""

import pyarrow as pa
from tenacity import (
    retry,
    retry_if_exception,
    stop_after_attempt,
    wait_exponential,
)

from constants import ENTITY_IDS, TABLE_COLUMNS
from subsets_utils import (
    NodeSpec,
    get,
    is_transient,
    raw_parquet_writer,
)

SLUG = "eea-bathing-water"
BASE_URL = "https://discodata.eea.europa.eu/sql"
DATABASE = "WISE_BWD"
SCHEMA = "latest"          # [latest] is the alias for the newest BWD release
PAGE_SIZE = 100_000        # docs: a single page > ~100k truncates; keep at 100k
MAX_PAGES = 1_000          # safety ceiling per partition — raises, never truncates

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


class _GatewayError(Exception):
    """A Discodata 200-OK response carrying an `errors` envelope instead of
    `results` (e.g. server-side 'Query timed out'). Treated as transient."""


def _node_id(entity_id: str) -> str:
    return f"{SLUG}-{entity_id.lower().replace('_', '-')}"


# Pure lookups built from constants (no I/O). The node id lowercases and
# dash-folds the table name, which is lossy, so the original casing cannot be
# recovered from the id alone — keep the map explicit.
NODE_TO_TABLE = {_node_id(e): e for e in ENTITY_IDS}


def _columns(table: str) -> list[str]:
    return [col for col, _ in TABLE_COLUMNS[table]]


def _schema_for(table: str) -> pa.Schema:
    return pa.schema([(col, _PA_TYPE[dtype]) for col, dtype in TABLE_COLUMNS[table]])


def _order_col(table: str) -> str | None:
    """A stable unique-ish column to ORDER BY so OFFSET paging is deterministic.
    Every WISE_BWD view exposes a per-row id (UID, lowercase uid on one view);
    None for the country aggregate, which is tiny and never pages past page 1."""
    cols = _columns(table)
    for cand in ("UID", "uid"):
        if cand in cols:
            return cand
    return None


def _retryable(exc: BaseException) -> bool:
    # Standard transient classification (network / 429 / 5xx) PLUS the gateway's
    # 200-OK "Query timed out" envelope, which is load-related and clears on retry.
    return is_transient(exc) or isinstance(exc, _GatewayError)


@retry(
    retry=retry_if_exception(_retryable),
    stop=stop_after_attempt(6),
    wait=wait_exponential(min=4, max=120),
    reraise=True,
)
def _run_query(sql: str, page: int) -> list[dict]:
    """Run one SQL query page against the gateway. Raises on non-2xx (transient
    5xx/429 retried) and on the `errors` envelope (retried as _GatewayError)."""
    resp = get(
        BASE_URL,
        params={"query": sql, "p": page, "nrOfHits": PAGE_SIZE},
        timeout=(10.0, 300.0),
    )
    resp.raise_for_status()
    payload = resp.json()
    if "results" not in payload:
        errs = payload.get("errors")
        msg = (
            errs[0].get("error")
            if isinstance(errs, list) and errs and isinstance(errs[0], dict)
            else str(payload)[:200]
        )
        raise _GatewayError(f"gateway returned no 'results' (page {page}): {msg}")
    return payload["results"]


def _paginate(writer, schema: pa.Schema, base_sql: str, label: str) -> int:
    """Page through base_sql, writing each page as a parquet row group. Stops on a
    short page; raises if MAX_PAGES is hit without one (source grew unexpectedly)."""
    total = 0
    for page in range(1, MAX_PAGES + 1):
        rows = _run_query(base_sql, page)
        if rows:
            writer.write_table(pa.Table.from_pylist(rows, schema=schema))
            total += len(rows)
        if len(rows) < PAGE_SIZE:
            return total
    raise RuntimeError(
        f"{label}: hit MAX_PAGES={MAX_PAGES} without a short page; "
        f"partition larger than expected — raise the ceiling."
    )


def fetch_one(node_id: str) -> None:
    """Stateless full re-pull of one WISE_BWD table to parquet.

    Season-bearing tables are pulled one season at a time (keeping the server-side
    OFFSET small); the season-less spatial table is paged by plain offset.
    """
    table = NODE_TO_TABLE[node_id]
    asset = node_id  # the spec id IS the asset name
    schema = _schema_for(table)
    fqtn = f"[{DATABASE}].[{SCHEMA}].[{table}]"
    order = _order_col(table)
    order_clause = f" ORDER BY {order}" if order else ""

    total = 0
    with raw_parquet_writer(asset, schema) as writer:
        if "season" in _columns(table):
            # Discover seasons (a tiny DISTINCT result), then pull each separately.
            seasons = sorted(
                {r["season"] for r in _run_query(f"SELECT DISTINCT season FROM {fqtn}", 1)},
                key=lambda v: (v is None, v),
            )
            for season in seasons:
                cond = "season IS NULL" if season is None else f"season = {int(season)}"
                base = f"SELECT * FROM {fqtn} WHERE {cond}{order_clause}"
                total += _paginate(writer, schema, base, f"{asset} season={season}")
        else:
            base = f"SELECT * FROM {fqtn}{order_clause}"
            total += _paginate(writer, schema, base, asset)
    print(f"{asset}: wrote {total} rows from {table}")


DOWNLOAD_SPECS = [
    NodeSpec(id=_node_id(e), fn=fetch_one, kind="download")
    for e in ENTITY_IDS
]
