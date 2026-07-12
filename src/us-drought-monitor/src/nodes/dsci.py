"""US Drought Monitor — DSCI subset.

Drought Severity and Coverage Index (0-500), per (date, region).
`region` is "US" (national CONUS) or a state/territory abbreviation, covering
the US + 50 states + DC + Puerto Rico (52 FIPS).
"""

import pyarrow as pa

from subsets_utils import save_raw_parquet
from utils import STATE_FIPS, fetch, iso_to_date

# State DSCI rows carry the full state `name`; severity rows carry
# `stateAbbreviation` directly. Map names to abbreviations so both subsets emit
# the same `region` value.
STATE_NAME_TO_ABBREV = {
    "Alabama": "AL", "Alaska": "AK", "Arizona": "AZ", "Arkansas": "AR",
    "California": "CA", "Colorado": "CO", "Connecticut": "CT", "Delaware": "DE",
    "District of Columbia": "DC", "Florida": "FL", "Georgia": "GA", "Hawaii": "HI",
    "Idaho": "ID", "Illinois": "IL", "Indiana": "IN", "Iowa": "IA",
    "Kansas": "KS", "Kentucky": "KY", "Louisiana": "LA", "Maine": "ME",
    "Maryland": "MD", "Massachusetts": "MA", "Michigan": "MI", "Minnesota": "MN",
    "Mississippi": "MS", "Missouri": "MO", "Montana": "MT", "Nebraska": "NE",
    "Nevada": "NV", "New Hampshire": "NH", "New Jersey": "NJ", "New Mexico": "NM",
    "New York": "NY", "North Carolina": "NC", "North Dakota": "ND", "Ohio": "OH",
    "Oklahoma": "OK", "Oregon": "OR", "Pennsylvania": "PA", "Puerto Rico": "PR",
    "Rhode Island": "RI", "South Carolina": "SC", "South Dakota": "SD",
    "Tennessee": "TN", "Texas": "TX", "Utah": "UT", "Vermont": "VT",
    "Virginia": "VA", "Washington": "WA", "West Virginia": "WV",
    "Wisconsin": "WI", "Wyoming": "WY",
}

DSCI_SCHEMA = pa.schema([
    ("date", pa.string()),
    ("region", pa.string()),
    ("dsci", pa.int64()),
])


def fetch_dsci(node_id: str) -> None:
    asset = node_id
    rows: list[dict] = []

    # National (CONUS) — national DSCI rows carry `name`.
    for item in fetch("USStatistics/GetDSCI", "us"):
        if item.get("name") != "CONUS":
            continue
        rows.append({
            "date": iso_to_date(item["mapDate"]),
            "region": "US",
            "dsci": item["dsci"],
        })

    # Per-state — state DSCI rows carry the full state `name`.
    for fips in STATE_FIPS:
        for item in fetch("StateStatistics/GetDSCI", fips):
            name = item.get("name") or ""
            abbrev = STATE_NAME_TO_ABBREV.get(name)
            if abbrev is None:
                raise ValueError(f"Unknown USDM state name: {name!r}")
            rows.append({
                "date": iso_to_date(item["mapDate"]),
                "region": abbrev,
                "dsci": item["dsci"],
            })

    table = pa.Table.from_pylist(rows, schema=DSCI_SCHEMA)
    print(f"  {asset}: {len(table):,} rows")
    save_raw_parquet(table, asset)
