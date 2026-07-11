"""FRA (Federal Railroad Administration, Office of Safety) connector.

Source: USDOT Socrata portal ``data.transportation.gov`` (attribution
"FRA Safe Team"). Each rank-accepted entity is one Socrata dataset (a 4x4 id)
with its own column schema — a catalog connector, one generic fetch fn over the
entity union in ``constants.ENTITY_IDS``.

Strategy: stateless full re-pull each run. Each table is read from the Socrata
resource CSV endpoint in bounded ``$limit``/``$offset`` pages ordered by
``:id`` and streamed straight to raw parquet. Socrata ``:id`` tokens are opaque
and unordered so they are unusable as a watermark; the full-corpus re-pull is
cheap enough and picks up source revisions for free.

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
import sys

import pyarrow as pa

from subsets_utils import (
    MaintainSpec,
    NodeSpec,
    get,
    raw_asset_exists,
    raw_parquet_writer,
)
from constants import ENTITY_IDS

BASE_URL = "https://data.transportation.gov/resource/{view}.csv"
# Socrata's public API handles 50k-row pages reliably while avoiding one huge
# response that can leave the hosted runner silent for too long.
PAGE_ROWS = 50_000
BATCH_ROWS = 25_000
# csv fields can be very large (long narratives); lift the default 128 KiB cap.
csv.field_size_limit(1 << 24)


def _flush(writer, schema, columns) -> None:
    arrays = [pa.array(col, type=pa.string()) for col in columns]
    writer.write_table(pa.Table.from_arrays(arrays, schema=schema))


def fetch_one(node_id: str) -> None:
    asset = node_id                       # the spec id IS the asset name
    view = node_id[len("fra-"):]          # recover the Socrata 4x4 id

    schema = None
    writer_cm = None
    writer = None
    total = 0
    offset = 0

    try:
        while True:
            resp = get(
                BASE_URL.format(view=view),
                params={"$limit": PAGE_ROWS, "$offset": offset, "$order": ":id"},
                timeout=(10.0, 180.0),
            )
            resp.raise_for_status()

            text = io.StringIO(resp.text, newline="")
            reader = csv.reader(text)
            header = next(reader, None)
            if not header:
                if total == 0:
                    raise AssertionError(f"{view}: empty CSV header")
                break

            if schema is None:
                schema = pa.schema([(c, pa.string()) for c in header])
                writer_cm = raw_parquet_writer(asset, schema)
                writer = writer_cm.__enter__()
            elif header != schema.names:
                raise AssertionError(f"{view}: schema changed while paging")

            ncol = len(header)
            cols = [[] for _ in range(ncol)]
            page_rows = 0
            batch_rows = 0
            for row in reader:
                # Socrata CSV is rectangular; pad/truncate defensively so one
                # stray row never aborts a multi-million-row pull.
                if len(row) != ncol:
                    row = (row + [""] * ncol)[:ncol]
                for i in range(ncol):
                    v = row[i]
                    cols[i].append(v if v != "" else None)
                page_rows += 1
                batch_rows += 1
                total += 1
                if batch_rows >= BATCH_ROWS:
                    _flush(writer, schema, cols)
                    cols = [[] for _ in range(ncol)]
                    batch_rows = 0
            if batch_rows:
                _flush(writer, schema, cols)

            print(f"{asset}: fetched {total} rows", flush=True)
            if page_rows < PAGE_ROWS:
                break
            offset += PAGE_ROWS

        if writer is None:
            raise AssertionError(f"{view}: no rows returned")
    finally:
        if writer_cm is not None:
            writer_cm.__exit__(*sys.exc_info())


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
