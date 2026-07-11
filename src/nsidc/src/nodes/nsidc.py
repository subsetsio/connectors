"""NSIDC Sea Ice Index (G02135) — raw fetches.

Static nginx file server at https://noaadata.apps.nsidc.org/NOAA/G02135. The
whole corpus is a handful of small files (<10MB), so every fetch is a stateless
full re-pull: download the file(s) for a subset, normalise to long-format rows
in Python (multi-line headers, -9999 sentinel, pivoted regional workbooks that
DuckDB cannot ingest raw), and write one typed parquet. Hemisphere is
normalised to Arctic/Antarctic everywhere.

Five published subsets, one download spec each:
  - sea-ice-extent-daily              (2 daily CSVs)
  - sea-ice-extent-daily-climatology  (2 climatology CSVs, 1981-2010 baseline)
  - sea-ice-extent-monthly            (24 monthly CSVs, 12 months x 2 hemispheres)
  - sea-ice-regional-daily            (2 regional daily xlsx workbooks)
  - sea-ice-regional-monthly          (2 regional monthly xlsx workbooks)
"""
import pyarrow as pa

from subsets_utils import NodeSpec, get, save_raw_parquet, transient_retry
from utils import (
    parse_climatology,
    parse_daily_extent,
    parse_monthly_extent,
    parse_regional_daily,
    parse_regional_monthly,
)

BASE_URL = "https://noaadata.apps.nsidc.org/NOAA/G02135"


@transient_retry()
def _get_text(path: str) -> str:
    resp = get(f"{BASE_URL}/{path}", timeout=(10.0, 120.0))
    resp.raise_for_status()
    return resp.text


@transient_retry()
def _get_bytes(path: str) -> bytes:
    resp = get(f"{BASE_URL}/{path}", timeout=(10.0, 180.0))
    resp.raise_for_status()
    return resp.content


# ── sea-ice-extent-daily ────────────────────────────────────────────────────
_DAILY_FILES = [
    ("north/daily/data/N_seaice_extent_daily_v4.0.csv", "Arctic"),
    ("south/daily/data/S_seaice_extent_daily_v4.0.csv", "Antarctic"),
]
_DAILY_SCHEMA = pa.schema([
    ("hemisphere", pa.string()),
    ("date", pa.date32()),
    ("year", pa.int64()),
    ("month", pa.int64()),
    ("day", pa.int64()),
    ("extent_million_sq_km", pa.float64()),
    ("missing_million_sq_km", pa.float64()),
])


def fetch_daily(node_id: str) -> None:
    rows: list[dict] = []
    for path, hemisphere in _DAILY_FILES:
        rows.extend(parse_daily_extent(_get_text(path), hemisphere))
    save_raw_parquet(pa.Table.from_pylist(rows, schema=_DAILY_SCHEMA), node_id)


# ── sea-ice-extent-daily-climatology ────────────────────────────────────────
_CLIMATOLOGY_FILES = [
    ("north/daily/data/N_seaice_extent_climatology_1981-2010_v4.0.csv", "Arctic"),
    ("south/daily/data/S_seaice_extent_climatology_1981-2010_v4.0.csv", "Antarctic"),
]
_CLIMATOLOGY_SCHEMA = pa.schema([
    ("hemisphere", pa.string()),
    ("day_of_year", pa.int64()),
    ("average_extent_million_sq_km", pa.float64()),
    ("std_deviation_million_sq_km", pa.float64()),
    ("pct_10", pa.float64()),
    ("pct_25", pa.float64()),
    ("pct_50", pa.float64()),
    ("pct_75", pa.float64()),
    ("pct_90", pa.float64()),
])


def fetch_climatology(node_id: str) -> None:
    rows: list[dict] = []
    for path, hemisphere in _CLIMATOLOGY_FILES:
        rows.extend(parse_climatology(_get_text(path), hemisphere))
    save_raw_parquet(pa.Table.from_pylist(rows, schema=_CLIMATOLOGY_SCHEMA), node_id)


# ── sea-ice-extent-monthly ──────────────────────────────────────────────────
_MONTHLY_DIRS = [("north/monthly/data", "N"), ("south/monthly/data", "S")]
_MONTHLY_SCHEMA = pa.schema([
    ("hemisphere", pa.string()),
    ("year", pa.int64()),
    ("month", pa.int64()),
    ("date", pa.date32()),
    ("source_dataset", pa.string()),
    ("extent_million_sq_km", pa.float64()),
    ("area_million_sq_km", pa.float64()),
])


def fetch_monthly(node_id: str) -> None:
    rows: list[dict] = []
    for directory, code in _MONTHLY_DIRS:
        for month in range(1, 13):
            path = f"{directory}/{code}_{month:02d}_extent_v4.0.csv"
            rows.extend(parse_monthly_extent(_get_text(path)))
    save_raw_parquet(pa.Table.from_pylist(rows, schema=_MONTHLY_SCHEMA), node_id)


# ── sea-ice-regional-daily ──────────────────────────────────────────────────
_REGIONAL_DAILY_FILES = [
    ("seaice_analysis/N_Sea_Ice_Index_Regional_Daily_Data_G02135_v4.0.xlsx", "Arctic"),
    ("seaice_analysis/S_Sea_Ice_Index_Regional_Daily_Data_G02135_v4.0.xlsx", "Antarctic"),
]
_REGIONAL_DAILY_SCHEMA = pa.schema([
    ("hemisphere", pa.string()),
    ("region", pa.string()),
    ("date", pa.date32()),
    ("year", pa.int64()),
    ("month", pa.int64()),
    ("day", pa.int64()),
    ("area_sq_km", pa.float64()),
    ("extent_sq_km", pa.float64()),
])


def fetch_regional_daily(node_id: str) -> None:
    rows: list[dict] = []
    for path, hemisphere in _REGIONAL_DAILY_FILES:
        rows.extend(parse_regional_daily(_get_bytes(path), hemisphere))
    save_raw_parquet(pa.Table.from_pylist(rows, schema=_REGIONAL_DAILY_SCHEMA), node_id)


# ── sea-ice-regional-monthly ────────────────────────────────────────────────
_REGIONAL_MONTHLY_FILES = [
    ("seaice_analysis/N_Sea_Ice_Index_Regional_Monthly_Data_G02135_v4.0.xlsx", "Arctic"),
    ("seaice_analysis/S_Sea_Ice_Index_Regional_Monthly_Data_G02135_v4.0.xlsx", "Antarctic"),
]
_REGIONAL_MONTHLY_SCHEMA = pa.schema([
    ("hemisphere", pa.string()),
    ("region", pa.string()),
    ("year", pa.int64()),
    ("month", pa.int64()),
    ("date", pa.date32()),
    ("area_sq_km", pa.float64()),
    ("area_rank", pa.float64()),
    ("extent_sq_km", pa.float64()),
    ("extent_rank", pa.float64()),
])


def fetch_regional_monthly(node_id: str) -> None:
    rows: list[dict] = []
    for path, hemisphere in _REGIONAL_MONTHLY_FILES:
        rows.extend(parse_regional_monthly(_get_bytes(path), hemisphere))
    save_raw_parquet(pa.Table.from_pylist(rows, schema=_REGIONAL_MONTHLY_SCHEMA), node_id)


DOWNLOAD_SPECS = [
    NodeSpec(id="nsidc-sea-ice-extent-daily", fn=fetch_daily, kind="download"),
    NodeSpec(id="nsidc-sea-ice-extent-daily-climatology", fn=fetch_climatology, kind="download"),
    NodeSpec(id="nsidc-sea-ice-extent-monthly", fn=fetch_monthly, kind="download"),
    NodeSpec(id="nsidc-sea-ice-regional-daily", fn=fetch_regional_daily, kind="download"),
    NodeSpec(id="nsidc-sea-ice-regional-monthly", fn=fetch_regional_monthly, kind="download"),
]
