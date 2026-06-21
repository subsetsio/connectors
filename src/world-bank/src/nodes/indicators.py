"""World Bank — indicators.

~29.5k indicator metadata records. Small relative to the values firehose and
re-pulled in full every run (stateless).
"""
import pyarrow as pa

from subsets_utils import NodeSpec, SqlNodeSpec, save_raw_parquet
from utils import _indicator_rows

_INDICATOR_SCHEMA = pa.schema([
    ("id", pa.string()),
    ("name", pa.string()),
    ("unit", pa.string()),
    ("source_id", pa.string()),
    ("source_name", pa.string()),
    ("source_note", pa.string()),
    ("source_organization", pa.string()),
    ("topic_ids", pa.string()),
    ("topic_names", pa.string()),
])


def fetch_indicators(node_id: str) -> None:
    asset = node_id
    rows = _indicator_rows()
    table = pa.Table.from_pylist(rows, schema=_INDICATOR_SCHEMA)
    save_raw_parquet(table, asset)


DOWNLOAD_SPECS = [
    NodeSpec(id="world-bank-indicators", fn=fetch_indicators, kind="download"),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="world-bank-indicators-transform",
        deps=["world-bank-indicators"],
        sql='''
            SELECT
                id                          AS indicator_code,
                name,
                NULLIF(unit, '')            AS unit,
                source_id,
                NULLIF(source_name, '')     AS source_name,
                NULLIF(source_note, '')     AS definition,
                NULLIF(source_organization, '') AS source_organization,
                NULLIF(topic_names, '')     AS topics
            FROM "world-bank-indicators"
            WHERE id IS NOT NULL
        ''',
    ),
]
