"""Berkeley Earth temperature-anomaly time series.

One published subset: long-format monthly land-surface (and, for the global
product, land+ocean) temperature anomalies, one row per
(region, level, variable, domain, year, month). Anomalies are degrees Celsius
relative to the Jan 1951-Dec 1980 baseline; uncertainties are 95% CIs.

Mechanism (research-chosen `bulk_regional_auto`, plus `bulk_global_s3` for the
global products): pure per-entity bulk download over stable HTTPS, no auth. Each
file is one whitespace-delimited fixed-column ASCII series with a leading
commented (`%`) header. Files are overwritten in place on each ~monthly release
(stable "LATEST"-style names), so we re-pull the full corpus every run and
overwrite — stateless full re-pull. There is no directory listing on either
host, so the region slugs come from `constants.py`.
"""
from __future__ import annotations

import httpx
import pyarrow as pa
import pyarrow.parquet as pq

from subsets_utils import NodeSpec, SqlNodeSpec, get, transient_retry, raw_parquet_writer
from constants import (
    GLOBAL_PRODUCTS,
    CONTINENT_SLUGS,
    COUNTRY_SLUGS,
    US_STATE_SLUGS,
)

S3_GLOBAL = "https://berkeley-earth-temperature.s3.us-west-1.amazonaws.com/Global/"
AUTO_REGIONAL = "https://data.berkeleyearth.org/auto/Regional/{var}/Text/{slug}-{var}-Trend.txt"
VARIABLES = ("TAVG", "TMAX", "TMIN")

# Explicit schema — the contract for every per-region batch written to the one
# raw asset. The 9 value columns mirror the source's fixed-column layout:
# monthly anomaly + uncertainty, then year/5yr/10yr/20yr centered moving
# averages, each with its own uncertainty.
SCHEMA = pa.schema([
    ("region_slug", pa.string()),
    ("region_name", pa.string()),
    ("level", pa.string()),
    ("variable", pa.string()),
    ("domain", pa.string()),
    ("year", pa.int64()),
    ("month", pa.int64()),
    ("monthly_anomaly", pa.float64()),
    ("monthly_unc", pa.float64()),
    ("annual_anomaly", pa.float64()),
    ("annual_unc", pa.float64()),
    ("five_year_anomaly", pa.float64()),
    ("five_year_unc", pa.float64()),
    ("ten_year_anomaly", pa.float64()),
    ("ten_year_unc", pa.float64()),
    ("twenty_year_anomaly", pa.float64()),
    ("twenty_year_unc", pa.float64()),
])


@transient_retry()
def _get(url: str) -> httpx.Response:
    resp = get(url, timeout=(10.0, 180.0))
    resp.raise_for_status()
    return resp


def _fetch_text(url: str) -> str | None:
    """Return the body, or None for a permanent 404 (region/variable absent)."""
    try:
        return _get(url).text
    except httpx.HTTPStatusError as exc:
        if exc.response.status_code == 404:
            print(f"[skip] 404 {url}")
            return None
        raise


def _num(tok: str) -> float | None:
    return None if tok == "NaN" else float(tok)


def _region_name(text: str, fallback: str) -> str:
    """Pull the human region name from the file's '% ... for the region:' header."""
    lines = text.splitlines()
    for i, ln in enumerate(lines):
        if "for the region:" in ln:
            for nxt in lines[i + 1:i + 6]:
                stripped = nxt.lstrip("%").strip()
                if stripped:
                    return stripped
    return fallback


def _parse(text: str, *, region_slug: str, region_name: str, level: str,
           variable: str, domain: str) -> list[dict]:
    rows = []
    for ln in text.splitlines():
        s = ln.strip()
        if not s or s.startswith("%"):
            continue
        parts = s.split()
        if len(parts) != 12:
            continue
        try:
            year, month = int(parts[0]), int(parts[1])
        except ValueError:
            continue
        v = [_num(p) for p in parts[2:]]
        rows.append({
            "region_slug": region_slug, "region_name": region_name,
            "level": level, "variable": variable, "domain": domain,
            "year": year, "month": month,
            "monthly_anomaly": v[0], "monthly_unc": v[1],
            "annual_anomaly": v[2], "annual_unc": v[3],
            "five_year_anomaly": v[4], "five_year_unc": v[5],
            "ten_year_anomaly": v[6], "ten_year_unc": v[7],
            "twenty_year_anomaly": v[8], "twenty_year_unc": v[9],
        })
    return rows


def fetch_timeseries(node_id: str) -> None:
    """Re-pull every global + regional series and stream them into one parquet.

    Stateless full re-pull: the source overwrites each file in place per release,
    so a stored watermark would only risk skipping revisions. Each region's rows
    are flushed as their own row group to keep memory bounded.
    """
    asset = node_id
    regions = (
        [(s, "continent") for s in CONTINENT_SLUGS]
        + [(s, "country") for s in COUNTRY_SLUGS]
        + [(s, "us-state") for s in US_STATE_SLUGS]
    )
    total = 0
    with raw_parquet_writer(asset, SCHEMA) as writer:
        # Global products (land+ocean blend and land-only) from S3.
        for product in GLOBAL_PRODUCTS:
            text = _fetch_text(S3_GLOBAL + product["file"])
            if text is None:
                continue
            rows = _parse(
                text, region_slug="global", region_name="Global",
                level="global", variable=product["variable"], domain=product["domain"],
            )
            if rows:
                writer.write_table(pa.Table.from_pylist(rows, schema=SCHEMA))
                total += len(rows)

        # Regional land-only series, one file per (region, variable).
        for slug, level in regions:
            for var in VARIABLES:
                text = _fetch_text(AUTO_REGIONAL.format(var=var, slug=slug))
                if text is None:
                    continue
                name = _region_name(text, slug.replace("-", " ").title())
                rows = _parse(
                    text, region_slug=slug, region_name=name,
                    level=level, variable=var, domain="land",
                )
                if rows:
                    writer.write_table(pa.Table.from_pylist(rows, schema=SCHEMA))
                    total += len(rows)

    if total == 0:
        raise RuntimeError(f"{asset}: fetched 0 rows — source layout may have changed")
    print(f"  {asset}: {total} rows")


DOWNLOAD_SPECS = [
    NodeSpec(id="berkeley-earth-temperature-timeseries", fn=fetch_timeseries, kind="download"),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="berkeley-earth-temperature-timeseries-transform",
        deps=["berkeley-earth-temperature-timeseries"],
        sql='''
            SELECT
                make_date(CAST(year AS INTEGER), CAST(month AS INTEGER), 1) AS date,
                region_slug,
                region_name,
                level,
                variable,
                domain,
                CAST(year AS INTEGER)  AS year,
                CAST(month AS INTEGER) AS month,
                monthly_anomaly,
                monthly_unc,
                annual_anomaly,
                annual_unc,
                five_year_anomaly,
                five_year_unc,
                ten_year_anomaly,
                ten_year_unc,
                twenty_year_anomaly,
                twenty_year_unc
            FROM "berkeley-earth-temperature-timeseries"
            WHERE monthly_anomaly IS NOT NULL
              AND month BETWEEN 1 AND 12
            QUALIFY row_number() OVER (
                PARTITION BY region_slug, level, variable, domain, year, month
                ORDER BY monthly_anomaly
            ) = 1
        ''',
    ),
]
