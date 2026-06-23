"""GeyserTimes (Yellowstone) connector.

Mechanism: GeyserTimes REST API v5 (https://www.geysertimes.org/api/v5),
public read-only JSON, no auth. Two published subsets:

  - eruptions: the core corpus of logged geyser eruption events. There is no
    bulk-dump endpoint; the /entries/{fromEpoch}/{toEpoch} endpoint returns all
    eruptions in a time window in one un-paginated response, so the full corpus
    is re-pulled every run by chunking the time axis one calendar year at a time
    (stateless full re-pull — revisions/late corrections picked up for free).
    Each year is written as its own raw parquet batch; the transform view
    glob-unions them. The API floors fromEpoch at 0 (negative epochs return
    nothing), so 1970 is the earliest reachable year; the end year is discovered
    dynamically from the wall clock.
  - geysers: the geyser reference/dimension table (one call to /geysers).

Datetimes are returned as Unix epoch seconds by default (we do NOT pass
?iso=1) and are converted in the transform SQL. All API values arrive as JSON
strings (or null); raw is stored as all-string parquet and cast downstream.
"""

from datetime import datetime, timezone

import pyarrow as pa

from subsets_utils import NodeSpec, SqlNodeSpec, get, transient_retry, save_raw_parquet

BASE = "https://www.geysertimes.org/api/v5"

# Earliest year reachable via the epoch endpoint (negative epochs return nothing).
START_YEAR = 1970

# All API fields stored verbatim as strings; cast in the transform.
ERUPTION_SCHEMA = pa.schema([
    ("eruptionID", pa.string()),
    ("geyserID", pa.string()),
    ("geyser", pa.string()),
    ("time", pa.string()),
    ("hasSeconds", pa.string()),
    ("exact", pa.string()),
    ("ns", pa.string()),
    ("ie", pa.string()),
    ("E", pa.string()),
    ("A", pa.string()),
    ("wc", pa.string()),
    ("ini", pa.string()),
    ("maj", pa.string()),
    ("min", pa.string()),
    ("q", pa.string()),
    ("duration", pa.string()),
    ("durationSec", pa.string()),
    ("durationRes", pa.string()),
    ("durationMod", pa.string()),
    ("entrant", pa.string()),
    ("entrantID", pa.string()),
    ("observer", pa.string()),
    ("comment", pa.string()),
    ("timeUpdated", pa.string()),
    ("timeEntered", pa.string()),
    ("primaryID", pa.string()),
])

GEYSER_SCHEMA = pa.schema([
    ("id", pa.string()),
    ("name", pa.string()),
    ("latitude", pa.string()),
    ("longitude", pa.string()),
    ("timezone", pa.string()),
    ("groupID", pa.string()),
    ("groupName", pa.string()),
    ("serverUpdate", pa.string()),
])


@transient_retry()
def _fetch(url):
    resp = get(url, timeout=(10.0, 180.0))
    resp.raise_for_status()
    return resp.json()


def _year_bounds(year):
    lo = int(datetime(year, 1, 1, tzinfo=timezone.utc).timestamp())
    hi = int(datetime(year + 1, 1, 1, tzinfo=timezone.utc).timestamp())
    return lo, hi


def fetch_eruptions(node_id):
    """Full re-pull of every eruption, one raw parquet batch per calendar year.

    Each batch overwrites itself every run; the transform globs all batches.
    """
    end_year = datetime.now(tz=timezone.utc).year
    for year in range(START_YEAR, end_year + 1):
        lo, hi = _year_bounds(year)
        data = _fetch(f"{BASE}/entries/{lo}/{hi}")
        rows = data.get("entries", [])
        table = pa.Table.from_pylist(rows, schema=ERUPTION_SCHEMA)
        save_raw_parquet(table, f"{node_id}-{year}")


def fetch_geysers(node_id):
    """The geyser reference table — one call returns the full catalog."""
    data = _fetch(f"{BASE}/geysers")
    rows = data.get("geysers", [])
    table = pa.Table.from_pylist(rows, schema=GEYSER_SCHEMA)
    save_raw_parquet(table, node_id)


DOWNLOAD_SPECS = [
    NodeSpec(id="geysertimes-eruptions", fn=fetch_eruptions, kind="download"),
    NodeSpec(id="geysertimes-geysers", fn=fetch_geysers, kind="download"),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="geysertimes-eruptions-transform",
        deps=["geysertimes-eruptions"],
        sql='''
            SELECT
                CAST(eruptionID AS BIGINT)               AS eruption_id,
                CAST(geyserID AS BIGINT)                 AS geyser_id,
                geyser                                   AS geyser_name,
                to_timestamp(CAST("time" AS BIGINT))     AS eruption_time,
                NULLIF(duration, '')                     AS duration_text,
                CAST(NULLIF(durationSec, '') AS INTEGER) AS duration_sec,
                durationRes                              AS duration_res,
                durationMod                              AS duration_mod,
                exact = '1'                              AS is_exact,
                ns = '1'                                 AS is_ns,
                ie = '1'                                 AS is_in_eruption,
                E = '1'                                  AS is_electronic,
                A = '1'                                  AS is_a,
                wc = '1'                                 AS is_webcam,
                ini = '1'                                AS is_initial,
                maj = '1'                                AS is_major,
                "min" = '1'                              AS is_minor,
                q = '1'                                  AS is_questionable,
                hasSeconds = '1'                         AS has_seconds,
                NULLIF(entrant, '')                      AS entrant,
                CAST(NULLIF(entrantID, '') AS BIGINT)    AS entrant_id,
                NULLIF(observer, '')                     AS observer,
                NULLIF(comment, '')                      AS comment,
                CAST(primaryID AS BIGINT)                AS primary_id,
                to_timestamp(CAST(timeEntered AS BIGINT)) AS entered_at,
                to_timestamp(CAST(timeUpdated AS BIGINT)) AS updated_at
            FROM "geysertimes-eruptions"
            WHERE eruptionID IS NOT NULL AND "time" IS NOT NULL
            QUALIFY row_number() OVER (
                PARTITION BY eruptionID ORDER BY CAST(timeUpdated AS BIGINT) DESC
            ) = 1
        ''',
    ),
    SqlNodeSpec(
        id="geysertimes-geysers-transform",
        deps=["geysertimes-geysers"],
        sql='''
            SELECT
                CAST(id AS BIGINT)                        AS geyser_id,
                name                                      AS geyser_name,
                CAST(NULLIF(latitude, '') AS DOUBLE)      AS latitude,
                CAST(NULLIF(longitude, '') AS DOUBLE)     AS longitude,
                NULLIF(timezone, '')                      AS timezone,
                CAST(NULLIF(groupID, '') AS BIGINT)       AS group_id,
                NULLIF(groupName, '')                     AS group_name,
                to_timestamp(CAST(serverUpdate AS BIGINT)) AS server_update
            FROM "geysertimes-geysers"
            WHERE id IS NOT NULL
            QUALIFY row_number() OVER (
                PARTITION BY id ORDER BY CAST(serverUpdate AS BIGINT) DESC
            ) = 1
        ''',
    ),
]
