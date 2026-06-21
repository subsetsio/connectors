"""NASA GISTEMP v4 — monthly Land-Ocean Temperature Index (LOTI).

GISS publishes the global/hemispheric tables WIDE (rows = year; columns =
Jan..Dec monthly anomalies + J-D/D-N annual means + seasonal means). This
subset melts the Jan..Dec columns of GLB/NH/SH into long monthly rows.
Published as nasa-gistemp-monthly (month YYYY-MM, region, anomaly_c).
"""

import pyarrow as pa

from subsets_utils import NodeSpec, SqlNodeSpec, save_raw_parquet
from utils import REGION_FILES, _fetch_csv, _parse_anomaly, _read_table

MONTH_NAMES = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
               "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

MONTHLY_SCHEMA = pa.schema([
    ("month", pa.string()),
    ("region", pa.string()),
    ("anomaly_c", pa.float64()),
])


def fetch_monthly(node_id: str) -> None:
    """Melt the Jan..Dec columns of GLB/NH/SH into long monthly rows."""
    asset = node_id
    rows = []
    for filename, region in REGION_FILES:
        header, data = _read_table(_fetch_csv(filename))
        for r in data:
            rec = dict(zip(header, r))
            year = rec["Year"].strip()
            for i, mname in enumerate(MONTH_NAMES, start=1):
                val = _parse_anomaly(rec.get(mname, ""))
                if val is None:
                    continue
                rows.append({"month": f"{year}-{i:02d}", "region": region, "anomaly_c": val})
    table = pa.Table.from_pylist(rows, schema=MONTHLY_SCHEMA)
    save_raw_parquet(table, asset)


DOWNLOAD_SPECS = [
    NodeSpec(id="nasa-gistemp-monthly", fn=fetch_monthly, kind="download"),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="nasa-gistemp-monthly-transform",
        deps=["nasa-gistemp-monthly"],
        sql='''
            SELECT
                month,
                region,
                CAST(anomaly_c AS DOUBLE) AS anomaly_c
            FROM "nasa-gistemp-monthly"
            WHERE anomaly_c IS NOT NULL
        ''',
    ),
]
