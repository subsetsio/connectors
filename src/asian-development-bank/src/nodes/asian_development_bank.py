"""Asian Development Bank — Key Indicators Database (KIDB) connector.

Mechanism: KIDB SDMX 3.0 REST API at https://kidb.adb.org/api/v4/sdmx.

One download node per rank-active dataflow (leaf thematic table). Each node
pulls the dataflow's full table in a single CSV request with the wildcard key
`A..` (annual frequency, all indicators, all economies) — KIDB is an annual
publication, so all observations are annual. The `..` (all-frequency) key
404s on this server; `A..` is the working full-table query.

Strategy: stateless full re-pull. Each dataflow CSV is small (tens of
thousands of rows at most), so we re-fetch the whole table every run and
overwrite — revisions and late corrections are picked up for free. No
watermark, no cursor.

Raw is saved as parquet with an all-string schema (faithful to the CSV); the
SQL transform casts/types and reshapes into a clean long-format table.
"""

import io
import csv

import pyarrow as pa

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    transient_retry,
    save_raw_parquet,
)
from constants import ENTITY_IDS

SLUG = "asian-development-bank"
BASE = "https://kidb.adb.org/api/v4/sdmx/data/ADB,"

# The 15 SDMX-CSV columns, stored verbatim as strings. The transform types them.
CSV_COLUMNS = [
    "DATAFLOW",
    "FREQ",
    "INDICATOR",
    "ECONOMY_CODE",
    "TIME_PERIOD",
    "OBS_VALUE",
    "UNIT",
    "UNIT_MULT",
    "DECIMALS",
    "OBS_STATUS",
    "REF_YEAR",
    "BASE_YEAR",
    "DATA_SOURCE",
    "METHODOLOGY",
    "FOOTNOTE",
]
SCHEMA = pa.schema([(c, pa.string()) for c in CSV_COLUMNS])


def _dataflow_id(node_id: str) -> str:
    """Recover the KIDB dataflow id from a download spec id.

    'asian-development-bank-egelc-eg' -> 'EGELC_EG'
    """
    eid = node_id[len(SLUG) + 1:]            # strip 'asian-development-bank-'
    return eid.upper().replace("-", "_")


@transient_retry()  # 6 attempts, exp backoff over transient net errors + 429 + 5xx
def _fetch_csv(dataflow_id: str) -> str:
    url = f"{BASE}{dataflow_id}/A..?format=sdmx-csv"
    resp = get(url, timeout=(10.0, 180.0))
    resp.raise_for_status()
    return resp.text


def fetch_one(node_id: str) -> None:
    asset = node_id                          # the spec id IS the asset name
    dataflow_id = _dataflow_id(node_id)
    text = _fetch_csv(dataflow_id)

    reader = csv.DictReader(io.StringIO(text))
    columns = {c: [] for c in CSV_COLUMNS}
    for row in reader:
        for c in CSV_COLUMNS:
            columns[c].append(row.get(c))

    table = pa.table({c: pa.array(columns[c], type=pa.string()) for c in CSV_COLUMNS},
                     schema=SCHEMA)
    save_raw_parquet(table, asset)


DOWNLOAD_SPECS = [
    NodeSpec(
        id=f"{SLUG}-{eid.lower().replace('_', '-')}",
        fn=fetch_one,
        kind="download",
    )
    for eid in ENTITY_IDS
]


def _transform_sql(download_id: str) -> str:
    return f'''
        SELECT
            INDICATOR                                        AS indicator,
            ECONOMY_CODE                                     AS economy_code,
            CAST(TIME_PERIOD AS INTEGER)                     AS year,
            CAST(OBS_VALUE AS DOUBLE)                        AS value,
            NULLIF(UNIT, '')                                 AS unit,
            TRY_CAST(NULLIF(UNIT_MULT, '') AS INTEGER)       AS unit_mult,
            TRY_CAST(NULLIF(DECIMALS, '') AS INTEGER)        AS decimals,
            NULLIF(OBS_STATUS, '')                           AS obs_status,
            NULLIF(REF_YEAR, '')                             AS ref_year,
            NULLIF(BASE_YEAR, '')                            AS base_year,
            NULLIF(DATA_SOURCE, '')                          AS data_source,
            NULLIF(FOOTNOTE, '')                             AS footnote
        FROM "{download_id}"
        WHERE OBS_VALUE IS NOT NULL AND OBS_VALUE <> ''
          AND TRY_CAST(OBS_VALUE AS DOUBLE) IS NOT NULL
          AND TRY_CAST(TIME_PERIOD AS INTEGER) IS NOT NULL
          AND INDICATOR IS NOT NULL
          AND ECONOMY_CODE IS NOT NULL
    '''


TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{s.id}-transform",
        deps=[s.id],
        sql=_transform_sql(s.id),
    )
    for s in DOWNLOAD_SPECS
]
