"""Umweltbundesamt air-data downloads."""

from __future__ import annotations

from datetime import date
from typing import Any

import pyarrow as pa

from subsets_utils import NodeSpec, get, save_raw_parquet


BASE_URL = "https://luftdaten.umweltbundesamt.de/api/air-data/v4"
TIMEOUT = (10.0, 180.0)
START_YEAR = 2016


COMPONENTS_SCHEMA = pa.schema(
    [
        ("component_id", pa.int64()),
        ("component_code", pa.string()),
        ("component_symbol", pa.string()),
        ("component_unit", pa.string()),
        ("component_name", pa.string()),
    ]
)

SCOPES_SCHEMA = pa.schema(
    [
        ("scope_id", pa.int64()),
        ("scope_code", pa.string()),
        ("scope_time_base", pa.string()),
        ("scope_time_scope", pa.int64()),
        ("scope_time_is_max", pa.bool_()),
        ("scope_name", pa.string()),
    ]
)

NETWORKS_SCHEMA = pa.schema(
    [
        ("network_id", pa.int64()),
        ("network_code", pa.string()),
        ("network_name", pa.string()),
    ]
)

STATIONS_SCHEMA = pa.schema(
    [
        ("station_id", pa.int64()),
        ("station_code", pa.string()),
        ("station_name", pa.string()),
        ("station_city", pa.string()),
        ("station_synonym", pa.string()),
        ("station_active_from", pa.date32()),
        ("station_active_to", pa.date32()),
        ("station_longitude", pa.float64()),
        ("station_latitude", pa.float64()),
        ("network_id", pa.int64()),
        ("station_setting_id", pa.int64()),
        ("station_type_id", pa.int64()),
        ("network_code", pa.string()),
        ("network_name", pa.string()),
        ("station_setting_name", pa.string()),
        ("station_setting_short_name", pa.string()),
        ("station_type_name", pa.string()),
        ("station_street", pa.string()),
        ("station_street_nr", pa.string()),
        ("station_zip_code", pa.string()),
    ]
)

ANNUALBALANCES_SCHEMA = pa.schema(
    [
        ("component_id", pa.int64()),
        ("scope_id", pa.int64()),
        ("year", pa.int64()),
        ("station_id", pa.int64()),
        ("annual_mean", pa.float64()),
        ("exceedance_days", pa.int64()),
        ("extra_value", pa.float64()),
    ]
)

TRANSGRESSIONS_SCHEMA = pa.schema(
    [
        ("component_id", pa.int64()),
        ("year", pa.int64()),
        ("station_id", pa.int64()),
        ("day_first", pa.date32()),
        ("day_recent", pa.date32()),
        ("value_of_year", pa.int64()),
        ("month_01", pa.int64()),
        ("month_02", pa.int64()),
        ("month_03", pa.int64()),
        ("month_04", pa.int64()),
        ("month_05", pa.int64()),
        ("month_06", pa.int64()),
        ("month_07", pa.int64()),
        ("month_08", pa.int64()),
        ("month_09", pa.int64()),
        ("month_10", pa.int64()),
        ("month_11", pa.int64()),
        ("month_12", pa.int64()),
    ]
)


def _json(path: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
    resp = get(f"{BASE_URL}/{path}", params=params, headers={"Accept": "application/json"}, timeout=TIMEOUT)
    resp.raise_for_status()
    payload = resp.json()
    if not isinstance(payload, dict):
        raise AssertionError(f"{path}: expected JSON object, got {type(payload).__name__}")
    return payload


def _int(value: Any) -> int | None:
    if value in (None, ""):
        return None
    return int(value)


def _float(value: Any) -> float | None:
    if value in (None, ""):
        return None
    return float(value)


def _str(value: Any) -> str | None:
    if value is None:
        return None
    return str(value)


def _date(value: Any) -> date | None:
    if value in (None, ""):
        return None
    return date.fromisoformat(str(value)[:10])


def _records_from_indexed_map(payload: dict[str, Any], columns: list[str]) -> list[dict[str, Any]]:
    data = payload.get("data")
    if not isinstance(data, dict):
        raise AssertionError("expected object-valued `data` map")
    rows: list[dict[str, Any]] = []
    for values in data.values():
        rows.append(dict(zip(columns, values, strict=True)))
    return rows


def _component_ids() -> list[int]:
    rows = _records_from_indexed_map(
        _json("components/json", {"lang": "en"}),
        ["component_id", "component_code", "component_symbol", "component_unit", "component_name"],
    )
    return sorted(_int(row["component_id"]) for row in rows if _int(row["component_id"]) is not None)


def _annual_component_scope_pairs() -> list[tuple[int, int]]:
    payload = _json(
        "meta/json",
        {
            "use": "measure",
            "date_from": f"{date.today().year}-01-01",
            "date_to": date.today().isoformat(),
            "time_from": 1,
            "time_to": 24,
            "lang": "en",
        },
    )
    pairs: set[tuple[int, int]] = set()
    for row in payload.get("xref", []):
        if len(row) >= 4 and row[3] == "1":
            pairs.add((int(row[0]), int(row[1])))
    if not pairs:
        raise AssertionError("meta xref returned no annual balance component/scope pairs")
    return sorted(pairs)


def fetch_components(node_id: str) -> None:
    rows = _records_from_indexed_map(
        _json("components/json", {"lang": "en"}),
        ["component_id", "component_code", "component_symbol", "component_unit", "component_name"],
    )
    table = pa.Table.from_pylist(
        [
            {
                "component_id": _int(row["component_id"]),
                "component_code": _str(row["component_code"]),
                "component_symbol": _str(row["component_symbol"]),
                "component_unit": _str(row["component_unit"]),
                "component_name": _str(row["component_name"]),
            }
            for row in rows
        ],
        schema=COMPONENTS_SCHEMA,
    )
    save_raw_parquet(table, node_id)


def fetch_scopes(node_id: str) -> None:
    rows = _records_from_indexed_map(
        _json("scopes/json", {"lang": "en"}),
        ["scope_id", "scope_code", "scope_time_base", "scope_time_scope", "scope_time_is_max", "scope_name"],
    )
    table = pa.Table.from_pylist(
        [
            {
                "scope_id": _int(row["scope_id"]),
                "scope_code": _str(row["scope_code"]),
                "scope_time_base": _str(row["scope_time_base"]),
                "scope_time_scope": _int(row["scope_time_scope"]),
                "scope_time_is_max": bool(_int(row["scope_time_is_max"])),
                "scope_name": _str(row["scope_name"]),
            }
            for row in rows
        ],
        schema=SCOPES_SCHEMA,
    )
    save_raw_parquet(table, node_id)


def fetch_networks(node_id: str) -> None:
    rows = _records_from_indexed_map(
        _json("networks/json", {"lang": "en"}),
        ["network_id", "network_code", "network_name"],
    )
    table = pa.Table.from_pylist(
        [
            {
                "network_id": _int(row["network_id"]),
                "network_code": _str(row["network_code"]),
                "network_name": _str(row["network_name"]),
            }
            for row in rows
        ],
        schema=NETWORKS_SCHEMA,
    )
    save_raw_parquet(table, node_id)


def fetch_stations(node_id: str) -> None:
    rows = _records_from_indexed_map(
        _json("stations/json", {"lang": "en"}),
        [
            "station_id",
            "station_code",
            "station_name",
            "station_city",
            "station_synonym",
            "station_active_from",
            "station_active_to",
            "station_longitude",
            "station_latitude",
            "network_id",
            "station_setting_id",
            "station_type_id",
            "network_code",
            "network_name",
            "station_setting_name",
            "station_setting_short_name",
            "station_type_name",
            "station_street",
            "station_street_nr",
            "station_zip_code",
        ],
    )
    table = pa.Table.from_pylist(
        [
            {
                "station_id": _int(row["station_id"]),
                "station_code": _str(row["station_code"]),
                "station_name": _str(row["station_name"]),
                "station_city": _str(row["station_city"]),
                "station_synonym": _str(row["station_synonym"]),
                "station_active_from": _date(row["station_active_from"]),
                "station_active_to": _date(row["station_active_to"]),
                "station_longitude": _float(row["station_longitude"]),
                "station_latitude": _float(row["station_latitude"]),
                "network_id": _int(row["network_id"]),
                "station_setting_id": _int(row["station_setting_id"]),
                "station_type_id": _int(row["station_type_id"]),
                "network_code": _str(row["network_code"]),
                "network_name": _str(row["network_name"]),
                "station_setting_name": _str(row["station_setting_name"]),
                "station_setting_short_name": _str(row["station_setting_short_name"]),
                "station_type_name": _str(row["station_type_name"]),
                "station_street": _str(row["station_street"]),
                "station_street_nr": _str(row["station_street_nr"]),
                "station_zip_code": _str(row["station_zip_code"]),
            }
            for row in rows
        ],
        schema=STATIONS_SCHEMA,
    )
    save_raw_parquet(table, node_id)


def fetch_annualbalances(node_id: str) -> None:
    rows: list[dict[str, Any]] = []
    for component_id, scope_id in _annual_component_scope_pairs():
        for year in range(START_YEAR, date.today().year + 1):
            payload = _json(
                "annualbalances/json",
                {"component": component_id, "scope": scope_id, "year": year, "lang": "en"},
            )
            for values in payload.get("data") or []:
                padded = list(values) + [None, None, None]
                rows.append(
                    {
                        "component_id": component_id,
                        "scope_id": scope_id,
                        "year": year,
                        "station_id": _int(padded[0]),
                        "annual_mean": _float(padded[1]),
                        "exceedance_days": _int(padded[2]),
                        "extra_value": _float(padded[3]),
                    }
                )
    if len(rows) < 10_000:
        raise AssertionError(f"{node_id}: expected at least 10000 annual balance rows, got {len(rows)}")
    save_raw_parquet(pa.Table.from_pylist(rows, schema=ANNUALBALANCES_SCHEMA), node_id)


def fetch_transgressions(node_id: str) -> None:
    rows: list[dict[str, Any]] = []
    for component_id in _component_ids():
        for year in range(START_YEAR, date.today().year + 1):
            payload = _json("transgressions/json", {"component": component_id, "year": year, "lang": "en"})
            for values in payload.get("data") or []:
                padded = list(values) + [None] * 16
                record = {
                    "component_id": component_id,
                    "year": year,
                    "station_id": _int(padded[0]),
                    "day_first": _date(padded[1]),
                    "day_recent": _date(padded[2]),
                    "value_of_year": _int(padded[3]),
                }
                for month in range(1, 13):
                    record[f"month_{month:02d}"] = _int(padded[3 + month])
                rows.append(record)
    if len(rows) < 1_000:
        raise AssertionError(f"{node_id}: expected at least 1000 transgression rows, got {len(rows)}")
    save_raw_parquet(pa.Table.from_pylist(rows, schema=TRANSGRESSIONS_SCHEMA), node_id)


DOWNLOAD_SPECS = [
    NodeSpec(id="umweltbundesamt-annualbalances", fn=fetch_annualbalances, kind="download"),
    NodeSpec(id="umweltbundesamt-components", fn=fetch_components, kind="download"),
    NodeSpec(id="umweltbundesamt-networks", fn=fetch_networks, kind="download"),
    NodeSpec(id="umweltbundesamt-scopes", fn=fetch_scopes, kind="download"),
    NodeSpec(id="umweltbundesamt-stations", fn=fetch_stations, kind="download"),
    NodeSpec(id="umweltbundesamt-transgressions", fn=fetch_transgressions, kind="download"),
]
