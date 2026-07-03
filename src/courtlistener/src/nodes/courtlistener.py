"""CourtListener / RECAP bulk-data connector.

Free Law Project publishes the full CourtListener database as quarterly,
bz2-compressed CSV snapshots (PostgreSQL COPY dialect) under the anonymous,
public S3 bucket `com-courtlistener-storage`, one file per relational table at
`bulk-data/<table>-<YYYY-MM-DD>.csv.bz2`. Each table is one publishable subset.

Strategy: stateless full re-pull. Each refresh discovers the newest snapshot
date for the table from the S3 listing, then streams that bz2 file straight to
Parquet without ever landing the whole (uncompressed, multi-GB) file on disk:
HTTP byte stream -> incremental bz2 decompress -> csv parse -> batched Parquet.
Raw is written all-string (the COPY dialect uses '' for NULL, 't'/'f' for bool,
ISO dates, and embeds newlines/smart-quotes in text columns); the SQL transform
does the typing pass. DuckDB cannot read .bz2, which is why decompression lives
here rather than in the transform.

There is no incremental/delta filter on the bulk export (files are full
snapshots), so every refresh re-pulls the whole table — this is the only path;
freshness/skip is the maintain step's concern, not ours.
"""

import bz2
import csv
import io
import re
import sys
import urllib.parse
import xml.etree.ElementTree as ET

import pyarrow as pa

from subsets_utils import NodeSpec, SqlNodeSpec, get, get_client, raw_parquet_writer, transient_retry
from constants import ENTITY_IDS, TABLE_COLUMNS

SLUG = "courtlistener"
BUCKET = "https://com-courtlistener-storage.s3-us-west-2.amazonaws.com"
BASE = f"{BUCKET}/bulk-data/"
S3_NS = "{http://s3.amazonaws.com/doc/2006-03-01/}"
BATCH_ROWS = 50_000
MAX_BATCH_BYTES = 64 << 20  # flush a batch once its text reaches ~64 MiB,
                           # so text-heavy rows can't balloon a fixed-row batch
DL_CHUNK = 1 << 20  # 1 MiB network reads


# --------------------------------------------------------------------------
# Download — stream bz2 CSV straight to all-string Parquet
# --------------------------------------------------------------------------

class _Bz2Reader(io.RawIOBase):
    """A readable binary stream that incrementally bz2-decompresses an iterator
    of compressed byte chunks. Lets csv.reader (via TextIOWrapper) pull from a
    network stream without materializing the full decompressed file."""

    def __init__(self, byte_iter):
        self._it = iter(byte_iter)
        self._dec = bz2.BZ2Decompressor()
        self._buf = b""
        self._eof = False

    def readable(self):
        return True

    def readinto(self, out):
        while not self._buf and not self._eof:
            try:
                chunk = next(self._it)
            except StopIteration:
                self._eof = True
                break
            if chunk:
                self._buf += self._dec.decompress(chunk)
        if not self._buf:
            return 0
        n = min(len(out), len(self._buf))
        out[:n] = self._buf[:n]
        self._buf = self._buf[n:]
        return n


@transient_retry()
def _discover_latest_date(table: str) -> str:
    """Newest YYYY-MM-DD snapshot for this table from the anonymous S3 listing.
    Discovered at runtime so the connector tracks new quarterly releases rather
    than pinning a hardcoded date."""
    prefix = f"bulk-data/{table}-"
    pat = re.compile(rf"^bulk-data/{re.escape(table)}-(\d{{4}}-\d{{2}}-\d{{2}})\.csv\.bz2$")
    base = f"{BUCKET}/?list-type=2&prefix={urllib.parse.quote(prefix)}"
    token = None
    latest = None
    while True:
        url = base + (f"&continuation-token={urllib.parse.quote(token)}" if token else "")
        resp = get(url, timeout=(10.0, 60.0))
        resp.raise_for_status()
        root = ET.fromstring(resp.content)
        for c in root.findall(S3_NS + "Contents"):
            key = c.findtext(S3_NS + "Key") or ""
            m = pat.match(key)
            if m and (latest is None or m.group(1) > latest):
                latest = m.group(1)
        if root.findtext(S3_NS + "IsTruncated") == "true":
            token = root.findtext(S3_NS + "NextContinuationToken")
            if not token:
                break
        else:
            break
    if not latest:
        raise RuntimeError(f"no bulk file found for table {table!r} under {prefix}")
    return latest


def _raise_csv_field_limit():
    """CourtListener opinion/oral-argument tables embed multi-100KB text fields
    (syllabus, headnotes, transcripts) that blow past csv's default 128KB field
    cap. Lift it to the platform max."""
    limit = sys.maxsize
    while True:
        try:
            csv.field_size_limit(limit)
            return
        except OverflowError:
            limit //= 10


def _flush(writer, columns, schema):
    writer.write_batch(
        pa.record_batch([pa.array(col, type=pa.string()) for col in columns], schema=schema)
    )


@transient_retry()
def _download_table(asset: str, url: str) -> int:
    """Stream the bz2 CSV at `url` into `asset` as all-string Parquet. Idempotent:
    raw_parquet_writer overwrites, so a retry restarts cleanly from scratch."""
    _raise_csv_field_limit()
    client = get_client()
    total = 0
    with client.stream("GET", url, timeout=(10.0, 300.0)) as resp:
        resp.raise_for_status()
        reader = io.BufferedReader(_Bz2Reader(resp.iter_bytes(DL_CHUNK)), buffer_size=DL_CHUNK)
        text = io.TextIOWrapper(reader, encoding="utf-8", errors="replace", newline="")
        rdr = csv.reader(text)
        header = next(rdr)
        ncol = len(header)
        schema = pa.schema([(c, pa.string()) for c in header])
        with raw_parquet_writer(asset, schema) as writer:
            columns = [[] for _ in range(ncol)]
            n = 0
            batch_bytes = 0
            for row in rdr:
                if len(row) != ncol:  # defensive: align ragged rows to header width
                    row = (row + [None] * ncol)[:ncol]
                for i in range(ncol):
                    v = row[i]
                    columns[i].append(v if v != "" else None)
                    if v:
                        batch_bytes += len(v)
                n += 1
                total += 1
                if n >= BATCH_ROWS or batch_bytes >= MAX_BATCH_BYTES:
                    _flush(writer, columns, schema)
                    columns = [[] for _ in range(ncol)]
                    n = 0
                    batch_bytes = 0
            if n:
                _flush(writer, columns, schema)
    if total == 0:
        raise RuntimeError(f"{asset}: parsed 0 data rows from {url}")
    return total


def fetch_one(node_id: str) -> None:
    asset = node_id  # the spec id IS the asset name
    table = node_id[len(SLUG) + 1:]  # strip "courtlistener-"
    date = _discover_latest_date(table)
    url = f"{BASE}{table}-{date}.csv.bz2"
    _download_table(asset, url)


DOWNLOAD_SPECS = [
    NodeSpec(id=f"{SLUG}-{eid.lower().replace('_', '-')}", fn=fetch_one, kind="download")
    for eid in ENTITY_IDS
]


# --------------------------------------------------------------------------
# Transform — thin typing pass over the all-string raw
# --------------------------------------------------------------------------
# Raw columns are all strings. We TRY_CAST keys, dates and timestamps to proper
# types (TRY_CAST -> NULL on a bad value, never fails the node) and pass the
# rest through. Court foreign keys are alphanumeric codes ('nc', 'ca5'), NOT
# integers, so they stay string.

_TS_COLS = {"date_created", "date_modified", "date_completed",
            "date_last_pacer_contact", "date_last_index"}
_STRING_ID_COLS = {"court_id", "parent_court_id", "appeal_from_id",
                   "circuit_id", "district_id", "pacer_court_id", "fjc_court_id"}
_INT_COLS = {"year", "year_of_tape", "depth", "citation_count", "page_count",
             "page_number", "view_count", "ia_upload_failure_count", "duration",
             "scdb_votes_majority", "scdb_votes_minority", "votes_yes", "votes_no"}
_DOUBLE_COLS = {"position", "score", "votes_yes_percent", "votes_no_percent",
                "monetary_demand", "amount_received"}
# Per-table columns dropped from the PUBLISHED table (raw retains everything).
# These are full-document free-text blobs (opinion bodies, transcripts, syllabi)
# that (a) overflow DuckDB's 2GB regular Arrow string buffer when a batch's
# string column exceeds 2GB and (b) are document text, not the statistical /
# metadata content these subsets are published for. Per-table (not global) so a
# short coded column like fjc's `disposition` is NOT dropped.
_DROP_COLS = {
    "oral-arguments": {"stt_transcript"},
    "opinion-clusters": {
        "syllabus", "headnotes", "summary", "procedural_history", "history",
        "headmatter", "arguments", "posture", "attorneys", "disposition",
        "cross_reference", "correction", "other_dates",
    },
}


def _is_date_col(col: str) -> bool:
    if col.endswith("_date"):  # start_date, end_date, transaction_date
        return True
    return (col.startswith("date_")
            and not col.startswith("date_granularity")
            and not col.endswith("_raw")
            and not col.endswith("_is_approximate"))


def _col_expr(table: str, col: str) -> str:
    q = f'"{col}"'
    if col in _STRING_ID_COLS:
        return q
    if col == "id":
        return q if table == "courts" else f"TRY_CAST({q} AS BIGINT) AS {q}"
    if col.endswith("_id"):
        return f"TRY_CAST({q} AS BIGINT) AS {q}"
    if col in _TS_COLS:
        return f"TRY_CAST({q} AS TIMESTAMP) AS {q}"
    if _is_date_col(col):
        return f"TRY_CAST({q} AS DATE) AS {q}"
    if col in _INT_COLS:
        return f"TRY_CAST({q} AS BIGINT) AS {q}"
    if col in _DOUBLE_COLS:
        return f"TRY_CAST({q} AS DOUBLE) AS {q}"
    return q


def _build_sql(table: str, asset: str) -> str:
    drop = _DROP_COLS.get(table, set())
    cols = [c for c in TABLE_COLUMNS[table] if c not in drop]
    exprs = ",\n    ".join(_col_expr(table, c) for c in cols)
    return f'SELECT\n    {exprs}\nFROM "{asset}"'


TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{s.id}-transform",
        deps=[s.id],
        sql=_build_sql(s.id[len(SLUG) + 1:], s.id),
        # Every bulk table is a PostgreSQL dump keyed on its `id` primary key
        # (always retained by the projection). `date_modified` is the record
        # update timestamp and the freshness signal wherever the table carries it.
        key=("id",),
        temporal=(
            "date_modified"
            if "date_modified" in TABLE_COLUMNS[s.id[len(SLUG) + 1:]]
            else None
        ),
    )
    for s in DOWNLOAD_SPECS
]
