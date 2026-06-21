"""NOAA Regional Snowfall Index (RSI) event table — pick the newest dated CSV
in access/.
"""

import csv
import io
import re

import pyarrow as pa

from subsets_utils import NodeSpec, SqlNodeSpec, save_raw_parquet

from utils import NCEI, _get_text, _list_hrefs, _normalize_header, _string_table

RSI_DIR = f"{NCEI}/data/regional-snowfall-index/access/"
_RSI_RE = re.compile(r"regional-snowfall-index_c\d+\.csv$")


def fetch_rsi(node_id: str) -> None:
    files = sorted(h for h in _list_hrefs(RSI_DIR) if _RSI_RE.match(h))
    if not files:
        raise RuntimeError(f"rsi: no dated CSV found at {RSI_DIR}")
    text = _get_text(RSI_DIR + files[-1])
    reader = csv.reader(io.StringIO(text))
    header = _normalize_header(next(reader))
    schema = pa.schema([(c, pa.string()) for c in header])
    table = _string_table(header, reader, schema)
    if table.num_rows < 50:
        raise RuntimeError(f"rsi: only {table.num_rows} rows in {files[-1]}")
    save_raw_parquet(table, node_id)


DOWNLOAD_SPECS = [
    NodeSpec(id="noaa-regional-snowfall-index", fn=fetch_rsi, kind="download"),
]

_SQL = '''
        SELECT
            REGION                          AS region,
            COALESCE(try_strptime("Start", '%m/%d/%Y')::DATE, TRY_CAST("Start" AS DATE)) AS start_date,
            COALESCE(try_strptime("End", '%m/%d/%Y')::DATE, TRY_CAST("End" AS DATE))     AS end_date,
            TRY_CAST(RSI AS DOUBLE)         AS rsi,
            TRY_CAST(CATEGORY AS INT)       AS category,
            TRY_CAST(TERM1PCT AS DOUBLE)    AS term1_pct,
            TRY_CAST(TERM2PCT AS DOUBLE)    AS term2_pct,
            TRY_CAST(TERM3PCT AS DOUBLE)    AS term3_pct,
            TRY_CAST(TERM4PCT AS DOUBLE)    AS term4_pct,
            TRY_CAST(AREA0 AS BIGINT)       AS area0,
            TRY_CAST(POP0 AS BIGINT)        AS pop0,
            TRY_CAST(AREA1 AS BIGINT)       AS area1,
            TRY_CAST(POP1 AS BIGINT)        AS pop1,
            TRY_CAST(AREA2 AS BIGINT)       AS area2,
            TRY_CAST(POP2 AS BIGINT)        AS pop2,
            TRY_CAST(AREA3 AS BIGINT)       AS area3,
            TRY_CAST(POP3 AS BIGINT)        AS pop3,
            TRY_CAST(AREA4 AS BIGINT)       AS area4,
            TRY_CAST(POP4 AS BIGINT)        AS pop4,
            STORM_ID                        AS storm_id,
            TRY_CAST(REGION_CODE AS INT)    AS region_code,
            TRY_CAST(YEAR AS INT)           AS year,
            TRY_CAST(MONTH AS INT)          AS month
        FROM "noaa-regional-snowfall-index"
        WHERE STORM_ID IS NOT NULL
        QUALIFY row_number() OVER (PARTITION BY STORM_ID, REGION_CODE ORDER BY YEAR) = 1
    '''

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="noaa-regional-snowfall-index-transform",
        deps=["noaa-regional-snowfall-index"],
        sql=_SQL,
    ),
]
