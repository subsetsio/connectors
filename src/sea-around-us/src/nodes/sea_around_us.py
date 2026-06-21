"""Sea Around Us — global marine fisheries catch reconstruction.

Mechanism: REST (rest_v1) at https://api.seaaroundus.org/api/v1/ — no auth.

Shape: stateless full re-pull. The source publishes discrete, versioned catch
reconstructions (not a continuously-updated feed) and exposes no incremental
`since`/cursor filter, so each refresh re-fetches the whole corpus and the
transform overwrites the published table. The corpus is a few thousand small
JSON time series, comfortably re-pullable per run.

Publishable units (15): 14 catch tables, one per (measure, dimension), each a
long-format annual time series (1950-present) spanning every spatial region
type as a `region_type` column; plus the `taxa` reference taxonomy.

Catch endpoint: /{region_type}/{measure}/{dimension}/?region_id={id} returns
{"data": [{"key", "values": [[year, amount], ...], "scientific_name"?,
"entity_id"?}]}. We iterate every region of every spatial region type and
flatten the (year, amount) pairs into rows. The taxon dimension carries
scientific_name + entity_id (taxon_key); other dimensions carry only `key`.

Region enumeration: the /{type}/ list endpoints return GeoJSON
FeatureCollections; we read region_id + title from feature.properties and
discard geometry. eez (~282), lme (66), rfmo (18) enumerate cleanly. The
/global/ list endpoint 500s, but global catch queries work, so global is a
single synthetic region. /high-seas/ lists empty and /fishing-entity/ is not a
valid catch region_type (404), so neither is included.
"""

import httpx
import pyarrow as pa

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    transient_retry,
    save_raw_parquet,
    raw_parquet_writer,
)

BASE = "https://api.seaaroundus.org/api/v1"

# Spatial region types whose list endpoints enumerate regions for catch queries.
SPATIAL_REGION_TYPES = ["eez", "lme", "rfmo"]
# /global/ listing is broken (500) but catch works; treat global as one region.
GLOBAL_REGION = ("global", 1, "Global")

MEASURES = ("tonnage", "value")

# Dimension path segment -> published breakdown column name (insertion order is
# the entity order used to build DOWNLOAD_SPECS, matching the entity union).
DIM_COL = {
    "taxon": "taxon",
    "commercialgroup": "commercial_group",
    "functionalgroup": "functional_group",
    "country": "fishing_country",
    "sector": "sector",
    "catchtype": "catch_type",
    "reporting-status": "reporting_status",
}

MEASURE_COL = {"tonnage": "catch_tonnes", "value": "landed_value_usd"}

CATCH_SCHEMA = pa.schema([
    ("region_type", pa.string()),
    ("region_id", pa.int64()),
    ("region_name", pa.string()),
    ("category", pa.string()),
    ("scientific_name", pa.string()),
    ("entity_id", pa.string()),
    ("year", pa.int64()),
    ("value", pa.float64()),
])

TAXA_SCHEMA = pa.schema([
    ("taxon_key", pa.int64()),
    ("scientific_name", pa.string()),
    ("common_name", pa.string()),
    ("functional_group", pa.int64()),
    ("commercial_group", pa.int64()),
    ("is_taxon_distribution_backfilled", pa.bool_()),
])

CATCH_PREFIX = "sea-around-us-catch-"


# ---------------------------------------------------------------------------
# HTTP
# ---------------------------------------------------------------------------

@transient_retry()
def _get_json(url, params=None):
    resp = get(url, params=params, timeout=(10.0, 180.0))
    resp.raise_for_status()
    return resp.json()


def _list_regions(region_type):
    """(region_id, title) for a spatial region type from its GeoJSON list
    endpoint; reads feature.properties only (geometry discarded)."""
    payload = _get_json(f"{BASE}/{region_type}/")
    data = payload.get("data", {})
    features = data.get("features", []) if isinstance(data, dict) else []
    out = []
    for feat in features:
        props = (feat or {}).get("properties") or {}
        rid = props.get("region_id")
        if rid is None:
            continue
        out.append((int(rid), props.get("title") or str(rid)))
    if not out:
        raise AssertionError(f"{region_type}: region list endpoint returned 0 regions")
    return out


def _fetch_series(region_type, measure, dimension, region_id):
    """Catch series for one region/measure/dimension. A 4xx (other than 429)
    means this region has no slice here — return [] rather than failing the
    whole spec. Transient errors are retried inside _get_json and propagate."""
    url = f"{BASE}/{region_type}/{measure}/{dimension}/"
    try:
        payload = _get_json(url, params={"region_id": region_id})
    except httpx.HTTPStatusError as exc:
        code = exc.response.status_code
        if code != 429 and 400 <= code < 500:
            return []
        raise
    data = payload.get("data", [])
    return data if isinstance(data, list) else []


# ---------------------------------------------------------------------------
# Fetch fns
# ---------------------------------------------------------------------------

def _parse_catch_id(node_id):
    """sea-around-us-catch-{measure}-by-{dimension} -> (measure, dimension)."""
    body = node_id[len(CATCH_PREFIX):]
    measure, dimension = body.split("-by-", 1)
    if measure not in MEASURES or dimension not in DIM_COL:
        raise AssertionError(f"unrecognized catch spec id: {node_id}")
    return measure, dimension


def fetch_catch(node_id):
    """One catch table = (measure, dimension) across all spatial regions.

    Streamed per-region to bound memory: the taxon tables reach millions of
    rows (hundreds of taxa x ~367 regions x ~70 years)."""
    asset = node_id
    measure, dimension = _parse_catch_id(node_id)

    regions = [
        (rt, rid, name)
        for rt in SPATIAL_REGION_TYPES
        for rid, name in _list_regions(rt)
    ]
    regions.append(GLOBAL_REGION)

    wrote_any = False
    with raw_parquet_writer(asset, CATCH_SCHEMA) as writer:
        for rt, rid, rname in regions:
            series = _fetch_series(rt, measure, dimension, rid)
            rows = []
            for s in series:
                key = s.get("key")
                sci = s.get("scientific_name")
                eid = s.get("entity_id")
                for pair in (s.get("values") or []):
                    if not pair or len(pair) < 2:
                        continue
                    year, amount = pair[0], pair[1]
                    if year is None or amount is None:
                        continue
                    rows.append({
                        "region_type": rt,
                        "region_id": rid,
                        "region_name": rname,
                        "category": key,
                        "scientific_name": sci,
                        "entity_id": str(eid) if eid is not None else None,
                        "year": int(year),
                        "value": float(amount),
                    })
            if rows:
                writer.write_table(pa.Table.from_pylist(rows, schema=CATCH_SCHEMA))
                wrote_any = True

    if not wrote_any:
        raise AssertionError(f"{asset}: no catch rows across {len(regions)} regions")


def _to_int(v):
    return int(v) if v is not None else None


def fetch_taxa(node_id):
    """Reference taxonomy of all fished taxa."""
    asset = node_id
    payload = _get_json(f"{BASE}/taxa/")
    data = payload.get("data", [])
    rows = []
    for t in data:
        rows.append({
            "taxon_key": int(t["taxon_key"]),
            "scientific_name": t.get("scientific_name"),
            "common_name": t.get("common_name"),
            "functional_group": _to_int(t.get("functional_group")),
            "commercial_group": _to_int(t.get("commercial_group")),
            "is_taxon_distribution_backfilled": t.get("is_taxon_distribution_backfilled"),
        })
    if not rows:
        raise AssertionError("taxa: endpoint returned 0 records")
    save_raw_parquet(pa.Table.from_pylist(rows, schema=TAXA_SCHEMA), asset)


# ---------------------------------------------------------------------------
# Specs
# ---------------------------------------------------------------------------

_CATCH_ENTITIES = [f"catch-{m}-by-{d}" for m in MEASURES for d in DIM_COL]

DOWNLOAD_SPECS = [
    NodeSpec(id=f"sea-around-us-{e}", fn=fetch_catch, kind="download")
    for e in _CATCH_ENTITIES
] + [
    NodeSpec(id="sea-around-us-taxa", fn=fetch_taxa, kind="download"),
]


def _catch_transform_sql(download_id, measure, dimension):
    dim_col = DIM_COL[dimension]
    meas_col = MEASURE_COL[measure]
    taxon_cols = ""
    if dimension == "taxon":
        taxon_cols = (
            "TRY_CAST(entity_id AS BIGINT) AS taxon_key,\n"
            "            scientific_name,\n            "
        )
    return f'''
        SELECT
            region_type,
            region_id,
            region_name,
            year,
            {taxon_cols}category AS {dim_col},
            value AS {meas_col}
        FROM "{download_id}"
        WHERE value IS NOT NULL AND category IS NOT NULL
    '''


TRANSFORM_SPECS = []
for _e in _CATCH_ENTITIES:
    _did = f"sea-around-us-{_e}"
    _m, _d = _parse_catch_id(_did)
    TRANSFORM_SPECS.append(
        SqlNodeSpec(id=f"{_did}-transform", deps=[_did], sql=_catch_transform_sql(_did, _m, _d))
    )

TRANSFORM_SPECS.append(
    SqlNodeSpec(
        id="sea-around-us-taxa-transform",
        deps=["sea-around-us-taxa"],
        sql='''
            SELECT
                taxon_key,
                scientific_name,
                common_name,
                functional_group,
                commercial_group,
                is_taxon_distribution_backfilled
            FROM "sea-around-us-taxa"
            WHERE taxon_key IS NOT NULL
        ''',
    )
)
