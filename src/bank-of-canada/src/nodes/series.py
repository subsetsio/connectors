"""Bank of Canada — series subset.

Reference catalog of ~15,600 individual time series (/lists/series/json), one
row per series. Stateless full re-pull.
"""
import pyarrow as pa

from subsets_utils import NodeSpec, SqlNodeSpec, save_raw_parquet

from utils import BASE, _fetch_json

SERIES_SCHEMA = pa.schema([
    ("series_id", pa.string()),
    ("label", pa.string()),
    ("description", pa.string()),
])


def fetch_series(node_id: str) -> None:
    asset = node_id
    payload = _fetch_json(f"{BASE}/lists/series/json")
    series = payload["series"]
    rows = [
        {
            "series_id": sid,
            "label": (meta.get("label") or "").strip() or None,
            "description": (meta.get("description") or "").strip() or None,
        }
        for sid, meta in series.items()
    ]
    assert rows, "series list returned no entries"
    table = pa.Table.from_pylist(rows, schema=SERIES_SCHEMA)
    save_raw_parquet(table, asset)


DOWNLOAD_SPECS = [
    NodeSpec(id="bank-of-canada-series", fn=fetch_series, kind="download"),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="bank-of-canada-series-transform",
        deps=["bank-of-canada-series"],
        sql='''
            SELECT
                series_id,
                label,
                description
            FROM "bank-of-canada-series"
            WHERE series_id IS NOT NULL
        ''',
    ),
]
