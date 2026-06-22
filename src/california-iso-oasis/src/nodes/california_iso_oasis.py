"""CAISO OASIS connector.

OASIS is a report-servlet API: one HTTP GET to
https://oasis.caiso.com/oasisapi/SingleZip per (queryname, market, date-window)
returns a ZIP wrapping a CSV (resultformat=6). Each `queryname` is a distinct
report with its own column list, so each report publishes its own Delta table.

Shape: incremental date-batched backfill (firehose). The OASIS corpus is an
unbounded time series stretching back years, so we do NOT re-pull the whole
history every run. Each fetch fn walks 31-day windows (the API's per-request cap)
from its watermark forward to the live edge, writing one raw NDJSON batch per
window and advancing the watermark after each. Re-runs resume at the last window
(re-fetching the open/current window to pick up late-arriving and revised
intervals — duplicates are removed in the transform with SELECT DISTINCT).

Raw is saved as NDJSON (all values are strings straight from the CSV); the SQL
transform casts and dedups. The four LMP reports are fetched for the canonical
trading-hub price nodes (see constants.HUB_NODES); aggregate/system reports carry
no node filter.
"""

import csv
import io
import time
import zipfile
from datetime import date, datetime, timedelta, timezone

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    transient_retry,
    save_raw_ndjson,
    load_state,
    save_state,
)
from constants import REPORTS, SOURCE_MIN_DATE

SLUG = "california-iso-oasis"
BASE_URL = "https://oasis.caiso.com/oasisapi/SingleZip"
WINDOW_DAYS = 31                 # OASIS per-request window cap
REQUEST_SPACING_S = 5            # respect documented ~1 req / 5s throttle
STATE_VERSION = 1


def _spec_id(entity_id: str) -> str:
    return f"{SLUG}-{entity_id.lower().replace('_', '-')}"


def _entity_from_spec_id(node_id: str) -> str:
    return node_id[len(SLUG) + 1:].upper().replace("-", "_")


@transient_retry()  # retries transient network errors + 429 + 5xx with backoff
def _fetch_zip(params: dict) -> bytes:
    resp = get(BASE_URL, params=params, timeout=(10.0, 180.0))
    resp.raise_for_status()
    return resp.content


def _parse_window(content: bytes) -> list[dict]:
    """Unzip an OASIS response and return its CSV rows as dicts.

    Returns [] for windows the source reports as having no data. Raises on a
    genuine parameter error (a bug in our query construction), so it surfaces
    loudly instead of silently producing an empty asset.
    """
    zf = zipfile.ZipFile(io.BytesIO(content))
    names = zf.namelist()
    if not names:
        return []
    name = names[0]
    payload = zf.read(name).decode("utf-8", errors="replace")
    if name.endswith(".xml") or "INVALID_REQUEST" in name:
        if "Invalid Parameters" in payload or "ERR_CODE>1001" in payload:
            raise RuntimeError(f"OASIS rejected query parameters: {payload[:300]}")
        # e.g. no data available for this window — treat as empty, not an error.
        return []
    reader = csv.DictReader(io.StringIO(payload))
    return [dict(row) for row in reader]


def fetch_one(node_id: str) -> None:
    entity_id = _entity_from_spec_id(node_id)
    cfg = REPORTS[entity_id]

    state = load_state(node_id)
    if state.get("schema_version") != STATE_VERSION:
        state = {}
    watermark = state.get("watermark", SOURCE_MIN_DATE)

    begin = datetime.strptime(watermark, "%Y%m%d").date()
    today = datetime.now(tz=timezone.utc).date()

    cur = begin
    while cur <= today:
        end = min(cur + timedelta(days=WINDOW_DAYS), today + timedelta(days=1))
        params = {
            "queryname": cfg["queryname"],
            "version": cfg["version"],
            "startdatetime": f"{cur:%Y%m%d}T08:00-0000",
            "enddatetime": f"{end:%Y%m%d}T08:00-0000",
            "resultformat": 6,
        }
        if cfg.get("market_run_id"):
            params["market_run_id"] = cfg["market_run_id"]
        if cfg.get("node"):
            params["node"] = cfg["node"]
        params.update(cfg.get("extra", {}))

        rows = _parse_window(_fetch_zip(params))
        if rows:
            # batch key is pure batch info (window start); the transform globs all
            batch_asset = f"{node_id}-{cur:%Y%m%d}"
            save_raw_ndjson(rows, batch_asset)        # write raw FIRST
        save_state(node_id, {                          # then advance watermark
            "schema_version": STATE_VERSION,
            "watermark": f"{cur:%Y%m%d}",
        })
        if end > today:
            break
        cur = end
        time.sleep(REQUEST_SPACING_S)


DOWNLOAD_SPECS = [
    NodeSpec(id=_spec_id(eid), fn=fetch_one, kind="download")
    for eid in REPORTS
]


# --- Transforms: one published Delta table per report ---------------------
# Raw NDJSON carries every column as a string; each SQL casts to typed columns,
# renames to stable snake_case, and SELECT DISTINCT removes the duplicate rows
# produced by re-fetching the open window on each refresh.

_LMP = """
    SELECT DISTINCT
        CAST(INTERVALSTARTTIME_GMT AS TIMESTAMPTZ) AS interval_start_utc,
        CAST(INTERVALENDTIME_GMT   AS TIMESTAMPTZ) AS interval_end_utc,
        CAST(OPR_DT AS DATE)        AS operating_date,
        TRY_CAST(OPR_HR AS INTEGER) AS operating_hour,
        {interval}
        NODE          AS node,
        MARKET_RUN_ID AS market_run_id,
        LMP_TYPE      AS lmp_type,
        TRY_CAST({val} AS DOUBLE) AS price_usd_per_mwh
    FROM "{src}"
    WHERE TRY_CAST({val} AS DOUBLE) IS NOT NULL
"""

_INTERVAL_COL = "TRY_CAST(OPR_INTERVAL AS INTEGER) AS operating_interval,"

TRANSFORM_SQL = {
    "PRC_LMP": _LMP.format(src=_spec_id("PRC_LMP"), val="MW", interval=""),
    "PRC_INTVL_LMP": _LMP.format(src=_spec_id("PRC_INTVL_LMP"), val="VALUE", interval=_INTERVAL_COL),
    "PRC_RTPD_LMP": _LMP.format(src=_spec_id("PRC_RTPD_LMP"), val="PRC", interval=_INTERVAL_COL),
    "PRC_HASP_LMP": _LMP.format(src=_spec_id("PRC_HASP_LMP"), val="MW", interval=_INTERVAL_COL),
    "SLD_FCST": f"""
        SELECT DISTINCT
            CAST(INTERVALSTARTTIME_GMT AS TIMESTAMPTZ) AS interval_start_utc,
            CAST(INTERVALENDTIME_GMT   AS TIMESTAMPTZ) AS interval_end_utc,
            CAST(OPR_DT AS DATE)        AS operating_date,
            TRY_CAST(OPR_HR AS INTEGER) AS operating_hour,
            MARKET_RUN_ID  AS market_run_id,
            TAC_AREA_NAME  AS tac_area,
            LOAD_TYPE      AS load_type,
            LABEL          AS label,
            EXECUTION_TYPE AS execution_type,
            TRY_CAST(MW AS DOUBLE) AS load_mw
        FROM "{_spec_id('SLD_FCST')}"
        WHERE TRY_CAST(MW AS DOUBLE) IS NOT NULL
    """,
    "SLD_REN_FCST": f"""
        SELECT DISTINCT
            CAST(INTERVALSTARTTIME_GMT AS TIMESTAMPTZ) AS interval_start_utc,
            CAST(INTERVALENDTIME_GMT   AS TIMESTAMPTZ) AS interval_end_utc,
            CAST(OPR_DT AS DATE)        AS operating_date,
            TRY_CAST(OPR_HR AS INTEGER) AS operating_hour,
            MARKET_RUN_ID  AS market_run_id,
            TRADING_HUB    AS trading_hub,
            RENEWABLE_TYPE AS renewable_type,
            LABEL          AS label,
            TRY_CAST(MW AS DOUBLE) AS forecast_mw
        FROM "{_spec_id('SLD_REN_FCST')}"
        WHERE TRY_CAST(MW AS DOUBLE) IS NOT NULL
    """,
    "ENE_SLRS": f"""
        SELECT DISTINCT
            CAST(INTERVALSTARTTIME_GMT AS TIMESTAMPTZ) AS interval_start_utc,
            CAST(INTERVALENDTIME_GMT   AS TIMESTAMPTZ) AS interval_end_utc,
            CAST(OPR_DT AS DATE)        AS operating_date,
            TRY_CAST(OPR_HR AS INTEGER) AS operating_hour,
            MARKET_RUN_ID AS market_run_id,
            SLRS_TYPE     AS slrs_type,
            TAC_ZONE_NAME AS tac_zone,
            SCHEDULE      AS schedule,
            TRY_CAST(MW AS DOUBLE) AS mw
        FROM "{_spec_id('ENE_SLRS')}"
        WHERE TRY_CAST(MW AS DOUBLE) IS NOT NULL
    """,
    "AS_RESULTS": f"""
        SELECT DISTINCT
            CAST(INTERVALSTARTTIME_GMT AS TIMESTAMPTZ) AS interval_start_utc,
            CAST(INTERVALENDTIME_GMT   AS TIMESTAMPTZ) AS interval_end_utc,
            CAST(OPR_DT AS DATE)        AS operating_date,
            TRY_CAST(OPR_HR AS INTEGER) AS operating_hour,
            MARKET_RUN_ID AS market_run_id,
            ANC_TYPE      AS anc_type,
            ANC_REGION    AS anc_region,
            RESULT_TYPE   AS result_type,
            UOM           AS uom,
            TRY_CAST(MW AS DOUBLE) AS value
        FROM "{_spec_id('AS_RESULTS')}"
        WHERE TRY_CAST(MW AS DOUBLE) IS NOT NULL
    """,
    "AS_REQ": f"""
        SELECT DISTINCT
            CAST(INTERVALSTARTTIME_GMT AS TIMESTAMPTZ) AS interval_start_utc,
            CAST(INTERVALENDTIME_GMT   AS TIMESTAMPTZ) AS interval_end_utc,
            CAST(OPR_DT AS DATE)        AS operating_date,
            TRY_CAST(OPR_HR AS INTEGER) AS operating_hour,
            MARKET_RUN_ID AS market_run_id,
            ANC_TYPE      AS anc_type,
            ANC_REGION    AS anc_region,
            LABEL         AS label,
            TRY_CAST(MW AS DOUBLE) AS requirement_mw
        FROM "{_spec_id('AS_REQ')}"
        WHERE TRY_CAST(MW AS DOUBLE) IS NOT NULL
    """,
    "PRC_FUEL": f"""
        SELECT DISTINCT
            CAST(INTERVALSTARTTIME_GMT AS TIMESTAMPTZ) AS interval_start_utc,
            CAST(INTERVALENDTIME_GMT   AS TIMESTAMPTZ) AS interval_end_utc,
            CAST(OPR_DT AS DATE)        AS operating_date,
            TRY_CAST(OPR_HR AS INTEGER) AS operating_hour,
            FUEL_REGION_ID AS fuel_region_id,
            TRY_CAST(PRC AS DOUBLE) AS price_usd_per_mmbtu
        FROM "{_spec_id('PRC_FUEL')}"
        WHERE TRY_CAST(PRC AS DOUBLE) IS NOT NULL
    """,
}

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{_spec_id(eid)}-transform",
        deps=[_spec_id(eid)],
        sql=TRANSFORM_SQL[eid],
    )
    for eid in REPORTS
]
