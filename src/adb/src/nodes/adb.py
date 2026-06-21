"""Asian Development Bank — Key Indicators Database (KIDB) connector.

Catalog connector over the KIDB SDMX 3.0 REST API (agency ADB). Each entity is
one *leaf* dataflow (the collect stage dropped the parent aggregations, which
are unions of their children). For each dataflow we pull the entire table in a
single SDMX-CSV request using the wildcard key ``A..`` (annual frequency / all
indicators / all economies, all years 2000-2024) and publish it as one
long-format Delta table.

Fetch shape: **stateless full re-pull** (shape 1). The whole corpus is a few
dozen CSV pulls totalling well under 1GB and the data is annual with frequent
historical revisions, so we never trust a stored watermark — re-fetch and
overwrite every run.

Rate limit: the API documents 20 requests/minute and enforces it with a
*temporary IP block returned as HTTP 403* (not 429). Each spec issues exactly
one request, but sibling specs share the ADB host, so we classify 403/429/5xx
as transient and let exponential backoff wait out any block.
"""

import csv
import io

import httpx
import pyarrow as pa
from tenacity import (
    retry,
    retry_if_exception,
    stop_after_attempt,
    wait_exponential,
)

from subsets_utils import NodeSpec, SqlNodeSpec, get, save_raw_parquet

# Entity union (rank-active leaf dataflows) — copied from
# data/sources/adb/work/entity_union.json. Inlined per the no-module-IO rule.
from constants import ENTITY_IDS

_BASE = "https://kidb.adb.org/api/v4/sdmx"

# SDMX-CSV columns returned by the KIDB data endpoint (stable across dataflows).
# Kept verbatim as strings in raw; the transform casts/cleans. UNIT_MULT and
# DECIMALS are numeric upstream but stay strings here so the raw is a faithful
# capture and all typing happens in one place (the transform correctness gate).
_COLUMNS = [
    "DATAFLOW", "FREQ", "INDICATOR", "ECONOMY_CODE", "TIME_PERIOD",
    "OBS_VALUE", "UNIT", "UNIT_MULT", "DECIMALS", "OBS_STATUS",
    "REF_YEAR", "BASE_YEAR", "DATA_SOURCE", "METHODOLOGY", "FOOTNOTE",
]
_SCHEMA = pa.schema([(c, pa.string()) for c in _COLUMNS])

_TRANSIENT_EXC = (
    httpx.ConnectError, httpx.ConnectTimeout, httpx.ReadTimeout,
    httpx.WriteTimeout, httpx.PoolTimeout, httpx.RemoteProtocolError,
    httpx.ProxyError,
)


def _is_transient(exc: BaseException) -> bool:
    if isinstance(exc, _TRANSIENT_EXC):
        return True
    if isinstance(exc, httpx.HTTPStatusError):
        code = exc.response.status_code
        # 403 is the KIDB rate-limit temporary block; 429/5xx are standard.
        return code in (403, 429) or 500 <= code < 600
    return False


@retry(
    retry=retry_if_exception(_is_transient),
    stop=stop_after_attempt(8),
    wait=wait_exponential(min=4, max=120),
    reraise=True,
)
def _fetch_csv(dataflow_id: str) -> str:
    url = f"{_BASE}/data/ADB,{dataflow_id}/A.."
    resp = get(
        url,
        params={"format": "sdmx-csv"},
        timeout=(10.0, 180.0),
    )
    resp.raise_for_status()
    return resp.text


def _dataflow_from_node(node_id: str) -> str:
    """Recover the SDMX dataflow id from the spec id.

    Spec ids are ``adb-<entity_lower_with_dashes>``; dataflow ids are uppercase
    with underscores, so the round-trip is upper() + dash->underscore.
    """
    return node_id[len("adb-"):].upper().replace("-", "_")


def fetch_one(node_id: str) -> None:
    asset = node_id  # the runtime passes the spec id; it IS the asset name
    dataflow_id = _dataflow_from_node(node_id)

    text = _fetch_csv(dataflow_id)
    rows = list(csv.DictReader(io.StringIO(text)))

    # Normalise every row to the full column set (defensive against any column
    # the source omits on a given dataflow); missing cells become empty string.
    columns = {c: [] for c in _COLUMNS}
    for row in rows:
        for c in _COLUMNS:
            columns[c].append(row.get(c, "") or "")

    table = pa.table(columns, schema=_SCHEMA)
    save_raw_parquet(table, asset)


DOWNLOAD_SPECS = [
    NodeSpec(
        id=f"adb-{eid.lower().replace('_', '-')}",
        fn=fetch_one,
        kind="download",
    )
    for eid in ENTITY_IDS
]


# One published Delta table per dataflow: cast the faithful string raw into a
# typed long-format observations table. SDMX encodes "not available" as the
# ellipsis placeholder ('…'), so we drop rows whose OBS_VALUE is not numerically
# castable (no real observation) and then CAST the survivors to DOUBLE — that
# strict cast stays as a correctness gate for any genuinely unexpected value.
def _transform_sql(download_id: str) -> str:
    return f'''
        SELECT
            INDICATOR                                    AS indicator,
            ECONOMY_CODE                                 AS economy_code,
            CAST(TIME_PERIOD AS INTEGER)                 AS year,
            CAST(OBS_VALUE AS DOUBLE)                    AS value,
            NULLIF(UNIT, '')                             AS unit,
            TRY_CAST(NULLIF(UNIT_MULT, '') AS INTEGER)   AS unit_mult,
            TRY_CAST(NULLIF(DECIMALS, '') AS INTEGER)    AS decimals,
            NULLIF(OBS_STATUS, '')                       AS obs_status,
            NULLIF(REF_YEAR, '')                         AS ref_year,
            NULLIF(BASE_YEAR, '')                        AS base_year,
            NULLIF(DATA_SOURCE, '')                      AS data_source,
            NULLIF(METHODOLOGY, '')                      AS methodology,
            NULLIF(FOOTNOTE, '')                         AS footnote
        FROM "{download_id}"
        WHERE OBS_VALUE IS NOT NULL
          AND OBS_VALUE <> ''
          AND TRY_CAST(OBS_VALUE AS DOUBLE) IS NOT NULL
    '''


TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{s.id}-transform",
        deps=[s.id],
        sql=_transform_sql(s.id),
    )
    for s in DOWNLOAD_SPECS
]
