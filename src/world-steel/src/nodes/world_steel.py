"""World Steel Association Steel Data Viewer downloads.

The public Steel Data Viewer uses a small JSON backend at
https://worldsteel.org/mappingworld-api/. The catalog endpoint returns
indicator metadata plus country/region metadata; the values endpoint accepts a
comma-separated list of indicator ids and returns nested geoitem -> period ->
value maps.

Raw shape:
  indicators  one row per indicator id
  geoitems    one row per country/region code
  values      long-format observations across indicator x geoitem x period

The source exposes no incremental filter, so each node performs a stateless
full refresh and overwrites its raw Parquet asset.
"""

import json

import pyarrow as pa

from subsets_utils import NodeSpec, get, save_raw_parquet

SLUG = "world-steel"
BASE_URL = "https://worldsteel.org/mappingworld-api/"
REFERER = "https://worldsteel.org/data/steel-data-viewer/"

CATALOG_PARAMS = {
    "lang": "",
    "rand": "17754",
    "meta": "",
    "geoitems": "",
    "indicators": "",
    "datasets": "",
}

INDICATORS_SCHEMA = pa.schema([
    ("indicator_id", pa.string()),
    ("label", pa.string()),
    ("unit", pa.string()),
    ("numberformat", pa.string()),
    ("group_id", pa.string()),
    ("datasource", pa.string()),
    ("world_all", pa.string()),
    ("forecast", pa.string()),
    ("statistics_from", pa.int32()),
    ("statistics_to", pa.int32()),
    ("metadata_json", pa.string()),
])

GEOITEMS_SCHEMA = pa.schema([
    ("geoitem_id", pa.string()),
    ("type", pa.string()),
    ("label", pa.string()),
    ("wsa", pa.string()),
    ("order_id", pa.string()),
    ("color", pa.string()),
    ("regions_json", pa.string()),
    ("children_json", pa.string()),
    ("metadata_json", pa.string()),
])

VALUES_SCHEMA = pa.schema([
    ("indicator_id", pa.string()),
    ("geoitem_id", pa.string()),
    ("period", pa.string()),
    ("year", pa.int32()),
    ("month", pa.int32()),
    ("value", pa.float64()),
])


def _fetch_json(params: dict[str, str]) -> dict:
    response = get(
        BASE_URL,
        params=params,
        headers={"Accept": "application/json, */*", "Referer": REFERER},
        timeout=(10.0, 180.0),
    )
    response.raise_for_status()
    if not response.text.strip():
        raise RuntimeError(f"empty response from {response.url}")
    return response.json()


def _catalog() -> dict:
    data = _fetch_json(CATALOG_PARAMS)
    if "indicators" not in data or "geoitems" not in data:
        raise RuntimeError("catalog response missing indicators or geoitems")
    return data


def _json_dumps(value) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _period_parts(period: str) -> tuple[int | None, int | None]:
    if len(period) == 4 and period.isdigit():
        return int(period), None
    if len(period) == 6 and period.isdigit():
        month = int(period[4:])
        if 1 <= month <= 12:
            return int(period[:4]), month
    return None, None


def _to_float(value) -> float | None:
    if value is None or value == "":
        return None
    return float(value)


def fetch_indicators(node_id: str) -> None:
    indicators = _catalog()["indicators"]
    rows = []
    for indicator_id, record in sorted(indicators.items()):
        stats_range = (record.get("statistics") or {}).get("range") or {}
        rows.append({
            "indicator_id": indicator_id,
            "label": record.get("label"),
            "unit": record.get("unit"),
            "numberformat": record.get("numberformat"),
            "group_id": record.get("group"),
            "datasource": record.get("datasource"),
            "world_all": record.get("world_all"),
            "forecast": record.get("forecast"),
            "statistics_from": stats_range.get("from"),
            "statistics_to": stats_range.get("to"),
            "metadata_json": _json_dumps(record),
        })
    save_raw_parquet(pa.Table.from_pylist(rows, schema=INDICATORS_SCHEMA), node_id)


def fetch_geoitems(node_id: str) -> None:
    geoitems = _catalog()["geoitems"]
    rows = []
    for geoitem_id, record in sorted(geoitems.items()):
        rows.append({
            "geoitem_id": geoitem_id,
            "type": record.get("type"),
            "label": record.get("label"),
            "wsa": record.get("wsa"),
            "order_id": record.get("order"),
            "color": record.get("color"),
            "regions_json": _json_dumps(record.get("regions") or []),
            "children_json": _json_dumps(record.get("geoitems") or []),
            "metadata_json": _json_dumps(record),
        })
    save_raw_parquet(pa.Table.from_pylist(rows, schema=GEOITEMS_SCHEMA), node_id)


def fetch_values(node_id: str) -> None:
    indicators = sorted(_catalog()["indicators"])
    data = _fetch_json({"values": ",".join(indicators), "lang": "EN"})
    payload = data.get("indicators") or {}
    missing = sorted(set(indicators) - set(payload))
    if missing:
        raise RuntimeError(f"values response missing {len(missing)} indicators: {missing[:10]}")

    rows = []
    for indicator_id in indicators:
        values = (payload[indicator_id] or {}).get("values") or {}
        for geoitem_id, periods in values.items():
            for period, value in periods.items():
                year, month = _period_parts(str(period))
                rows.append({
                    "indicator_id": indicator_id,
                    "geoitem_id": geoitem_id,
                    "period": str(period),
                    "year": year,
                    "month": month,
                    "value": _to_float(value),
                })
    if not rows:
        raise RuntimeError("values endpoint returned no observations")
    save_raw_parquet(pa.Table.from_pylist(rows, schema=VALUES_SCHEMA), node_id)


DOWNLOAD_SPECS = [
    NodeSpec(id="world-steel-indicators", fn=fetch_indicators, kind="download"),
    NodeSpec(id="world-steel-values", fn=fetch_values, kind="download"),
    NodeSpec(id="world-steel-geoitems", fn=fetch_geoitems, kind="download"),
]
