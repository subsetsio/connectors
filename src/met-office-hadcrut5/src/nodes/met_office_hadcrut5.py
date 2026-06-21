"""Met Office HadCRUT5 - global surface temperature anomalies.

Source: https://www.metoffice.gov.uk/hadobs/hadcrut5/
Publishes: hadcrut5_monthly / hadcrut5_annual

HadCRUT5 is the Met Office Hadley Centre + UEA CRU global surface temperature
record (one of the four canonical series alongside NOAA, GISTEMP, Berkeley).
We pull the analysis "summary_series" CSVs, which publish the ensemble-mean
monthly and annual anomalies for the Global, Northern-Hemisphere and
Southern-Hemisphere means, each with 95% confidence bounds, relative to the
1961-1990 base period.

Each summary CSV has a stable header:
    Time, Anomaly (deg C), Lower confidence limit (2.5%), Upper confidence limit (97.5%)
Time is YYYY-MM for monthly and YYYY for annual.

Fetch shape: stateless full re-pull. The whole corpus is 6 tiny CSVs
(~0.5MB total); we re-fetch and overwrite every run, so revisions are picked
up for free. The VERSION segment is part of the URL and bumps on a new
release (e.g. 5.0.2.0 -> 5.1.0.0) — update the constant when the Met Office
ships a new version.

License: UK Open Government Licence v3 (redistribution OK with attribution).
"""

import csv
import io

import pyarrow as pa

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    save_raw_parquet,
    transient_retry,
)

VERSION = "5.1.0.0"
BASE_URL = (
    f"https://www.metoffice.gov.uk/hadobs/hadcrut5/data/HadCRUT.{VERSION}"
    f"/analysis/diagnostics"
)

# (region_slug, region_label) — region becomes a column value, not a dataset.
REGIONS = [
    ("global", "Global"),
    ("northern_hemisphere", "Northern Hemisphere"),
    ("southern_hemisphere", "Southern Hemisphere"),
]

# Each entity (monthly / annual) shares this schema; the time-key column name
# differs and is supplied per cadence.
_VALUE_FIELDS = [
    ("region", pa.string()),
    ("anomaly_c", pa.float64()),
    ("lower_95_c", pa.float64()),
    ("upper_95_c", pa.float64()),
]
MONTHLY_SCHEMA = pa.schema([("month", pa.string())] + _VALUE_FIELDS)
ANNUAL_SCHEMA = pa.schema([("year", pa.string())] + _VALUE_FIELDS)


@transient_retry()
def _fetch_csv(url: str) -> str:
    resp = get(url, timeout=(10.0, 120.0))
    resp.raise_for_status()
    return resp.text


def _summary_url(region_slug: str, cadence: str) -> str:
    return (
        f"{BASE_URL}/HadCRUT.{VERSION}.analysis.summary_series."
        f"{region_slug}.{cadence}.csv"
    )


def _parse_summary(content: str) -> list[tuple[str, str, str, str]]:
    """Return (time, anomaly, lower, upper) string tuples, skipping the header."""
    reader = csv.reader(io.StringIO(content))
    rows = list(reader)
    out: list[tuple[str, str, str, str]] = []
    for row in rows[1:]:
        if len(row) < 4 or not row[0].strip():
            continue
        out.append(
            (row[0].strip(), row[1].strip(), row[2].strip(), row[3].strip())
        )
    return out


def _to_float(s: str):
    return float(s) if s else None


def _fetch_cadence(node_id: str, cadence: str, schema: pa.Schema, time_col: str) -> None:
    """Fetch the 3 region CSVs for one cadence and write a single parquet asset."""
    rows: list[dict] = []
    for region_slug, region_label in REGIONS:
        url = _summary_url(region_slug, cadence)
        content = _fetch_csv(url)
        parsed = _parse_summary(content)
        if not parsed:
            raise AssertionError(f"{url}: parsed 0 data rows (format changed?)")
        for time_str, anomaly, lower, upper in parsed:
            rows.append(
                {
                    time_col: time_str,
                    "region": region_label,
                    "anomaly_c": _to_float(anomaly),
                    "lower_95_c": _to_float(lower),
                    "upper_95_c": _to_float(upper),
                }
            )
    table = pa.Table.from_pylist(rows, schema=schema)
    save_raw_parquet(table, node_id)


def fetch_monthly(node_id: str) -> None:
    _fetch_cadence(node_id, "monthly", MONTHLY_SCHEMA, "month")


def fetch_annual(node_id: str) -> None:
    _fetch_cadence(node_id, "annual", ANNUAL_SCHEMA, "year")


DOWNLOAD_SPECS = [
    NodeSpec(id="met-office-hadcrut5-hadcrut5-monthly", fn=fetch_monthly, kind="download"),
    NodeSpec(id="met-office-hadcrut5-hadcrut5-annual", fn=fetch_annual, kind="download"),
]


TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="met-office-hadcrut5-hadcrut5-monthly-transform",
        deps=["met-office-hadcrut5-hadcrut5-monthly"],
        sql='''
            SELECT DISTINCT
                CAST(month AS VARCHAR)      AS month,
                CAST(region AS VARCHAR)     AS region,
                CAST(anomaly_c AS DOUBLE)   AS anomaly_c,
                CAST(lower_95_c AS DOUBLE)  AS lower_95_c,
                CAST(upper_95_c AS DOUBLE)  AS upper_95_c
            FROM "met-office-hadcrut5-hadcrut5-monthly"
            WHERE month IS NOT NULL AND anomaly_c IS NOT NULL
            ORDER BY region, month
        ''',
    ),
    SqlNodeSpec(
        id="met-office-hadcrut5-hadcrut5-annual-transform",
        deps=["met-office-hadcrut5-hadcrut5-annual"],
        sql='''
            SELECT DISTINCT
                CAST(year AS VARCHAR)       AS year,
                CAST(region AS VARCHAR)     AS region,
                CAST(anomaly_c AS DOUBLE)   AS anomaly_c,
                CAST(lower_95_c AS DOUBLE)  AS lower_95_c,
                CAST(upper_95_c AS DOUBLE)  AS upper_95_c
            FROM "met-office-hadcrut5-hadcrut5-annual"
            WHERE year IS NOT NULL AND anomaly_c IS NOT NULL
            ORDER BY region, year
        ''',
    ),
]
