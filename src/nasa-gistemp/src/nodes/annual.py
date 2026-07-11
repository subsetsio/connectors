"""NASA GISTEMP v4 — annual Land-Ocean Temperature Index (LOTI).

Takes the J-D (Jan-Dec mean) column of the GLB/NH/SH wide tables as the annual
mean. Published as nasa-gistemp-annual (year, region, anomaly_c).
"""

import pyarrow as pa

from subsets_utils import save_raw_parquet
from utils import REGION_FILES, _fetch_csv, _parse_anomaly, _read_table

ANNUAL_SCHEMA = pa.schema([
    ("year", pa.int32()),
    ("region", pa.string()),
    ("anomaly_c", pa.float64()),
])


def fetch_annual(node_id: str) -> None:
    """Take the J-D (Jan-Dec mean) column of GLB/NH/SH as the annual mean."""
    asset = node_id
    rows = []
    for filename, region in REGION_FILES:
        header, data = _read_table(_fetch_csv(filename))
        for r in data:
            rec = dict(zip(header, r))
            val = _parse_anomaly(rec.get("J-D", ""))
            if val is None:
                continue
            rows.append({"year": int(rec["Year"].strip()), "region": region, "anomaly_c": val})
    table = pa.Table.from_pylist(rows, schema=ANNUAL_SCHEMA)
    save_raw_parquet(table, asset)
