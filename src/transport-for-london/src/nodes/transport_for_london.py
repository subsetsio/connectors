"""Transport for London downloads.

The accepted datasets use TfL's anonymous cycling S3 bucket. Count extracts are
ingested file-by-file as fragments of one logical raw asset so interrupted runs
can resume, while the monitoring-location reference CSV is fetched as one table.
Every column is normalised to string; model/transform owns typing.
"""

import io
import re
import urllib.parse

import pyarrow as pa
import pyarrow.compute as pc
import pyarrow.csv as pacsv

from subsets_utils import (
    NodeSpec,
    get,
    load_state,
    save_raw_parquet,
    save_state,
)

SLUG = "transport-for-london"
STATE_VERSION = 1

S3_ORIGIN = "https://s3-eu-west-1.amazonaws.com/cycling.data.tfl.gov.uk/"
CDN = "https://cycling.data.tfl.gov.uk/"
MONITORING_LOCATIONS_KEY = "ActiveTravelCountsProgramme/1 Monitoring locations.csv"


# --------------------------------------------------------------------------- #
# HTTP helpers
# --------------------------------------------------------------------------- #
def _get_bytes(url: str) -> bytes:
    resp = get(url, timeout=(10.0, 300.0))
    resp.raise_for_status()
    return resp.content


# --------------------------------------------------------------------------- #
# S3 ListBucketV2 enumeration (regex over the XML — stable, dependency-free)
# --------------------------------------------------------------------------- #
_CONTENTS = re.compile(r"<Contents>(.*?)</Contents>", re.S)
_KEY = re.compile(r"<Key>(.*?)</Key>", re.S)
_SIZE = re.compile(r"<Size>(\d+)</Size>", re.S)
_NEXT = re.compile(r"<NextContinuationToken>(.*?)</NextContinuationToken>", re.S)


def _unescape(s: str) -> str:
    return (
        s.replace("&amp;", "&")
        .replace("&lt;", "<")
        .replace("&gt;", ">")
        .replace("&quot;", '"')
        .replace("&apos;", "'")
    )


def _s3_list(prefix: str) -> list[tuple[str, int]]:
    """All objects (key, size) under a bucket prefix, following pagination."""
    out: list[tuple[str, int]] = []
    token = None
    for _ in range(500):  # safety ceiling: ~500k objects; raises if exceeded
        url = f"{S3_ORIGIN}?list-type=2&prefix={urllib.parse.quote(prefix)}&max-keys=1000"
        if token:
            url += f"&continuation-token={urllib.parse.quote(token)}"
        xml = _get_bytes(url).decode("utf-8")
        for block in _CONTENTS.findall(xml):
            k = _KEY.search(block)
            if not k:
                continue
            key = _unescape(k.group(1))
            if key.endswith("/"):
                continue  # folder placeholder
            s = _SIZE.search(block)
            out.append((key, int(s.group(1)) if s else 0))
        if "<IsTruncated>true" in xml:
            nt = _NEXT.search(xml)
            token = nt.group(1) if nt else None
            if not token:
                break
        else:
            break
    else:
        raise RuntimeError(f"S3 listing for {prefix!r} exceeded the page ceiling")
    return out


# --------------------------------------------------------------------------- #
# CSV → fixed-schema all-string parquet (drift-proof normalisation)
# --------------------------------------------------------------------------- #
def _norm(name: str) -> str:
    return re.sub(r"[^a-z0-9]", "", name.lower())


def _read_csv(content: bytes) -> pa.Table:
    return pacsv.read_csv(
        io.BytesIO(content),
        read_options=pacsv.ReadOptions(block_size=1 << 26),
        parse_options=pacsv.ParseOptions(newlines_in_values=False),
        convert_options=pacsv.ConvertOptions(strings_can_be_null=True),
    )


def _string_table(t: pa.Table, mapping: dict[str, list[str]]) -> pa.Table:
    """Project `t` onto the canonical columns in `mapping`, every column cast to
    string. Source columns are matched by normalised name (so 'StartStation Id'
    and 'Start station number' both resolve); a canonical column with no source
    match becomes an all-null string column. The output schema is identical for
    every file of an asset, so the parquet batches glob-union cleanly downstream.
    """
    norm_to_col: dict[str, str] = {}
    for name in t.column_names:
        norm_to_col.setdefault(_norm(name), name)
    n = t.num_rows
    cols, names = [], []
    for out_name, candidates in mapping.items():
        src = next((norm_to_col[c] for c in candidates if c in norm_to_col), None)
        cols.append(pa.nulls(n, pa.string()) if src is None else pc.cast(t.column(src), pa.string()))
        names.append(out_name)
    return pa.table(cols, names=names)


JOURNEY_MAP = {
    "rental_id": ["rentalid", "number"],
    "duration": ["duration", "totalduration"],
    "start_date": ["startdate"],
    "end_date": ["enddate"],
    "start_station_id": ["startstationid", "startstationnumber"],
    "start_station_name": ["startstationname", "startstation"],
    "end_station_id": ["endstationid", "endstationnumber"],
    "end_station_name": ["endstationname", "endstation"],
}

COUNTS_MAP = {
    "wave": ["wave"],
    "site_id": ["siteid"],
    "date": ["date"],
    "weather": ["weather"],
    "time": ["time"],
    "day": ["day"],
    "round": ["round"],
    "direction": ["direction"],
    "path": ["path"],
    "mode": ["mode"],
    "count": ["count"],
}

LOCATIONS_MAP = {
    "site_id": ["siteid"],
    "location_description": ["locationdescription"],
    "borough": ["borough"],
    "functional_area": ["functionalareaformonitoring"],
    "road_type": ["roadtype"],
    "strategic_cio_panel": ["isitonthestrategicciopanel"],
    "old_site_id": ["oldsiteidlegacy"],
    "easting": ["eastingukgrid"],
    "northing": ["northingukgrid"],
    "latitude": ["latitude"],
    "longitude": ["longitude"],
}


def _parse_journeys(content: bytes, key: str) -> pa.Table:
    return _string_table(_read_csv(content), JOURNEY_MAP)


def _parse_counts(content: bytes, key: str) -> pa.Table:
    return _string_table(_read_csv(content), COUNTS_MAP)


def _parse_locations(content: bytes) -> pa.Table:
    return _string_table(_read_csv(content), LOCATIONS_MAP)


# --------------------------------------------------------------------------- #
# Batched, resumable ingestion of one bucket folder
# --------------------------------------------------------------------------- #
def _batch_key(key: str, prefix: str) -> str:
    rel = key[len(prefix):] if key.startswith(prefix) else key
    rel = re.sub(r"\.[^.]*$", "", rel)  # drop extension
    return re.sub(r"[^a-z0-9]+", "-", rel.lower()).strip("-")


def _ingest(node_id: str, prefix: str, file_filter, parser) -> None:
    files = [(k, s) for (k, s) in _s3_list(prefix) if file_filter(k)]
    # Dedupe filename variants (TfL publishes some files both with and without
    # spaces in the name — same bytes, two keys).
    seen, uniq = set(), []
    for k, s in sorted(files):
        nk = _norm(k.rsplit("/", 1)[-1])
        if nk in seen:
            continue
        seen.add(nk)
        uniq.append((k, s))
    if not uniq:
        raise RuntimeError(f"{node_id}: no source files matched under {prefix!r}")

    state = load_state(node_id)
    if state.get("schema_version") != STATE_VERSION:
        state = {"schema_version": STATE_VERSION, "done": []}
    done = set(state.get("done", []))

    for k, _size in uniq:
        if k in done:
            continue
        content = _get_bytes(CDN + urllib.parse.quote(k, safe="/"))
        table = parser(content, k)
        if table is not None and table.num_rows > 0:
            save_raw_parquet(table, node_id, fragment=_batch_key(k, prefix))
        done.add(k)
        state["done"] = sorted(done)
        save_state(node_id, state)  # then advance the watermark


# --------------------------------------------------------------------------- #
# Download fns — one per entity-union entry
# --------------------------------------------------------------------------- #
def fetch_active_travel_counts(node_id: str) -> None:
    # Quarterly count CSVs are named "<year> Q.. (..)-<region>.csv"; the leading
    # 4-digit year distinguishes them from the reference files ("1 Monitoring
    # locations.csv", "2 Availability matrix.csv") and the methodology PDFs.
    def is_count_csv(k: str) -> bool:
        base = k.rsplit("/", 1)[-1]
        return k.lower().endswith(".csv") and re.match(r"\d{4}", base) is not None

    _ingest(node_id, "ActiveTravelCountsProgramme/", is_count_csv, _parse_counts)


def fetch_active_travel_monitoring_locations(node_id: str) -> None:
    content = _get_bytes(CDN + urllib.parse.quote(MONITORING_LOCATIONS_KEY, safe="/"))
    table = _parse_locations(content)
    if table.num_rows == 0:
        raise RuntimeError("monitoring locations CSV contained no rows")
    save_raw_parquet(table, node_id)


DOWNLOAD_SPECS = [
    NodeSpec(id=f"{SLUG}-active-travel-counts", fn=fetch_active_travel_counts, kind="download"),
    NodeSpec(
        id=f"{SLUG}-active-travel-monitoring-locations",
        fn=fetch_active_travel_monitoring_locations,
        kind="download",
    ),
]
