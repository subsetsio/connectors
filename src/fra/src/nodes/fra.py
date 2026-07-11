"""FRA (Federal Railroad Administration, Office of Safety) connector.

Source: USDOT Socrata portal ``data.transportation.gov`` (attribution
"FRA Safe Team"). Each rank-accepted entity is one Socrata dataset (a 4x4 id)
with its own column schema — a catalog connector, one generic fetch fn over the
entity union in ``constants.ENTITY_IDS``.

Strategy: stateless full re-pull each run. Each table is paged from the Socrata
resource CSV endpoint with ``$order=:id`` + ``$offset`` at the verified 50k-row
SoQL ceiling, and each page is appended to a single raw parquet asset. ``:id``
tokens are opaque and unusable as a watermark, so the full re-pull is what picks
up source revisions; it is cheap enough to redo every run.

Why paged (``$order=:id``) rather than one big unordered request: three of these
tables are the Form 71 Crossing Inventory (~5M rows × ~185 cols). ``:id`` is
Socrata's indexed internal row key, so ``$order=:id`` is served from the natural
storage order — a 50k-row page anywhere in a 5M-row table returns in ~20s (no
server-side re-sort). Paging keeps memory bounded to one page, gives a natural
per-page retry point (a transient failure re-fetches one 50k page, never the
whole table), holds each HTTP connection open only for seconds rather than the
tens of minutes a single full-table stream would need, and is the fleet idiom
(see ``bjs.py``). ``$order`` is required for correctness: unordered ``$offset``
paging on Socrata does NOT return stable page boundaries (verified — the same
offset yields different rows across requests), so it would drop/duplicate rows.

The whole table is written atomically: a page-by-page pull into one open
``raw_parquet_writer``, committed to the raw manifest only when the writer exits
cleanly. A runner that dies mid-table therefore commits nothing for that table,
and the MaintainSpec re-fetches it whole on the next run while skipping tables
that already finished — table-granular resume with no risk of a partial commit.

Raw format: parquet with an all-``string`` schema derived from the CSV header
(the resource endpoint's API field names). The datasets are wide, code-heavy,
and Socrata serves every value as text anyway; forcing every column to string
makes the parse deterministic over millions of rows and keeps the raw schema
stable regardless of which optional fields a page omits.

Each page is parsed with Python's ``csv`` module rather than a line reader:
several tables carry free-text ``narrative`` columns whose values contain
embedded newlines, so a row can span multiple physical lines. ``csv.reader``
reassembles quoted multi-line fields correctly. The transform publishes each
table faithfully; typing of individual coded columns is left to downstream
curation.
"""

import csv
import io

import pyarrow as pa

from subsets_utils import (
    MaintainSpec,
    NodeSpec,
    get,
    raw_asset_exists,
    raw_parquet_writer,
    transient_retry,
)
from constants import ENTITY_IDS

BASE_URL = "https://data.transportation.gov/resource/{view}.csv"
# Verified SoQL $limit ceiling on this portal; :id-ordered pages at this size
# return in ~20s even 4M rows deep into a 5M-row table.
PAGE_SIZE = 50_000
# Safety ceiling: the largest tables are ~5M rows = ~100 pages. 500 pages covers
# 25M rows; hitting it means the source grew far past expectations, so we raise
# rather than silently truncate.
MAX_PAGES = 500
# Tolerate a tiny count drift between the count(*) probe and the paged pull (the
# source can be revised mid-pull); anything larger is a real hole and must fail.
COUNT_TOLERANCE = 0.001
# csv fields can be very large (long narratives); lift the default 128 KiB cap.
csv.field_size_limit(1 << 24)


def _row_count(view: str) -> int:
    resp = get(
        BASE_URL.format(view=view),
        params={"$select": "count(*)"},
        timeout=(10.0, 60.0),
    )
    resp.raise_for_status()
    rows = list(csv.reader(io.StringIO(resp.text)))
    # header row + one value row: [["count"], ["4988495"]]
    return int(rows[1][0])


@transient_retry()
def _fetch_page(view: str, offset: int) -> str:
    """Return one page of CSV text (header + up to PAGE_SIZE rows).

    Retried as a unit on transient errors — a failed page re-fetches just this
    offset, never the whole table."""
    resp = get(
        BASE_URL.format(view=view),
        params={"$order": ":id", "$limit": PAGE_SIZE, "$offset": offset},
        timeout=(10.0, 180.0),
    )
    resp.raise_for_status()
    return resp.text


def _parse_page(text: str, ncol: int, cols: list) -> tuple[list[str], int]:
    """Parse a page's CSV text, appending data cells into ``cols``.

    Returns (header, data_row_count). ``cols`` must be a list of ``ncol`` lists
    when ncol is known; on the first page pass ncol=0 / cols=[] and the header
    width defines the schema (the caller re-allocates cols)."""
    reader = csv.reader(io.StringIO(text))
    header = next(reader, None)
    if header is None:
        return [], 0
    if not cols:
        return header, 0
    rows = 0
    for row in reader:
        # Socrata CSV is rectangular; pad/truncate defensively so one stray row
        # never aborts a multi-million-row pull.
        if len(row) != ncol:
            row = (row + [""] * ncol)[:ncol]
        for i in range(ncol):
            v = row[i]
            cols[i].append(v if v != "" else None)
        rows += 1
    return header, rows


def _flush(writer, schema, cols) -> None:
    arrays = [pa.array(c, type=pa.string()) for c in cols]
    writer.write_table(pa.Table.from_arrays(arrays, schema=schema))


def fetch_one(node_id: str) -> None:
    asset = node_id                       # the spec id IS the asset name
    view = node_id[len("fra-"):]          # recover the Socrata 4x4 id

    expected = _row_count(view)

    # Page 0 defines the header/schema.
    first_text = _fetch_page(view, 0)
    header, _ = _parse_page(first_text, 0, [])
    if not header:
        raise AssertionError(f"{view}: empty CSV header")
    ncol = len(header)
    schema = pa.schema([(c, pa.string()) for c in header])

    total = 0
    pages = 0
    with raw_parquet_writer(asset, schema) as writer:
        text = first_text
        for page_idx in range(MAX_PAGES):
            if page_idx > 0:
                text = _fetch_page(view, page_idx * PAGE_SIZE)
            cols = [[] for _ in range(ncol)]
            page_header, n = _parse_page(text, ncol, cols)
            if page_header and page_header != header:
                raise AssertionError(
                    f"{view}: header drift on page {page_idx} "
                    f"(schema changed mid-pull)"
                )
            if n:
                _flush(writer, schema, cols)
            total += n
            pages += 1
            print(f"{asset}: page {page_idx} (+{n}), {total} rows", flush=True)
            if n < PAGE_SIZE:
                break
        else:
            raise RuntimeError(
                f"{asset}: exceeded MAX_PAGES={MAX_PAGES} "
                f"(offset {MAX_PAGES * PAGE_SIZE}); source larger than expected"
            )

    if not total:
        raise AssertionError(f"{view}: no rows returned")
    # Guard against a truncated pull: a short read would otherwise commit a
    # partial table as if complete.
    if expected and total < expected * (1.0 - COUNT_TOLERANCE):
        raise AssertionError(
            f"{view}: pulled {total} rows but count(*) reported {expected} "
            f"— likely truncated"
        )
    print(
        f"{asset}: done, {total} rows across {pages} page(s) "
        f"(count(*)={expected})",
        flush=True,
    )


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
