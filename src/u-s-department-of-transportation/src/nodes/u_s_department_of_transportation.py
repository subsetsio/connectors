"""U.S. Department of Transportation - data.transportation.gov (Socrata).

Catalog connector: one generic fetch per rank-accepted dataset. Each dataset is
pulled in full every run (stateless full re-pull) via the Socrata resource CSV
endpoint, paged at the 50000-row SoQL ceiling with a stable ``$order=:id``.

The earlier JSON API path could spend an entire GitHub run on one large table.
CSV pages are the same fleet pattern used by the FRA USDOT connector: one page
is a bounded HTTP request, parsed with Python's CSV reader for embedded
newlines, and flushed to raw Parquet as all-string columns. The all-string raw
schema is deliberate because Socrata serves CSV cells as text and these catalog
datasets have heterogeneous, code-heavy schemas.
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

PREFIX = "u-s-department-of-transportation-"
BASE = "https://data.transportation.gov/resource/{view}.csv"
PAGE = 50_000
MAX_PAGES = 500
csv.field_size_limit(1 << 24)


@transient_retry()
def _fetch_page(ds_id: str, offset: int) -> str:
    resp = get(
        BASE.format(view=ds_id),
        params={"$limit": PAGE, "$offset": offset, "$order": ":id"},
        timeout=(10.0, 180.0),
    )
    resp.raise_for_status()
    return resp.text


def _parse_page(text: str, header: list[str] | None) -> tuple[list[str], list[list[str | None]], int]:
    reader = csv.reader(io.StringIO(text))
    page_header = next(reader, None)
    if not page_header:
        return [], [], 0
    if header is None:
        header = page_header
    elif page_header != header:
        raise AssertionError("Socrata CSV header changed while paging")

    ncol = len(header)
    cols: list[list[str | None]] = [[] for _ in range(ncol)]
    rows = 0
    for row in reader:
        if len(row) != ncol:
            row = (row + [""] * ncol)[:ncol]
        for idx, value in enumerate(row):
            cols[idx].append(value if value != "" else None)
        rows += 1
    return header, cols, rows


def _write_page(writer, schema: pa.Schema, cols: list[list[str | None]]) -> None:
    arrays = [pa.array(col, type=pa.string()) for col in cols]
    writer.write_table(pa.Table.from_arrays(arrays, schema=schema))


def fetch_one(node_id: str) -> None:
    asset = node_id
    ds_id = node_id[len(PREFIX):]
    first_text = _fetch_page(ds_id, 0)
    header, cols, rows = _parse_page(first_text, None)
    if not header:
        raise AssertionError(f"{ds_id}: empty CSV header")
    schema = pa.schema([(col, pa.string()) for col in header])
    total = rows

    with raw_parquet_writer(asset, schema) as writer:
        if rows:
            _write_page(writer, schema, cols)
        print(f"{asset}: page 0 (+{rows}), {total} rows", flush=True)
        exhausted = rows == PAGE
        for page_idx in range(1, MAX_PAGES):
            if rows < PAGE:
                exhausted = False
                break
            text = _fetch_page(ds_id, page_idx * PAGE)
            _, cols, rows = _parse_page(text, header)
            if rows:
                _write_page(writer, schema, cols)
            total += rows
            print(f"{asset}: page {page_idx} (+{rows}), {total} rows", flush=True)
        if exhausted and rows == PAGE:
            raise RuntimeError(
                f"{asset}: exceeded MAX_PAGES={MAX_PAGES}; source larger than expected"
            )
    print(f"{asset}: wrote {total} rows from dataset {ds_id}", flush=True)


DOWNLOAD_SPECS = [
    NodeSpec(
        id=f"{PREFIX}{eid.lower().replace('_', '-')}",
        fn=fetch_one,
        kind="download",
    )
    for eid in ENTITY_IDS
]

MAINTAIN_SPECS = [
    MaintainSpec(
        asset_id=spec.id,
        description=(
            "Weekly refresh cadence per connector maintenance.json; raw "
            "Socrata snapshot present in manifest and newer than 7 days"
        ),
        check=lambda aid: raw_asset_exists(aid, "parquet", max_age_days=7),
    )
    for spec in DOWNLOAD_SPECS
]
