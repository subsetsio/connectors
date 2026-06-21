"""Environment and Climate Change Canada — MSC GeoMet OGC API Features connector.

Mechanism (from research): the GeoMet-OGC-API at https://api.weather.gc.ca.
Each rank-active collect entity is one OGC API Features collection; we fetch its
/collections/<id>/items endpoint as GeoJSON and publish one Delta table per
collection. Station/site is a column value within each collection, never a
separate subset.

Fetch shape: stateless full re-pull (shape 1), but PER STATION for the large
observation collections. The backend's offset pagination is O(offset) — a deep
page on a multi-million-row collection takes minutes (climate-monthly offset=1.9M
measured at 161s), so a straight crawl is unusable. Filtering to one station
returns a small indexed slice in ~0.1s, so for every collection in
STATION_PARTITIONS we enumerate stations from the companion station collection
and pull each station's slice. The pulls run concurrently inside the node (the
DAG itself runs nodes sequentially: DAG_PARALLELISM defaults to 1), which keeps a
multi-thousand-station collection to a few minutes. The small *-stations
reference collections are pulled with plain shallow pagination.

Every page is streamed straight to a gzip NDJSON raw asset, so memory stays
bounded regardless of collection size. NDJSON (not parquet) because the 19
collections have heterogeneous, partly bilingual property sets with many
sometimes-present flag columns; the transform re-types on read. No incremental
watermark — the corpus re-pulls whole each refresh, picking up source revisions
for free.
"""
import json
from concurrent.futures import ThreadPoolExecutor, as_completed

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    transient_retry,
    raw_writer,
)
from constants import ENTITY_IDS, STATION_PARTITIONS

SLUG = "environment-and-climate-change-canada"
BASE = "https://api.weather.gc.ca"
PAGE = 10000            # server caps page size at 10000 (verified)
MAX_PAGES = 10000       # per-query safety ceiling; raises on hit
WORKERS = 8             # concurrent per-station requests inside one node


@transient_retry()      # 6 attempts, exp backoff over transient net + 429 + 5xx
def _fetch_page(collection: str, params: dict) -> dict:
    resp = get(
        f"{BASE}/collections/{collection}/items",
        params=params,
        timeout=(15.0, 300.0),
    )
    resp.raise_for_status()
    return resp.json()


def _iter_features(collection: str, extra: dict):
    """Yield every feature of a collection (optionally filtered by `extra`),
    paginating with offset. Shallow because `extra` slices the result small."""
    offset = 0
    pages = 0
    total = None
    while True:
        if pages >= MAX_PAGES:
            raise RuntimeError(
                f"{collection}: hit MAX_PAGES={MAX_PAGES} at offset {offset} "
                f"(filter={extra}) — pagination not terminating"
            )
        params = {"limit": PAGE, "offset": offset, "f": "json"}
        params.update(extra)
        doc = _fetch_page(collection, params)
        if total is None:
            total = doc.get("numberMatched")
        feats = doc.get("features") or []
        for f in feats:
            yield f
        n = len(feats)
        offset += n
        pages += 1
        if n < PAGE or (total is not None and offset >= total):
            break


def _row_line(f: dict) -> str:
    """Flatten one GeoJSON feature to a single NDJSON line: its properties plus
    a stable feature_id key and geometry coords."""
    row = dict(f.get("properties") or {})
    row["feature_id"] = f.get("id")
    geom = f.get("geometry") or {}
    coords = geom.get("coordinates")
    if isinstance(coords, list) and len(coords) >= 2:
        row["geom_lon"] = coords[0]
        row["geom_lat"] = coords[1]
    return json.dumps(row, default=str)


def _station_ids(stations_collection: str, id_field: str) -> list:
    seen = set()
    out = []
    for f in _iter_features(stations_collection, {}):
        v = (f.get("properties") or {}).get(id_field)
        if v is not None and v not in seen:
            seen.add(v)
            out.append(v)
    return out


def _station_lines(collection: str, field: str, station_id) -> list:
    return [_row_line(f) for f in _iter_features(collection, {field: station_id})]


def _collection_of(node_id: str) -> str:
    # spec id is f"{SLUG}-{entity}"; entity ids are the OGC collection ids
    # (lowercase, hyphenated), so stripping the slug prefix recovers them.
    return node_id[len(SLUG) + 1:]


def fetch_one(node_id: str) -> None:
    asset = node_id
    collection = _collection_of(node_id)
    written = 0

    with raw_writer(asset, "ndjson.gz", mode="wt", compression="gzip") as w:
        if collection in STATION_PARTITIONS:
            field, stn_coll, stn_field = STATION_PARTITIONS[collection]
            station_ids = _station_ids(stn_coll, stn_field)
            if not station_ids:
                raise RuntimeError(
                    f"{collection}: 0 station ids from {stn_coll}.{stn_field} — "
                    f"station collection shape changed"
                )
            # Concurrent per-station pulls; the writer is single-threaded (only
            # the main loop touches it), so results are written as they arrive.
            # An isolated station that exhausts its retries is tolerated (one
            # flaky station shouldn't sink a multi-thousand-station pull), but a
            # systemic failure rate raises.
            failed = 0
            with ThreadPoolExecutor(max_workers=WORKERS) as ex:
                futs = {
                    ex.submit(_station_lines, collection, field, sid): sid
                    for sid in station_ids
                }
                for fut in as_completed(futs):
                    try:
                        lines = fut.result()
                    except Exception as e:
                        failed += 1
                        print(
                            f"[{collection}] station {futs[fut]!r} failed after "
                            f"retries: {type(e).__name__}: {e}"
                        )
                        continue
                    for line in lines:
                        w.write(line)
                        w.write("\n")
                        written += 1
            tolerance = max(10, int(0.01 * len(station_ids)))
            if failed > tolerance:
                raise RuntimeError(
                    f"{collection}: {failed}/{len(station_ids)} stations failed "
                    f"(exceeds tolerance {tolerance}) — systemic fetch problem"
                )
        else:
            for f in _iter_features(collection, {}):
                w.write(_row_line(f))
                w.write("\n")
                written += 1

    if written == 0:
        raise RuntimeError(
            f"{collection}: wrote 0 features — endpoint shape changed or "
            f"collection emptied"
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
