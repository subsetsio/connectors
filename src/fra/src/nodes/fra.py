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
value as text anyway; forcing every column to string makes the streamed parse
deterministic over millions of rows (no type-inference drift between blocks) and
keeps memory bounded. The transform publishes each table faithfully; typing of
individual coded columns is left to downstream curation.
"""

import csv
import io

import pyarrow as pa
import pyarrow.csv as pacsv

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    get_client,
    raw_parquet_writer,
    transient_retry,
)
from constants import ENTITY_IDS

BASE_URL = "https://data.transportation.gov/resource/{view}.csv"
# Safe ceiling above the largest table (~5M rows) so a single request returns the
# whole corpus. `$order=:id` gives Socrata a stable full scan.
FULL_LIMIT = 20_000_000
READ_BLOCK = 1 << 20   # 1 MiB pyarrow CSV block
HTTP_CHUNK = 1 << 16   # 64 KiB network read chunk


class _ByteStreamReader(io.RawIOBase):
    """Adapt an iterator of byte chunks into a readable binary file object so
    pyarrow's CSV reader can stream over an httpx response without buffering the
    whole (multi-GB) body in memory."""

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


@transient_retry()
def _header_columns(view: str) -> list[str]:
    """Fetch the CSV header (api field names) via a zero-row request."""
    resp = get(BASE_URL.format(view=view), params={"$limit": 0}, timeout=(10.0, 60.0))
    resp.raise_for_status()
    return next(csv.reader([resp.text.strip()]))


@transient_retry()
def fetch_one(node_id: str) -> None:
    asset = node_id                       # the spec id IS the asset name
    view = node_id[len("fra-"):]          # recover the Socrata 4x4 id

    columns = _header_columns(view)
    if not columns:
        raise AssertionError(f"{view}: empty CSV header")
    schema = pa.schema([(c, pa.string()) for c in columns])

    convert = pacsv.ConvertOptions(column_types={c: pa.string() for c in columns})
    read_opts = pacsv.ReadOptions(block_size=READ_BLOCK)

    client = get_client()
    with client.stream(
        "GET",
        BASE_URL.format(view=view),
        params={"$limit": FULL_LIMIT, "$order": ":id"},
        timeout=(10.0, 600.0),
    ) as resp:
        resp.raise_for_status()
        fobj = io.BufferedReader(_ByteStreamReader(resp.iter_bytes(HTTP_CHUNK)))
        reader = pacsv.open_csv(fobj, read_options=read_opts, convert_options=convert)
        with raw_parquet_writer(asset, schema) as writer:
            for batch in reader:
                # Reorder/align to the declared schema, then write (bounded memory).
                table = pa.Table.from_batches([batch]).select(schema.names)
                writer.write_table(table)


DOWNLOAD_SPECS = [
    NodeSpec(
        id=f"fra-{eid.lower().replace('_', '-')}",
        fn=fetch_one,
        kind="download",
    )
    for eid in ENTITY_IDS
]

# One published Delta table per dataset — a faithful all-column passthrough of the
# raw export. Casting/reshaping of individual coded columns is out of scope here.
TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{spec.id}-transform",
        deps=[spec.id],
        sql=f'SELECT * FROM "{spec.id}"',
    )
    for spec in DOWNLOAD_SPECS
]
