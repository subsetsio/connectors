"""CFPB Consumer Complaint Database — the full-corpus export.

One persistent ~1.4 GB ZIP holds the whole ~16M-row corpus. We stream the ZIP
to a tempfile, stream-extract its single CSV member, slugify the spaced header
(`Date received` -> `date_received`) and re-emit it as Parquet (all columns
string). The transform casts the date and id columns back to proper types.
"""

from __future__ import annotations

import csv
import io
import re
import tempfile
import zipfile

import httpx
from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get_client,
    raw_parquet_writer,
)
from utils import _ensure_ua

_COMPLAINTS_ZIP_URL = "https://files.consumerfinance.gov/ccdb/complaints.csv.zip"
_COMPLAINTS_BATCH = 100_000


def _slugify(name: str) -> str:
    """`Consumer consent provided?` -> `consumer_consent_provided`."""
    s = re.sub(r"[^0-9a-zA-Z]+", "_", name.strip().lower())
    return s.strip("_")


@retry(
    retry=retry_if_exception_type((httpx.TransportError, httpx.TimeoutException)),
    wait=wait_exponential(multiplier=2, max=60),
    stop=stop_after_attempt(3),
    reraise=True,
)
def fetch_complaints(node_id: str) -> None:
    """Stream the ~1.4 GB complaints ZIP, extract its single CSV member, and
    re-emit it as Parquet (all columns string) as `node_id`.

    Parquet with an explicit all-string schema rather than CSV/NDJSON: the
    `consumer_complaint_narrative` field has embedded newlines (breaks the SQL
    transform's parallel CSV reader) and the date columns auto-sniff to
    TIMESTAMP under read_json_auto (a later malformed date then aborts the read).
    An explicit Parquet schema carries the types verbatim — no sniffing — and the
    transform casts dates/id back to proper types deterministically. The ZIP
    central directory lives at the end of the file, so zipfile needs a seekable
    handle; we stream the download to a tempfile (scratch, not a raw asset) then
    stream-extract the member in row batches.
    """
    import pyarrow as pa

    _ensure_ua()
    client = get_client()
    with tempfile.NamedTemporaryFile(suffix=".zip") as tmp:
        with client.stream("GET", _COMPLAINTS_ZIP_URL, timeout=600) as resp:
            resp.raise_for_status()
            for chunk in resp.iter_bytes(8 * 1024 * 1024):
                tmp.write(chunk)
        tmp.flush()

        with zipfile.ZipFile(tmp.name) as zf:
            members = [n for n in zf.namelist() if n.lower().endswith(".csv")]
            if not members:
                raise ValueError(
                    f"{node_id}: no .csv member in complaints ZIP (members={zf.namelist()})"
                )
            member = members[0]
            with zf.open(member) as raw:
                reader = csv.reader(io.TextIOWrapper(raw, encoding="utf-8", newline=""))
                keys = [_slugify(c) for c in next(reader)]
                schema = pa.schema([(k, pa.string()) for k in keys])
                ncols = len(keys)
                n = 0

                def _flush(batch_cols, writer):
                    writer.write_table(pa.table(batch_cols, schema=schema))

                with raw_parquet_writer(node_id, schema) as writer:
                    cols = [[] for _ in keys]
                    for row in reader:
                        if len(row) != ncols:  # pad/truncate defensively
                            row = (row + [""] * ncols)[:ncols]
                        for j in range(ncols):
                            cols[j].append(row[j])
                        n += 1
                        if n % _COMPLAINTS_BATCH == 0:
                            _flush({k: cols[i] for i, k in enumerate(keys)}, writer)
                            cols = [[] for _ in keys]
                    if any(cols):
                        _flush({k: cols[i] for i, k in enumerate(keys)}, writer)
    print(f"  {node_id}: wrote {n:,} complaint rows from member {member!r}")


# Complaints is stored all-string Parquet (to dodge CSV/JSON type sniffing), so
# its transform casts the date and id columns back to proper types.
_COMPLAINTS_SQL = '''
    SELECT
        * EXCLUDE (date_received, date_sent_to_company, complaint_id),
        TRY_CAST(date_received AS DATE)        AS date_received,
        TRY_CAST(date_sent_to_company AS DATE) AS date_sent_to_company,
        TRY_CAST(complaint_id AS BIGINT)       AS complaint_id
    FROM "cfpb-consumer-complaints"
'''

_DOWNLOAD_SPECS = [
    NodeSpec(id="cfpb-consumer-complaints", fn=fetch_complaints, kind="download"),
]

_TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="cfpb-consumer-complaints-transform",
        deps=("cfpb-consumer-complaints",),
        sql=_COMPLAINTS_SQL,
    ),
]
