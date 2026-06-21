"""World Bank — countries.

Country + aggregate-region reference table. Small, re-pulled in full every run
(stateless).
"""
import pyarrow as pa

from subsets_utils import NodeSpec, SqlNodeSpec, save_raw_parquet
from utils import _fetch_all_pages, _nested, _to_float

_COUNTRY_SCHEMA = pa.schema([
    ("id", pa.string()),
    ("iso2_code", pa.string()),
    ("name", pa.string()),
    ("region_id", pa.string()),
    ("region_value", pa.string()),
    ("adminregion_id", pa.string()),
    ("adminregion_value", pa.string()),
    ("income_level_id", pa.string()),
    ("income_level_value", pa.string()),
    ("lending_type_id", pa.string()),
    ("lending_type_value", pa.string()),
    ("capital_city", pa.string()),
    ("longitude", pa.float64()),
    ("latitude", pa.float64()),
])


def fetch_countries(node_id: str) -> None:
    asset = node_id
    records = _fetch_all_pages("country", {}, per_page=400)
    rows = []
    for r in records:
        rows.append({
            "id": r.get("id"),
            "iso2_code": r.get("iso2Code"),
            "name": (r.get("name") or "").strip(),
            "region_id": _nested(r, "region", "id"),
            "region_value": _nested(r, "region", "value"),
            "adminregion_id": _nested(r, "adminregion", "id"),
            "adminregion_value": _nested(r, "adminregion", "value"),
            "income_level_id": _nested(r, "incomeLevel", "id"),
            "income_level_value": _nested(r, "incomeLevel", "value"),
            "lending_type_id": _nested(r, "lendingType", "id"),
            "lending_type_value": _nested(r, "lendingType", "value"),
            "capital_city": (r.get("capitalCity") or "").strip(),
            "longitude": _to_float(r.get("longitude")),
            "latitude": _to_float(r.get("latitude")),
        })
    table = pa.Table.from_pylist(rows, schema=_COUNTRY_SCHEMA)
    save_raw_parquet(table, asset)


DOWNLOAD_SPECS = [
    NodeSpec(id="world-bank-countries", fn=fetch_countries, kind="download"),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="world-bank-countries-transform",
        deps=["world-bank-countries"],
        sql='''
            SELECT
                id                  AS country_code,
                iso2_code,
                name,
                region_id,
                NULLIF(region_value, '')        AS region,
                NULLIF(income_level_value, '')  AS income_level,
                NULLIF(lending_type_value, '')  AS lending_type,
                NULLIF(capital_city, '')        AS capital_city,
                longitude,
                latitude
            FROM "world-bank-countries"
            WHERE id IS NOT NULL
        ''',
    ),
]
