"""US Drought Monitor — drought severity subset.

Percent of area in each drought category (D0-D4) + none, per (date, region).
`region` is "US" (national CONUS) or a state/territory abbreviation: CONUS,
the 50 states, DC, and Puerto Rico (53 region codes total).
"""

import pyarrow as pa

from subsets_utils import save_raw_parquet
from utils import REGION_CODES, STATE_FIPS, fetch, iso_to_date

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

    # Per-state/DC/PR — `stateAbbreviation` is the region directly.
    for fips in STATE_FIPS:
        for item in fetch("StateStatistics/GetDroughtSeverityStatisticsByAreaPercent", fips):
            region = item["stateAbbreviation"]
            if region not in REGION_CODES:
                raise ValueError(f"Unknown USDM state abbreviation: {region!r}")
            rows.append({
                "date": iso_to_date(item["mapDate"]),
                "region": region,
                "none": item["none"], "d0": item["d0"], "d1": item["d1"],
                "d2": item["d2"], "d3": item["d3"], "d4": item["d4"],
            })

    table = pa.Table.from_pylist(rows, schema=SEVERITY_SCHEMA)
    print(f"  {asset}: {len(table):,} rows")
    save_raw_parquet(table, asset)
