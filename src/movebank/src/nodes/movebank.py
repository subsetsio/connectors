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
import io
import json
import posixpath
import tempfile
import zipfile

from subsets_utils import (
    NodeSpec,
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


def _is_reference_or_readme(name):
    low = name.lower()
    return (
        low.endswith("-reference-data.csv")
        or "/reference-data" in low
        or "readme" in low
    )


def _movement_priority(name):
    low = name.lower()
    if "gps" in low:
        return 0
    if "acc" in low or "acceleration" in low:
        return 2
    return 1


def _main_csv_sources(item_uuid):
    """Return main movement CSV bitstreams from the ORIGINAL bundle.

    Movebank often stores large exports as one or more ``.csv.zip`` bitstreams.
    When both GPS/location and acceleration exports are present, publish the GPS
    series; acceleration-only bundles do not satisfy this connector's location
    table model.
    """
    bundles = _get_json(f"{API}/core/items/{item_uuid}/bundles")
    orig = next(
        (b for b in bundles["_embedded"]["bundles"] if b["name"] == "ORIGINAL"),
        None,
    )
    if orig is None:
        return []
    bs_url = orig["_links"]["bitstreams"]["href"]

    candidates = []
    page = 0
    while True:
        data = _get_json(f"{bs_url}?size=100&page={page}")
        bitstreams = data["_embedded"]["bitstreams"]
        for b in bitstreams:
            name = (b.get("name") or "")
            low = name.lower()
            if _is_reference_or_readme(name):
                continue
            if low.endswith(".csv"):
                zipped = False
            elif low.endswith(".csv.zip"):
                zipped = True
            else:
                continue
            candidates.append(
                {
                    "name": name,
                    "priority": _movement_priority(name),
                    "size": b.get("sizeBytes") or 0,
                    "url": b["_links"]["content"]["href"],
                    "zipped": zipped,
                }
            )
        pinfo = data.get("page", {})
        page += 1
        if page >= pinfo.get("totalPages", 1):
            break
    if not candidates:
        return []

    best_priority = min(c["priority"] for c in candidates)
    if best_priority == 2:
        return []
    return sorted(
        (c for c in candidates if c["priority"] == best_priority),
        key=lambda c: c["name"].lower(),
    )


def _write_csv_rows(reader, out):
    try:
        header = next(reader)
    except StopIteration:
        return 0

    idx_to_field = {
        i: CORE_COLUMNS[col]
        for i, col in enumerate(header)
        if col in CORE_COLUMNS
    }
    row_count = 0
    for row in reader:
        rec = {f: None for f in OUTPUT_FIELDS}
        for i, field in idx_to_field.items():
            if i < len(row):
                v = row[i]
                rec[field] = v if v != "" else None
        out.write(json.dumps(rec) + "\n")
        row_count += 1
    return row_count


def _zip_csv_members(handle):
    members = []
    for info in handle.infolist():
        name = info.filename
        base = posixpath.basename(name)
        low = name.lower()
        if (
            info.is_dir()
            or "__macosx/" in low
            or base.startswith(".")
            or not low.endswith(".csv")
        ):
            continue
        if _is_reference_or_readme(name):
            continue
        members.append((info.filename, _movement_priority(name)))
    if not members:
        return []
    best_priority = min(priority for _, priority in members)
    if best_priority == 2:
        return []
    return sorted(name for name, priority in members if priority == best_priority)


@transient_retry()
def _stream_normalize(sources, asset):
    """Stream main CSV source(s) and write a normalized core-schema raw asset.

    Plain CSV bodies are consumed line-by-line. Zipped CSV exports are spooled to
    a temporary file because ``zipfile`` needs random access to the central
    directory. Rows are projected by header name; transforms do typing/casting.
    """
    client = get_client()
    total_rows = 0
    with raw_writer(asset, "ndjson.gz", mode="wt", compression="gzip") as out:
        for source in sources:
            with client.stream("GET", source["url"], timeout=_TIMEOUT) as resp:
                resp.raise_for_status()
                if not source["zipped"]:
                    total_rows += _write_csv_rows(csv.reader(resp.iter_lines()), out)
                    continue

                with tempfile.SpooledTemporaryFile(max_size=128 * 1024 * 1024) as tmp:
                    for chunk in resp.iter_bytes():
                        tmp.write(chunk)
                    tmp.seek(0)
                    with zipfile.ZipFile(tmp) as zf:
                        members = _zip_csv_members(zf)
                        if not members:
                            raise ValueError(
                                f"{asset}: no movement CSV found inside {source['name']}"
                            )
                        for member in members:
                            with zf.open(member) as fh:
                                text = io.TextIOWrapper(
                                    fh,
                                    encoding="utf-8-sig",
                                    errors="replace",
                                    newline="",
                                )
                                total_rows += _write_csv_rows(csv.reader(text), out)
    if total_rows == 0:
        raise ValueError(f"{asset}: main CSV source(s) produced 0 rows")


def fetch_one(node_id: str) -> None:
    asset = node_id  # the runtime passes the spec id; it IS the asset name
    entity_id = node_id[len("movebank-"):]
    if entity_id not in ENTITY_HANDLES:
        entity_id = entity_id.replace("-", "_")
    handle = ENTITY_HANDLES[entity_id]
    item_uuid = _resolve_item_uuid(handle)
    sources = _main_csv_sources(item_uuid)
    if not sources:
        raise ValueError(
            f"{asset}: no main location CSV found in ORIGINAL bundle for {handle}"
        )
    _stream_normalize(sources, asset)


DOWNLOAD_SPECS = [
    NodeSpec(
        id=f"movebank-{eid.lower().replace('_', '-')}",
        fn=fetch_one,
        kind="download",
    )
    for eid in ENTITY_IDS
]
