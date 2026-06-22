"""Transport for London connector.

Four published subsets, two access surfaces (both anonymous):

* PRIMARY — the public S3 bucket ``cycling.data.tfl.gov.uk`` (mechanism
  ``cycling_s3``). Folders are enumerated via the S3 ListBucketV2 XML at the
  ``s3-eu-west-1.amazonaws.com`` origin; individual files are pulled by stable
  key from the CDN host. CSV column layouts drift across eras (the Santander
  cycle-hire extract was re-schemed in ~2024), so every fetch normalises to a
  fixed all-string parquet schema and the real typing happens in the SQL
  transform. The cycle-counter files carry a ``.xls`` extension but are plain
  108-column CSVs of per-vehicle records.
* SECONDARY — the Unified API (``unified_api_rest``), used only for
  ``/AccidentStats/{year}`` (full-year road-casualty JSON, no key required).

The three bucket-backed assets are large and made of immutable historical
files, so they ingest file-by-file (one parquet batch per source file) and keep
a per-asset watermark of completed keys in state — a run interrupted partway
resumes instead of restarting, and newly-published files are picked up on the
next refresh. AccidentStats is small (~15 years) and re-pulled in full each run.
"""

import datetime
import io
import re
import urllib.parse

import pyarrow as pa
import pyarrow.compute as pc
import pyarrow.csv as pacsv

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    load_state,
    save_raw_parquet,
    save_state,
    transient_retry,
)

SLUG = "transport-for-london"
STATE_VERSION = 1

S3_ORIGIN = "https://s3-eu-west-1.amazonaws.com/cycling.data.tfl.gov.uk/"
CDN = "https://cycling.data.tfl.gov.uk/"
ACCIDENT_API = "https://api.tfl.gov.uk/AccidentStats"
# Documented earliest AccidentStats year; the upper bound is discovered live by
# probing each year up to the current one (the API 400s on out-of-range years),
# so this is not a hardcoded coverage window.
ACCIDENT_MIN_YEAR = 2005


# --------------------------------------------------------------------------- #
# HTTP helpers
# --------------------------------------------------------------------------- #
@transient_retry()
def _get_bytes(url: str) -> bytes:
    resp = get(url, timeout=(10.0, 300.0))
    resp.raise_for_status()
    return resp.content


@transient_retry()
def _accident_year(year: int):
    """Full-year AccidentStats payload, or None when the year is out of range.

    The API answers an unavailable year with HTTP 400 (a permanent signal, not a
    transient error) — treat that as 'no data for this year' rather than raising.
    """
    resp = get(f"{ACCIDENT_API}/{year}", timeout=(10.0, 300.0))
    if resp.status_code == 400:
        return None
    resp.raise_for_status()
    return resp.json()


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

COUNTERS_MAP = {
    "site_number": ["sitenumber"],
    "site_id": ["siteid"],
    "serial": ["serialnumber"],
    "date": ["date"],
    "time_string": ["timestring"],
    "lane": ["lane"],
    "direction": ["direction"],
    "direction_number": ["directionnumber"],
    "speed": ["speed"],
    "speed_mph": ["speedmph"],
    "vclass": ["class"],
    "length": ["length"],
}


def _parse_journeys(content: bytes, key: str) -> pa.Table:
    return _string_table(_read_csv(content), JOURNEY_MAP)


def _parse_counts(content: bytes, key: str) -> pa.Table:
    return _string_table(_read_csv(content), COUNTS_MAP)


def _parse_counters(content: bytes, key: str) -> pa.Table:
    return _string_table(_read_csv(content), COUNTERS_MAP)


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
            save_raw_parquet(table, f"{node_id}-{_batch_key(k, prefix)}")  # raw first
        done.add(k)
        state["done"] = sorted(done)
        save_state(node_id, state)  # then advance the watermark


# --------------------------------------------------------------------------- #
# Download fns — one per entity-union entry
# --------------------------------------------------------------------------- #
ACCIDENT_SCHEMA = pa.schema([
    ("accident_id", pa.int64()),
    ("year", pa.int32()),
    ("date", pa.string()),
    ("lat", pa.float64()),
    ("lon", pa.float64()),
    ("location", pa.string()),
    ("severity", pa.string()),
    ("borough", pa.string()),
    ("n_casualties", pa.int32()),
    ("n_vehicles", pa.int32()),
])


def fetch_accident_stats(node_id: str) -> None:
    this_year = datetime.datetime.now(datetime.timezone.utc).year
    rows = []
    for year in range(ACCIDENT_MIN_YEAR, this_year + 1):
        data = _accident_year(year)
        if not data:
            continue
        for rec in data:
            rows.append({
                "accident_id": rec.get("id"),
                "year": year,
                "date": rec.get("date"),
                "lat": rec.get("lat"),
                "lon": rec.get("lon"),
                "location": rec.get("location"),
                "severity": rec.get("severity"),
                "borough": rec.get("borough"),
                "n_casualties": len(rec.get("casualties") or []),
                "n_vehicles": len(rec.get("vehicles") or []),
            })
    if not rows:
        raise RuntimeError("AccidentStats returned no data for any probed year")
    save_raw_parquet(pa.Table.from_pylist(rows, schema=ACCIDENT_SCHEMA), node_id)


def fetch_cycle_hire_journeys(node_id: str) -> None:
    _ingest(node_id, "usage-stats/", lambda k: k.lower().endswith(".csv"), _parse_journeys)


def fetch_active_travel_counts(node_id: str) -> None:
    # Quarterly count CSVs are named "<year> Q.. (..)-<region>.csv"; the leading
    # 4-digit year distinguishes them from the reference files ("1 Monitoring
    # locations.csv", "2 Availability matrix.csv") and the methodology PDFs.
    def is_count_csv(k: str) -> bool:
        base = k.rsplit("/", 1)[-1]
        return k.lower().endswith(".csv") and re.match(r"\d{4}", base) is not None

    _ingest(node_id, "ActiveTravelCountsProgramme/", is_count_csv, _parse_counts)


def fetch_cycle_counters(node_id: str) -> None:
    # The ".xls" files are actually comma-delimited CSVs of per-vehicle records.
    _ingest(node_id, "CycleCounters/", lambda k: k.lower().endswith(".xls"), _parse_counters)


DOWNLOAD_SPECS = [
    NodeSpec(id=f"{SLUG}-accident-stats", fn=fetch_accident_stats, kind="download"),
    NodeSpec(id=f"{SLUG}-active-travel-counts", fn=fetch_active_travel_counts, kind="download"),
    NodeSpec(id=f"{SLUG}-cycle-counters", fn=fetch_cycle_counters, kind="download"),
    NodeSpec(id=f"{SLUG}-cycle-hire-journeys", fn=fetch_cycle_hire_journeys, kind="download"),
]


# --------------------------------------------------------------------------- #
# Transforms — one published Delta table per subset
# --------------------------------------------------------------------------- #
TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{SLUG}-accident-stats-transform",
        deps=[f"{SLUG}-accident-stats"],
        sql=f'''
            SELECT
                CAST(accident_id AS BIGINT)                                   AS accident_id,
                CAST(year AS INTEGER)                                          AS year,
                COALESCE(try_strptime(date, '%Y-%m-%dT%H:%M:%SZ'),
                         try_cast(date AS TIMESTAMP))                          AS occurred_at,
                CAST(lat AS DOUBLE)                                            AS lat,
                CAST(lon AS DOUBLE)                                            AS lon,
                location,
                severity,
                borough,
                CAST(n_casualties AS INTEGER)                                  AS n_casualties,
                CAST(n_vehicles AS INTEGER)                                    AS n_vehicles
            FROM "{SLUG}-accident-stats"
            WHERE accident_id IS NOT NULL
        ''',
    ),
    SqlNodeSpec(
        id=f"{SLUG}-cycle-hire-journeys-transform",
        deps=[f"{SLUG}-cycle-hire-journeys"],
        # Journey-level extracts aggregated to daily trip counts per start
        # station — the publishable statistical time series. Start-date format
        # drifts across eras (DD/MM/YYYY in the legacy extracts, ISO in the 2024+
        # re-scheme), so parse defensively. Duration is omitted: its units/format
        # are inconsistent across eras (seconds vs "14m 30s") and not reconcilable
        # in a thin transform.
        sql=f'''
            WITH parsed AS (
                SELECT
                    CAST(COALESCE(
                        try_strptime(start_date, '%d/%m/%Y %H:%M'),
                        try_strptime(start_date, '%d/%m/%Y %H:%M:%S'),
                        try_strptime(start_date, '%Y-%m-%d %H:%M'),
                        try_strptime(start_date, '%Y-%m-%d %H:%M:%S'),
                        try_cast(start_date AS TIMESTAMP)
                    ) AS DATE)                       AS date,
                    start_station_id,
                    start_station_name
                FROM "{SLUG}-cycle-hire-journeys"
            )
            SELECT
                date,
                start_station_id,
                any_value(start_station_name)        AS start_station_name,
                COUNT(*)                             AS trips
            FROM parsed
            WHERE date IS NOT NULL AND start_station_id IS NOT NULL
            GROUP BY date, start_station_id
        ''',
    ),
    SqlNodeSpec(
        id=f"{SLUG}-active-travel-counts-transform",
        deps=[f"{SLUG}-active-travel-counts"],
        sql=f'''
            SELECT
                wave,
                site_id,
                CAST(COALESCE(try_strptime(date, '%d/%m/%Y'),
                              try_cast(date AS DATE)) AS DATE)  AS date,
                time,
                day,
                direction,
                path,
                mode,
                weather,
                try_cast(count AS BIGINT)                       AS count
            FROM "{SLUG}-active-travel-counts"
            WHERE try_cast(count AS BIGINT) IS NOT NULL
        ''',
    ),
    SqlNodeSpec(
        id=f"{SLUG}-cycle-counters-transform",
        deps=[f"{SLUG}-cycle-counters"],
        sql=f'''
            SELECT
                site_id,
                site_number,
                serial,
                COALESCE(try_strptime(date, '%d/%m/%Y %H:%M:%S'),
                         try_cast(date AS TIMESTAMP))           AS observed_at,
                time_string,
                direction,
                try_cast(direction_number AS INTEGER)           AS direction_number,
                try_cast(speed AS INTEGER)                      AS speed,
                try_cast(speed_mph AS DOUBLE)                   AS speed_mph,
                vclass                                          AS class,
                try_cast(length AS INTEGER)                     AS length
            FROM "{SLUG}-cycle-counters"
            WHERE site_id IS NOT NULL
        ''',
    ),
]
