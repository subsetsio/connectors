"""Environment and Climate Change Canada — MSC GeoMet OGC API Features connector.

Mechanism (from research): the GeoMet-OGC-API at https://api.weather.gc.ca.
Each rank-active collect entity is one OGC API Features collection; we fetch
its /collections/<id>/items endpoint as GeoJSON and publish one Delta table per
collection. Station/site is a column value within each collection (e.g.
CLIMATE_IDENTIFIER, STATION_NUMBER), never a separate subset.

Fetch shape: stateless full re-pull (shape 1). Every collection here paginates
to completion in minutes (largest is hydrometric-monthly-mean ~2.3M rows = ~230
pages of 10000). The server honours offset pagination at depth (verified to
offset 50000+) and caps page size at 10000. We stream each page straight to a
gzip-compressed NDJSON raw asset, so memory stays bounded regardless of size.
NDJSON (not parquet) because the 19 collections have heterogeneous, partly
bilingual property sets with many sometimes-present flag columns; the transform
re-types on read.

No incremental watermark: the corpus is small enough to re-pull whole each
refresh, which picks up source revisions/late corrections for free.
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
PAGE = 10000                # server caps page size at 10000 (verified)
MAX_PAGES = 100000          # safety ceiling; raises on hit (detects runaway / source growth)


@transient_retry()          # 6 attempts, exp backoff over transient net + 429 + 5xx
def _fetch_page(collection: str, offset: int) -> dict:
    resp = get(
        f"{BASE}/collections/{collection}/items",
        params={"limit": PAGE, "offset": offset, "f": "json"},
        timeout=(15.0, 300.0),
    )
    resp.raise_for_status()
    return resp.json()


def _collection_of(node_id: str) -> str:
    # spec id is f"{SLUG}-{entity}"; the entity ids are already the OGC
    # collection ids (lowercase, hyphenated), so stripping the slug prefix
    # recovers the collection id exactly.
    return node_id[len(SLUG) + 1:]


def fetch_one(node_id: str) -> None:
    asset = node_id                       # the spec id IS the asset name
    collection = _collection_of(node_id)
    offset = 0
    pages = 0
    written = 0
    total = None

    with raw_writer(asset, "ndjson.gz", mode="wt", compression="gzip") as w:
        while True:
            if pages >= MAX_PAGES:
                raise RuntimeError(
                    f"{collection}: hit MAX_PAGES={MAX_PAGES} safety cap at "
                    f"offset {offset} (total reported {total}) — source grew "
                    f"unexpectedly or pagination is not terminating"
                )
            doc = _fetch_page(collection, offset)
            if total is None:
                total = doc.get("numberMatched")
            feats = doc.get("features") or []
            n = len(feats)
            for f in feats:
                row = dict(f.get("properties") or {})
                # The OGC feature id is the stable per-row key; geometry coords
                # are kept so a station's location survives even when a
                # collection omits LATITUDE/LONGITUDE from properties.
                row["feature_id"] = f.get("id")
                geom = f.get("geometry") or {}
                coords = geom.get("coordinates")
                if isinstance(coords, list) and len(coords) >= 2:
                    row["geom_lon"] = coords[0]
                    row["geom_lat"] = coords[1]
                w.write(json.dumps(row, default=str))
                w.write("\n")
            written += n
            pages += 1
            offset += n
            if n < PAGE:
                break
            if total is not None and offset >= total:
                break

    if written == 0:
        raise RuntimeError(
            f"{collection}: wrote 0 features (numberMatched reported {total}) — "
            f"endpoint shape changed or collection emptied"
        )


DOWNLOAD_SPECS = [
    NodeSpec(
        id=f"{SLUG}-{eid.lower().replace('_', '-')}",
        fn=fetch_one,
        kind="download",
    )
    for eid in ENTITY_IDS
]

# One published Delta table per collection. The raw NDJSON rows are already flat
# (GeoJSON properties + feature_id + geom coords); DuckDB infers column types on
# read. A thin pass: project everything through, dropping any all-empty row.
# A 0-row result fails the node, so an empty/broken pull surfaces here.
TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{s.id}-transform",
        deps=[s.id],
        sql=f'SELECT * FROM "{s.id}" WHERE feature_id IS NOT NULL',
    )
    for s in DOWNLOAD_SPECS
]
