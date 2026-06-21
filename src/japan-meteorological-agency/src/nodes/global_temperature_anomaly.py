"""TCC: global surface temperature anomaly."""
import io

import pyarrow as pa

from subsets_utils import NodeSpec, SqlNodeSpec, get, save_raw_parquet
from utils import TCC

_TEMP_SCHEMA = pa.schema([
    ("year", pa.int64()),
    ("month", pa.int64()),
    ("anomaly", pa.float64()),
])


def fetch_global_temperature_anomaly(node_id: str) -> None:
    text = get(f"{TCC}/gwp/temp/list/csv/mon_wld.csv", timeout=60).text
    rows = []
    reader = io.StringIO(text)
    header = reader.readline()  # Year,Jan,...,Dec
    for line in reader:
        line = line.strip()
        if not line:
            continue
        cells = line.split(",")
        year = int(cells[0])
        for month, raw in enumerate(cells[1:13], start=1):
            raw = raw.strip().rstrip("*")  # trailing '*' marks preliminary values
            if not raw:
                continue
            rows.append({"year": year, "month": month, "anomaly": float(raw)})
    if not rows:
        raise RuntimeError("global temperature anomaly CSV parsed to 0 rows")
    save_raw_parquet(pa.Table.from_pylist(rows, schema=_TEMP_SCHEMA), node_id)


DOWNLOAD_SPECS = [
    NodeSpec(id="japan-meteorological-agency-global-temperature-anomaly", fn=fetch_global_temperature_anomaly, kind="download"),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="japan-meteorological-agency-global-temperature-anomaly-transform",
        deps=["japan-meteorological-agency-global-temperature-anomaly"],
        sql='''
            SELECT
                make_date(CAST(year AS INTEGER), CAST(month AS INTEGER), 1) AS date,
                year, month, anomaly
            FROM "japan-meteorological-agency-global-temperature-anomaly"
            WHERE anomaly IS NOT NULL
            ORDER BY year, month
        ''',
    ),
]
