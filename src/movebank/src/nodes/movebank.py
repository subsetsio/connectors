"""Movebank Data Repository connector.

Source: the Movebank Data Repository (datarepository.movebank.org), a DSpace 7
archive of curated, peer-reviewed animal-tracking datasets. The publishable unit
is a `Datapackage` item — one published study, one DOI, one main location CSV.

Strategy: stateless full re-pull, one spec per Datapackage (the rank-active entity
union). For each item we resolve its DSpace handle to a UUID, walk
item -> ORIGINAL bundle -> bitstreams, pick the study's main location CSV series
(see `_pick_location_series`), and stream-normalize it to a stable core schema
(event_id, timestamp, longitude, latitude, sensor_type, taxon, individual_id,
tag_id, study_name). Study-specific extra columns are dropped so every published
table shares one clean, comparable schema. The HTTP body is streamed straight to
the raw ndjson file so the multi-million-row studies never materialize in memory.

No auth (all repository data is public). No incremental query — each study CSV is
re-fetched in full; the maintain step decides whether a node runs.
"""

import csv
import codecs
import io
import json
import posixpath
import re
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
SPEC_ENTITY_IDS = {
    f"movebank-{eid.lower().replace('_', '-')}": eid for eid in ENTITY_IDS
}

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
_RANGE_CHUNK_BYTES = 8 * 1024 * 1024
_RANGE_MIN_BYTES = 256 * 1024 * 1024


@transient_retry()
def _get_json(url):
    resp = get(url, timeout=(10.0, 120.0), headers={"Accept": "application/json"})
    resp.raise_for_status()
    return resp.json()


def _resolve_item_uuid(handle):
    """Resolve a DSpace handle (e.g. '10255/move.882') to its item UUID."""
    item = _get_json(f"{API}/pid/find?id={handle}")
    return item["uuid"]


# A Movebank Datapackage exports one study as `<study title>-<series>.csv[.zip]`,
# split into per-sensor series. Only some series carry location fixes; the rest
# (light levels, twilights, barometer, acceleration, ...) share the timestamp/tag
# columns but have no location-lat/long at all, so folding them into the location
# table yields rows that are ~all-null on the coordinates. Classify on the TRAILING
# series token — a substring match reads "gps" out of `...GPS_2003-2021-accessory`
# and "acc" out of `...-accessory`, and would drop `...-twilights-tracks` (a
# derived TRACK series). Multi-part exports (`-gps-1of4`, `_part`) are chunks of
# one series and are concatenated.
_CSV_EXT = re.compile(r"(?i)\.csv(\.zip)?$")
_CHUNK = re.compile(r"(?i)[-_ ]?\d+\s*of\s*\d+$")
_PART = re.compile(r"(?i)[-_ ]?part$")
_LOCATION_SERIES = re.compile(
    r"(?i)[-_ ](gps|tracks|argos|argos[- ]tracking|argos[- ]data|"
    r"fastloc[- ]gps(?:[- ]data)?|locations?)$"
)
_OTHER_SERIES = re.compile(
    r"(?i)[-_ ](reference[- ]data|metadata|light[- ]levels?|levels|twilights?|"
    r"barometer|bar|acc|acceleration|accessory|mag|magnetometer|messages|"
    r"transmitter|temperature|activity|output)$"
)


def _series_base(name):
    """The export name minus its extension and any chunk/part markers."""
    base = _CSV_EXT.sub("", name)
    prev = None
    while prev != base:
        prev = base
        base = _CHUNK.sub("", base)
        base = _PART.sub("", base)
    return base


def _series(name):
    """`location` (publishable), `other` (no coordinates), or `plain` (untagged)."""
    if "readme" in name.lower():
        return "other"
    base = _series_base(name)
    if _LOCATION_SERIES.search(base):
        return "location"
    if _OTHER_SERIES.search(base):
        return "other"
    return "plain"


def _normalize(text):
    return re.sub(r"[^a-z0-9]", "", text.lower())


def _study_prefixes(names):
    """Study titles, recovered from each `<title>-reference-data.csv` companion.

    Every export the study itself publishes carries one; the loose analysis CSVs
    some bundles also archive (model output, weather covariates, morphology) do
    not, and are the other way a non-location file reaches the location table.
    Compared punctuation-insensitively: a title is not spelled identically across
    a bundle's bitstreams (`Scotia, NSW` vs `Scotia NSW`).
    """
    prefixes = []
    for name in names:
        match = re.match(r"(?i)^(.+?)-reference[- ]data", _CSV_EXT.sub("", name))
        if match:
            prefix = _normalize(_series_base(match.group(1)))
            if prefix:
                prefixes.append(prefix)
    return prefixes


def _pick_location_series(names):
    """The subset of `names` that make up the study's main location series."""
    prefixes = _study_prefixes(names)

    def in_study(name):
        if not prefixes:
            return True
        base = _normalize(_series_base(name))
        return any(base.startswith(prefix) for prefix in prefixes)

    usable = [n for n in names if _series(n) != "other" and in_study(n)]
    located = [n for n in usable if _series(n) == "location"]
    return located or usable


def _main_csv_sources(item_uuid):
    """Return the study's main location CSV bitstreams from the ORIGINAL bundle.

    Movebank often stores large exports as one or more ``.csv.zip`` bitstreams.
    All the bundle's bitstreams are classified together, because the pick is
    relative: a bundle's location series is only recognisable next to the sensor
    series and reference data it ships beside.
    """
    bundles = _get_json(f"{API}/core/items/{item_uuid}/bundles")
    orig = next(
        (b for b in bundles["_embedded"]["bundles"] if b["name"] == "ORIGINAL"),
        None,
    )
    if orig is None:
        return []
    bs_url = orig["_links"]["bitstreams"]["href"]

    bitstreams = []
    page = 0
    while True:
        data = _get_json(f"{bs_url}?size=100&page={page}")
        bitstreams.extend(data["_embedded"]["bitstreams"])
        pinfo = data.get("page", {})
        page += 1
        if page >= pinfo.get("totalPages", 1):
            break

    candidates, seen = {}, set()
    for b in bitstreams:
        name = b.get("name") or ""
        low = name.lower()
        if not (low.endswith(".csv") or low.endswith(".csv.zip")):
            continue
        if low in seen:  # a bundle may list the same bitstream twice
            continue
        seen.add(low)
        candidates[name] = {
            "name": name,
            "size": b.get("sizeBytes") or 0,
            "url": b["_links"]["content"]["href"],
            "zipped": low.endswith(".csv.zip"),
        }

    picked = _pick_location_series(list(candidates))
    return [candidates[n] for n in sorted(picked, key=str.lower)]


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


@transient_retry()
def _get_range_bytes(url, start, end):
    resp = get(
        url,
        timeout=_TIMEOUT,
        headers={"Range": f"bytes={start}-{end}"},
    )
    resp.raise_for_status()
    if resp.status_code != 206:
        raise ValueError(f"range request returned HTTP {resp.status_code}")
    expected = end - start + 1
    if len(resp.content) != expected:
        raise ValueError(
            f"range request returned {len(resp.content)} bytes, expected {expected}"
        )
    return resp.content


def _iter_ranged_lines(url, size):
    decoder = codecs.getincrementaldecoder("utf-8-sig")(errors="replace")
    pending = ""
    start = 0
    while start < size:
        end = min(start + _RANGE_CHUNK_BYTES - 1, size - 1)
        text = decoder.decode(_get_range_bytes(url, start, end), final=False)
        lines = (pending + text).splitlines(keepends=True)
        if lines and not (lines[-1].endswith("\n") or lines[-1].endswith("\r")):
            pending = lines.pop()
        else:
            pending = ""
        for line in lines:
            yield line
        start = end + 1

    tail = decoder.decode(b"", final=True)
    if tail:
        pending += tail
    if pending:
        yield pending


def _zip_csv_members(handle):
    """The location-series members of a `.csv.zip` export, by the same rules."""
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
        members.append(name)
    return sorted(_pick_location_series(members))


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
            if not source["zipped"] and source.get("size", 0) >= _RANGE_MIN_BYTES:
                total_rows += _write_csv_rows(
                    csv.reader(_iter_ranged_lines(source["url"], source["size"])),
                    out,
                )
                continue

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
    entity_id = SPEC_ENTITY_IDS[node_id]
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
