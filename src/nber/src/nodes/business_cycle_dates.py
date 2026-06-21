"""US Business Cycle Expansions and Contractions — the canonical NBER recession
chronology, a single small JSON at
data.nber.org/cycles/business_cycle_dates.json.
"""
import pyarrow as pa

from subsets_utils import NodeSpec, SqlNodeSpec, save_raw_parquet
from utils import _get

CYCLES_URL = "https://data.nber.org/cycles/business_cycle_dates.json"

CYCLES_SCHEMA = pa.schema([
    ("peak", pa.string()),
    ("trough", pa.string()),
])


def fetch_business_cycle_dates(node_id: str) -> None:
    asset = node_id
    data = _get(CYCLES_URL).json()
    rows = [
        {
            "peak": (c.get("peak") or "").strip() or None,
            "trough": (c.get("trough") or "").strip() or None,
        }
        for c in data
    ]
    save_raw_parquet(pa.Table.from_pylist(rows, schema=CYCLES_SCHEMA), asset)


DOWNLOAD_SPECS = [
    NodeSpec(id="nber-business-cycle-dates", fn=fetch_business_cycle_dates, kind="download"),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="nber-business-cycle-dates-transform",
        deps=["nber-business-cycle-dates"],
        sql='''
            SELECT
                CAST(peak AS DATE)   AS peak_date,
                CAST(trough AS DATE) AS trough_date
            FROM "nber-business-cycle-dates"
        ''',
    ),
]
