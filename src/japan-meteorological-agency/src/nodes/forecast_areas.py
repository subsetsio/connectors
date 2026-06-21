"""bosai: forecast-area taxonomy."""
import pyarrow as pa

from subsets_utils import NodeSpec, SqlNodeSpec, get, save_raw_parquet
from utils import BOSAI

_AREA_SCHEMA = pa.schema([
    ("code", pa.string()),
    ("level", pa.string()),
    ("name_ja", pa.string()),
    ("name_en", pa.string()),
    ("office_name", pa.string()),
    ("parent", pa.string()),
])


def fetch_forecast_areas(node_id: str) -> None:
    area = get(f"{BOSAI}/common/const/area.json", timeout=60).json()
    rows = []
    for level in ("centers", "offices", "class10s", "class20s"):
        for code, rec in area.get(level, {}).items():
            rows.append({
                "code": code,
                "level": level,
                "name_ja": rec.get("name"),
                "name_en": rec.get("enName"),
                "office_name": rec.get("officeName"),
                "parent": rec.get("parent"),
            })
    save_raw_parquet(pa.Table.from_pylist(rows, schema=_AREA_SCHEMA), node_id)


DOWNLOAD_SPECS = [
    NodeSpec(id="japan-meteorological-agency-forecast-areas", fn=fetch_forecast_areas, kind="download"),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="japan-meteorological-agency-forecast-areas-transform",
        deps=["japan-meteorological-agency-forecast-areas"],
        sql='''
            SELECT code, level, name_ja, name_en, office_name, parent
            FROM "japan-meteorological-agency-forecast-areas"
            WHERE code IS NOT NULL
        ''',
    ),
]
