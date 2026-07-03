"""UNCTAD Data Hub connector.

One published Delta table per UNCTAD report (dataset table). UNCTAD exposes a
no-auth bulk-download facility: each report ships its full time series as one or
more 7z (LZMA2) archives, each holding a single CSV. We fetch the report's bulk
file list, download each 7z, decompress it to a temp file on disk, then stream
the CSV through a column-typed transcoder into a single Parquet raw asset.

Fetch shape: **stateless full re-pull**. Every report's whole history fits in
one bulk download; there is no incremental/`since` filter on the bulk path, and
re-pulling each refresh picks up upstream revisions for free. Freshness gating is
the maintain step's concern, not ours.

The few multi-GB reports were demoted below the publish threshold at the rank
stage (operationally infeasible to materialize on a CI runner), so every report
here transcodes within bounded memory and disk: we hold only one row-batch in
RAM at a time and delete each 7z/CSV temp file as soon as it is consumed.

CSV layout (stable across reports): a leading time column (`Year` or a period),
then for each dimension a (code, "<dim> Label") pair, then for each measure a
("<measure>", "<measure> Footnote", "<measure> Missing value") triplet. We type
measures as DOUBLE, everything else as VARCHAR (dimension codes carry significant
leading zeros, e.g. economy "0000" = World), and clean column names to snake_case.
"""

from __future__ import annotations

import csv
import io as _io
import os
import tempfile

import py7zr
import pyarrow as pa
import pyarrow.parquet as pq

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    get_client,
    raw_parquet_writer,
    transient_retry,
)

API = "https://unctadstat-api.unctad.org"
BATCH_ROWS = 50_000  # rows per Parquet row-group / streamed RecordBatch

# The rank-accepted entity union — exact UNCTAD report codes (reportName),
# verbatim with original case (the bulk URL path is case-sensitive).
from constants import ENTITY_IDS


def _node_id(entity_id: str) -> str:
    return f"unctad-{entity_id.lower().replace('_', '-')}"


# node id -> exact reportName (id formula is lossy: lowercases and maps '_'→'-',
# and report codes contain no literal hyphens, so this reverse map is exact).
NODE_TO_REPORT = {_node_id(e): e for e in ENTITY_IDS}


# --------------------------------------------------------------------------- #
# HTTP with retry/backoff
# --------------------------------------------------------------------------- #
@transient_retry()
def _get_json(url: str):
    resp = get(url, timeout=(10.0, 120.0))
    resp.raise_for_status()
    return resp.json()


@transient_retry()
def _download_to(url: str, dest_path: str) -> None:
    """Stream a (potentially multi-hundred-MB) 7z body straight to disk."""
    with get_client().stream(
        "GET", url, timeout=(10.0, 600.0),
        headers={"Accept": "application/octet-stream"},
    ) as resp:
        resp.raise_for_status()
        with open(dest_path, "wb") as fh:
            for chunk in resp.iter_bytes(chunk_size=1 << 20):
                fh.write(chunk)


# --------------------------------------------------------------------------- #
# CSV typing / cleaning
# --------------------------------------------------------------------------- #
def _clean(name: str) -> str:
    out = []
    prev_us = False
    for ch in name.strip().lower():
        if ch.isalnum() and ch.isascii():
            out.append(ch)
            prev_us = False
        else:
            if not prev_us:
                out.append("_")
            prev_us = True
    return "".join(out).strip("_") or "col"


def _plan_schema(header: list[str]):
    """Classify columns and build (pa.Schema, clean_names, is_double[]).

    A column is a measure (DOUBLE) iff a sibling '<col> Footnote' column exists.
    Everything else (time, dimension codes, labels, footnotes, missing flags)
    is kept as VARCHAR to preserve leading zeros and free-text values.
    """
    hset = set(header)
    is_double = [f"{h} Footnote" in hset for h in header]

    raw_clean = [_clean(h) for h in header]
    seen: dict[str, int] = {}
    clean_names: list[str] = []
    for c in raw_clean:
        if c in seen:
            seen[c] += 1
            clean_names.append(f"{c}_{seen[c]}")
        else:
            seen[c] = 0
            clean_names.append(c)

    fields = [
        pa.field(clean_names[i], pa.float64() if is_double[i] else pa.string())
        for i in range(len(header))
    ]
    return pa.schema(fields), clean_names, is_double


def _to_value(raw: str, as_double: bool):
    if raw is None:
        return None
    if as_double:
        s = raw.strip()
        if s == "":
            return None
        try:
            return float(s)
        except ValueError:
            return None
    return raw


def _transcode_csv(csv_path: str, schema, clean_names, is_double, writer_holder):
    """Stream a CSV file into the shared ParquetWriter in row batches.

    writer_holder is a 1-element list whose slot is lazily filled with the
    raw_parquet_writer context the first time we have a schema to declare.
    """
    ncol = len(clean_names)
    with open(csv_path, "r", encoding="utf-8-sig", newline="") as fh:
        reader = csv.reader(fh)
        file_header = next(reader, None)
        if file_header is None:
            return
        # Guard against silent schema drift between bulk files of one report.
        if [_clean(h) for h in file_header] != clean_names:
            raise AssertionError(
                f"CSV header mismatch in {os.path.basename(csv_path)}: "
                f"{file_header[:6]}..."
            )

        cols: list[list] = [[] for _ in range(ncol)]
        n = 0

        def flush():
            nonlocal cols, n
            if n == 0:
                return
            arrays = [
                pa.array(cols[i], type=schema.field(i).type) for i in range(ncol)
            ]
            writer_holder[0].write_batch(
                pa.RecordBatch.from_arrays(arrays, schema=schema)
            )
            cols = [[] for _ in range(ncol)]
            n = 0

        for row in reader:
            if len(row) != ncol:
                # pad/truncate defensively to the declared width
                row = (row + [None] * ncol)[:ncol]
            for i in range(ncol):
                cols[i].append(_to_value(row[i], is_double[i]))
            n += 1
            if n >= BATCH_ROWS:
                flush()
        flush()


# --------------------------------------------------------------------------- #
# Download
# --------------------------------------------------------------------------- #
def fetch_one(node_id: str) -> None:
    asset = node_id
    report = NODE_TO_REPORT[node_id]

    bulk_files = _get_json(f"{API}/api/reportMetadata/{report}/bulkfiles/en")
    if not bulk_files:
        raise AssertionError(f"{report}: no bulk files returned")

    schema = clean_names = is_double = None
    writer_holder: list = [None]
    parquet_ctx = None
    tmpdir = tempfile.mkdtemp(prefix="unctad-")
    try:
        for bf in bulk_files:
            blob = bf["fileBlobName"]
            seven_path = os.path.join(tmpdir, f"{blob}.7z")
            _download_to(f"{API}/bulkdownload/{report}/{blob}", seven_path)

            # Decompress the single inner CSV to disk, then drop the 7z.
            with py7zr.SevenZipFile(seven_path, "r") as archive:
                names = archive.getnames()
                archive.extractall(path=tmpdir)
            os.remove(seven_path)

            csv_name = next((nm for nm in names if nm.lower().endswith(".csv")), None)
            if csv_name is None:
                raise AssertionError(f"{report}/{blob}: no CSV inside archive {names}")
            csv_path = os.path.join(tmpdir, csv_name)

            if schema is None:
                with open(csv_path, "r", encoding="utf-8-sig", newline="") as fh:
                    header = next(csv.reader(fh))
                schema, clean_names, is_double = _plan_schema(header)
                parquet_ctx = raw_parquet_writer(asset, schema)
                writer_holder[0] = parquet_ctx.__enter__()

            _transcode_csv(csv_path, schema, clean_names, is_double, writer_holder)
            os.remove(csv_path)

        if writer_holder[0] is None:
            raise AssertionError(f"{report}: nothing written")
    finally:
        if parquet_ctx is not None:
            parquet_ctx.__exit__(None, None, None)
        # best-effort temp cleanup
        try:
            for fn in os.listdir(tmpdir):
                try:
                    os.remove(os.path.join(tmpdir, fn))
                except OSError:
                    pass
            os.rmdir(tmpdir)
        except OSError:
            pass


DOWNLOAD_SPECS = [
    NodeSpec(id=_node_id(eid), fn=fetch_one, kind="download")
    for eid in ENTITY_IDS
]


# --------------------------------------------------------------------------- #
# Transform — publish one Delta table per report, verbatim typed columns.
# --------------------------------------------------------------------------- #
# Every report is a time-series panel with a leading period column. Most carry a
# yearly `year` column; a handful are quarterly/monthly/period-coded and their
# period column is not named `year`, so override the temporal for those. Keys are
# left undeclared: the grain is a composite of period + several dimension codes
# that is not verified unique here.
TEMPORAL_OVERRIDE = {
    "unctad-us.creativegoodsgr": "period",
    "unctad-us.gdpgr": "period",
    "unctad-us.lsbci": "quarter",
    "unctad-us.lsci": "quarter",
    "unctad-us.lsci-m": "month",
    "unctad-us.merchvolumequarterly": "quarter",
    "unctad-us.plsci": "quarter",
    "unctad-us.portcalls-s": "period",
    "unctad-us.portcallsarrivals-s": "period",
    "unctad-us.totandcomservicesquarterly": "period",
    "unctad-us.ucpi-m": "period",
}

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{s.id}-transform",
        deps=[s.id],
        sql=f'SELECT * FROM "{s.id}"',
        temporal=TEMPORAL_OVERRIDE.get(s.id, "year"),
    )
    for s in DOWNLOAD_SPECS
]
