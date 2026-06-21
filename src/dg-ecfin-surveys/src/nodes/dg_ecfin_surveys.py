"""DG ECFIN Joint Harmonised EU Business and Consumer Surveys.

One download per BCS dataflow, fetched whole from the ECFIN SDMX 2.1
dissemination API (same RedisStat stack as Eurostat) as SDMX-CSV. Each
dataflow is a tidy long table:

    DATAFLOW, LAST UPDATE, <dimension columns...>, TIME_PERIOD, OBS_VALUE

The dimension columns vary by survey product (the standard surveys carry
REF_AREA/ACTIVITY/INDICATOR/SEASONAL_ADJUST/FREQ, optionally SURVEY and
UNIT_MEASURE; the investment surveys swap INDICATOR for
TYPE_OF_INVESTMENT/INV_PERIOD, STIMULATING_FACTOR or
STRUCTURE_OF_THE_INVESTMENT), so we land every column as a string and let one
generic transform cast OBS_VALUE and pass the native dimensions through.

Fetch shape: stateless full re-pull. The whole corpus is a few hundred MB and
revises historically (monthly publication, end of month), so we never trust a
stored watermark — re-fetch each dataflow in full and overwrite. The API
exposes no all-dataflows bulk dump; per-dataflow SDMX-CSV IS the bulk path.
Note: a plain unfiltered request returns the full table, but adding a
`lastNObservations`/`startPeriod` filter trips a 1M-row size estimate (HTTP
413) on the large subsector flows — so we deliberately pass no filter.
"""

import csv
import io

import pyarrow as pa
import pyarrow.csv as pacsv

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    save_raw_parquet,
    transient_retry,
)

PREFIX = "dg-ecfin-surveys-"
BASE = "https://webgate.ec.europa.eu/ecfin/redisstat/api/dissemination/sdmx/2.1/data"

# The entity union — one BCS dataflow per entry (collect + rank).
from constants import ENTITY_IDS


@transient_retry()
def _fetch_csv(dataflow: str) -> bytes:
    url = f"{BASE}/{dataflow}"
    # (connect, read) — the large subsector flows are several hundred MB.
    resp = get(
        url,
        params={"format": "SDMX-CSV", "lang": "en"},
        timeout=(30.0, 900.0),
    )
    resp.raise_for_status()
    return resp.content


def _dataflow_for(node_id: str) -> str:
    return node_id[len(PREFIX):].upper().replace("-", "_")


def fetch_one(node_id: str) -> None:
    asset = node_id
    raw = _fetch_csv(_dataflow_for(node_id))

    # Header tells us the real column names; data rows carry one extra trailing
    # (empty) field beyond the header — name every physical column so pyarrow
    # parses cleanly, then keep only the named header columns.
    reader = csv.reader(io.StringIO(raw.decode("utf-8")))
    header = next(reader)
    first_row = next(reader, None)
    width = max(len(header), len(first_row) if first_row else 0)
    col_names = list(header) + [f"_extra{i}" for i in range(len(header), width)]

    table = pacsv.read_csv(
        pa.py_buffer(raw),
        read_options=pacsv.ReadOptions(column_names=col_names, skip_rows=1),
        parse_options=pacsv.ParseOptions(newlines_in_values=False),
        convert_options=pacsv.ConvertOptions(
            column_types={name: pa.string() for name in col_names},
            strings_can_be_null=False,
        ),
    )
    table = table.select(header)  # drop the unnamed trailing field(s)
    save_raw_parquet(table, asset)


DOWNLOAD_SPECS = [
    NodeSpec(
        id=f"{PREFIX}{eid.lower().replace('_', '-')}",
        fn=fetch_one,
        kind="download",
    )
    for eid in ENTITY_IDS
]

# One generic transform per dataflow: drop the constant DATAFLOW dimension,
# cast OBS_VALUE to DOUBLE (empty cells -> NULL, filtered out), and pass every
# native dimension column through unchanged. Identical SQL across all flows
# because `* EXCLUDE` adapts to whichever dimensions a flow exposes.
TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{s.id}-transform",
        deps=[s.id],
        sql=f'''
            SELECT
                * EXCLUDE (DATAFLOW, "LAST UPDATE", TIME_PERIOD, OBS_VALUE),
                TIME_PERIOD               AS time_period,
                TRY_CAST(OBS_VALUE AS DOUBLE) AS obs_value,
                "LAST UPDATE"             AS last_update
            FROM "{s.id}"
            WHERE TRY_CAST(OBS_VALUE AS DOUBLE) IS NOT NULL
        ''',
    )
    for s in DOWNLOAD_SPECS
]
