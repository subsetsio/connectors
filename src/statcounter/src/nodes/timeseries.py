"""StatCounter time-series statistics (browser, OS, search engine, social media,
device vendor, platform comparison).

Mechanism (research `csv_chart`): a parameterized CSV endpoint at
`/chart.php?...&csv=1`. One GET returns the full monthly time series (2009-01 to
the latest published month) for a single (statType x region) as a wide CSV
(`Date` + one column per category, cells are % market share). There is no bulk
all-in-one export and no incremental filter beyond narrowing the date range, so
each refresh is a stateless full re-pull (shape 1): every region is re-fetched
and the table overwritten. Each CSV is tiny; we hold at most one region in
memory and stream row groups to parquet.

Granularity: one download node per *statistic* (collect entity). Region, date
and category are dimensions melted into long form — NOT separate nodes. The
region set is discovered live from the site's region dropdown (worldwide + 7
continents + ~249 ISO alpha-2 countries) rather than hardcoded.

`screen-resolution` is a distinct dataset (aggregate-only at source) and lives
in its own module.
"""

import csv as _csv
import io as _io
import os
import time

import pyarrow as pa

from subsets_utils import list_raw_fragments, raw_parquet_writer
from utils import (
    BASE_URL,
    SOURCE_MIN_MONTH,
    _current_month,
    _discover_regions,
    _get_text,
    _MONTH_RE,
    _permanent_4xx,
)

# Per-statistic config, keyed by collect entity id (hyphenated == the node-id
# suffix). `device`/`multi` are the platform settings under which the statistic
# is meaningful (device vendor only for mobile; platform comparison spans all).
STATS = {
    "browser":                            {"code": "browser",                            "device": "desktop+tablet+mobile",     "multi": True},
    "browser-version":                    {"code": "browser_version",                    "device": "desktop+tablet+mobile",     "multi": True},
    "browser-version-partially-combined": {"code": "browser_version_partially_combined", "device": "desktop+tablet+mobile",     "multi": True},
    "os":                                 {"code": "os",                                 "device": "desktop+tablet+mobile",     "multi": True},
    "search-engine":                      {"code": "search_engine",                      "device": "desktop+tablet+mobile",     "multi": True},
    "search-engine-host":                 {"code": "search_engine_host",                 "device": "desktop+tablet+mobile",     "multi": True},
    "social-media":                       {"code": "social_media",                       "device": "desktop+tablet+mobile",     "multi": True},
    "device-vendor":                      {"code": "vendor",                             "device": "mobile",                    "multi": False},
    "platform-comparison":                {"code": "comparison",                         "device": "desktop+mobile+tablet+console", "multi": True},
}

_TIMESERIES_SCHEMA = pa.schema([
    ("date", pa.string()),          # "YYYY-MM"
    ("region_code", pa.string()),
    ("region_name", pa.string()),
    ("region_type", pa.string()),   # worldwide | continent | country
    ("category", pa.string()),
    ("market_share", pa.float64()),
])


def _parse_timeseries_csv(text: str) -> list[tuple[str, str, float]]:
    """Wide CSV -> long [(date, category, market_share), ...]. Skips the leading
    Date column, blank cells and any row whose first cell isn't YYYY-MM (guards
    against a sparse region returning the aggregate 'bar' shape instead)."""
    rows = list(_csv.reader(_io.StringIO(text)))
    if len(rows) < 2:
        return []
    header = rows[0]
    if not header or header[0].strip().lower() != "date":
        return []  # not a time-series response
    categories = header[1:]
    out: list[tuple[str, str, float]] = []
    for r in rows[1:]:
        if not r or not _MONTH_RE.match(r[0].strip()):
            continue
        date = r[0].strip()
        for i, cat in enumerate(categories):
            cat = cat.strip()
            if not cat:
                continue
            raw = r[i + 1].strip() if i + 1 < len(r) else ""
            if raw == "":
                continue
            try:
                val = float(raw)
            except ValueError:
                continue
            out.append((date, cat, val))
    return out


def fetch_statistic(node_id: str) -> None:
    """Time-series statistics: fetch the full monthly history for every region
    and stream a long-format parquet (one row per date x region x category)."""
    asset = node_id
    eid = node_id[len("statcounter-"):]
    cfg = STATS[eid]
    code, device, multi = cfg["code"], cfg["device"], cfg["multi"]

    regions = _discover_regions()
    to_month = _current_month()
    run_id = os.environ.get("RUN_ID", "unknown")
    done_fragments = {
        key
        for key, meta in list_raw_fragments(asset, "parquet").items()
        if meta.get("run_id") == run_id
    }

    failed: list[str] = []
    regions_written = 0
    total_rows = 0

    for region_code, region_name, region_type in regions:
        if region_code in done_fragments:
            regions_written += 1
            continue
        params = {
            "statType_hidden": code,
            "region_hidden": region_code,
            "granularity": "monthly",
            "csv": "1",
            "device_hidden": device,
            "multi-device": "true" if multi else "false",
            "fromMonthYear": SOURCE_MIN_MONTH,
            "toMonthYear": to_month,
        }
        try:
            text = _get_text(BASE_URL, params)
        except Exception as exc:  # noqa: BLE001 - logged + classified below
            if _permanent_4xx(exc):
                print(f"  {asset}: region {region_code} permanent {exc}; skipping")
            else:
                print(f"  {asset}: region {region_code} fetch failed: {type(exc).__name__}: {exc}")
            failed.append(region_code)
            continue

        long_rows = _parse_timeseries_csv(text)
        if not long_rows:
            continue
        batch = {
            "date": [d for d, _, _ in long_rows],
            "region_code": [region_code] * len(long_rows),
            "region_name": [region_name] * len(long_rows),
            "region_type": [region_type] * len(long_rows),
            "category": [c for _, c, _ in long_rows],
            "market_share": [v for _, _, v in long_rows],
        }
        with raw_parquet_writer(asset, _TIMESERIES_SCHEMA, fragment=region_code) as writer:
            writer.write_table(pa.table(batch, schema=_TIMESERIES_SCHEMA))
        regions_written += 1
        total_rows += len(long_rows)
        time.sleep(0.2)  # politeness; no documented rate limit

    # Integrity guards: worldwide must succeed, and a systemic failure
    # (many regions down) must not quietly publish a gutted table.
    if "ww" in failed:
        raise RuntimeError(f"{asset}: worldwide (ww) fetch failed; aborting node")
    if len(failed) > len(regions) * 0.25:
        raise RuntimeError(
            f"{asset}: {len(failed)}/{len(regions)} regions failed (>25%); aborting node"
        )
    if regions_written == 0:
        raise RuntimeError(f"{asset}: produced 0 regions; source format likely changed")
    if total_rows == 0 and not done_fragments:
        raise RuntimeError(f"{asset}: produced 0 rows; source format likely changed")

    print(f"  {asset}: {total_rows} rows across {regions_written} regions ({len(failed)} skipped)")
