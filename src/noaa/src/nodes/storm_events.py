"""NOAA storm-events — NWS Storm Events Database, per-year detail CSVs (gzip)
under the SWDI bulk directory.
"""

import csv
import gzip
import io
import re

import pyarrow as pa

from subsets_utils import NodeSpec, SqlNodeSpec, raw_parquet_writer

from utils import NCEI, _get_bytes, _list_hrefs, _string_table

STORM_DIR = f"{NCEI}/pub/data/swdi/stormevents/csvfiles/"
_STORM_RE = re.compile(r"StormEvents_details-ftp_v1\.0_d(\d{4})_c\d+\.csv\.gz$")


def fetch_storm_events(node_id: str) -> None:
    asset = node_id
    files: dict[int, str] = {}
    for h in _list_hrefs(STORM_DIR):
        m = _STORM_RE.match(h)
        if m:
            files[int(m.group(1))] = h  # one detail file per year
    if len(files) < 60:
        raise RuntimeError(
            f"storm-events: only {len(files)} yearly detail files at {STORM_DIR}; "
            "listing shape likely changed"
        )
    years = sorted(files)

    # Header from the earliest file defines the (all-string) schema; later files
    # must match it exactly or we treat it as silent source drift.
    first = gzip.decompress(_get_bytes(STORM_DIR + files[years[0]])).decode("latin-1")
    first_reader = csv.reader(io.StringIO(first))
    header = next(first_reader)
    schema = pa.schema([(c, pa.string()) for c in header])

    total = 0
    with raw_parquet_writer(asset, schema) as w:
        tbl = _string_table(header, first_reader, schema)
        total += tbl.num_rows
        w.write_table(tbl)
        for y in years[1:]:
            text = gzip.decompress(_get_bytes(STORM_DIR + files[y])).decode("latin-1")
            r = csv.reader(io.StringIO(text))
            h = next(r)
            if h != header:
                raise RuntimeError(f"storm-events {y}: header drift vs baseline")
            tbl = _string_table(header, r, schema)
            total += tbl.num_rows
            w.write_table(tbl)
    if total < 100000:
        raise RuntimeError(f"storm-events: only {total} rows across {len(years)} years")


DOWNLOAD_SPECS = [
    NodeSpec(id="noaa-storm-events", fn=fetch_storm_events, kind="download"),
]

_SQL = '''
        SELECT
            TRY_CAST(EVENT_ID AS BIGINT)                            AS event_id,
            TRY_CAST(EPISODE_ID AS BIGINT)                          AS episode_id,
            make_date(
                CAST(substr(BEGIN_YEARMONTH, 1, 4) AS INT),
                CAST(substr(BEGIN_YEARMONTH, 5, 2) AS INT),
                TRY_CAST(BEGIN_DAY AS INT)
            )                                                       AS begin_date,
            BEGIN_TIME                                              AS begin_time,
            TRY_CAST(YEAR AS INT)                                   AS year,
            MONTH_NAME                                              AS month_name,
            STATE                                                   AS state,
            TRY_CAST(STATE_FIPS AS INT)                             AS state_fips,
            EVENT_TYPE                                              AS event_type,
            CZ_TYPE                                                 AS cz_type,
            CZ_NAME                                                 AS cz_name,
            WFO                                                     AS wfo,
            TRY_CAST(INJURIES_DIRECT AS INT)                        AS injuries_direct,
            TRY_CAST(INJURIES_INDIRECT AS INT)                      AS injuries_indirect,
            TRY_CAST(DEATHS_DIRECT AS INT)                          AS deaths_direct,
            TRY_CAST(DEATHS_INDIRECT AS INT)                        AS deaths_indirect,
            DAMAGE_PROPERTY                                         AS damage_property,
            DAMAGE_CROPS                                            AS damage_crops,
            TRY_CAST(MAGNITUDE AS DOUBLE)                           AS magnitude,
            MAGNITUDE_TYPE                                          AS magnitude_type,
            TOR_F_SCALE                                             AS tor_f_scale,
            TRY_CAST(BEGIN_LAT AS DOUBLE)                           AS begin_lat,
            TRY_CAST(BEGIN_LON AS DOUBLE)                           AS begin_lon,
            TRY_CAST(END_LAT AS DOUBLE)                             AS end_lat,
            TRY_CAST(END_LON AS DOUBLE)                             AS end_lon,
            SOURCE                                                  AS source,
            FLOOD_CAUSE                                             AS flood_cause
        FROM "noaa-storm-events"
        WHERE TRY_CAST(EVENT_ID AS BIGINT) IS NOT NULL
        QUALIFY row_number() OVER (PARTITION BY EVENT_ID ORDER BY BEGIN_YEARMONTH) = 1
    '''

TRANSFORM_SPECS = [
    SqlNodeSpec(id="noaa-storm-events-transform", deps=["noaa-storm-events"], sql=_SQL),
]
