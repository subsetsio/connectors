"""US Drought Monitor — drought severity subset.

Percent of area in each drought category (D0-D4) + none, per (date, region).
`region` is "US" (national CONUS) or a state/territory abbreviation, covering
the US + 50 states + DC + Puerto Rico (52 FIPS).
"""

import pyarrow as pa

from subsets_utils import NodeSpec, SqlNodeSpec, save_raw_parquet
from utils import STATE_FIPS, fetch, iso_to_date

SEVERITY_SCHEMA = pa.schema([
    ("date", pa.string()),
    ("region", pa.string()),
    ("none", pa.float64()),
    ("d0", pa.float64()),
    ("d1", pa.float64()),
    ("d2", pa.float64()),
    ("d3", pa.float64()),
    ("d4", pa.float64()),
])


def fetch_drought_severity(node_id: str) -> None:
    asset = node_id
    rows: list[dict] = []

    # National (CONUS) — filter out the "Total" rows that include territories.
    for item in fetch("USStatistics/GetDroughtSeverityStatisticsByAreaPercent", "us"):
        if item.get("areaOfInterest") != "CONUS":
            continue
        rows.append({
            "date": iso_to_date(item["mapDate"]),
            "region": "US",
            "none": item["none"], "d0": item["d0"], "d1": item["d1"],
            "d2": item["d2"], "d3": item["d3"], "d4": item["d4"],
        })

    # Per-state — `stateAbbreviation` is the region directly.
    for fips in STATE_FIPS:
        for item in fetch("StateStatistics/GetDroughtSeverityStatisticsByAreaPercent", fips):
            rows.append({
                "date": iso_to_date(item["mapDate"]),
                "region": item["stateAbbreviation"],
                "none": item["none"], "d0": item["d0"], "d1": item["d1"],
                "d2": item["d2"], "d3": item["d3"], "d4": item["d4"],
            })

    table = pa.Table.from_pylist(rows, schema=SEVERITY_SCHEMA)
    print(f"  {asset}: {len(table):,} rows")
    save_raw_parquet(table, asset)


DOWNLOAD_SPECS = [
    NodeSpec(id="us-drought-monitor-drought-severity", fn=fetch_drought_severity, kind="download"),
]

TRANSFORM_SPECS = [
    # Severity: convert cumulative D0-D4 into exclusive categories so
    # none + D0..D4 ~ 100%. Negatives from rounding are clamped to zero.
    SqlNodeSpec(
        id="us-drought-monitor-drought-severity-transform",
        deps=["us-drought-monitor-drought-severity"],
        sql='''
            SELECT
                CAST(date AS DATE)                    AS date,
                region,
                ROUND(none, 2)                        AS none_pct,
                ROUND(GREATEST(d0 - d1, 0), 2)        AS d0_pct,
                ROUND(GREATEST(d1 - d2, 0), 2)        AS d1_pct,
                ROUND(GREATEST(d2 - d3, 0), 2)        AS d2_pct,
                ROUND(GREATEST(d3 - d4, 0), 2)        AS d3_pct,
                ROUND(d4, 2)                          AS d4_pct
            FROM "us-drought-monitor-drought-severity"
            WHERE date IS NOT NULL AND region IS NOT NULL
        ''',
    ),
]
