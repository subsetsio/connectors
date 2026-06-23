"""ECA&D connector — daily station observations + station reference.

Mechanism: bulk ASCII ZIPs ('bulk_zip_ascii'). One stable S3 ZIP per element of
the canonical *blended* variant:
    https://knmi-ecad-assets-prd.s3.amazonaws.com/download/ECA_blend_{elem}.zip
Each ZIP holds one fixed-format ASCII file per station (a prose header, then a
`STAID, SOUID, DATE, <ELEM>, Q_<ELEM>` block; DATE is YYYYMMDD, value is an
integer in the element's documented scale, -9999 = missing, Q is 0/1/9). The
station metadata table is published from the standalone `download/stations.txt`.

Strategy: stateless full re-pull (shape 1). There is no incremental query — each
refresh re-fetches the whole ZIP and overwrites. The ZIPs are huge (hundreds of
MB compressed, up to ~15 GB uncompressed for temperature), so we never hold a
whole element in memory or extract a whole ZIP to disk at once: we stream the ZIP
to a temp file, extract station files in bounded chunks, parse each chunk with
DuckDB's CSV reader (ignore_errors skips the prose header lines), drop missing
values, and stream the result into one row-group-streamed parquet asset.

Values are stored as the raw ECA&D integer (lossless); the transform divides by
the documented per-element scale to publish physical units.
"""
import os
import re
import shutil
import tempfile
import zipfile

import duckdb
import pyarrow as pa
from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    get_client,
    save_raw_parquet,
    raw_parquet_writer,
    transient_retry,
)

BASE = "https://knmi-ecad-assets-prd.s3.amazonaws.com/download/"

# element code -> (human name, integer scale divisor, physical unit)
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

_OBS_SCHEMA = pa.schema([
    ("station_id", pa.int32()),
    ("source_id", pa.int32()),
    ("date", pa.int32()),    # YYYYMMDD, decoded to DATE in the transform
    ("value", pa.int32()),   # raw ECA&D integer, scaled in the transform
    ("quality", pa.int8()),  # 0=valid, 1=suspect
])

_STATION_FILES_PER_CHUNK = 500  # bounds peak temp-dir disk to ~1 GB


@transient_retry()
def _download_to(url: str, dest: str) -> None:
    """Stream a (large) URL to a local file, restarting cleanly on transient errors."""
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
            CAST(d     AS INTEGER) AS date,
            CAST(val   AS INTEGER) AS value,
            CAST(q     AS TINYINT) AS quality
        FROM read_csv(
            '{glob}',
            header=false,
            columns={{'staid':'INTEGER','souid':'INTEGER','d':'INTEGER','val':'INTEGER','q':'TINYINT'}},
            delim=',', auto_detect=false, ignore_errors=true,
            null_padding=true, strict_mode=false
        )
        WHERE val IS NOT NULL AND val <> -9999 AND staid IS NOT NULL AND d IS NOT NULL
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
    prefix = f"{elem.upper()}_STAID"

    work = tempfile.mkdtemp(prefix=f"ecad_{elem}_")
    zip_path = os.path.join(work, "data.zip")
    con = duckdb.connect()
    try:
        _download_to(url, zip_path)
        with zipfile.ZipFile(zip_path) as zf:
            members = [
                n for n in zf.namelist()
                if n.startswith(prefix) and n.endswith(".txt")
            ]
            if not members:
                raise AssertionError(f"no station files found in {url}")
            with raw_parquet_writer(node_id, _OBS_SCHEMA) as writer:
                for i in range(0, len(members), _STATION_FILES_PER_CHUNK):
                    chunk = members[i:i + _STATION_FILES_PER_CHUNK]
                    cdir = os.path.join(work, "chunk")
                    os.makedirs(cdir, exist_ok=True)
                    for name in chunk:
                        # flatten any path component; these archives are flat anyway
                        target = os.path.join(cdir, os.path.basename(name))
                        with zf.open(name) as src, open(target, "wb") as out:
                            shutil.copyfileobj(src, out)
                    _parse_chunk_into(con, cdir, writer)
                    shutil.rmtree(cdir, ignore_errors=True)
    finally:
        con.close()
        shutil.rmtree(work, ignore_errors=True)


def _dms_to_decimal(s: str) -> float:
    s = s.strip()
    sign = -1.0 if s.startswith("-") else 1.0
    deg, minute, second = s.lstrip("+-").split(":")
    return sign * (int(deg) + int(minute) / 60.0 + int(second) / 3600.0)


def fetch_stations(node_id: str) -> None:
    """Download and parse the station metadata reference table."""
    resp = get(f"{BASE}stations.txt", timeout=120.0)
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
        # latitude/longitude/elevation are the last three fields; the name itself
        # could (in principle) contain a comma, so index from the right.
        hght = parts[-1].strip()
        station_id.append(int(parts[0]))
        name.append(",".join(parts[1:-4]).strip())
        country.append(parts[-4].strip())
        lat.append(_dms_to_decimal(parts[-3]))
        lon.append(_dms_to_decimal(parts[-2]))
        elevation.append(int(hght) if hght and hght != "-9999" else None)

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


DOWNLOAD_SPECS = [
    NodeSpec(id=f"eca-d-blend-{elem}", fn=fetch_element, kind="download")
    for elem in ELEMENTS
] + [
    NodeSpec(id="eca-d-stations", fn=fetch_stations, kind="download"),
]


def _element_transform(elem: str, scale: int, unit: str) -> SqlNodeSpec:
    dl = f"eca-d-blend-{elem}"
    return SqlNodeSpec(
        id=f"{dl}-transform",
        deps=[dl],
        sql=f"""
            SELECT
                station_id,
                source_id,
                make_date(date // 10000, (date // 100) % 100, date % 100) AS date,
                CAST(value AS DOUBLE) / {scale}.0 AS value,
                '{unit}' AS unit,
                quality
            FROM "{dl}"
        """,
    )


TRANSFORM_SPECS = [
    _element_transform(elem, scale, unit)
    for elem, (_name, scale, unit) in ELEMENTS.items()
] + [
    SqlNodeSpec(
        id="eca-d-stations-transform",
        deps=["eca-d-stations"],
        sql="""
            SELECT
                station_id,
                station_name,
                country,
                latitude,
                longitude,
                elevation_m
            FROM "eca-d-stations"
        """,
    ),
]
