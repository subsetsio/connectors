"""UN Statistics Division connector — fetches + transforms.

Two access surfaces, one node module:

1. SDG Global Database (flagship) via the SDG REST API. Stateless full re-pull:
   one observations table built by walking every series in Series/List and
   paging Series/Data. Raw -> streamed parquet. The API exposes no
   modified-since filter, and a stored watermark would silently skip the SDG
   database's frequent back-revisions, so every refresh re-pulls the full corpus.

2. Four UNSD SDMX 2.1 dataflows on data.un.org. One parametric fetcher: each
   dataflow is fetched whole as SDMX-CSV (Accept: application/vnd.sdmx.data+csv)
   and saved verbatim as a csv read directly by the transform. The two energy
   flows are ~84-136MB; downloaded in one shot. No modified-since delta filter
   exists, so every refresh re-pulls the full flow.
"""
import pyarrow as pa

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    raw_parquet_writer,
    save_raw_file,
    transient_retry,
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


@transient_retry()
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
    "df-undata-unfcc": "DF_UNData_UNFCC",
}


@transient_retry()
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
    NodeSpec(id="un-statistics-division-df-undata-countrydata", fn=fetch_sdmx, kind="download"),
    NodeSpec(id="un-statistics-division-df-undata-energy", fn=fetch_sdmx, kind="download"),
    NodeSpec(id="un-statistics-division-df-undata-energybalance", fn=fetch_sdmx, kind="download"),
    NodeSpec(id="un-statistics-division-df-undata-unfcc", fn=fetch_sdmx, kind="download"),
]


# SDMX flows share the same generic shape: keep every dimension column, type the
# observation value, drop rows with no numeric value. DATAFLOW is redundant.
def _sdmx_transform(download_id: str) -> SqlNodeSpec:
    return SqlNodeSpec(
        id=f"{download_id}-transform",
        deps=[download_id],
        sql=f'''
            SELECT * EXCLUDE (OBS_VALUE, DATAFLOW),
                   TRY_CAST(OBS_VALUE AS DOUBLE) AS obs_value
            FROM "{download_id}"
            WHERE TRY_CAST(OBS_VALUE AS DOUBLE) IS NOT NULL
        ''',
    )


TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="un-statistics-division-sdg-data-transform",
        deps=["un-statistics-division-sdg-data"],
        sql='''
            SELECT
                series,
                series_description,
                goal,
                target,
                indicator,
                geo_area_code,
                geo_area_name,
                time_period AS year,
                TRY_CAST(value AS DOUBLE) AS value,
                value_type,
                source
            FROM "un-statistics-division-sdg-data"
            WHERE TRY_CAST(value AS DOUBLE) IS NOT NULL
              AND time_period IS NOT NULL
        ''',
    ),
    _sdmx_transform("un-statistics-division-df-undata-countrydata"),
    _sdmx_transform("un-statistics-division-df-undata-energy"),
    _sdmx_transform("un-statistics-division-df-undata-energybalance"),
    _sdmx_transform("un-statistics-division-df-undata-unfcc"),
]
