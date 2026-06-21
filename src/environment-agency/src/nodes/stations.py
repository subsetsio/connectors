"""Environment Agency (England) Hydrology — stations.

Reference catalog, one row per monitoring station (~9.5k). Tiny single-shot
pull re-fetched in full every run (stateless).
"""

import pyarrow as pa

from subsets_utils import NodeSpec, SqlNodeSpec, save_raw_parquet

from utils import (
    _get_json,
    _as_list,
    _id_of,
    _label_of,
    _str,
    _to_int,
    _to_float,
)

_STATIONS_SCHEMA = pa.schema([
    ("station_guid", pa.string()),
    ("name", pa.string()),
    ("notation", pa.string()),
    ("wiski_id", pa.string()),
    ("river_name", pa.string()),
    ("easting", pa.int64()),
    ("northing", pa.int64()),
    ("lat", pa.float64()),
    ("long", pa.float64()),
    ("date_opened", pa.string()),
    ("status", pa.string()),
    ("observed_properties", pa.string()),
    ("n_measures", pa.int64()),
])


def fetch_stations(node_id: str) -> None:
    asset = node_id
    items = _get_json("id/stations.json", _limit=1_000_000).get("items", [])
    rows = []
    for s in items:
        status = _as_list(s.get("status"))
        rows.append({
            "station_guid": _str(s.get("stationGuid") or s.get("notation")),
            "name": _str(s.get("label")),
            "notation": _str(s.get("notation")),
            "wiski_id": _str(s.get("wiskiID")),
            "river_name": _str(s.get("riverName")),
            "easting": _to_int(s.get("easting")),
            "northing": _to_int(s.get("northing")),
            "lat": _to_float(s.get("lat")),
            "long": _to_float(s.get("long")),
            "date_opened": _str(s.get("dateOpened")),
            "status": ", ".join(x for x in (_label_of(v) for v in status) if x) or None,
            "observed_properties": ", ".join(
                x for x in (_id_of(v) for v in _as_list(s.get("observedProperty"))) if x
            ) or None,
            "n_measures": len(_as_list(s.get("measures"))),
        })
    table = pa.Table.from_pylist(rows, schema=_STATIONS_SCHEMA)
    save_raw_parquet(table, asset)


DOWNLOAD_SPECS = [
    NodeSpec(id="environment-agency-stations", fn=fetch_stations, kind="download"),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="environment-agency-stations-transform",
        deps=["environment-agency-stations"],
        sql='''
            SELECT
                station_guid,
                name,
                notation,
                wiski_id,
                river_name,
                easting,
                northing,
                lat,
                long,
                TRY_CAST(date_opened AS DATE) AS date_opened,
                status,
                observed_properties,
                n_measures
            FROM "environment-agency-stations"
            WHERE station_guid IS NOT NULL
        ''',
    ),
]
