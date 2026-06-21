"""NSIDC Sea Ice Index — daily climatology (1981-2010 baseline).

Published subset: nsidc-sea-ice-extent-daily-climatology
"""

import csv
import io

import pyarrow as pa

from subsets_utils import NodeSpec, SqlNodeSpec, save_raw_parquet
from utils import download_csv, parse_float

_CLIMATOLOGY_FILES = [
    ("north/daily/data/N_seaice_extent_climatology_1981-2010_v4.0.csv", "Arctic"),
    ("south/daily/data/S_seaice_extent_climatology_1981-2010_v4.0.csv", "Antarctic"),
]

_CLIMATOLOGY_SCHEMA = pa.schema([
    ("day_of_year", pa.int32()),
    ("hemisphere", pa.string()),
    ("average_extent_million_km2", pa.float64()),
    ("std_deviation_million_km2", pa.float64()),
    ("pctl_10_million_km2", pa.float64()),
    ("pctl_25_million_km2", pa.float64()),
    ("pctl_50_million_km2", pa.float64()),
    ("pctl_75_million_km2", pa.float64()),
    ("pctl_90_million_km2", pa.float64()),
])


def _parse_climatology(content: str, hemisphere: str) -> list[dict]:
    rows = list(csv.reader(io.StringIO(content)))
    # rows[0] = "std Years = 1981-2010" preamble, rows[1] = header.
    header = [h.strip() for h in rows[1]]
    i_doy = header.index("DOY")
    i_avg = header.index("Average Extent")
    i_std = header.index("Std Deviation")
    i_10 = header.index("10th")
    i_25 = header.index("25th")
    i_50 = header.index("50th")
    i_75 = header.index("75th")
    i_90 = header.index("90th")

    out = []
    for r in rows[2:]:
        if len(r) <= i_90:
            continue
        doy = r[i_doy].strip()
        if not doy.isdigit():
            continue
        out.append({
            "day_of_year": int(doy),
            "hemisphere": hemisphere,
            "average_extent_million_km2": parse_float(r[i_avg]),
            "std_deviation_million_km2": parse_float(r[i_std]),
            "pctl_10_million_km2": parse_float(r[i_10]),
            "pctl_25_million_km2": parse_float(r[i_25]),
            "pctl_50_million_km2": parse_float(r[i_50]),
            "pctl_75_million_km2": parse_float(r[i_75]),
            "pctl_90_million_km2": parse_float(r[i_90]),
        })
    return out


def fetch_climatology(node_id: str) -> None:
    asset = node_id
    records: list[dict] = []
    for path, hemisphere in _CLIMATOLOGY_FILES:
        records.extend(_parse_climatology(download_csv(path), hemisphere))
    table = pa.Table.from_pylist(records, schema=_CLIMATOLOGY_SCHEMA)
    save_raw_parquet(table, asset)


DOWNLOAD_SPECS = [
    NodeSpec(
        id="nsidc-sea-ice-extent-daily-climatology",
        fn=fetch_climatology,
        kind="download",
    ),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="nsidc-sea-ice-extent-daily-climatology-transform",
        deps=["nsidc-sea-ice-extent-daily-climatology"],
        sql='''
            SELECT
                day_of_year,
                hemisphere,
                average_extent_million_km2,
                std_deviation_million_km2,
                pctl_10_million_km2,
                pctl_25_million_km2,
                pctl_50_million_km2,
                pctl_75_million_km2,
                pctl_90_million_km2
            FROM "nsidc-sea-ice-extent-daily-climatology"
            ORDER BY hemisphere, day_of_year
        ''',
    ),
]
