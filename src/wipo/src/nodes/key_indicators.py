"""WIPO key-indicator subset: the 11 pre-computed headline indicators.

``keyindicators-json`` lists the 11 headline indicators; ``keysearch-json/{id}``
returns clean JSON ({recordInfo, columns, records}) with type/office/origin +
year columns. Unlike the ips/pmh table-result endpoint, keysearch-json formats
the displayed cell with thousands separators (``"1,202,500"``) and route/origin
breakdowns live in the rows (the ``origin`` column), not packed in cells -- so
each (row, year) is a single value read from the ``<year>_SeqOrder`` companion.

Fetch shape: stateless full re-pull every run. Raw is streamed to one parquet
file per subset via ``raw_parquet_writer``.
"""

import pyarrow as pa

from subsets_utils import NodeSpec, SqlNodeSpec, raw_parquet_writer
from utils import get_json, year_columns

# Schema for the pre-computed key-indicator subset (has an IP-right column).
KEY_SCHEMA = pa.schema([
    ("indicator_id", pa.int32()),
    ("indicator", pa.string()),
    ("ip_right", pa.string()),
    ("office", pa.string()),
    ("origin", pa.string()),
    ("year", pa.int32()),
    ("breakdown_index", pa.int32()),
    ("value", pa.float64()),
])


def _parse_key_table(data: dict, indicator_id: int, indicator: str) -> list[dict]:
    """Parse a keyindicator keysearch-json envelope into long-format rows.

    Unlike the ips/pmh table-result endpoint, keysearch-json formats the
    displayed cell with thousands separators (``"1,202,500"``) and route/origin
    breakdowns live in the rows (the ``origin`` column), not packed in cells --
    so each (row, year) is a single value. We read the clean numeric companion
    ``<year>_SeqOrder`` rather than parse the comma-formatted display string.
    """
    cols = year_columns(data.get("columns") or [])
    rows: list[dict] = []
    for rec in data.get("records") or []:
        ip_right = rec.get("ipr")
        office = rec.get("office")
        origin = rec.get("origin")
        for code, year in cols:
            raw = rec.get(f"{code}_SeqOrder")
            if raw is None or raw == "":
                continue
            try:
                value = float(raw)
            except (TypeError, ValueError):
                continue
            rows.append({
                "indicator_id": indicator_id,
                "indicator": indicator,
                "ip_right": ip_right,
                "office": office,
                "origin": origin,
                "year": year,
                "breakdown_index": 0,
                "value": value,
            })
    return rows


def fetch_keyindicator(node_id: str) -> None:
    """Fetch all 11 pre-computed headline key indicators."""
    asset = node_id
    catalog = get_json("keyindicator/keyindicators-json", {})
    if not isinstance(catalog, dict) or not catalog:
        raise AssertionError(f"{asset}: empty keyindicators-json catalog")

    written = 0
    with raw_parquet_writer(asset, KEY_SCHEMA) as writer:
        for key_id, label in catalog.items():
            data = get_json(f"keyindicator/keysearch-json/{key_id}", {})
            rows = _parse_key_table(data, int(key_id), str(label))
            if rows:
                writer.write_table(pa.Table.from_pylist(rows, schema=KEY_SCHEMA))
                written += len(rows)
    if written == 0:
        raise AssertionError(f"{asset}: key indicators produced no rows")


DOWNLOAD_SPECS = [
    NodeSpec(id="wipo-key-indicators", fn=fetch_keyindicator, kind="download"),
]

_KEY_SQL = '''
    SELECT
        indicator_id,
        indicator,
        ip_right,
        office,
        origin,
        CAST(year AS INTEGER)          AS year,
        breakdown_index,
        CAST(value AS DOUBLE)          AS value
    FROM "{dep}"
    WHERE value IS NOT NULL
'''

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="wipo-key-indicators-transform",
        deps=["wipo-key-indicators"],
        sql=_KEY_SQL.format(dep="wipo-key-indicators"),
    ),
]
