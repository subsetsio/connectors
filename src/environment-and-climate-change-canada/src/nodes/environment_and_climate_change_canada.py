"""Environment and Climate Change Canada — MSC GeoMet OGC API Features connector.

Mechanism (from research): the GeoMet-OGC-API at https://api.weather.gc.ca.
Each rank-active collect entity is one OGC API Features collection; we fetch its
/collections/<id>/items endpoint as GeoJSON and publish one Delta table per
collection. Station/site is a column value within each collection, never a
separate subset.

Fetch shape: stateless full re-pull (shape 1) via plain offset pagination. The
GeoMet backend's offset pagination is O(offset) — a deep page on a multi-million
-row collection takes minutes (climate-monthly offset=1.9M measured at 161s) — so
the rank step deferred every collection above ~600k rows; the 16 built here keep
their max offset shallow (largest is climate-normals ~593k) and each paginates in
under ten minutes. Plain offset is deliberate: it is server-bound and uniform,
with no dependence on whether a given collection has an index on a station/date
filter field (per-station filtering was measured to trigger slow full scans on
some collections).

Each page is streamed straight to a gzip NDJSON raw asset, so memory stays
bounded. NDJSON (not parquet) because the 16 collections have heterogeneous,
partly bilingual property sets with many sometimes-present flag columns; the
transform re-types on read. No incremental watermark — the corpus re-pulls whole
each refresh, picking up source revisions for free.
"""
import json

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    transient_retry,
    raw_writer,
)
from constants import ENTITY_IDS

SLUG = "environment-and-climate-change-canada"
BASE = "https://api.weather.gc.ca"
PAGE = 10000        # server caps page size at 10000 (verified)
MAX_PAGES = 5000    # safety ceiling; raises on hit (deferred collections are <600k rows = <60 pages)


@transient_retry()  # 6 attempts, exp backoff over transient net + 429 + 5xx
def _fetch_page(collection: str, offset: int) -> dict:
    resp = get(
        f"{BASE}/collections/{collection}/items",
        params={"limit": PAGE, "offset": offset, "f": "json"},
        timeout=(15.0, 300.0),
    )
    resp.raise_for_status()
    return resp.json()


def _row_line(f: dict) -> str:
    """Flatten one GeoJSON feature to a single NDJSON line: its properties plus a
    stable feature_id key and geometry coords."""
    row = dict(f.get("properties") or {})
    row["feature_id"] = f.get("id")
    geom = f.get("geometry") or {}
    coords = geom.get("coordinates")
    if isinstance(coords, list) and len(coords) >= 2:
        row["geom_lon"] = coords[0]
        row["geom_lat"] = coords[1]
    return json.dumps(row, default=str)


def _collection_of(node_id: str) -> str:
    # spec id is f"{SLUG}-{entity}"; entity ids are the OGC collection ids
    # (lowercase, hyphenated), so stripping the slug prefix recovers them.
    return node_id[len(SLUG) + 1:]


def fetch_one(node_id: str) -> None:
    asset = node_id
    collection = _collection_of(node_id)
    offset = 0
    pages = 0
    total = None
    written = 0

    with raw_writer(asset, "ndjson.gz", mode="wt", compression="gzip") as w:
        while True:
            if pages >= MAX_PAGES:
                raise RuntimeError(
                    f"{collection}: hit MAX_PAGES={MAX_PAGES} at offset {offset} "
                    f"(numberMatched={total}) — collection grew past the offset "
                    f"budget; it should be deferred and partitioned"
                )
            doc = _fetch_page(collection, offset)
            if total is None:
                total = doc.get("numberMatched")
            feats = doc.get("features") or []
            for f in feats:
                w.write(_row_line(f))
                w.write("\n")
                written += 1
            n = len(feats)
            offset += n
            pages += 1
            if n < PAGE or (total is not None and offset >= total):
                break

    if written == 0:
        raise RuntimeError(
            f"{collection}: wrote 0 features (numberMatched={total}) — endpoint "
            f"shape changed or collection emptied"
        )


DOWNLOAD_SPECS = [
    NodeSpec(
        id=f"{SLUG}-{eid.lower().replace('_', '-')}",
        fn=fetch_one,
        kind="download",
    )
    for eid in ENTITY_IDS
]

# One published Delta table per collection. Raw NDJSON rows are already flat
# (GeoJSON properties + feature_id + geom coords); DuckDB infers column types on
# read. A 0-row result fails the node, so an empty/broken pull surfaces here.
TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{s.id}-transform",
        deps=[s.id],
        sql=f'SELECT * FROM "{s.id}" WHERE feature_id IS NOT NULL',
    )
    for s in DOWNLOAD_SPECS
]
