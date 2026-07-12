"""OBIS connector — statistical / catalog subsets from the OBIS v3 REST API.

Mechanism: rest_v3 (https://api.obis.org/v3/) — no auth, no documented or
observed rate limit. Every subset is small enough for a stateless full re-pull
each run (no watermarks, no cursors): the largest is the species checklist
(~197k rows). All endpoints return the whole result set in one shot or via a
simple `skip` offset.

The raw ~200M-record occurrence corpus is intentionally NOT published here — it
is a ~50GB GeoParquet bulk archive (s3://obis-open-data) that does not fit a
single-table REST publish; rank holds it below threshold pending dedicated bulk
infrastructure. What ships here is the aggregated / catalog surface: a global
records-per-year time series, the same broken down by OBIS node and by marine
area, the dataset catalog, and the species checklist.
"""

import pyarrow as pa
from subsets_utils import (
    NodeSpec,
    get,
    save_raw_ndjson,
    save_raw_parquet,
    transient_retry,
)

BASE = "https://api.obis.org/v3"
MAX_PAGES = 1000  # safety ceiling for paginated endpoints; raises if exceeded


@transient_retry()
def _get_json(path, **params):
    resp = get(f"{BASE}{path}", params=params, timeout=(10.0, 180.0))
    resp.raise_for_status()
    return resp.json()


def _paginate(path, page_size, **params):
    """Yield every result dict across all pages using OBIS's `skip` offset."""
    skip = 0
    pages = 0
    total = None
    while True:
        pages += 1
        if pages > MAX_PAGES:
            raise RuntimeError(f"{path}: exceeded MAX_PAGES={MAX_PAGES}")
        body = _get_json(path, size=page_size, skip=skip, **params)
        if total is None:
            total = body.get("total")
        results = body.get("results", [])
        if not results:
            break
        for r in results:
            yield r
        skip += len(results)
        if total is not None and skip >= total:
            break
        if len(results) < page_size:
            break


def _join_names(lst):
    if not isinstance(lst, list):
        return None
    names = [x.get("name") for x in lst if isinstance(x, dict) and x.get("name")]
    return "; ".join(names) if names else None


# --------------------------------------------------------------------------
# statistics: records per year (global, and broken down by node / area)
# --------------------------------------------------------------------------

_YEARS_SCHEMA = pa.schema([
    ("year", pa.int32()),
    ("records", pa.int64()),
])

_NODE_YEARS_SCHEMA = pa.schema([
    ("nodeid", pa.string()),
    ("node_name", pa.string()),
    ("node_type", pa.string()),
    ("year", pa.int32()),
    ("records", pa.int64()),
])

_AREA_YEARS_SCHEMA = pa.schema([
    ("areaid", pa.string()),
    ("area_name", pa.string()),
    ("area_type", pa.string()),
    ("year", pa.int32()),
    ("records", pa.int64()),
])

_AREAS_SCHEMA = pa.schema([
    ("areaid", pa.string()),
    ("area_name", pa.string()),
    ("area_type", pa.string()),
])

_NODES_SCHEMA = pa.schema([
    ("nodeid", pa.string()),
    ("node_name", pa.string()),
    ("description", pa.string()),
    ("theme", pa.string()),
    ("node_type", pa.string()),
    ("lon", pa.float64()),
    ("lat", pa.float64()),
    ("url_count", pa.int32()),
    ("feed_count", pa.int32()),
    ("contact_count", pa.int32()),
])


def fetch_statistics_by_year(node_id: str) -> None:
    asset = node_id
    data = _get_json("/statistics/years")  # list of {year, records}
    rows = [
        {"year": d["year"], "records": d.get("records")}
        for d in data
        if d.get("year") is not None
    ]
    save_raw_parquet(pa.Table.from_pylist(rows, schema=_YEARS_SCHEMA), asset)


def fetch_statistics_by_node_year(node_id: str) -> None:
    asset = node_id
    nodes = _get_json("/node").get("results", [])
    rows = []
    for nd in nodes:
        nid = nd.get("id")
        years = _get_json("/statistics/years", nodeid=nid)
        for y in years:
            if y.get("year") is None:
                continue
            rows.append({
                "nodeid": nid,
                "node_name": nd.get("name"),
                "node_type": nd.get("type"),
                "year": y["year"],
                "records": y.get("records"),
            })
    save_raw_parquet(pa.Table.from_pylist(rows, schema=_NODE_YEARS_SCHEMA), asset)


def fetch_statistics_by_area_year(node_id: str) -> None:
    asset = node_id
    areas = _get_json("/area").get("results", [])
    rows = []
    for ar in areas:
        aid = str(ar.get("id"))
        years = _get_json("/statistics/years", areaid=aid)
        for y in years:
            if y.get("year") is None:
                continue
            rows.append({
                "areaid": aid,
                "area_name": ar.get("name"),
                "area_type": ar.get("type"),
                "year": y["year"],
                "records": y.get("records"),
            })
    save_raw_parquet(pa.Table.from_pylist(rows, schema=_AREA_YEARS_SCHEMA), asset)


# --------------------------------------------------------------------------
# reference dimensions
# --------------------------------------------------------------------------

def fetch_areas(node_id: str) -> None:
    asset = node_id
    rows = []
    for ar in _get_json("/area").get("results", []):
        rows.append({
            "areaid": str(ar.get("id")) if ar.get("id") is not None else None,
            "area_name": ar.get("name"),
            "area_type": ar.get("type"),
        })
    save_raw_parquet(pa.Table.from_pylist(rows, schema=_AREAS_SCHEMA), asset)


def fetch_nodes(node_id: str) -> None:
    asset = node_id
    rows = []
    for nd in _get_json("/node").get("results", []):
        rows.append({
            "nodeid": nd.get("id"),
            "node_name": nd.get("name"),
            "description": nd.get("description"),
            "theme": nd.get("theme"),
            "node_type": nd.get("type"),
            "lon": nd.get("lon"),
            "lat": nd.get("lat"),
            "url_count": len(nd.get("url") or []),
            "feed_count": len(nd.get("feeds") or []),
            "contact_count": len(nd.get("contacts") or []),
        })
    save_raw_parquet(pa.Table.from_pylist(rows, schema=_NODES_SCHEMA), asset)


# --------------------------------------------------------------------------
# datasets catalog
# --------------------------------------------------------------------------

def fetch_datasets(node_id: str) -> None:
    asset = node_id
    rows = []
    for d in _paginate("/dataset", 1000):
        stats = d.get("statistics") or {}
        rows.append({
            "dataset_id": d.get("id"),
            "title": d.get("title"),
            "node_names": _join_names(d.get("nodes")),
            "institutions": _join_names(d.get("institutes")),
            "license": d.get("intellectualrights"),
            "core": d.get("core"),
            "records": d.get("records"),
            "occurrence_count": stats.get("Occurrence"),
            "dropped_count": stats.get("dropped"),
            "published": d.get("published"),
            "created": d.get("created"),
            "updated": d.get("updated"),
            "extent_wkt": d.get("extent"),
            "citation": d.get("citation"),
        })
    save_raw_ndjson(rows, asset)


# --------------------------------------------------------------------------
# species checklist
# --------------------------------------------------------------------------

_CHECKLIST_KEYS = [
    "taxonID", "scientificName", "taxonRank", "taxonomicStatus",
    "acceptedNameUsage", "acceptedNameUsageID",
    "kingdom", "phylum", "class", "order", "family", "genus", "species",
    "is_marine", "is_brackish", "is_freshwater", "is_terrestrial",
    "records",
]


def fetch_checklist(node_id: str) -> None:
    asset = node_id
    # The global /checklist endpoint can only be paged to skip<100000 (server
    # 500s past its max_result_window), but the corpus is ~197k taxa. Partition
    # by OBIS node instead — every node's checklist is < 100k so paging stays
    # under the cap, and every taxon belongs to >=1 node (it only exists in the
    # checklist because it has occurrences, which live in node datasets). Each
    # node row carries that node's per-taxon record count; the transform sums
    # them across nodes back to the global count and dedupes to one row per
    # taxon. Normalise to a fixed key set so the NDJSON has a stable column
    # union (lower-rank taxa omit family/genus/species otherwise).
    nodes = _get_json("/node").get("results", [])
    rows = []
    for nd in nodes:
        for r in _paginate("/checklist", 10000, nodeid=nd.get("id")):
            rows.append({k: r.get(k) for k in _CHECKLIST_KEYS})
    save_raw_ndjson(rows, asset)


# --------------------------------------------------------------------------
# specs
# --------------------------------------------------------------------------

DOWNLOAD_SPECS = [
    NodeSpec(id="obis-areas", fn=fetch_areas, kind="download"),
    NodeSpec(id="obis-nodes", fn=fetch_nodes, kind="download"),
    NodeSpec(id="obis-statistics-by-year",
             fn=fetch_statistics_by_year, kind="download"),
    NodeSpec(id="obis-statistics-by-node-year",
             fn=fetch_statistics_by_node_year, kind="download"),
    NodeSpec(id="obis-statistics-by-area-year",
             fn=fetch_statistics_by_area_year, kind="download"),
    NodeSpec(id="obis-datasets", fn=fetch_datasets, kind="download"),
    NodeSpec(id="obis-checklist", fn=fetch_checklist, kind="download"),
]
