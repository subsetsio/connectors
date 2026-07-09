"""CFPB Mortgage Performance Trends (NMDB, joint CFPB/FHFA).

The download page filenames embed the through-date, so we parse the page each
refresh to discover the current State/MetroArea/County filenames for both
delinquency buckets (30-89 / 90-plus days late). The CSVs are wide (one row per
region, one column per month); we melt the months here, tag rows with `bucket`,
and write one long-format NDJSON asset (one row per region/bucket/month).
"""

from __future__ import annotations

import csv
import io
import re

from subsets_utils import NodeSpec, SqlNodeSpec, save_raw_ndjson
from utils import _http_get

_MP_PAGE = (
    "https://www.consumerfinance.gov/data-research/"
    "mortgage-performance-trends/download-the-data/"
)
_MP_GEO_PREFIX = {
    "mortgage-performance-state": "State",
    "mortgage-performance-metro-area": "MetroArea",
    "mortgage-performance-county": "County",
}
_MP_BUCKETS = ("30-89DaysLate", "90-plusDaysLate")
# The wide CSVs have one column per month (YYYY-MM); everything else (RegionType,
# Name, FIPSCode, and — in the metro file — CBSACode) is metadata, not a value.
_MONTH_RE = re.compile(r"^\d{4}-\d{2}$")


def _mp_latest_urls(geo_prefix: str, page_html: str) -> dict[str, str]:
    """Parse the download page for the most recent CSV (max thru-date) per
    delinquency bucket for one geography level."""
    pattern = re.compile(
        r"https://files\.consumerfinance\.gov/data/mortgage-performance/downloads/"
        + re.escape(geo_prefix)
        + r"MortgagesPercent-(30-89DaysLate|90-plusDaysLate)-thru-(\d{4}-\d{2})\.csv"
    )
    best: dict[str, tuple[str, str]] = {}  # bucket -> (thru_date, url)
    for match in pattern.finditer(page_html):
        url, bucket, thru = match.group(0), match.group(1), match.group(2)
        if bucket not in best or thru > best[bucket][0]:
            best[bucket] = (thru, url)
    return {bucket: url for bucket, (thru, url) in best.items()}


def fetch_mortgage_performance(node_id: str) -> None:
    """Fetch both delinquency-bucket CSVs for one geography level and write one
    long-format NDJSON asset: one row per (region, bucket, month). The source
    CSVs are wide (one column per month, ~210 of them), which exceeds
    read_json_auto's map-inference threshold if stored verbatim — so we melt the
    months here, where the column set is known, rather than UNPIVOT downstream.
    Filenames are discovered from the download page (the through-date is embedded
    and changes each release)."""
    entity = node_id[len("cfpb-"):]
    geo_prefix = _MP_GEO_PREFIX[entity]

    page = _http_get(_MP_PAGE, timeout=60)
    page.raise_for_status()
    urls = _mp_latest_urls(geo_prefix, page.text)
    missing = [b for b in _MP_BUCKETS if b not in urls]
    if missing:
        raise ValueError(
            f"{node_id}: download page missing {geo_prefix} CSV(s) for buckets {missing}"
        )

    rows: list[dict] = []
    for bucket, url in urls.items():
        resp = _http_get(url, timeout=120)
        resp.raise_for_status()
        reader = csv.DictReader(io.StringIO(resp.text))
        n_before = len(rows)
        for record in reader:
            region_type = record.get("RegionType")
            if region_type == "National":
                continue  # keep only the geographic level this entity describes
            region_name = record.get("Name")
            # Metro/non-metro rows carry a CBSACode and an empty FIPSCode; use
            # whichever identifier is populated as the geographic code.
            fips_code = (
                record.get("FIPSCode") or record.get("CBSACode") or ""
            ).replace("'", "")
            for period, raw_rate in record.items():
                # Melt only the month columns (YYYY-MM); every other column
                # (RegionType/Name/FIPSCode/CBSACode/…) is metadata, not a value.
                if not _MONTH_RE.match(period or "") or raw_rate is None or raw_rate == "":
                    continue
                try:
                    rate = float(raw_rate)
                except ValueError:
                    continue
                rows.append({
                    "region_type": region_type,
                    "region_name": region_name,
                    "fips_code": fips_code,
                    "bucket": bucket,
                    "period": period,
                    "delinquency_rate": rate,
                })
        print(f"  {node_id}: {bucket} -> {len(rows) - n_before} observations")

    if not rows:
        raise ValueError(f"{node_id}: no mortgage-performance rows for {geo_prefix}")
    save_raw_ndjson(rows, node_id)


_DOWNLOAD_SPECS = [
    NodeSpec(id="cfpb-mortgage-performance-county", fn=fetch_mortgage_performance, kind="download"),
    NodeSpec(id="cfpb-mortgage-performance-metro-area", fn=fetch_mortgage_performance, kind="download"),
    NodeSpec(id="cfpb-mortgage-performance-state", fn=fetch_mortgage_performance, kind="download"),
]

_TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{spec.id}-transform",
        deps=(spec.id,),
        sql=f'SELECT * FROM "{spec.id}"',
    )
    for spec in _DOWNLOAD_SPECS
]
