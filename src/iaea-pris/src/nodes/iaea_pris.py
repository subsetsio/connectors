"""IAEA PRIS — Power Reactor Information System connector.

PRIS migrated its legacy ASP.NET reactor detail pages to the public
pris-stats.iaea.org application. Reactor metadata is available from JSON
endpoints in that app; annual performance rows are served from the embedded
PowerBI model behind the PRIS data browser.

We keep the original published raw schemas stable:

  * iaea-pris-reactors      — one row per reactor (specifications)
  * iaea-pris-performance   — one row per (reactor, year) (annual time series)
"""

from __future__ import annotations

import json
from datetime import datetime

import pyarrow as pa

from subsets_utils import get, post, save_raw_parquet, transient_retry

API_BASE = "https://pris-stats.iaea.org"
POWERBI_CLUSTER = "https://wabi-north-europe-j-primary-redirect.analysis.windows.net"
DATA_BROWSER_ELECTRICITY_REPORT_ID = "12749967-8d91-46cd-a792-093b776499c2"
ANNUAL_ENTITY = "Fact_ReactorAnnualProduction"
ANNUAL_FIELDS = [
    "ReactorId",
    "Year",
    "Energy",
    "NetElecCapacity",
    "HoursOnline",
    "OperatingFactor",
    "AvailFactor",
    "LoadFactor",
]


@transient_retry()
def _get_json(url: str, **kwargs):
    resp = get(url, timeout=(15.0, 120.0), **kwargs)
    resp.raise_for_status()
    return resp.json()


@transient_retry()
def _post_json(url: str, **kwargs):
    resp = post(url, timeout=(15.0, 120.0), **kwargs)
    resp.raise_for_status()
    return resp.json()


def _api_json(path: str):
    return _get_json(f"{API_BASE}{path}")


def _items(payload) -> list[dict]:
    if isinstance(payload, dict):
        items = payload.get("items", [])
        if isinstance(items, list):
            return items
    raise RuntimeError("unexpected PRIS API payload shape")


def _as_float(value):
    if value in (None, "", "NC"):
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _as_int(value):
    if value in (None, ""):
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def _iso_date(value):
    if not value:
        return None
    if isinstance(value, str):
        text = value.strip()
        if not text:
            return None
        if text.startswith("/Date("):
            try:
                millis = int(text.removeprefix("/Date(").split(")")[0])
                return datetime.utcfromtimestamp(millis / 1000).date().isoformat()
            except (ValueError, OSError):
                return None
        return text[:10]
    return None


def _all_reactor_records() -> list[dict]:
    countries = _items(_api_json("/country/countries/"))
    by_id: dict[int, dict] = {}
    for country in countries:
        code = country.get("countryCode")
        if not code:
            continue
        for record in _items(_api_json(f"/reactor/reactors-by-code/{code}")):
            rid = _as_int(record.get("id"))
            if rid is not None:
                by_id[rid] = record

    if not by_id:
        raise RuntimeError("PRIS reactor API returned no reactor records")

    detailed: list[dict] = []
    for rid in sorted(by_id):
        detail = _api_json(f"/reactor/reactor-by-id/{rid}")
        if isinstance(detail, dict):
            merged = dict(by_id[rid])
            merged.update(detail)
            detailed.append(merged)
        else:
            detailed.append(by_id[rid])
    return detailed


def _reactor_row(record: dict) -> dict:
    lifetime = record.get("lifetimeFactor") if isinstance(record.get("lifetimeFactor"), dict) else {}
    return {
        "reactor_id": _as_int(record.get("id")),
        "name": record.get("unitName"),
        "alternate_name": record.get("alternateName"),
        "country": record.get("countryName"),
        "country_code": record.get("countryCode"),
        "status": record.get("statusName"),
        "reactor_type": record.get("typeCode") or record.get("typeName"),
        "model": record.get("model"),
        "reference_unit_power_mwe": _as_float(record.get("netElectricalCapacity")),
        "design_net_capacity_mwe": _as_float(record.get("designNetElectricalCapacity")),
        "gross_capacity_mwe": _as_float(record.get("grossElectricalCapacity")),
        "thermal_capacity_mwt": _as_float(record.get("thermalPower")),
        "construction_start_date": _iso_date(record.get("constructionDate")),
        "first_criticality_date": _iso_date(record.get("criticalityDate")),
        "first_grid_connection_date": _iso_date(record.get("gridDate")),
        "commercial_operation_date": _iso_date(record.get("commercialDate")),
        "long_term_shutdown_date": _iso_date(record.get("latestSuspendedOperationsDate")),
        "permanent_shutdown_date": _iso_date(record.get("shutdownDate")),
        "lifetime_electricity_supplied_twh": _as_float(lifetime.get("lifetimeGeneration")),
        "lifetime_operation_factor_pct": _as_float(lifetime.get("operatingFactor")),
        "lifetime_energy_availability_factor_pct": _as_float(lifetime.get("availabilityFactor")),
        "lifetime_load_factor_pct": _as_float(lifetime.get("loadFactor")),
    }


def _powerbi_context(report_id: str) -> dict:
    raw = _api_json(f"/databrowser/report-by-id/{report_id}")
    embed = json.loads(raw) if isinstance(raw, str) else raw
    token = embed["EmbedToken"]["Token"]
    headers = {
        "Authorization": f"EmbedToken {token}",
        "Origin": "https://app.powerbi.com",
        "Referer": "https://app.powerbi.com/",
        "x-powerbi-hostenv": "Embed for Customers",
    }
    exploration = _get_json(
        f"{POWERBI_CLUSTER}/explore/reports/{report_id}/modelsAndExploration"
        "?preferReadOnlySession=true&skipQueryData=true",
        headers=headers,
    )
    return {
        "model_id": exploration["models"][0]["id"],
        "capacity_uri": exploration["exploration"]["capacityUri"].rstrip("/"),
        "mwc_token": exploration["exploration"]["mwcToken"],
    }


def _qes_query(entity: str, fields: list[str], top_count: int) -> dict:
    ctx = _powerbi_context(DATA_BROWSER_ELECTRICITY_REPORT_ID)
    select = [
        {
            "Column": {
                "Expression": {"SourceRef": {"Source": "f"}},
                "Property": field,
            },
            "Name": f"{entity}.{field}",
            "NativeReferenceName": field,
        }
        for field in fields
    ]
    body = {
        "version": "1.0.0",
        "queries": [
            {
                "Query": {
                    "Commands": [
                        {
                            "SemanticQueryDataShapeCommand": {
                                "Query": {
                                    "Version": 2,
                                    "From": [{"Name": "f", "Entity": entity, "Type": 0}],
                                    "Select": select,
                                },
                                "Binding": {
                                    "Primary": {
                                        "Groupings": [{"Projections": list(range(len(fields)))}]
                                    },
                                    "DataReduction": {
                                        "DataVolume": 3,
                                        "Primary": {"Top": {"Count": top_count}},
                                    },
                                },
                                "ExecutionMetricsKind": 1,
                            }
                        }
                    ]
                },
                "CacheKey": f"subsets-{entity}",
                "QueryId": "",
            }
        ],
        "cancelQueries": [],
        "modelId": ctx["model_id"],
        "userPreferredLocale": "en-US",
        "allowLongRunningQueries": True,
    }
    headers = {
        "Authorization": f"MWCToken {ctx['mwc_token']}",
        "Origin": "https://app.powerbi.com",
        "Referer": "https://app.powerbi.com/",
        "x-powerbi-hostenv": "Embed for Customers",
    }
    return _post_json(f"{ctx['capacity_uri']}/query", headers=headers, json=body)


def _dsr_rows(payload: dict) -> list[list]:
    try:
        encoded = payload["results"][0]["result"]["data"]["dsr"]["DS"][0]["PH"][0]["DM0"]
    except (KeyError, IndexError, TypeError) as exc:
        raise RuntimeError("unexpected PowerBI QES payload shape") from exc

    decoded: list[list] = []
    previous = [None] * len(ANNUAL_FIELDS)
    for row in encoded:
        values = row.get("C", [])
        repeated = row.get("R", 0)
        out = []
        value_index = 0
        for idx in range(len(ANNUAL_FIELDS)):
            if repeated & (1 << idx):
                out.append(previous[idx])
            else:
                value = values[value_index] if value_index < len(values) else None
                out.append(value)
                value_index += 1
        previous = out
        decoded.append(out)
    return decoded


def _performance_rows() -> list[dict]:
    payload = _qes_query(ANNUAL_ENTITY, ANNUAL_FIELDS, top_count=50000)
    rows = []
    for values in _dsr_rows(payload):
        rid = _as_int(values[0])
        year = _as_int(values[1])
        if rid is None or year is None:
            continue
        rows.append({
            "reactor_id": rid,
            "year": year,
            "electricity_supplied_gwh": _as_float(values[2]),
            "reference_unit_power_mw": _as_float(values[3]),
            "annual_time_on_line_h": _as_float(values[4]),
            "operation_factor_pct": _as_float(values[5]),
            "energy_availability_factor_pct": _as_float(values[6]),
            "load_factor_pct": _as_float(values[7]),
        })
    if not rows:
        raise RuntimeError("PowerBI annual production query returned no rows")
    return rows


# ---------------------------------------------------------------------------
# Schemas
# ---------------------------------------------------------------------------

REACTORS_SCHEMA = pa.schema([
    ("reactor_id", pa.int64()),
    ("name", pa.string()),
    ("alternate_name", pa.string()),
    ("country", pa.string()),
    ("country_code", pa.string()),
    ("status", pa.string()),
    ("reactor_type", pa.string()),
    ("model", pa.string()),
    ("reference_unit_power_mwe", pa.float64()),
    ("design_net_capacity_mwe", pa.float64()),
    ("gross_capacity_mwe", pa.float64()),
    ("thermal_capacity_mwt", pa.float64()),
    ("construction_start_date", pa.string()),
    ("first_criticality_date", pa.string()),
    ("first_grid_connection_date", pa.string()),
    ("commercial_operation_date", pa.string()),
    ("long_term_shutdown_date", pa.string()),
    ("permanent_shutdown_date", pa.string()),
    ("lifetime_electricity_supplied_twh", pa.float64()),
    ("lifetime_operation_factor_pct", pa.float64()),
    ("lifetime_energy_availability_factor_pct", pa.float64()),
    ("lifetime_load_factor_pct", pa.float64()),
])

PERFORMANCE_SCHEMA = pa.schema([
    ("reactor_id", pa.int64()),
    ("year", pa.int64()),
    ("electricity_supplied_gwh", pa.float64()),
    ("reference_unit_power_mw", pa.float64()),
    ("annual_time_on_line_h", pa.float64()),
    ("operation_factor_pct", pa.float64()),
    ("energy_availability_factor_pct", pa.float64()),
    ("load_factor_pct", pa.float64()),
])


# ---------------------------------------------------------------------------
# Download fns
# ---------------------------------------------------------------------------

def fetch_reactors(node_id: str) -> None:
    rows = [_reactor_row(record) for record in _all_reactor_records()]
    table = pa.Table.from_pylist(rows, schema=REACTORS_SCHEMA)
    save_raw_parquet(table, node_id)


def fetch_performance(node_id: str) -> None:
    table = pa.Table.from_pylist(_performance_rows(), schema=PERFORMANCE_SCHEMA)
    save_raw_parquet(table, node_id)


# ---------------------------------------------------------------------------
# Specs
# ---------------------------------------------------------------------------

from subsets_utils import NodeSpec  # noqa: E402

DOWNLOAD_SPECS = [
    NodeSpec(id="iaea-pris-reactors", fn=fetch_reactors, kind="download"),
    NodeSpec(id="iaea-pris-performance", fn=fetch_performance, kind="download"),
]
