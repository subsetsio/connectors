"""CoCoRaHS connector — community precipitation & hail observations.

One export API (data.cocorahs.org/export/) serves a homogeneous corpus of
volunteer weather observations in a few distinct report-type feeds plus a
station reference table. Each feed is queried per US state + date range; the
US state is a column value, so each report type is ONE published table (never
one per state).

Volume note: the Daily feed is enormous (~5M reports/year, ~135 MB for a single
big state-year). It is pulled over a rolling multi-year window. The MultiDay /
Hail / SigWx / Stations feeds are small and pulled over full history (1998+).
"""

import calendar
import datetime as dt
import io
import time

import pyarrow as pa
import pyarrow.csv as pacsv

from subsets_utils import NodeSpec, SqlNodeSpec, get, raw_parquet_writer

REPORTS_URL = "https://data.cocorahs.org/export/exportreports.aspx"
STATIONS_URL = "https://data.cocorahs.org/export/exportstations.aspx"

# US states + DC + territories. CoCoRaHS station numbers are namespaced by these
# 2-letter codes; a state with no data returns a header-only response (skipped).
STATES = [
    "AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "DC", "FL", "GA", "HI",
    "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", "MA", "MI", "MN",
    "MS", "MO", "MT", "NE", "NV", "NH", "NJ", "NM", "NY", "NC", "ND", "OH",
    "OK", "OR", "PA", "RI", "SC", "SD", "TN", "TX", "UT", "VT", "VA", "WA",
    "WV", "WI", "WY", "AS", "GU", "MP", "PR", "VI",
]

# Exact CSV column lists per report type (ResponseFields=all), in header order.
# The Hail export emits a duplicate "MoreRainThanHail" header; the second
# occurrence is renamed so column names stay unique for parquet/DuckDB.
DAILY_COLS = [
    "ObservationDate", "ObservationTime", "EntryDateTime", "StationNumber",
    "StationName", "Latitude", "Longitude", "TotalPrecipAmt", "NewSnowDepth",
    "NewSnowSWE", "TotalSnowDepth", "TotalSnowSWE", "DateTimeStamp",
    "PrecipBegan", "PrecipEnded", "PrecipMinLasted", "HeavyPrecipBegan",
    "HeavyPrecipEnded", "HeavyPrecipMinLasted", "PrecipDurationAccuracy",
    "HasAdditionalData", "Flooding", "Notes",
]
MULTIDAY_COLS = [
    "StartDate", "EndDateTime", "EntryDateTime", "StationNumber", "StationName",
    "Latitude", "Longitude", "TotalPrecipAmt", "TotalSnowDepth", "TotalSnowSWE",
    "DateTimeStamp",
]
HAIL_COLS = [
    "ObservationDate", "ObservationTime", "EntryDateTime", "StationNumber",
    "StationName", "Latitude", "Longitude", "SmallestSize", "AverageSize",
    "LargestSize", "DurationMinutes", "DurationAccuracy", "Timing",
    "StoneConsistency", "MoreRainThanHail", "HailStarted", "LargestHailStarted",
    "MoreRainThanHail_2", "Damage", "AngleOfImpact", "NumberOfStonesOnPad",
    "DistanceBtwnStonesOnPad", "DepthOnGround", "DateTimeStamp",
]
SIGWX_COLS = [
    "ObservationDate", "ObservationTime", "EntryDateTime", "StationNumber",
    "StationName", "Latitude", "Longitude", "TotalPrecipAmt", "NewSnowDepth",
    "TotalSnowDepth", "DateTimeStamp", "Flooding", "PrecipDurationAmt",
    "PrecipDurationMin",
]
STATION_COLS = [
    "StationNumber", "StationName", "StationType", "State", "County", "City",
    "Latitude", "Longitude", "Elevation", "StationStatus", "CreationDate",
    "DateTimeStamp",
]

# node_id -> (ReportType, column list). The Daily feed is windowed; the rest
# are full-history (see _report_year_ranges).
REPORT_CONFIG = {
    "cocorahs-daily-reports": ("Daily", DAILY_COLS),
    "cocorahs-multiday-reports": ("MultiDay", MULTIDAY_COLS),
    "cocorahs-hail-reports": ("Hail", HAIL_COLS),
    "cocorahs-sigwx-reports": ("SigWx", SIGWX_COLS),
}

# Daily is pulled over a rolling window of this many calendar years (current
# year inclusive); other feeds go back to FULL_HISTORY_START.
DAILY_WINDOW_YEARS = 3
FULL_HISTORY_START = 1998


def _fetch_csv(url: str, params: dict) -> bytes:
    """GET a CSV export with polite backoff retries.

    The endpoint 500s intermittently and, more importantly, fails on
    oversized responses — so callers keep each request's date range small
    (the Daily feed is chunked by month).
    """
    last = None
    for attempt in range(6):
        try:
            resp = get(url, params=params, timeout=300)
            resp.raise_for_status()
            return resp.content
        except Exception as e:  # noqa: BLE001 - transient 5xx / timeouts
            last = e
            time.sleep(min(3 * (attempt + 1), 20))
    raise RuntimeError(f"failed to fetch {url} params={params}: {last}")


def _month_ranges(years: range) -> list[tuple[str, str]]:
    """(StartDate, EndDate) MM/DD/YYYY pairs, one per calendar month, so each
    Daily request stays small enough for the server to materialize."""
    out = []
    for y in years:
        for m in range(1, 13):
            last_day = calendar.monthrange(y, m)[1]
            out.append((f"{m:02d}/01/{y}", f"{m:02d}/{last_day:02d}/{y}"))
    return out


def _skip_invalid_row(row) -> str:
    """Drop genuinely malformed rows (free-text Notes fields occasionally carry
    unquoted line breaks that split a record into the wrong column count)."""
    return "skip"


def _parse_csv(content: bytes, columns: list[str], state: str | None) -> pa.Table:
    """Parse a CoCoRaHS CSV (all columns as strings) under a fixed schema.

    Handles the server's duplicate Hail header by supplying explicit column
    names and skipping the original header row, multi-line quoted Notes via
    newlines_in_values, and the rare unquoted-newline record via an
    invalid-row handler. Returns a 0-row table for header-only (empty)
    responses. When `state` is given it is appended as a constant column (the
    report CSVs carry no state field).
    """
    read_opts = pacsv.ReadOptions(column_names=columns, skip_rows=1)
    parse_opts = pacsv.ParseOptions(
        newlines_in_values=True, invalid_row_handler=_skip_invalid_row
    )
    convert_opts = pacsv.ConvertOptions(
        column_types={c: pa.string() for c in columns},
        strings_can_be_null=True,
    )
    table = pacsv.read_csv(
        io.BytesIO(content),
        read_options=read_opts,
        parse_options=parse_opts,
        convert_options=convert_opts,
    )
    if state is not None:
        table = table.append_column(
            "State", pa.array([state] * table.num_rows, pa.string())
        )
    return table


def _report_schema(columns: list[str]) -> pa.Schema:
    return pa.schema([(c, pa.string()) for c in columns] + [("State", pa.string())])


def fetch_reports(node_id: str) -> None:
    """Fetch one report-type feed across all states into a single parquet asset."""
    report_type, columns = REPORT_CONFIG[node_id]
    this_year = dt.date.today().year

    if report_type == "Daily":
        # Monthly chunks over the rolling window: the Daily feed is huge and the
        # server 500s on big (full-year, large-state) responses.
        date_ranges = _month_ranges(
            range(this_year - DAILY_WINDOW_YEARS + 1, this_year + 1)
        )
    else:
        # MultiDay / Hail / SigWx are small — one full-history request per state.
        date_ranges = [(f"01/01/{FULL_HISTORY_START}", f"12/31/{this_year}")]

    schema = _report_schema(columns)
    wrote_any = False
    with raw_parquet_writer(node_id, schema) as writer:
        for state in STATES:
            for start, end in date_ranges:
                content = _fetch_csv(
                    REPORTS_URL,
                    {
                        "Format": "csv",
                        "ReportType": report_type,
                        "ResponseFields": "all",
                        "state": state,
                        "ReportDateType": "reportdate",
                        "StartDate": start,
                        "EndDate": end,
                    },
                )
                table = _parse_csv(content, columns, state)
                if table.num_rows == 0:
                    continue
                writer.write_table(table.cast(schema))
                wrote_any = True
    if not wrote_any:
        raise RuntimeError(f"{node_id}: no rows fetched across any state")


def fetch_stations(node_id: str) -> None:
    """Fetch the station catalog across all states into one parquet asset."""
    schema = pa.schema([(c, pa.string()) for c in STATION_COLS])
    wrote_any = False
    with raw_parquet_writer(node_id, schema) as writer:
        for state in STATES:
            content = _fetch_csv(
                STATIONS_URL,
                {"format": "csv", "state": state, "responsefields": "all"},
            )
            table = _parse_csv(content, STATION_COLS, None)
            if table.num_rows == 0:
                continue
            writer.write_table(table.cast(schema))
            wrote_any = True
    if not wrote_any:
        raise RuntimeError(f"{node_id}: no station rows fetched")


DOWNLOAD_SPECS = [
    NodeSpec(id="cocorahs-daily-reports", fn=fetch_reports, kind="download"),
    NodeSpec(id="cocorahs-multiday-reports", fn=fetch_reports, kind="download"),
    NodeSpec(id="cocorahs-hail-reports", fn=fetch_reports, kind="download"),
    NodeSpec(id="cocorahs-sigwx-reports", fn=fetch_reports, kind="download"),
    NodeSpec(id="cocorahs-stations", fn=fetch_stations, kind="download"),
]

# strptime pattern for CoCoRaHS timestamps like "2024-01-01 02:32 PM".
_TS = "%Y-%m-%d %I:%M %p"

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="cocorahs-daily-reports-transform",
        deps=["cocorahs-daily-reports"],
        sql=f'''
            SELECT
                TRIM(StationNumber)                              AS station_number,
                TRIM(StationName)                                AS station_name,
                TRIM(State)                                      AS state,
                TRY_CAST(TRIM(ObservationDate) AS DATE)          AS observation_date,
                TRIM(ObservationTime)                            AS observation_time,
                TRY_CAST(TRIM(Latitude) AS DOUBLE)               AS latitude,
                TRY_CAST(TRIM(Longitude) AS DOUBLE)              AS longitude,
                TRY_CAST(TRIM(TotalPrecipAmt) AS DOUBLE)         AS total_precip_in,
                TRY_CAST(TRIM(NewSnowDepth) AS DOUBLE)           AS new_snow_in,
                TRY_CAST(TRIM(NewSnowSWE) AS DOUBLE)             AS new_snow_swe_in,
                TRY_CAST(TRIM(TotalSnowDepth) AS DOUBLE)         AS total_snow_depth_in,
                TRY_CAST(TRIM(TotalSnowSWE) AS DOUBLE)           AS total_snow_swe_in,
                TRIM(Flooding)                                   AS flooding,
                NULLIF(TRIM(Notes), '')                          AS notes,
                TRY(strptime(TRIM(DateTimeStamp), '{_TS}'))      AS updated_at
            FROM "cocorahs-daily-reports"
            WHERE TRY_CAST(TRIM(ObservationDate) AS DATE) IS NOT NULL
        ''',
        temporal="observation_date",
    ),
    SqlNodeSpec(
        id="cocorahs-multiday-reports-transform",
        deps=["cocorahs-multiday-reports"],
        sql=f'''
            SELECT
                TRIM(StationNumber)                              AS station_number,
                TRIM(StationName)                                AS station_name,
                TRIM(State)                                      AS state,
                TRY_CAST(TRIM(StartDate) AS DATE)                AS start_date,
                TRY(strptime(TRIM(EndDateTime), '{_TS}'))        AS end_datetime,
                TRY_CAST(TRIM(Latitude) AS DOUBLE)               AS latitude,
                TRY_CAST(TRIM(Longitude) AS DOUBLE)              AS longitude,
                TRY_CAST(TRIM(TotalPrecipAmt) AS DOUBLE)         AS total_precip_in,
                TRY_CAST(TRIM(TotalSnowDepth) AS DOUBLE)         AS total_snow_depth_in,
                TRY_CAST(TRIM(TotalSnowSWE) AS DOUBLE)           AS total_snow_swe_in,
                TRY(strptime(TRIM(DateTimeStamp), '{_TS}'))      AS updated_at
            FROM "cocorahs-multiday-reports"
            WHERE TRY_CAST(TRIM(StartDate) AS DATE) IS NOT NULL
        ''',
        temporal="start_date",
    ),
    SqlNodeSpec(
        id="cocorahs-hail-reports-transform",
        deps=["cocorahs-hail-reports"],
        sql=f'''
            SELECT
                TRIM(StationNumber)                              AS station_number,
                TRIM(StationName)                                AS station_name,
                TRIM(State)                                      AS state,
                TRY_CAST(TRIM(ObservationDate) AS DATE)          AS observation_date,
                TRIM(ObservationTime)                            AS observation_time,
                TRY_CAST(TRIM(Latitude) AS DOUBLE)               AS latitude,
                TRY_CAST(TRIM(Longitude) AS DOUBLE)              AS longitude,
                TRY_CAST(TRIM(SmallestSize) AS DOUBLE)           AS smallest_size_in,
                TRY_CAST(TRIM(AverageSize) AS DOUBLE)            AS average_size_in,
                TRY_CAST(TRIM(LargestSize) AS DOUBLE)            AS largest_size_in,
                TRY_CAST(TRIM(DurationMinutes) AS DOUBLE)        AS duration_minutes,
                TRIM(Timing)                                     AS timing,
                TRIM(StoneConsistency)                           AS stone_consistency,
                TRIM(MoreRainThanHail)                           AS more_rain_than_hail,
                TRY_CAST(TRIM(NumberOfStonesOnPad) AS DOUBLE)    AS number_of_stones_on_pad,
                TRY_CAST(TRIM(DepthOnGround) AS DOUBLE)          AS depth_on_ground_in,
                NULLIF(TRIM(Damage), '')                         AS damage,
                TRY(strptime(TRIM(DateTimeStamp), '{_TS}'))      AS updated_at
            FROM "cocorahs-hail-reports"
            WHERE TRY_CAST(TRIM(ObservationDate) AS DATE) IS NOT NULL
        ''',
        temporal="observation_date",
    ),
    SqlNodeSpec(
        id="cocorahs-sigwx-reports-transform",
        deps=["cocorahs-sigwx-reports"],
        sql=f'''
            SELECT
                TRIM(StationNumber)                              AS station_number,
                TRIM(StationName)                                AS station_name,
                TRIM(State)                                      AS state,
                TRY_CAST(TRIM(ObservationDate) AS DATE)          AS observation_date,
                TRIM(ObservationTime)                            AS observation_time,
                TRY_CAST(TRIM(Latitude) AS DOUBLE)               AS latitude,
                TRY_CAST(TRIM(Longitude) AS DOUBLE)              AS longitude,
                TRY_CAST(TRIM(TotalPrecipAmt) AS DOUBLE)         AS total_precip_in,
                TRY_CAST(TRIM(NewSnowDepth) AS DOUBLE)           AS new_snow_in,
                TRY_CAST(TRIM(TotalSnowDepth) AS DOUBLE)         AS total_snow_depth_in,
                TRIM(Flooding)                                   AS flooding,
                TRY_CAST(TRIM(PrecipDurationMin) AS DOUBLE)      AS precip_duration_min,
                TRY(strptime(TRIM(DateTimeStamp), '{_TS}'))      AS updated_at
            FROM "cocorahs-sigwx-reports"
            WHERE TRY_CAST(TRIM(ObservationDate) AS DATE) IS NOT NULL
        ''',
        temporal="observation_date",
    ),
    SqlNodeSpec(
        id="cocorahs-stations-transform",
        deps=["cocorahs-stations"],
        sql=f'''
            SELECT
                TRIM(StationNumber)                              AS station_number,
                TRIM(StationName)                                AS station_name,
                TRIM(StationType)                                AS station_type,
                TRIM(State)                                      AS state,
                TRIM(County)                                     AS county,
                TRIM(City)                                       AS city,
                TRY_CAST(TRIM(Latitude) AS DOUBLE)               AS latitude,
                TRY_CAST(TRIM(Longitude) AS DOUBLE)              AS longitude,
                TRY_CAST(TRIM(Elevation) AS DOUBLE)              AS elevation_ft,
                TRIM(StationStatus)                              AS status,
                TRY(strptime(TRIM(CreationDate), '{_TS}'))       AS created_at,
                TRY(strptime(TRIM(DateTimeStamp), '{_TS}'))      AS updated_at
            FROM "cocorahs-stations"
            WHERE TRIM(StationNumber) IS NOT NULL AND TRIM(StationNumber) <> ''
        ''',
        key=("station_number",),
        temporal="updated_at",
    ),
]
