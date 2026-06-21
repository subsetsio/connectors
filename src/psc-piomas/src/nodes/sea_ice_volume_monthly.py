"""PIOMAS monthly pan-Arctic sea-ice VOLUME (10^3 km^3).

Stable CSV URL (bare "Current" token), full 1979-present corpus per request.
No auth, no pagination, no incremental query.
"""

import csv
import datetime as dt
import io

import pyarrow as pa

from subsets_utils import NodeSpec, SqlNodeSpec, save_raw_parquet
from utils import fetch

MONTHLY_CSV_URL = (
    "https://psc.apl.uw.edu/wordpress/wp-content/uploads/schweiger/"
    "ice_volume/PIOMAS.monthly.Current.v2.1.csv"
)

MONTHLY_SCHEMA = pa.schema(
    [("date", pa.date32()), ("volume_thousand_km3", pa.float64())]
)


def fetch_volume_monthly(node_id: str) -> None:
    asset = node_id
    text = fetch(MONTHLY_CSV_URL).text
    rows: list[dict] = []
    reader = csv.reader(io.StringIO(text))
    next(reader, None)  # header: year,Jan,...,Dec
    for parts in reader:
        if not parts or not parts[0].strip():
            continue
        try:
            year = int(float(parts[0]))  # source writes "1979.00"
        except ValueError:
            continue
        for month in range(1, 13):
            if month >= len(parts):
                break
            try:
                value = float(parts[month])
            except ValueError:
                continue
            if value < 0:
                continue  # -1 = month not yet available
            rows.append(
                {
                    "date": dt.date(year, month, 1),
                    "volume_thousand_km3": value,
                }
            )
    if not rows:
        raise RuntimeError(
            "PIOMAS monthly parser produced no rows — upstream format changed"
        )
    save_raw_parquet(pa.Table.from_pylist(rows, schema=MONTHLY_SCHEMA), asset)


DOWNLOAD_SPECS = [
    NodeSpec(
        id="psc-piomas-sea-ice-volume-monthly",
        fn=fetch_volume_monthly,
        kind="download",
    ),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="psc-piomas-sea-ice-volume-monthly-transform",
        deps=["psc-piomas-sea-ice-volume-monthly"],
        sql='''
            SELECT
                CAST(date AS DATE)                AS date,
                CAST(volume_thousand_km3 AS DOUBLE) AS volume_thousand_km3
            FROM "psc-piomas-sea-ice-volume-monthly"
            WHERE volume_thousand_km3 IS NOT NULL
            ORDER BY date
        ''',
    ),
]
