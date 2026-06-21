"""FBI Crime Data Explorer (CDE) connector.

Source: the FBI's UCR bulk-download catalog, enumerated by the CDE's own static
JSON manifest (no auth):
    https://cde.ucr.cjis.gov/LATEST/webapp/assets/JSON/downloads/downloads.json

Each manifest dataset is a curated, full-history file. Some ship as a single
CSV, others as a ZIP bundling one or more data CSVs (plus non-data
readme/pdf/docx members we ignore). The LEOKA "Assaults on Law Enforcement
Officers" ZIP holds two distinct-schema CSVs, published as two tables.

Fetch path (the CDE bulk-download mechanism, per research):
  1. resolve the dataset's current `awsFile` S3 key from the live manifest
     (so a year-bump in the filename, e.g. estimated_crimes_1979_2025.csv,
     is picked up automatically),
  2. GET https://api.usa.gov/crime/fbi/cde/s3/signedurl?key=<awsFile>&API_KEY=<key>
     -> { "<awsFile>": "<presigned GovCloud-S3 url>" },
  3. GET that presigned URL for the CSV/ZIP bytes (the S3 GET needs no key),
  4. select the data CSV(s) — ZIP datasets are matched by member-name PREFIX
     (the manifest's listed member names are stale and the real members carry
     year-range suffixes, e.g. LEOKA_ASSAULT_TIME_WEAPON_INJURY_1995_2024.csv);
     some datasets (LEOKA assignment/activity) are split across several
     year-range CSVs sharing one schema, which we union into one table,
  5. parse the CSV(s) with DuckDB (whole-file type sniff via sample_size=-1,
     literal "NULL"/"NA" tokens treated as null) and save typed Parquet.

Parsing in DuckDB up front — rather than leaving raw CSV for the transform's
view to auto-read — is deliberate: the transform view uses read_csv_auto with
default options (20480-row sample), which mis-types columns whose "NULL" string
values appear only deep in the file. A whole-file sniff here types each column
correctly (or falls back to VARCHAR on genuine mixing) and never hard-fails, so
the connector still carries no hand-written per-dataset schema.

API key: every api.usa.gov/crime/fbi call needs a data.gov key. We read
FBI_CRIME_DATA_API_KEY from the environment and fall back to the public
"DEMO_KEY" (sufficient for this connector's ~9 signedurl calls per refresh,
which sit well under DEMO_KEY's per-IP hourly cap; a registered key from
https://api.data.gov/signup/ lifts the cap). Same optional-key pattern as the
senate-lda connector.

Refresh model: stateless full re-pull. Each file is a complete historical
snapshot re-published in full every run; there is no incremental query on the
bulk path and no stored watermark, so revisions are picked up for free.
"""

from __future__ import annotations

import io
import os
import tempfile
import zipfile

import duckdb
import httpx
from tenacity import (
    retry,
    retry_if_exception,
    stop_after_attempt,
    wait_exponential,
)

from subsets_utils import NodeSpec, SqlNodeSpec, get, save_raw_parquet

MANIFEST_URL = "https://cde.ucr.cjis.gov/LATEST/webapp/assets/JSON/downloads/downloads.json"
SIGNEDURL_ENDPOINT = "https://api.usa.gov/crime/fbi/cde/s3/signedurl"


def _api_key() -> str:
    return os.environ.get("FBI_CRIME_DATA_API_KEY", "DEMO_KEY")


# entity_id (collect/rank id) -> (manifest dataset id, ZIP member-name prefix).
# The prefix is None for datasets whose awsFile is itself a single data CSV.
# For ZIP datasets the prefix selects member CSVs by basename (the real member
# names carry year-range suffixes the manifest doesn't list); ALL .csv members
# matching the prefix are unioned into one table — usually one file, but LEOKA
# assignment/activity is split across several year-range CSVs sharing a schema.
# The two LEOKA entries point at the same ZIP via disjoint prefixes.
ENTITY_MAP = {
    "srs": ("srs", None),
    "pe": ("pe", None),
    "ucr-participation": ("ucr-participation", None),
    "territories": ("territories", None),
    "hc": ("hc", "Hate_Crime"),
    "ht": ("ht", "HT_"),
    "ct": ("ct", "CT_"),
    "le-assaults-leoka-assault-time-weapon-injury": (
        "le-assaults",
        "LEOKA_ASSAULT_TIME_WEAPON_INJURY",
    ),
    "le-assaults-leoka-assignment-activity": (
        "le-assaults",
        "LEOKA_ASSIGNMENT_ACTIVITY",
    ),
}

# Tokens the FBI CSVs use for missing values (besides empty string). Treated as
# NULL so numeric columns sniff as numbers instead of falling back to VARCHAR.
_NULL_TOKENS = ["", "NULL", "null", "NA", "N/A", "n/a"]

_TRANSIENT_EXC = (
    httpx.ConnectError,
    httpx.ConnectTimeout,
    httpx.ReadTimeout,
    httpx.WriteTimeout,
    httpx.PoolTimeout,
    httpx.RemoteProtocolError,
    httpx.ProxyError,
)


def _is_transient(exc: BaseException) -> bool:
    if isinstance(exc, _TRANSIENT_EXC):
        return True
    if isinstance(exc, httpx.HTTPStatusError):
        code = exc.response.status_code
        # 429 = data.gov rate cap (DEMO_KEY); 5xx = server. Both worth a retry.
        return code == 429 or 500 <= code < 600
    return False


@retry(
    retry=retry_if_exception(_is_transient),
    stop=stop_after_attempt(6),
    wait=wait_exponential(min=4, max=120),
    reraise=True,
)
def _get_json(url: str, **params):
    resp = get(url, params=params or None, timeout=(10.0, 120.0))
    resp.raise_for_status()
    return resp.json()


@retry(
    retry=retry_if_exception(_is_transient),
    stop=stop_after_attempt(6),
    wait=wait_exponential(min=4, max=120),
    reraise=True,
)
def _get_bytes(url: str) -> bytes:
    resp = get(url, timeout=(10.0, 300.0))
    resp.raise_for_status()
    return resp.content


def _manifest() -> list:
    data = _get_json(MANIFEST_URL)
    if not isinstance(data, list) or not data:
        raise ValueError(f"manifest at {MANIFEST_URL} not a non-empty list")
    return data


def _aws_file_for(dataset_id: str) -> str:
    for rec in _manifest():
        if rec.get("id") == dataset_id:
            aws = rec.get("awsFile")
            if not aws:
                raise ValueError(f"manifest dataset {dataset_id!r} has no awsFile")
            return aws
    raise ValueError(f"dataset {dataset_id!r} not present in CDE download manifest")


def _signed_url(aws_file: str) -> str:
    payload = _get_json(SIGNEDURL_ENDPOINT, key=aws_file, API_KEY=_api_key())
    if not isinstance(payload, dict) or not payload:
        raise ValueError(f"signedurl for {aws_file!r} returned no url: {payload!r}")
    # Response is { "<awsFile>": "<presigned url>" }; tolerate key variance.
    url = payload.get(aws_file) or next(iter(payload.values()))
    if not isinstance(url, str) or not url.startswith("https://"):
        raise ValueError(f"signedurl for {aws_file!r} gave bad url: {url!r}")
    return url


def _extract_members(content: bytes, prefix: str) -> list[bytes]:
    """Return the bytes of every .csv member whose basename starts with prefix."""
    with zipfile.ZipFile(io.BytesIO(content)) as zf:
        names = zf.namelist()
        matched = [
            n for n in names
            if n.split("/")[-1].startswith(prefix) and n.lower().endswith(".csv")
        ]
        if not matched:
            raise FileNotFoundError(
                f"no .csv member with prefix {prefix!r} in zip; members={names}"
            )
        return [zf.read(n) for n in sorted(matched)]


def _csvs_to_parquet(csv_blobs: list[bytes]):
    """Parse one-or-more CSVs (sharing a schema) into a single Arrow table.

    DuckDB sniffs types over the WHOLE file (sample_size=-1) and treats the
    FBI's literal null tokens as NULL, so numeric columns stay numeric and a
    genuinely mixed column degrades to VARCHAR rather than raising. Multiple
    blobs (year-range partitions of one dataset) are unioned by column name.
    """
    paths = []
    con = duckdb.connect()
    try:
        for blob in csv_blobs:
            tf = tempfile.NamedTemporaryFile(suffix=".csv", delete=False)
            tf.write(blob)
            tf.close()
            paths.append(tf.name)
        rel = con.execute(
            "SELECT * FROM read_csv(?, sample_size=-1, header=true, "
            "all_varchar=false, union_by_name=true, nullstr=?)",
            [paths, _NULL_TOKENS],
        )
        return rel.fetch_arrow_table()
    finally:
        con.close()
        for p in paths:
            try:
                os.unlink(p)
            except OSError:
                pass


def fetch_one(node_id: str) -> None:
    asset = node_id  # the runtime passes the spec id; it IS the asset name
    entity_id = node_id[len("fbi-"):]
    dataset_id, prefix = ENTITY_MAP[entity_id]

    aws_file = _aws_file_for(dataset_id)
    content = _get_bytes(_signed_url(aws_file))

    if aws_file.lower().endswith(".zip"):
        if not prefix:
            raise ValueError(f"{entity_id}: zip dataset but no member prefix configured")
        csv_blobs = _extract_members(content, prefix)
    else:
        csv_blobs = [content]

    if not any(blob.strip() for blob in csv_blobs):
        raise ValueError(f"{entity_id}: downloaded CSV is empty (aws_file={aws_file})")

    table = _csvs_to_parquet(csv_blobs)
    if table.num_rows == 0:
        raise ValueError(f"{entity_id}: parsed 0 rows (aws_file={aws_file})")

    save_raw_parquet(table, asset)


DOWNLOAD_SPECS = [
    NodeSpec(id=f"fbi-{eid}", fn=fetch_one, kind="download")
    for eid in ENTITY_MAP
]

# Thin publish pass: DuckDB read_csv_auto (wired by the runtime view) infers the
# header and column types from the FBI's stable CSV; we publish it verbatim.
TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{s.id}-transform",
        deps=[s.id],
        sql=f'SELECT * FROM "{s.id}"',
    )
    for s in DOWNLOAD_SPECS
]
