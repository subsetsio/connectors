"""Environment Agency (England) Hydrology — measures (series catalog).

One row per measure = station x parameter x period x statistic (~32k). Tiny
single-shot pull re-fetched in full every run (stateless).
"""

import pyarrow as pa

from subsets_utils import NodeSpec, SqlNodeSpec, save_raw_parquet

from utils import (
    _get_json,
    _last_seg,
    _id_of,
    _label_of,
    _str,
    _to_int,
)

_MEASURES_SCHEMA = pa.schema([
    ("measure_id", pa.string()),
    ("name", pa.string()),
    ("parameter", pa.string()),
    ("parameter_name", pa.string()),
    ("period", pa.int64()),
    ("period_name", pa.string()),
    ("value_type", pa.string()),
    ("value_statistic", pa.string()),
    ("observation_type", pa.string()),
    ("observed_property", pa.string()),
    ("observed_property_label", pa.string()),
    ("station_guid", pa.string()),
    ("station_label", pa.string()),
    ("unit", pa.string()),
    ("unit_name", pa.string()),
])


def fetch_measures(node_id: str) -> None:
    asset = node_id
    items = _get_json("id/measures.json", _limit=2_000_000).get("items", [])
    rows = []
    for m in items:
        station = m.get("station") if isinstance(m.get("station"), dict) else {}
        rows.append({
            "measure_id": _str(m.get("notation")),
            "name": _str(m.get("label")),
            "parameter": _str(m.get("parameter")),
            "parameter_name": _str(m.get("parameterName")),
            "period": _to_int(m.get("period")),
            "period_name": _str(m.get("periodName")),
            "value_type": _str(m.get("valueType")),
            "value_statistic": _label_of(m.get("valueStatistic")),
            "observation_type": _label_of(m.get("observationType")),
            "observed_property": _id_of(m.get("observedProperty")),
            "observed_property_label": _label_of(m.get("observedProperty")),
            "station_guid": _last_seg(station.get("@id")) if station else None,
            "station_label": _str(station.get("label")) if station else None,
            "unit": _id_of(m.get("unit")),
            "unit_name": _str(m.get("unitName")),
        })
    table = pa.Table.from_pylist(rows, schema=_MEASURES_SCHEMA)
    save_raw_parquet(table, asset)


DOWNLOAD_SPECS = [
    NodeSpec(id="environment-agency-measures", fn=fetch_measures, kind="download"),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="environment-agency-measures-transform",
        deps=["environment-agency-measures"],
        sql='''
            SELECT
                measure_id,
                name,
                parameter,
                parameter_name,
                period,
                period_name,
                value_type,
                value_statistic,
                observation_type,
                observed_property,
                observed_property_label,
                station_guid,
                station_label,
                unit,
                unit_name
            FROM "environment-agency-measures"
            WHERE measure_id IS NOT NULL
        ''',
    ),
]
