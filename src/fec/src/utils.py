"""Shared transport + parsing helpers for the FEC bulk-data connector.

Source: FEC bulk download portal (https://www.fec.gov/files/bulk-downloads/).
One stable URL per (election cycle, file type); www.fec.gov 302-redirects to a
GovCloud S3 bucket. No auth. Files are partitioned by 2-year election cycle.

This module holds the HTTP transport and the generic, column-parameterised
parse helpers shared across the per-subset node files in nodes/. It defines no
NodeSpecs and no per-dataset column layouts (those live with their datasets).
"""

from __future__ import annotations

import csv
import io
import os
import tempfile
import zipfile
from datetime import date

import duckdb
import pyarrow as pa

from subsets_utils import (
    get,
    get_client,
    load_state,
    save_raw_parquet,
    save_state,
    transient_retry,
)

BULK = "https://www.fec.gov/files/bulk-downloads"
N_CYCLES = 4                 # most recent N 2-year cycles
STREAM_BATCH = 300_000       # rows per parquet batch for streamed files
STATE_VERSION = 1


# --------------------------------------------------------------------------- #
# HTTP / transport
# --------------------------------------------------------------------------- #


def _cycles() -> list[str]:
    """The most recent N election cycles (2-year periods ending in even years),
    derived from the current date — no hardcoded year range."""
    y = date.today().year
    latest = y if y % 2 == 0 else y + 1
    return [str(latest - 2 * i) for i in range(N_CYCLES)]


@transient_retry()
def _zip_member_bytes(cycle: str, prefix: str) -> bytes | None:
    """Download a small/medium cycle ZIP into memory and return its single data
    member's bytes. Returns None if the file does not exist (e.g. the current
    cycle hasn't published this file type yet)."""
    url = f"{BULK}/{cycle}/{prefix}{cycle[2:]}.zip"
    resp = get(url, timeout=(10.0, 300.0))
    if resp.status_code == 404:
        return None
    resp.raise_for_status()
    zf = zipfile.ZipFile(io.BytesIO(resp.content))
    member = [n for n in zf.namelist() if not n.startswith("__MACOSX")][0]
    return zf.read(member)


@transient_retry()
def _stream_zip_to_tempfile(url: str) -> str | None:
    """Stream a (possibly multi-GB) ZIP to a local temp file so it never sits
    in RAM. Returns the temp path, or None on 404. The temp file is scratch for
    processing — not a raw asset — and the caller deletes it."""
    client = get_client()
    fd, path = tempfile.mkstemp(suffix=".zip")
    os.close(fd)
    try:
        with client.stream("GET", url, timeout=(10.0, 300.0)) as resp:
            if resp.status_code == 404:
                os.unlink(path)
                return None
            resp.raise_for_status()
            with open(path, "wb") as fh:  # local scratch only, not a raw asset
                for chunk in resp.iter_bytes(chunk_size=1 << 20):
                    fh.write(chunk)
        return path
    except BaseException:
        if os.path.exists(path):
            os.unlink(path)
        raise


@transient_retry()
def _ie_get(url: str) -> bytes | None:
    resp = get(url, timeout=(10.0, 300.0))
    if resp.status_code == 404:
        return None
    resp.raise_for_status()
    return resp.content


# --------------------------------------------------------------------------- #
# Parsing helpers
# --------------------------------------------------------------------------- #

def _csv_clause(path: str, columns: list[str]) -> str:
    """A DuckDB read_csv() clause for a headerless pipe file with fixed names,
    everything read as VARCHAR (types are cast in the SQL transform)."""
    names = "[" + ",".join("'%s'" % c for c in columns) + "]"
    return (
        f"read_csv('{path}', delim='|', header=false, names={names}, "
        f"all_varchar=true, ignore_errors=true, quote='')"
    )


def _bytes_to_tempfile(data: bytes) -> str:
    fd, path = tempfile.mkstemp(suffix=".txt")
    with os.fdopen(fd, "wb") as fh:  # local scratch only, not a raw asset
        fh.write(data)
    return path


def _parse_pipe_member(data: bytes, columns: list[str], cycle: str) -> pa.Table:
    """Parse one headerless pipe member (in-memory) into an all-string Arrow
    table with a leading `cycle` column."""
    path = _bytes_to_tempfile(data)
    try:
        rel = duckdb.sql(
            f"SELECT '{cycle}' AS cycle, * FROM {_csv_clause(path, columns)}"
        )
        return rel.to_arrow_table()
    finally:
        os.unlink(path)


def _save_simple(node_id: str, prefix: str, columns: list[str]) -> None:
    """Fetch a small/medium pipe file across all cycles, concatenate, and write
    a single raw parquet asset named after the node."""
    parts = []
    for cycle in _cycles():
        data = _zip_member_bytes(cycle, prefix)
        if data is None:
            print(f"  {node_id}: {prefix} {cycle} not published, skipping")
            continue
        tbl = _parse_pipe_member(data, columns, cycle)
        parts.append(tbl)
        print(f"  {node_id}: {cycle} -> {tbl.num_rows:,} rows")
    if not parts:
        raise RuntimeError(f"{node_id}: no cycles fetched for {prefix}")
    save_raw_parquet(pa.concat_tables(parts), node_id)


def _write_batch(node_id: str, cycle: str, seq: int,
                 columns: list[str], rows: list[list[str]]) -> None:
    """Write one batch of streamed rows as a parquet batch asset
    `<node_id>-<cycle>-<seq>` (pure batch coordinate)."""
    cols = list(zip(*rows)) if rows else [()] * len(columns)
    arrays = [pa.array([cycle] * len(rows), pa.string())]
    for i in range(len(columns)):
        vals = [v if v != "" else None for v in cols[i]]
        arrays.append(pa.array(vals, pa.string()))
    table = pa.table(arrays, names=["cycle"] + columns)
    save_raw_parquet(table, f"{node_id}-{cycle}-{seq:05d}")


def _stream_cycle(node_id: str, prefix: str, columns: list[str], cycle: str) -> int:
    """Stream one cycle of a large pipe file: download ZIP to disk, decompress
    the member on the fly, parse pipe rows, and write parquet batches. Returns
    the number of batch files written."""
    url = f"{BULK}/{cycle}/{prefix}{cycle[2:]}.zip"
    zip_path = _stream_zip_to_tempfile(url)
    if zip_path is None:
        print(f"  {node_id}: {prefix} {cycle} not published, skipping")
        return 0
    ncols = len(columns)
    seq = 0
    total = 0
    skipped = 0
    try:
        zf = zipfile.ZipFile(zip_path)
        member = [n for n in zf.namelist() if not n.startswith("__MACOSX")][0]
        with zf.open(member) as raw:
            text = io.TextIOWrapper(raw, encoding="latin-1", newline="")
            reader = csv.reader(text, delimiter="|", quoting=csv.QUOTE_NONE)
            batch: list[list[str]] = []
            for fields in reader:
                # FEC files occasionally carry a trailing empty field (e.g.
                # oppexp ships 26 fields for a 25-column layout). Accept any row
                # with at least the expected count and keep the first ncols;
                # rows with too few fields (e.g. an embedded newline split one)
                # are malformed and dropped.
                if len(fields) < ncols:
                    skipped += 1
                    continue
                batch.append(fields[:ncols])
                if len(batch) >= STREAM_BATCH:
                    _write_batch(node_id, cycle, seq, columns, batch)
                    seq += 1
                    total += len(batch)
                    batch = []
            if batch:
                _write_batch(node_id, cycle, seq, columns, batch)
                seq += 1
                total += len(batch)
    finally:
        os.unlink(zip_path)
    print(f"  {node_id}: {cycle} -> {total:,} rows in {seq} batch(es) "
          f"({skipped} malformed rows skipped)")
    return seq


def _fetch_stream(node_id: str, prefix: str, columns: list[str]) -> None:
    """Stream a large transaction file cycle-by-cycle into parquet batches.
    Closed (past) cycles are recorded in state and skipped on later runs; the
    current cycle is always re-fetched (its data is still being filed)."""
    cycles = _cycles()
    latest = cycles[0]
    state = load_state(node_id)
    if state.get("schema_version") != STATE_VERSION:
        state = {}
    completed = set(state.get("completed_cycles", []))
    for cycle in cycles:
        if cycle != latest and cycle in completed:
            print(f"  {node_id}: {cycle} already complete, skipping")
            continue
        _stream_cycle(node_id, prefix, columns, cycle)
        if cycle != latest:
            completed.add(cycle)
            save_state(node_id, {
                "schema_version": STATE_VERSION,
                "completed_cycles": sorted(completed),
            })
