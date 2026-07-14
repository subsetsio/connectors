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
import os

import pyarrow as pa

from subsets_utils import (
    delete_raw_file,
    list_raw_fragments,
    MaintainSpec,
    NodeSpec,
    get,
    raw_asset_exists,
    raw_parquet_writer,
)
from constants import ENTITY_IDS

PREFIX = "u-s-department-of-transportation-"
BASE = "https://data.transportation.gov/resource/{view}.csv"
PAGE = 50_000
PAGES_PER_FRAGMENT = 10
LARGE_DATASETS = {
    # Counted via SODA `select count(*)` in July 2026. These exceed the old
    # 25M-row ceiling, so write restartable fragments rather than one huge file.
    "4wpf-u82y",
    "5js8-2ffg",
    "6bch-d3uv",
    "8gz6-23ex",
    "fsfq-kawt",
    "ihrz-ddnk",
    "j246-y2rf",
    "q8hw-cdnd",
    # Count probes timed out locally; the fragmented path is safe for them too.
    "j7k2-8r24",
    "trfk-mhda",
}
csv.field_size_limit(1 << 24)


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


def _fetch_fragment(
    asset: str,
    ds_id: str,
    header: list[str],
    schema: pa.Schema,
    start_page: int,
) -> tuple[int, bool]:
    rows_written = 0
    complete = False
    fragment = f"part-{start_page:05d}"
    with raw_parquet_writer(asset, schema, fragment=fragment) as writer:
        for page_idx in range(start_page, start_page + PAGES_PER_FRAGMENT):
            text = _fetch_page(ds_id, page_idx * PAGE)
            _, cols, rows = _parse_page(text, header)
            if rows:
                _write_page(writer, schema, cols)
            rows_written += rows
            print(
                f"{asset}: page {page_idx} (+{rows}), fragment {fragment}",
                flush=True,
            )
            if rows < PAGE:
                complete = True
                break
    return rows_written, complete


def _fetch_large(asset: str, ds_id: str, header: list[str], schema: pa.Schema) -> None:
    fragments = list_raw_fragments(asset, "parquet")
    if "full" in fragments:
        delete_raw_file(asset, "parquet")
        fragments = {}

    run_id = os.environ.get("RUN_ID", "unknown")
    done = {frag for frag, meta in fragments.items() if meta.get("run_id") == run_id}
    total = 0
    start_page = 0
    while True:
        fragment = f"part-{start_page:05d}"
        if fragment in done:
            print(f"{asset}: {fragment} already present, skipping", flush=True)
            start_page += PAGES_PER_FRAGMENT
            continue

        rows, complete = _fetch_fragment(asset, ds_id, header, schema, start_page)
        total += rows
        print(f"{asset}: wrote {rows} rows to {fragment}", flush=True)
        if complete:
            break
        start_page += PAGES_PER_FRAGMENT
    print(f"{asset}: wrote {total} new rows from large dataset {ds_id}", flush=True)


def fetch_one(node_id: str) -> None:
    asset = node_id
    ds_id = node_id[len(PREFIX):]
    first_text = _fetch_page(ds_id, 0)
    header, cols, rows = _parse_page(first_text, None)
    if not header:
        raise AssertionError(f"{ds_id}: empty CSV header")
    schema = pa.schema([(col, pa.string()) for col in header])
    total = rows

    if ds_id in LARGE_DATASETS:
        _fetch_large(asset, ds_id, header, schema)
        return

    with raw_parquet_writer(asset, schema) as writer:
        if rows:
            _write_page(writer, schema, cols)
        print(f"{asset}: page 0 (+{rows}), {total} rows", flush=True)
        page_idx = 1
        while rows == PAGE:
            if rows < PAGE:
                break
            text = _fetch_page(ds_id, page_idx * PAGE)
            _, cols, rows = _parse_page(text, header)
            if rows:
                _write_page(writer, schema, cols)
            total += rows
            print(f"{asset}: page {page_idx} (+{rows}), {total} rows", flush=True)
            page_idx += 1
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
