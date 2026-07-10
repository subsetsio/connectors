"""FRA (Federal Railroad Administration, Office of Safety) connector.

Source: USDOT Socrata portal ``data.transportation.gov`` (attribution
"FRA Safe Team"). Each rank-accepted entity is one Socrata dataset (a 4x4 id)
with its own column schema — a catalog connector, one generic fetch fn over the
entity union in ``constants.ENTITY_IDS``.

Strategy: stateless full re-pull each run. The whole table is exported in a
single request from the Socrata resource CSV endpoint
``/resource/{id}.csv?$limit=<huge>&$order=:id`` and streamed straight to raw
parquet — no pagination, no watermark. Socrata ``:id`` tokens are opaque and
unordered so they are unusable as a watermark; the full-corpus re-pull is cheap
enough (largest tables ~5M rows) and picks up source revisions for free.

Raw format: parquet with an all-``string`` schema derived from the CSV header.
The datasets are wide (up to ~265 columns), code-heavy, and Socrata serves every
value as text anyway; forcing every column to string makes the parse
deterministic over millions of rows and keeps memory bounded.

The CSV is parsed with Python's ``csv`` module over a streamed text wrapper
rather than pyarrow's block CSV reader: several tables carry free-text
``narrative`` columns whose values contain embedded newlines, which desync
pyarrow's block chunker at block boundaries. The stdlib reader handles quoted
multi-line fields correctly while still streaming. The transform publishes each
table faithfully; typing of individual coded columns is left to downstream
curation.
"""

import csv
import io

import pyarrow as pa

from subsets_utils import (
    MaintainSpec,
    NodeSpec,
    get_client,
    raw_asset_exists,
    raw_parquet_writer,
    transient_retry,
)
from constants import ENTITY_IDS

BASE_URL = "https://data.transportation.gov/resource/{view}.csv"
# Safe ceiling above the largest table (~5M rows) so a single request returns the
# whole corpus. `$order=:id` gives Socrata a stable full scan.
FULL_LIMIT = 20_000_000
HTTP_CHUNK = 1 << 16   # 64 KiB network read chunk
BATCH_ROWS = 50_000    # rows per parquet row-group write
# csv fields can be very large (long narratives); lift the default 128 KiB cap.
csv.field_size_limit(1 << 24)


class _ByteStreamReader(io.RawIOBase):
    """Adapt an iterator of byte chunks into a readable binary file object so a
    TextIOWrapper can stream over an httpx response without buffering the whole
    (multi-GB) body in memory."""

    def __init__(self, chunk_iter):
        self._it = chunk_iter
        self._buf = b""

    def readable(self):
        return True

    def readinto(self, b):
        while not self._buf:
            try:
                self._buf = next(self._it)
            except StopIteration:
                return 0
        n = min(len(b), len(self._buf))
        b[: n] = self._buf[:n]
        self._buf = self._buf[n:]
        return n


def _flush(writer, schema, columns) -> None:
    arrays = [pa.array(col, type=pa.string()) for col in columns]
    writer.write_table(pa.Table.from_arrays(arrays, schema=schema))


@transient_retry()
def fetch_one(node_id: str) -> None:
    asset = node_id                       # the spec id IS the asset name
    view = node_id[len("fra-"):]          # recover the Socrata 4x4 id

    client = get_client()
    with client.stream(
        "GET",
        BASE_URL.format(view=view),
        params={"$limit": FULL_LIMIT, "$order": ":id"},
        timeout=(10.0, 600.0),
    ) as resp:
        resp.raise_for_status()
        text = io.TextIOWrapper(
            io.BufferedReader(_ByteStreamReader(resp.iter_bytes(HTTP_CHUNK))),
            encoding="utf-8",
            newline="",
        )
        reader = csv.reader(text)
        header = next(reader)
        if not header:
            raise AssertionError(f"{view}: empty CSV header")
        ncol = len(header)
        schema = pa.schema([(c, pa.string()) for c in header])

        with raw_parquet_writer(asset, schema) as writer:
            cols = [[] for _ in range(ncol)]
            n = 0
            for row in reader:
                # Socrata CSV is rectangular; pad/truncate defensively so one
                # stray row never aborts a multi-million-row pull.
                if len(row) != ncol:
                    row = (row + [""] * ncol)[:ncol]
                for i in range(ncol):
                    v = row[i]
                    cols[i].append(v if v != "" else None)
                n += 1
                if n >= BATCH_ROWS:
                    _flush(writer, schema, cols)
                    cols = [[] for _ in range(ncol)]
                    n = 0
            if n:
                _flush(writer, schema, cols)


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
