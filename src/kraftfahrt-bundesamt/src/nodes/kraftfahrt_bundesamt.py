"""Kraftfahrt-Bundesamt (KBA) Statistikportal connector.

One published Delta table per KBA Statistikportal dataset. Each dataset is a
single hosted ArcGIS Online FeatureServer layer (org U09msXRZoxesNntH on
services-eu1) — see research mechanism `arcgis_rest`. We fetch the full
attribute table per layer via the GeoServices `/query` endpoint
(where=1=1, returnGeometry=false), paginating with resultOffset, and write it
as NDJSON (the 22 datasets have heterogeneous schemas, so a per-dataset parquet
schema would buy nothing). The transform is a thin SQL pass that drops the
ArcGIS internal columns (ObjectId / Shape__* / sort helpers) and publishes the
statistical attributes as-is.

Stateless full re-pull: every layer is small-to-medium (tens to ~780k rows) and
static-snapshot (services are overwritten in place each release), so we re-pull
the whole table each refresh and overwrite. No incremental filter is exposed by
the source for our pattern.
"""
from constants import ENTITY_IDS, SERVICES
from subsets_utils import NodeSpec, get, save_raw_ndjson, transient_retry

PREFIX = "kraftfahrt-bundesamt-"
PAGE = 1000                 # ArcGIS hosted maxRecordCount
MAX_PAGES = 5000            # safety ceiling: 5M rows; raises, never silently returns


@transient_retry()
def _get_json(url, **params):
    resp = get(url, params=params, timeout=(10.0, 120.0))
    resp.raise_for_status()
    data = resp.json()
    # ArcGIS returns HTTP 200 with an inline {"error": {...}} envelope.
    if isinstance(data, dict) and "error" in data:
        raise RuntimeError(f"ArcGIS error for {url}: {data['error']}")
    return data


def _oid_field(base_url):
    """OID field name to order by — keeps resultOffset pagination stable."""
    meta = _get_json(base_url, f="json")
    return meta.get("objectIdField") or "OBJECTID"


def _iter_attributes(base_url):
    """Yield one attributes dict per feature, paginating the full layer."""
    oid = _oid_field(base_url)
    offset = 0
    pages = 0
    while True:
        data = _get_json(
            base_url + "/query",
            where="1=1",
            outFields="*",
            returnGeometry="false",
            orderByFields=oid,
            resultOffset=offset,
            resultRecordCount=PAGE,
            f="json",
        )
        feats = data.get("features", [])
        for feat in feats:
            yield feat.get("attributes", {})
        pages += 1
        if pages > MAX_PAGES:
            raise RuntimeError(f"{base_url}: exceeded MAX_PAGES={MAX_PAGES} — source grew unexpectedly")
        more = data.get("exceededTransferLimit", len(feats) == PAGE)
        if not more or not feats:
            break
        offset += PAGE


def fetch_one(node_id: str) -> None:
    asset = node_id  # the runtime passes the spec id; it IS the asset name
    slug = node_id[len(PREFIX):] if node_id.startswith(PREFIX) else node_id
    base_url = SERVICES[slug]
    # Stream pages straight into the NDJSON writer — peak memory is one page.
    save_raw_ndjson(_iter_attributes(base_url), asset)


DOWNLOAD_SPECS = [
    NodeSpec(
        id=f"{PREFIX}{eid.lower().replace('_', '-')}",
        fn=fetch_one,
        kind="download",
    )
    for eid in ENTITY_IDS
]
