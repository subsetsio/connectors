"""FRA (Federal Railroad Administration, Office of Safety) connector.

Source: USDOT Socrata portal ``data.transportation.gov`` (attribution
"FRA Safe Team"). Each rank-accepted entity is one Socrata dataset (a 4x4 id)
with its own column schema — a catalog connector, one generic fetch fn over the
entity union in ``constants.ENTITY_IDS``.

Strategy: stateless full re-pull each run. Each table is read from the Socrata
resource CSV endpoint in ONE streaming request with an explicit ``$limit`` set
above the largest corpus, and streamed straight to raw parquet. ``:id`` tokens
are opaque and unordered so they are unusable as a watermark; the full re-pull
is cheap enough and picks up source revisions for free.

Why one big request instead of ``$offset`` paging: three of these tables are
the Form 71 Crossing Inventory (~5M rows × ~185 cols). Offset paging needs a
stable ``$order`` and the only stable key is ``:id``; ordering by ``:id`` makes
Socrata re-sort the whole corpus on *every* page (measured ~4 min per 50k-row
page), so a 5M-row table can't finish inside the runner budget. A single
unordered full-table request avoids the sort entirely and completeness no
longer depends on a stable page order (there are no pages). The row count is
verified against a ``count(*)`` probe so a silently truncated response fails
loudly instead of leaving a hole.

Raw format: parquet with an all-``string`` schema derived from the CSV header
(the resource endpoint's API field names). The datasets are wide, code-heavy,
and Socrata serves every value as text anyway; forcing every column to string
makes the parse deterministic over millions of rows and keeps memory bounded.

The CSV is parsed with Python's ``csv`` module over a streamed text wrapper
rather than pyarrow's block CSV reader: several tables carry free-text
``narrative`` columns whose values contain embedded newlines, which desync
pyarrow's block chunker at block boundaries. The stdlib reader handles quoted
multi-line fields correctly while still streaming (the byte stream is wrapped
in a ``TextIOWrapper`` opened with ``newline=""``). The transform publishes each
table faithfully; typing of individual coded columns is left to downstream
curation.
"""

import csv
import io
import time

import httpx
import pyarrow as pa

from subsets_utils import (
    MaintainSpec,
    NodeSpec,
    get,
    get_client,
    raw_asset_exists,
    raw_parquet_writer,
)
from constants import ENTITY_IDS

BASE_URL = "https://data.transportation.gov/resource/{view}.csv"
# One request per table; $limit sits well above the largest corpus (~5M rows).
FETCH_LIMIT = 20_000_000
BATCH_ROWS = 25_000
# A full-table stream is one long-lived response: allow a slow first byte
# (Socrata generates the CSV server-side, ~25s observed) and slow inter-chunk
# gaps, but keep a bounded connect budget.
STREAM_TIMEOUT = httpx.Timeout(connect=30.0, read=300.0, write=30.0, pool=60.0)
# Restart the whole stream on a transient network failure (there is no
# mid-stream resume without $order, which we deliberately avoid).
MAX_ATTEMPTS = 4
# Tolerate a tiny count drift between the count(*) probe and the stream (the
# source can be revised between the two requests); anything larger is a real
# truncation and must fail.
COUNT_TOLERANCE = 0.001
# csv fields can be very large (long narratives); lift the default 128 KiB cap.
csv.field_size_limit(1 << 24)


class _IterStream(io.RawIOBase):
    """Adapt an httpx byte-chunk iterator into a readable binary stream so a
    ``TextIOWrapper`` (and thus ``csv.reader``) can consume it incrementally."""

    def __init__(self, chunks):
        self._chunks = chunks
        self._buf = b""

    def readable(self) -> bool:
        return True

    def readinto(self, b) -> int:
        while not self._buf:
            try:
                self._buf = next(self._chunks)
            except StopIteration:
                return 0
        n = min(len(b), len(self._buf))
        b[: n], self._buf = self._buf[:n], self._buf[n:]
        return n


def _flush(writer, schema, columns) -> None:
    arrays = [pa.array(col, type=pa.string()) for col in columns]
    writer.write_table(pa.Table.from_arrays(arrays, schema=schema))


def _row_count(view: str) -> int:
    resp = get(
        BASE_URL.format(view=view),
        params={"$select": "count(*)"},
        timeout=60.0,
    )
    resp.raise_for_status()
    rows = list(csv.reader(io.StringIO(resp.text)))
    # header row + one value row: [["count"], ["4988495"]]
    return int(rows[1][0])


def _stream_to_parquet(view: str, asset: str) -> int:
    """Stream the full table into raw parquet; return the row count written.

    Raises on any failure BEFORE the raw_parquet_writer block exits cleanly, so
    a partial/failed stream is never committed to the raw manifest (stage_write
    runs only when the `with` block exits without an exception)."""
    client = get_client()
    with client.stream(
        "GET",
        BASE_URL.format(view=view),
        params={"$limit": FETCH_LIMIT},
        timeout=STREAM_TIMEOUT,
    ) as resp:
        resp.raise_for_status()
        raw = io.BufferedReader(_IterStream(resp.iter_bytes()))
        text = io.TextIOWrapper(raw, encoding="utf-8", errors="replace", newline="")
        reader = csv.reader(text)

        header = next(reader, None)
        if not header:
            raise AssertionError(f"{view}: empty CSV header")
        schema = pa.schema([(c, pa.string()) for c in header])
        ncol = len(header)

        total = 0
        with raw_parquet_writer(asset, schema) as writer:
            cols = [[] for _ in range(ncol)]
            batch_rows = 0
            for row in reader:
                # Socrata CSV is rectangular; pad/truncate defensively so one
                # stray row never aborts a multi-million-row pull.
                if len(row) != ncol:
                    row = (row + [""] * ncol)[:ncol]
                for i in range(ncol):
                    v = row[i]
                    cols[i].append(v if v != "" else None)
                batch_rows += 1
                total += 1
                if batch_rows >= BATCH_ROWS:
                    _flush(writer, schema, cols)
                    cols = [[] for _ in range(ncol)]
                    batch_rows = 0
                    print(f"{asset}: streamed {total} rows", flush=True)
            if batch_rows:
                _flush(writer, schema, cols)
        return total


def fetch_one(node_id: str) -> None:
    asset = node_id                       # the spec id IS the asset name
    view = node_id[len("fra-"):]          # recover the Socrata 4x4 id

    expected = _row_count(view)

    total = None
    for attempt in range(1, MAX_ATTEMPTS + 1):
        try:
            total = _stream_to_parquet(view, asset)
            break
        except httpx.HTTPError as exc:
            if attempt == MAX_ATTEMPTS:
                raise
            wait = min(60.0, 2.0 * (2 ** (attempt - 1)))
            print(
                f"{asset}: stream failed ({type(exc).__name__}: {exc}) — "
                f"retry {attempt}/{MAX_ATTEMPTS - 1} in {wait:.0f}s",
                flush=True,
            )
            time.sleep(wait)

    if not total:
        raise AssertionError(f"{view}: no rows returned")
    # Guard against a silently truncated response: without paging, a short read
    # would otherwise commit a partial table as if complete.
    if expected and total < expected * (1.0 - COUNT_TOLERANCE):
        raise AssertionError(
            f"{view}: streamed {total} rows but count(*) reported {expected} "
            f"— likely truncated"
        )
    print(f"{asset}: done, {total} rows (count(*)={expected})", flush=True)


DOWNLOAD_SPECS = [
    NodeSpec(
        id=f"fra-{eid.lower().replace('_', '-')}",
        fn=fetch_one,
        kind="download",
    )
    for eid in ENTITY_IDS
]

MAINTAIN_SPECS = [
    MaintainSpec(
        asset_id=spec.id,
        description=(
            "FRA Office of Safety data is refreshed from the Socrata portal; "
            "reuse raw parquet for up to 7 days (inferred weekly factory cadence, "
            "source portal https://data.transportation.gov/browse?attribution=FRA+Safe+Team)."
        ),
        check=lambda aid: raw_asset_exists(aid, "parquet", max_age_days=7),
    )
    for spec in DOWNLOAD_SPECS
]
