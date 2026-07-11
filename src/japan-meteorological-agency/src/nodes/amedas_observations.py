"""bosai: latest AMeDAS observation snapshot (long format)."""
import re

import pyarrow as pa

from subsets_utils import NodeSpec, SqlNodeSpec, get, save_raw_parquet
from utils import BOSAI

_OBS_SCHEMA = pa.schema([
    ("station_id", pa.string()),
    ("observed_at", pa.string()),   # ISO8601 with JST offset, as published
    ("element", pa.string()),
    ("value", pa.float64()),
    ("quality_flag", pa.int64()),
])


def fetch_amedas_observations(node_id: str) -> None:
    # Resolve the rolling "latest" pointer, then fetch that snapshot.
    latest = get(f"{BOSAI}/amedas/data/latest_time.txt", timeout=60).text.strip()
    ts = re.sub(r"[-:T]", "", latest).split("+")[0]  # 2026-06-19T07:00:00+09:00 -> 20260619070000
    snapshot = get(f"{BOSAI}/amedas/data/map/{ts}.json", timeout=120).json()
    rows = []
    for sid, elements in snapshot.items():
        for elem, pair in elements.items():
            if not isinstance(pair, list) or not pair:
                continue
            val = pair[0]
            flag = pair[1] if len(pair) > 1 else None
            rows.append({
                "station_id": sid,
                "observed_at": latest,
                "element": elem,
                "value": float(val) if isinstance(val, (int, float)) else None,
                "quality_flag": int(flag) if isinstance(flag, int) else None,
            })
    save_raw_parquet(pa.Table.from_pylist(rows, schema=_OBS_SCHEMA), node_id)


_DOWNLOAD_SPECS = [
    NodeSpec(id="japan-meteorological-agency-amedas-observations", fn=fetch_amedas_observations, kind="download"),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="japan-meteorological-agency-amedas-observations-transform",
        deps=["japan-meteorological-agency-amedas-observations"],
        sql='''
            SELECT
                station_id,
                CAST(observed_at AS TIMESTAMPTZ) AS observed_at,
                element, value, quality_flag
            FROM "japan-meteorological-agency-amedas-observations"
            WHERE station_id IS NOT NULL AND element IS NOT NULL AND value IS NOT NULL
        ''',
    ),
]
