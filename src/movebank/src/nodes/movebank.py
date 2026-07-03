"""Movebank Data Repository connector.

Source: the Movebank Data Repository (datarepository.movebank.org), a DSpace 7
archive of curated, peer-reviewed animal-tracking datasets. The publishable unit
is a `Datapackage` item — one published study, one DOI, one main location CSV.

Strategy: stateless full re-pull, one spec per Datapackage (the rank-active entity
union). For each item we resolve its DSpace handle to a UUID, walk
item -> ORIGINAL bundle -> bitstreams, pick the main location CSV (the largest
non-reference, non-README .csv), and stream-normalize it to a stable core schema
(event_id, timestamp, longitude, latitude, sensor_type, taxon, individual_id,
tag_id, study_name). Study-specific extra columns are dropped so every published
table shares one clean, comparable schema. The HTTP body is streamed straight to
the raw ndjson file so the multi-million-row studies never materialize in memory.

No auth (all repository data is public). No incremental query — each study CSV is
re-fetched in full; the maintain step decides whether a node runs.
"""

import csv
import json

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    get_client,
    raw_writer,
    transient_retry,
)
from constants import ENTITY_IDS, ENTITY_HANDLES

API = "https://datarepository.movebank.org/server/api"

# Movebank standard export column -> our normalized field name. Every field is
# pulled by header name, so a study missing one of these simply gets nulls.
CORE_COLUMNS = {
    "event-id": "event_id",
    "timestamp": "timestamp",
    "location-long": "longitude",
    "location-lat": "latitude",
    "sensor-type": "sensor_type",
    "individual-taxon-canonical-name": "taxon",
    "individual-local-identifier": "individual_id",
    "tag-local-identifier": "tag_id",
    "study-name": "study_name",
}
OUTPUT_FIELDS = list(CORE_COLUMNS.values())

_TIMEOUT = (10.0, 300.0)


@transient_retry()
def _get_json(url):
    resp = get(url, timeout=(10.0, 120.0), headers={"Accept": "application/json"})
    resp.raise_for_status()
    return resp.json()


def _resolve_item_uuid(handle):
    """Resolve a DSpace handle (e.g. '10255/move.882') to its item UUID."""
    item = _get_json(f"{API}/pid/find?id={handle}")
    return item["uuid"]


def _main_csv_url(item_uuid):
    """Walk item -> ORIGINAL bundle -> bitstreams; return the content URL of the
    main location CSV (largest .csv that is neither the reference-data CSV nor a
    README). Returns None if the item exposes no plain CSV."""
    bundles = _get_json(f"{API}/core/items/{item_uuid}/bundles")
    orig = next(
        (b for b in bundles["_embedded"]["bundles"] if b["name"] == "ORIGINAL"),
        None,
    )
    if orig is None:
        return None
    bs_url = orig["_links"]["bitstreams"]["href"]

    best = None
    page = 0
    while True:
        data = _get_json(f"{bs_url}?size=100&page={page}")
        bitstreams = data["_embedded"]["bitstreams"]
        for b in bitstreams:
            name = (b.get("name") or "")
            low = name.lower()
            if not low.endswith(".csv"):
                continue
            if low.endswith("-reference-data.csv"):
                continue
            size = b.get("sizeBytes") or 0
            url = b["_links"]["content"]["href"]
            if best is None or size > best[0]:
                best = (size, url)
        pinfo = data.get("page", {})
        page += 1
        if page >= pinfo.get("totalPages", 1):
            break
    return best[1] if best else None


@transient_retry()
def _stream_normalize(content_url, asset):
    """Stream the main CSV and write a normalized core-schema ndjson.gz raw asset.

    The HTTP body is consumed line-by-line (never fully buffered) and each row is
    projected onto the core columns by header name. Strings are kept as-is; the
    transform does the typing/casting."""
    client = get_client()
    with client.stream("GET", content_url, timeout=_TIMEOUT) as resp:
        resp.raise_for_status()
        lines = resp.iter_lines()  # yields decoded str lines
        reader = csv.reader(lines)
        try:
            header = next(reader)
        except StopIteration:
            raise ValueError(f"{asset}: main CSV is empty (no header)")
        # header column index -> normalized field name (only the core columns)
        idx_to_field = {
            i: CORE_COLUMNS[col]
            for i, col in enumerate(header)
            if col in CORE_COLUMNS
        }
        with raw_writer(asset, "ndjson.gz", mode="wt", compression="gzip") as out:
            for row in reader:
                rec = {f: None for f in OUTPUT_FIELDS}
                for i, field in idx_to_field.items():
                    if i < len(row):
                        v = row[i]
                        rec[field] = v if v != "" else None
                out.write(json.dumps(rec) + "\n")


def fetch_one(node_id: str) -> None:
    asset = node_id  # the runtime passes the spec id; it IS the asset name
    entity_id = node_id[len("movebank-"):]
    handle = ENTITY_HANDLES[entity_id]
    item_uuid = _resolve_item_uuid(handle)
    content_url = _main_csv_url(item_uuid)
    if content_url is None:
        raise ValueError(
            f"{asset}: no main location CSV found in ORIGINAL bundle for {handle}"
        )
    _stream_normalize(content_url, asset)


DOWNLOAD_SPECS = [
    NodeSpec(
        id=f"movebank-{eid.lower().replace('_', '-')}",
        fn=fetch_one,
        kind="download",
    )
    for eid in ENTITY_IDS
]


def _transform_sql(download_id: str) -> str:
    return f'''
        SELECT
            TRY_CAST(event_id AS BIGINT)            AS event_id,
            TRY_CAST(timestamp AS TIMESTAMP)        AS timestamp,
            TRY_CAST(longitude AS DOUBLE)           AS longitude,
            TRY_CAST(latitude AS DOUBLE)            AS latitude,
            sensor_type,
            taxon,
            individual_id,
            tag_id,
            study_name
        FROM "{download_id}"
    '''


TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{s.id}-transform",
        deps=[s.id],
        temporal="timestamp",
        sql=_transform_sql(s.id),
    )
    for s in DOWNLOAD_SPECS
]
