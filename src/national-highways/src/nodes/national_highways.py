"""National Highways WebTRIS download nodes.

Source: WebTRIS REST API (https://webtris.highwaysengland.co.uk/api/v1.0), a
free key-less JSON API exposing traffic-sensor measurements for the English
strategic road network. See assets/research for the full surface.

This module ships three of the five catalogued entities:

  * ``sites``          — the ~20,076 monitoring-site register (one bulk GET).
  * ``areas``          — the 25 DBFO/regional grouping areas (one bulk GET).
  * ``annual_reports`` — per-site, per-month Average Daily / Weekday Traffic
    (ADT/AWT) statistics over 12/16/18/24-hour windows. Fetched per 30-site
    batch (the report endpoints accept a comma-separated ``sites`` list capped
    at 30) across the full available year range.

The daily (15-min interval) and monthly (per-day) report families are NOT
built here — deferred at accept as ``soft_too_large`` (billions / tens of
millions of rows via per-site paging against a throttling API).

API quirks learned by probing (2026-07):

  * ``sites`` accepts at most 30 comma-separated site ids; 40+ returns HTTP 400.
  * ``start_date`` / ``end_date`` are ``ddmmyyyy``. The annual endpoint rejects
    windows spanning more than ~7 years and windows starting before ~2017
    (no data) with HTTP 400 — hence ``FLOOR_YEAR`` + bounded ``_annual_windows``.
  * The generic HTTP 400 body "Report Request Invalid…" doubles as an
    UNDOCUMENTED THROTTLE response after request bursts (recovers in ~60-75s).
    A well-formed request that 400s is therefore treated as transient and
    retried with backoff (``_report_get``); the fetch is also rate-limited.
"""

from datetime import date

import httpx
import pyarrow as pa
from ratelimit import limits, sleep_and_retry
from tenacity import retry, retry_if_exception, stop_after_attempt, wait_exponential

from subsets_utils import (
    NodeSpec,
    MaintainSpec,
    get,
    is_transient,
    raw_asset_exists,
    raw_parquet_writer,
    save_raw_parquet,
)

BASE = "https://webtris.highwaysengland.co.uk/api/v1.0"

# The annual endpoint returns HTTP 400 for start_dates before this year (no
# data exists that early — confirmed by probing). The upper bound is computed
# from today at runtime, never hardcoded.
FLOOR_YEAR = 2017
# Endpoint rejects windows spanning more than ~7 years; keep well under it.
WINDOW_SPAN_YEARS = 5
# Max site ids per report request (the endpoint's own cap; 40+ -> HTTP 400).
SITE_BATCH = 30


# ---------------------------------------------------------------------------
# HTTP helpers
# ---------------------------------------------------------------------------
@sleep_and_retry
@limits(calls=40, period=60)  # conservative pace to stay under the undocumented throttle
def _rate_limited_get(path: str, params: dict | None = None) -> httpx.Response:
    return get(f"{BASE}/{path}", params=params, timeout=(10.0, 120.0))


def _retryable(exc: BaseException) -> bool:
    # Standard transient classification PLUS WebTRIS's throttle-as-400: a
    # well-formed report request that 400s is (empirically) the server
    # throttling, not a real parameter error, so back off and retry.
    if is_transient(exc):
        return True
    if isinstance(exc, httpx.HTTPStatusError) and exc.response.status_code == 400:
        return True
    return False


@retry(
    retry=retry_if_exception(_retryable),
    wait=wait_exponential(multiplier=2, min=4, max=90),
    stop=stop_after_attempt(8),
    reraise=True,
)
def _report_get(path: str, params: dict) -> dict:
    resp = _rate_limited_get(path, params)
    resp.raise_for_status()
    return resp.json()


def _get_json(path: str) -> dict:
    resp = _rate_limited_get(path)
    resp.raise_for_status()
    return resp.json()


def _num(v):
    """Report numerics arrive as JSON strings; empty cells are ''."""
    if v is None:
        return None
    s = str(v).strip()
    if not s:
        return None
    try:
        return float(s)
    except ValueError:
        return None


def _chunks(seq, n):
    for i in range(0, len(seq), n):
        yield seq[i : i + n]


# ---------------------------------------------------------------------------
# sites
# ---------------------------------------------------------------------------
SITES_SCHEMA = pa.schema(
    [
        ("site_id", pa.string()),
        ("name", pa.string()),
        ("description", pa.string()),
        ("longitude", pa.float64()),
        ("latitude", pa.float64()),
        ("status", pa.string()),
    ]
)


def fetch_sites(node_id: str) -> None:
    asset = node_id
    data = _get_json("sites")
    rows = [
        {
            "site_id": str(s.get("Id")),
            "name": s.get("Name"),
            "description": s.get("Description"),
            "longitude": _num(s.get("Longitude")),
            "latitude": _num(s.get("Latitude")),
            "status": s.get("Status"),
        }
        for s in data.get("sites", [])
    ]
    save_raw_parquet(pa.Table.from_pylist(rows, schema=SITES_SCHEMA), asset)


# ---------------------------------------------------------------------------
# areas
# ---------------------------------------------------------------------------
AREAS_SCHEMA = pa.schema(
    [
        ("area_id", pa.string()),
        ("name", pa.string()),
        ("description", pa.string()),
        ("x_longitude", pa.float64()),
        ("x_latitude", pa.float64()),
        ("y_longitude", pa.float64()),
        ("y_latitude", pa.float64()),
    ]
)


def fetch_areas(node_id: str) -> None:
    asset = node_id
    data = _get_json("areas")
    rows = [
        {
            "area_id": str(a.get("Id")),
            "name": a.get("Name"),
            "description": a.get("Description"),
            "x_longitude": _num(a.get("XLongitude")),
            "x_latitude": _num(a.get("XLatitude")),
            "y_longitude": _num(a.get("YLongitude")),
            "y_latitude": _num(a.get("YLatitude")),
        }
        for a in data.get("areas", [])
    ]
    save_raw_parquet(pa.Table.from_pylist(rows, schema=AREAS_SCHEMA), asset)


# ---------------------------------------------------------------------------
# annual reports
# ---------------------------------------------------------------------------
MONTHS = {
    "Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "May": 5, "Jun": 6,
    "Jul": 7, "Aug": 8, "Sep": 9, "Oct": 10, "Nov": 11, "Dec": 12,
}

# (source key, output column) for the 16 ADT/AWT metrics.
ANNUAL_FIELDS = [
    ("ADT24Hour", "adt_24hour"),
    ("ADT24LargeVehiclePercentage", "adt_24hour_large_vehicle_pct"),
    ("AWT24Hour", "awt_24hour"),
    ("AWT24LargeVehiclePercentage", "awt_24hour_large_vehicle_pct"),
    ("ADT18Hour", "adt_18hour"),
    ("ADT18LargeVehiclePercentage", "adt_18hour_large_vehicle_pct"),
    ("AWT18Hour", "awt_18hour"),
    ("AWT18LargeVehiclePercentage", "awt_18hour_large_vehicle_pct"),
    ("ADT16Hour", "adt_16hour"),
    ("ADT16LargeVehiclePercentage", "adt_16hour_large_vehicle_pct"),
    ("AWT16Hour", "awt_16hour"),
    ("AWT16LargeVehiclePercentage", "awt_16hour_large_vehicle_pct"),
    ("ADT12Hour", "adt_12hour"),
    ("ADT12LargeVehiclePercentage", "adt_12hour_large_vehicle_pct"),
    ("AWT12Hour", "awt_12hour"),
    ("AWT12LargeVehiclePercentage", "awt_12hour_large_vehicle_pct"),
]

ANNUAL_SCHEMA = pa.schema(
    [
        ("site_id", pa.string()),
        ("year", pa.int32()),
        ("month_num", pa.int32()),
        ("month_name", pa.string()),
    ]
    + [(col, pa.float64()) for _, col in ANNUAL_FIELDS]
)


def _annual_windows():
    """Contiguous [start_ddmmyyyy, end_ddmmyyyy] windows from FLOOR_YEAR to the
    current year, each spanning <= WINDOW_SPAN_YEARS (both endpoints inclusive
    on the endpoint's side). Upper bound follows the calendar, so new years are
    picked up automatically."""
    cy = date.today().year
    windows = []
    a = FLOOR_YEAR
    while a <= cy:
        b = min(a + WINDOW_SPAN_YEARS, cy)
        windows.append((f"0101{a}", f"0101{b}"))
        a = b + 1
    return windows


def _parse_annual(body, out_rows):
    for site_blk in body:
        sid = str(site_blk.get("SiteId"))
        yr = site_blk.get("Year")
        try:
            year = int(yr)
        except (TypeError, ValueError):
            continue
        for mrow in site_blk.get("AnnualReportMonthlyDataRows", []):
            mname = mrow.get("MonthName")
            ar = mrow.get("AnnualReportRow") or {}
            row = {
                "site_id": sid,
                "year": year,
                "month_num": MONTHS.get(mname),
                "month_name": mname,
            }
            for src, col in ANNUAL_FIELDS:
                row[col] = _num(ar.get(src))
            out_rows.append(row)


def fetch_annual_reports(node_id: str) -> None:
    asset = node_id
    site_ids = [str(s.get("Id")) for s in _get_json("sites").get("sites", [])]
    if not site_ids:
        raise RuntimeError("WebTRIS /sites returned no sites; cannot enumerate annual reports")
    windows = _annual_windows()

    with raw_parquet_writer(asset, ANNUAL_SCHEMA) as writer:
        for chunk in _chunks(site_ids, SITE_BATCH):
            sites_param = ",".join(chunk)
            rows: list[dict] = []
            for start_date, end_date in windows:
                payload = _report_get(
                    "reports/annual",
                    {
                        "sites": sites_param,
                        "start_date": start_date,
                        "end_date": end_date,
                        "page": 1,
                        "page_size": 90000,
                    },
                )
                header = payload.get("Header", {}) or {}
                if any(l.get("rel") == "nextPage" for l in header.get("links", []) or []):
                    raise RuntimeError(
                        f"annual report paginated unexpectedly (sites={sites_param}, "
                        f"window={start_date}-{end_date}); raise page_size or add paging"
                    )
                _parse_annual(payload.get("AnnualReportBody", []) or [], rows)
            if rows:
                writer.write_table(pa.Table.from_pylist(rows, schema=ANNUAL_SCHEMA))


# ---------------------------------------------------------------------------
# specs
# ---------------------------------------------------------------------------
DOWNLOAD_SPECS = [
    NodeSpec(id="national-highways-sites", fn=fetch_sites, kind="download"),
    NodeSpec(id="national-highways-areas", fn=fetch_areas, kind="download"),
    NodeSpec(id="national-highways-annual-reports", fn=fetch_annual_reports, kind="download"),
]

# WebTRIS publishes traffic data roughly one month in arrears and exposes no
# reliable ETag/Last-Modified on these dynamic endpoints, so freshness falls
# back to asset age sized to the ~monthly cadence.
MAINTAIN_SPECS = [
    MaintainSpec(
        asset_id="national-highways-sites",
        description="Site register refreshed monthly (inferred — no published cadence; data lands ~1 month in arrears)",
        check=lambda aid: raw_asset_exists(aid, "parquet", max_age_days=25),
    ),
    MaintainSpec(
        asset_id="national-highways-areas",
        description="Area register refreshed monthly (inferred — no published cadence)",
        check=lambda aid: raw_asset_exists(aid, "parquet", max_age_days=25),
    ),
    MaintainSpec(
        asset_id="national-highways-annual-reports",
        description="Annual ADT/AWT statistics refreshed monthly (data published ~1 month in arrears; no published cadence)",
        check=lambda aid: raw_asset_exists(aid, "parquet", max_age_days=25),
    ),
]
