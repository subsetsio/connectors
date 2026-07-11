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
Time is YYYY-MM for monthly and YYYY for annual. We normalise the period label
into a real `date` column (first of the month for monthly; Jan 1 for annual)
so the raw is directly comparable and the freshness assertions stay robust.

Fetch shape: stateless full re-pull. The whole corpus is 6 tiny CSVs
(~0.5MB total); we re-fetch and overwrite every run, so revisions are picked
up for free. The VERSION segment is part of the URL and bumps on a new
release (e.g. 5.0.2.0 -> 5.1.0.0) - update the constant when the Met Office
ships a new version.

License: UK Open Government Licence v3 (redistribution OK with attribution).
"""

import csv
import io
from datetime import date

import pyarrow as pa

from subsets_utils import (
    NodeSpec,
    get,
    save_raw_parquet,
    transient_retry,
)

VERSION = "5.1.0.0"
BASE_URL = (
    f"https://www.metoffice.gov.uk/hadobs/hadcrut5/data/HadCRUT.{VERSION}"
    f"/analysis/diagnostics"
)

# (region_slug, region_label) - region becomes a column value, not a dataset.
REGIONS = [
    ("global", "Global"),
    ("northern_hemisphere", "Northern Hemisphere"),
    ("southern_hemisphere", "Southern Hemisphere"),
]

# Both cadences share the value columns; the temporal column is a real date
# (first-of-period), so the schema is identical for monthly and annual.
SCHEMA = pa.schema(
    [
        ("date", pa.date32()),
        ("region", pa.string()),
        ("anomaly_c", pa.float64()),
        ("lower_95_c", pa.float64()),
        ("upper_95_c", pa.float64()),
    ]
)


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


def _parse_period(time_str: str) -> date:
    """'YYYY-MM' -> date(Y, M, 1); 'YYYY' -> date(Y, 1, 1)."""
    time_str = time_str.strip()
    if "-" in time_str:
        year, month = time_str.split("-", 1)
        return date(int(year), int(month), 1)
    return date(int(time_str), 1, 1)


def _to_float(s: str):
    s = s.strip()
    return float(s) if s else None


def _parse_summary(content: str) -> list[list[str]]:
    """Return the non-empty data rows (each a 4-field list), skipping header."""
    reader = csv.reader(io.StringIO(content))
    rows = list(reader)
    out: list[list[str]] = []
    for row in rows[1:]:
        if len(row) < 4 or not row[0].strip():
            continue
        out.append(row)
    return out


def _fetch_cadence(node_id: str, cadence: str) -> None:
    """Fetch the 3 region CSVs for one cadence and write a single parquet asset."""
    rows: list[dict] = []
    for region_slug, region_label in REGIONS:
        url = _summary_url(region_slug, cadence)
        parsed = _parse_summary(_fetch_csv(url))
        if not parsed:
            raise AssertionError(f"{url}: parsed 0 data rows (format changed?)")
        for row in parsed:
            rows.append(
                {
                    "date": _parse_period(row[0]),
                    "region": region_label,
                    "anomaly_c": _to_float(row[1]),
                    "lower_95_c": _to_float(row[2]),
                    "upper_95_c": _to_float(row[3]),
                }
            )
    table = pa.Table.from_pylist(rows, schema=SCHEMA)
    save_raw_parquet(table, node_id)


def fetch_monthly(node_id: str) -> None:
    _fetch_cadence(node_id, "monthly")


def fetch_annual(node_id: str) -> None:
    _fetch_cadence(node_id, "annual")


DOWNLOAD_SPECS = [
    NodeSpec(id="met-office-hadcrut5-hadcrut5-monthly", fn=fetch_monthly, kind="download"),
    NodeSpec(id="met-office-hadcrut5-hadcrut5-annual", fn=fetch_annual, kind="download"),
]
