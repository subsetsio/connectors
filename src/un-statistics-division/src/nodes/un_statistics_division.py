"""UN Statistics Division connector downloads.

Two access surfaces, one node module:

1. SDG Global Database (flagship) via the SDG REST API. Stateless full re-pull:
   one observations table built by walking every series in Series/List and
   paging Series/Data, plus four small reference taxonomies from the SDG list
   endpoints. Raw -> parquet. The API exposes no modified-since filter, and a
   stored watermark would silently skip the SDG database's frequent
   back-revisions, so every refresh re-pulls the full corpus.

2. Three UNSD SDMX 2.1 dataflows on data.un.org. One parametric fetcher: each
   dataflow is fetched whole as SDMX-CSV (Accept: application/vnd.sdmx.data+csv)
   and saved verbatim as a csv. The two energy flows are large; downloaded in
   one shot. No modified-since delta filter exists, so every refresh re-pulls
   the full flow.
"""
import json

import pyarrow as pa

from subsets_utils import (
    NodeSpec,
    get,
    raw_parquet_writer,
    save_raw_file,
    save_raw_parquet,
)

# --------------------------------------------------------------------------- #
# SDG Global Database (sdg_data)
# --------------------------------------------------------------------------- #
SDG_BASE = "https://unstats.un.org/SDGAPI/v1/sdg"

SDG_SCHEMA = pa.schema([
    ("series", pa.string()),
    ("series_description", pa.string()),
    ("goal", pa.string()),
    ("target", pa.string()),
    ("indicator", pa.string()),
    ("geo_area_code", pa.string()),
    ("geo_area_name", pa.string()),
    ("time_period", pa.int32()),
    ("value", pa.string()),       # raw; transform TRY_CASTs to DOUBLE
    ("value_type", pa.string()),
    ("source", pa.string()),
])

SDG_GOALS_SCHEMA = pa.schema([
    ("code", pa.string()),
    ("title", pa.string()),
    ("description", pa.string()),
    ("uri", pa.string()),
])

SDG_TARGETS_SCHEMA = pa.schema([
    ("goal", pa.string()),
    ("code", pa.string()),
    ("title", pa.string()),
    ("description", pa.string()),
    ("uri", pa.string()),
    ("indicators", pa.string()),
])

SDG_INDICATORS_SCHEMA = pa.schema([
    ("goal", pa.string()),
    ("target", pa.string()),
    ("code", pa.string()),
    ("description", pa.string()),
    ("tier", pa.string()),
    ("uri", pa.string()),
    ("series", pa.string()),
])

SDG_SERIES_SCHEMA = pa.schema([
    ("goal", pa.string()),
    ("target", pa.string()),
    ("indicator", pa.string()),
    ("release", pa.string()),
    ("code", pa.string()),
    ("description", pa.string()),
    ("uri", pa.string()),
])


def _get_json(url, params=None):
    resp = get(url, params=params, headers={"Accept": "application/json"}, timeout=(10.0, 180.0))
    resp.raise_for_status()
    return resp.json()


def _first(v):
    """SDG goal/target/indicator come back as lists; join distinct values."""
    if isinstance(v, list):
        return ";".join(str(x) for x in v) if v else None
    return str(v) if v is not None else None


def _to_int_year(v):
    if v is None or v == "":
        return None
    try:
        return int(float(v))
    except (TypeError, ValueError):
        return None


def _rows_to_table(rows):
    return pa.table({
        "series": [r.get("series") for r in rows],
        "series_description": [r.get("seriesDescription") for r in rows],
        "goal": [_first(r.get("goal")) for r in rows],
        "target": [_first(r.get("target")) for r in rows],
        "indicator": [_first(r.get("indicator")) for r in rows],
        "geo_area_code": [str(r["geoAreaCode"]) if r.get("geoAreaCode") is not None else None for r in rows],
        "geo_area_name": [r.get("geoAreaName") for r in rows],
        "time_period": [_to_int_year(r.get("timePeriodStart")) for r in rows],
        "value": [str(r["value"]) if r.get("value") is not None else None for r in rows],
        "value_type": [r.get("valueType") for r in rows],
        "source": [r.get("source") for r in rows],
    }, schema=SDG_SCHEMA)


def _json_or_none(value):
    if value is None:
        return None
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def _taxonomy_table(rows, schema, columns):
    return pa.table({col: [row.get(col) for row in rows] for col in columns}, schema=schema)


def fetch_sdg(node_id: str) -> None:
    """Walk every SDG series and stream all observations to one parquet asset."""
    asset = node_id
    series = _get_json(f"{SDG_BASE}/Series/List")
    codes = [s["code"] for s in series if s.get("code")]
    if not codes:
        raise AssertionError("SDG Series/List returned no series codes")

    written = 0
    with raw_parquet_writer(asset, SDG_SCHEMA) as w:
        for code in codes:
            page = 1
            total_pages = 1
            while page <= total_pages:
                d = _get_json(f"{SDG_BASE}/Series/Data",
                              params={"seriesCode": code, "pageSize": 10000, "page": page})
                total_pages = d.get("totalPages") or 0
                rows = d.get("data") or []
                if rows:
                    w.write_table(_rows_to_table(rows))
                    written += len(rows)
                if total_pages <= page:
                    break
                page += 1
    if written == 0:
        raise AssertionError(f"{asset}: fetched 0 SDG observations across {len(codes)} series")


def fetch_sdg_goals(node_id: str) -> None:
    rows = _get_json(f"{SDG_BASE}/Goal/List")
    if len(rows) < 17:
        raise AssertionError(f"{node_id}: expected at least 17 SDG goals, got {len(rows)}")
    save_raw_parquet(_taxonomy_table(rows, SDG_GOALS_SCHEMA, ("code", "title", "description", "uri")), node_id)


def fetch_sdg_targets(node_id: str) -> None:
    rows = _get_json(f"{SDG_BASE}/Target/List")
    if len(rows) < 169:
        raise AssertionError(f"{node_id}: expected at least 169 SDG targets, got {len(rows)}")
    prepared = [{**row, "indicators": _json_or_none(row.get("indicators"))} for row in rows]
    save_raw_parquet(
        _taxonomy_table(prepared, SDG_TARGETS_SCHEMA, ("goal", "code", "title", "description", "uri", "indicators")),
        node_id,
    )


def fetch_sdg_indicators(node_id: str) -> None:
    rows = _get_json(f"{SDG_BASE}/Indicator/List")
    if len(rows) < 200:
        raise AssertionError(f"{node_id}: expected hundreds of SDG indicators, got {len(rows)}")
    prepared = [{**row, "series": _json_or_none(row.get("series"))} for row in rows]
    save_raw_parquet(
        _taxonomy_table(
            prepared,
            SDG_INDICATORS_SCHEMA,
            ("goal", "target", "code", "description", "tier", "uri", "series"),
        ),
        node_id,
    )


def fetch_sdg_series(node_id: str) -> None:
    rows = _get_json(f"{SDG_BASE}/Series/List")
    if len(rows) < 500:
        raise AssertionError(f"{node_id}: expected hundreds of SDG series, got {len(rows)}")
    prepared = [
        {
            **row,
            "goal": _first(row.get("goal")),
            "target": _first(row.get("target")),
            "indicator": _first(row.get("indicator")),
        }
        for row in rows
    ]
    save_raw_parquet(
        _taxonomy_table(
            prepared,
            SDG_SERIES_SCHEMA,
            ("goal", "target", "indicator", "release", "code", "description", "uri"),
        ),
        node_id,
    )


# --------------------------------------------------------------------------- #
# UNSD SDMX 2.1 dataflows
# --------------------------------------------------------------------------- #
SDMX_BASE = "https://data.un.org/WS/rest/data/UNSD"
SDMX_CSV = "application/vnd.sdmx.data+csv;version=1.0.0"

# Case-sensitive SDMX dataflow ids (the API rejects a wrong case). Keyed by the
# lowered node-id suffix so fetch_sdmx can recover the real id from its node id.
SDMX_FLOWS = {
    "df-undata-countrydata": "DF_UNDATA_COUNTRYDATA",
    "df-undata-energy": "DF_UNDATA_ENERGY",
    "df-undata-energybalance": "DF_UNData_EnergyBalance",
}


def _get_text(url, headers=None):
    resp = get(url, headers=headers, timeout=(10.0, 600.0))
    resp.raise_for_status()
    return resp.text


def fetch_sdmx(node_id: str) -> None:
    """Fetch one UNSD SDMX dataflow whole as SDMX-CSV; save the csv verbatim."""
    asset = node_id
    suffix = node_id[len("un-statistics-division-"):]
    flow = SDMX_FLOWS.get(suffix)
    if flow is None:
        raise AssertionError(f"{asset}: no SDMX dataflow mapped for suffix '{suffix}'")
    text = _get_text(f"{SDMX_BASE},{flow}/", headers={"Accept": SDMX_CSV})
    if text.count("\n") < 2:
        raise AssertionError(f"{asset}: SDMX-CSV for {flow} has no data rows")
    save_raw_file(text, asset, extension="csv")


# --------------------------------------------------------------------------- #
# DOWNLOAD_SPECS — one per entity-union entry
# --------------------------------------------------------------------------- #
DOWNLOAD_SPECS = [
    NodeSpec(id="un-statistics-division-sdg-data", fn=fetch_sdg, kind="download"),
    NodeSpec(id="un-statistics-division-sdg-goals", fn=fetch_sdg_goals, kind="download"),
    NodeSpec(id="un-statistics-division-sdg-targets", fn=fetch_sdg_targets, kind="download"),
    NodeSpec(id="un-statistics-division-sdg-indicators", fn=fetch_sdg_indicators, kind="download"),
    NodeSpec(id="un-statistics-division-sdg-series", fn=fetch_sdg_series, kind="download"),
    NodeSpec(id="un-statistics-division-df-undata-countrydata", fn=fetch_sdmx, kind="download"),
    NodeSpec(id="un-statistics-division-df-undata-energy", fn=fetch_sdmx, kind="download"),
    NodeSpec(id="un-statistics-division-df-undata-energybalance", fn=fetch_sdmx, kind="download"),
]
