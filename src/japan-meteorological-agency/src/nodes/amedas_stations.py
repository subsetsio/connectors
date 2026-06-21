"""bosai: AMeDAS station registry."""
import pyarrow as pa

from subsets_utils import NodeSpec, SqlNodeSpec, get, save_raw_parquet
from utils import BOSAI

_STATION_SCHEMA = pa.schema([
    ("station_id", pa.string()),
    ("type", pa.string()),
    ("elems", pa.string()),
    ("lat", pa.float64()),
    ("lon", pa.float64()),
    ("alt", pa.float64()),
    ("name_ja", pa.string()),
    ("name_kana", pa.string()),
    ("name_en", pa.string()),
])


def _dms_to_decimal(parts) -> float:
    """[degrees, minutes] -> decimal degrees."""
    deg, minute = parts[0], parts[1]
    return round(deg + minute / 60.0, 6)


def fetch_amedas_stations(node_id: str) -> None:
    tbl = get(f"{BOSAI}/amedas/const/amedastable.json", timeout=60).json()
    rows = []
    for sid, rec in tbl.items():
        rows.append({
            "station_id": sid,
            "type": rec.get("type"),
            "elems": rec.get("elems"),
            "lat": _dms_to_decimal(rec["lat"]) if rec.get("lat") else None,
            "lon": _dms_to_decimal(rec["lon"]) if rec.get("lon") else None,
            "alt": float(rec["alt"]) if rec.get("alt") is not None else None,
            "name_ja": rec.get("kjName"),
            "name_kana": rec.get("knName"),
            "name_en": rec.get("enName"),
        })
    save_raw_parquet(pa.Table.from_pylist(rows, schema=_STATION_SCHEMA), node_id)


DOWNLOAD_SPECS = [
    NodeSpec(id="japan-meteorological-agency-amedas-stations", fn=fetch_amedas_stations, kind="download"),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="japan-meteorological-agency-amedas-stations-transform",
        deps=["japan-meteorological-agency-amedas-stations"],
        sql='''
            SELECT
                station_id, type AS station_type, elems,
                lat, lon, alt,
                name_ja, name_kana, name_en
            FROM "japan-meteorological-agency-amedas-stations"
            WHERE station_id IS NOT NULL
        ''',
    ),
]
