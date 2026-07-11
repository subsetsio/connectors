"""NASA GISTEMP v4 — zonal annual Land-Ocean Temperature Index (LOTI).

Melts the 14 latitude-band columns of ZonAnn.Ts+dSST.csv into long rows.
Published as nasa-gistemp-zonal-annual (year, zone, anomaly_c).
"""

import pyarrow as pa

from subsets_utils import save_raw_parquet
from utils import _fetch_csv, _parse_anomaly, _read_table

ZONAL_FILE = "ZonAnn.Ts+dSST.csv"

ZONAL_SCHEMA = pa.schema([
    ("year", pa.int32()),
    ("zone", pa.string()),
    ("anomaly_c", pa.float64()),
])


def fetch_zonal_annual(node_id: str) -> None:
    """Melt the 14 latitude-band columns of ZonAnn.Ts+dSST.csv into long rows."""
    asset = node_id
    header, data = _read_table(_fetch_csv(ZONAL_FILE))
    rows = []
    for r in data:
        year = int(r[0].strip())
        for col_idx, zone in enumerate(header[1:], start=1):
            if col_idx >= len(r):
                continue
            val = _parse_anomaly(r[col_idx])
            if val is None:
                continue
            rows.append({"year": year, "zone": zone, "anomaly_c": val})
    table = pa.Table.from_pylist(rows, schema=ZONAL_SCHEMA)
    save_raw_parquet(table, asset)
