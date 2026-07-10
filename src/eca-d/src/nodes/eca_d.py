"""ECA&D connector — daily blended station observations + the station index.

Mechanism ('bulk_zip_ascii'): one stable S3 ZIP per element of the canonical
*blended* variant —
    https://knmi-ecad-assets-prd.s3.amazonaws.com/download/ECA_blend_{elem}.zip
Each ZIP holds one fixed-format ASCII file per station (a prose header, then a
`STAID, SOUID, DATE, <ELEM>, Q_<ELEM>` block; DATE is YYYYMMDD, value is an
integer in the element's documented scale, -9999 = missing, Q is 0/1/9). The
station index is the small standalone `download/stations.txt`, fetched directly
rather than unpacking an ~800 MB ZIP to read it.

Strategy: stateless full re-pull (shape 1). There is no incremental query — each
refresh re-fetches the whole ZIP and overwrites; ECA&D revises history, so a
stored watermark would silently skip corrections. The ZIPs are huge (rr ~1.8 GB,
tg/tn/tx/sd ~800 MB, several GB uncompressed), so we never hold a whole element
in memory or extract a whole ZIP at once: stream the ZIP to a temp file, extract
station files in bounded chunks to disk, parse each chunk with DuckDB's CSV
reader (`ignore_errors` skips the prose header lines and the sentinel rows), and
stream the result into one row-group-streamed parquet asset. Missing rows
(value = -9999) are dropped — they carry no observation. `MAINTAIN_SPECS` skips
an element whose S3 object is byte-for-byte unchanged (ETag/Last-Modified) so a
periodic refresh does not re-pull ~8.8 GB when nothing moved.

Values are stored as the raw ECA&D integer (lossless); the element-specific unit
scale is applied downstream in the compiled transform, where it is reconciled
against the archive's own `elements.txt`.
"""
import os
import shutil
import tempfile
import zipfile

import duckdb
import pyarrow as pa
from subsets_utils import (
    MaintainSpec,
    NodeSpec,
    get,
    get_client,
    raw_asset_exists,
    raw_parquet_writer,
    record_source_signature,
    save_raw_parquet,
    source_unchanged,
    transient_retry,
)

BASE = "https://knmi-ecad-assets-prd.s3.amazonaws.com/download/"

# The 13 blended elements. The scale/unit here is documentation for the model
# stage (which reconciles it against the archive's elements.txt); the download
# stores the raw integer value unscaled.
ELEMENTS = {
    "cc": ("Cloud cover", 1, "oktas"),
    "dd": ("Wind direction", 1, "degrees"),
    "fg": ("Mean wind speed", 10, "m/s"),
    "fx": ("Maximum wind gust", 10, "m/s"),
    "hu": ("Relative humidity", 1, "%"),
    "pp": ("Sea-level pressure", 10, "hPa"),
    "qq": ("Global radiation", 1, "W/m2"),
    "rr": ("Precipitation amount", 10, "mm"),
    "sd": ("Snow depth", 1, "cm"),
    "ss": ("Sunshine duration", 10, "hours"),
    "tg": ("Mean temperature", 10, "degC"),
    "tn": ("Minimum temperature", 10, "degC"),
    "tx": ("Maximum temperature", 10, "degC"),
}

# Uniform observation schema across every element table.
_OBS_SCHEMA = pa.schema([
    ("station_id", pa.int32()),   # STAID
    ("source_id", pa.int32()),    # SOUID (underlying series)
    ("date", pa.date32()),        # observation day
    ("value", pa.int32()),        # raw integer-scaled value (scaled in transform)
    ("quality", pa.int8()),       # 0=valid, 1=suspect (9=missing rows are dropped)
])

_STATION_FILES_PER_CHUNK = 300  # bounds peak temp-dir disk to a few hundred MB


@transient_retry()
def _download_to(url: str, dest: str) -> None:
    """Stream a (large) URL to a local file through the configured client."""
    with get_client().stream("GET", url, timeout=600.0) as resp:
        resp.raise_for_status()
        with open(dest, "wb") as fh:
            for chunk in resp.iter_bytes(chunk_size=1 << 20):
                fh.write(chunk)


def _parse_chunk_into(con, members_dir: str, writer) -> None:
    """Parse every station file in `members_dir` and stream valid rows to `writer`."""
    glob = os.path.join(members_dir, "*.txt").replace("\\", "/")
    sql = f"""
        SELECT
            CAST(staid AS INTEGER) AS station_id,
            CAST(souid AS INTEGER) AS source_id,
            make_date(d // 10000, (d // 100) % 100, d % 100) AS date,
            CAST(val AS INTEGER)   AS value,
            CAST(q AS TINYINT)     AS quality
        FROM read_csv(
            '{glob}',
            header=false,
            columns={{'staid':'INTEGER','souid':'INTEGER','d':'INTEGER','val':'INTEGER','q':'INTEGER'}},
            delim=',', auto_detect=false, ignore_errors=true,
            null_padding=true, strict_mode=false
        )
        WHERE val IS NOT NULL AND val <> -9999
          AND staid IS NOT NULL AND souid IS NOT NULL AND d IS NOT NULL
          AND d BETWEEN 17000101 AND 30000101
    """
    reader = con.execute(sql).fetch_record_batch(1_000_000)
    for batch in reader:
        if batch.num_rows:
            writer.write_table(pa.Table.from_batches([batch]).cast(_OBS_SCHEMA))


def fetch_element(node_id: str) -> None:
    """Download one element's blended ZIP and publish a long observations table."""
    elem = node_id[len("eca-d-blend-"):]
    if elem not in ELEMENTS:
        raise ValueError(f"unknown element in node id {node_id!r}")
    url = f"{BASE}ECA_blend_{elem}.zip"
    prefix = f"{elem.upper()}_"

    work = tempfile.mkdtemp(prefix=f"ecad_{elem}_")
    zip_path = os.path.join(work, "data.zip")
    con = duckdb.connect()
    try:
        _download_to(url, zip_path)
        with zipfile.ZipFile(zip_path) as zf:
            members = [
                n for n in zf.namelist()
                if os.path.basename(n).upper().startswith(prefix)
                and n.lower().endswith(".txt")
            ]
            if not members:
                raise AssertionError(f"no '{prefix}*' station files found in {url}")
            with raw_parquet_writer(node_id, _OBS_SCHEMA) as writer:
                for i in range(0, len(members), _STATION_FILES_PER_CHUNK):
                    chunk = members[i:i + _STATION_FILES_PER_CHUNK]
                    cdir = os.path.join(work, "chunk")
                    os.makedirs(cdir, exist_ok=True)
                    for name in chunk:
                        target = os.path.join(cdir, os.path.basename(name))
                        with zf.open(name) as src, open(target, "wb") as out:
                            shutil.copyfileobj(src, out)
                    _parse_chunk_into(con, cdir, writer)
                    shutil.rmtree(cdir, ignore_errors=True)
    finally:
        con.close()
        shutil.rmtree(work, ignore_errors=True)
    record_source_signature(node_id, url)


def _dms_to_decimal(s: str) -> float:
    s = s.strip()
    sign = -1.0 if s.startswith("-") else 1.0
    deg, minute, second = s.lstrip("+-").split(":")
    return sign * (int(deg) + int(minute) / 60.0 + int(second) / 3600.0)


def fetch_stations(node_id: str) -> None:
    """Download and parse the station metadata reference table."""
    url = f"{BASE}stations.txt"
    resp = get(url, timeout=120.0)
    resp.raise_for_status()
    lines = resp.content.decode("latin-1").splitlines()
    start = next(
        i for i, ln in enumerate(lines)
        if ln.startswith("STAID,") and "STANAME" in ln
    )

    station_id, name, country, lat, lon, elevation = [], [], [], [], [], []
    for ln in lines[start + 1:]:
        if not ln.strip():
            continue
        parts = ln.split(",")
        if len(parts) < 6:
            continue
        # lat/lon/elevation are the last three fields; the name itself could in
        # principle contain a comma, so index the fixed tail from the right.
        hght = parts[-1].strip()
        station_id.append(int(parts[0]))
        name.append(",".join(parts[1:-4]).strip())
        country.append(parts[-4].strip())
        lat.append(_dms_to_decimal(parts[-3]))
        lon.append(_dms_to_decimal(parts[-2]))
        elevation.append(int(hght) if hght and hght != "-9999" else None)

    if not station_id:
        raise AssertionError(f"parsed 0 stations from {url}")

    table = pa.table(
        {
            "station_id": pa.array(station_id, pa.int32()),
            "station_name": pa.array(name, pa.string()),
            "country": pa.array(country, pa.string()),
            "latitude": pa.array(lat, pa.float64()),
            "longitude": pa.array(lon, pa.float64()),
            "elevation_m": pa.array(elevation, pa.int32()),
        }
    )
    save_raw_parquet(table, node_id)
    record_source_signature(node_id, url, response=resp)


DOWNLOAD_SPECS = [
    NodeSpec(id=f"eca-d-blend-{elem}", fn=fetch_element, kind="download")
    for elem in ELEMENTS
] + [
    NodeSpec(id="eca-d-stations", fn=fetch_stations, kind="download"),
]

MAINTAIN_SPECS = [
    MaintainSpec(
        asset_id=f"eca-d-blend-{elem}",
        description=(
            "ECA&D predefined blended daily series, refreshed periodically "
            "(https://www.ecad.eu/dailydata/predefinedseries.php); skip when the "
            "S3 object's ETag/Last-Modified is unchanged"
        ),
        check=(lambda aid, e=elem: source_unchanged(aid, f"{BASE}ECA_blend_{e}.zip")
               and raw_asset_exists(aid, "parquet")),
    )
    for elem in ELEMENTS
] + [
    MaintainSpec(
        asset_id="eca-d-stations",
        description=(
            "ECA&D station index (stations.txt), refreshed alongside the series; "
            "skip when the S3 object is unchanged (ETag/Last-Modified)"
        ),
        check=lambda aid: source_unchanged(aid, f"{BASE}stations.txt")
        and raw_asset_exists(aid, "parquet"),
    ),
]
