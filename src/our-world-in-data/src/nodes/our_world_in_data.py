"""Our World in Data — Grapher Chart API connector.

Each published OWID Grapher chart maps to one stable URL that returns the full
underlying table as CSV:

    https://ourworldindata.org/grapher/{slug}.csv?csvType=full&useColumnShortNames=true

Charts are heterogeneous — every chart has its own value column(s) on top of the
shared entity/code/year(or day) backbone — so each chart is its own raw asset and
its own published Delta table (the heterogeneous-catalog shape). The chart slug is
recovered from the spec id by stripping the ``our-world-in-data-`` prefix; collect
verified every slug is already lowercase-hyphenated, so the round-trip is exact.

Two classes of chart are excluded upstream in collect because their CSV endpoint
cannot serve the full table: non-redistributable charts (permanent 403) and a
handful of oversized COVID-era charts that exceed OWID's Cloudflare worker limit
(persistent 503). ``fetch_one`` still degrades gracefully on 403/404/410 so a
chart newly flagged between collect and run becomes a missing asset rather than a
hard crash.

CSV parsing: OWID data is mostly clean, but a few charts (e.g. notable-AI-systems)
carry dirty entity labels with embedded commas/newlines. We parse with pyarrow in
tolerant mode — ``newlines_in_values=True`` plus an invalid-row handler that skips
the rare malformed line — which reads those files correctly without regressing the
clean ones.

Fetch shape: stateless full re-pull. Each chart CSV is small (a single curated
dataset) and the API exposes no per-row incremental filter, so every run re-fetches
the full table and overwrites. No watermark, no cursor.

Raw is saved as parquet: each asset is written exactly once per run from a single
CSV, so pyarrow's CSV type inference is a safe, stable contract for that asset (the
auto-inference caveat applies to batched/repeated writes, which this is not).
"""
import io

import httpx
import pyarrow.csv as pacsv

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    save_raw_parquet,
    transient_retry,
)

PREFIX = "our-world-in-data-"
BASE = "https://ourworldindata.org/grapher/"

# Browser-like UA for the Cloudflare-fronted grapher origin.
UA = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"
)


def _skip_invalid_row(row):
    # Tolerate the rare malformed line (dirty entity labels with stray
    # commas/newlines) rather than failing the whole chart.
    return "skip"


def _dedup_columns(table):
    # A chart with two dimensions mapping to variables that share a short name
    # yields duplicate CSV headers; parquet tolerates them but DuckDB's
    # `SELECT *` in the transform would raise on the duplicate. Rename collisions
    # deterministically (name, name_2, name_3, ...).
    seen, names = {}, []
    for col in table.column_names:
        if col in seen:
            seen[col] += 1
            names.append(f"{col}_{seen[col]}")
        else:
            seen[col] = 1
            names.append(col)
    return table.rename_columns(names) if names != table.column_names else table


@transient_retry()
def _fetch_csv(url: str) -> httpx.Response:
    resp = get(
        url,
        params={"csvType": "full", "useColumnShortNames": "true"},
        headers={"User-Agent": UA},
        timeout=(10.0, 180.0),
    )
    # Permanent per-chart conditions (handled by the caller, not retried).
    # 503 is transient (retried by the decorator) — persistently-503 charts are
    # excluded upstream in collect.
    if resp.status_code in (403, 404, 410):
        return resp
    resp.raise_for_status()
    return resp


def fetch_one(node_id: str) -> None:
    asset = node_id  # the runtime passes the spec id; it IS the asset name
    slug = node_id[len(PREFIX):]
    url = f"{BASE}{slug}.csv"
    resp = _fetch_csv(url)
    if resp.status_code in (403, 404, 410):
        print(f"[our-world-in-data] {slug}: {resp.status_code} not downloadable; skipping")
        return
    table = pacsv.read_csv(
        io.BytesIO(resp.content),
        parse_options=pacsv.ParseOptions(
            newlines_in_values=True,
            invalid_row_handler=_skip_invalid_row,
        ),
    )
    table = _dedup_columns(table)
    save_raw_parquet(table, asset)


def _spec_id(eid: str) -> str:
    return f"{PREFIX}{eid.lower().replace('_', '-')}"


from constants import ENTITY_IDS

DOWNLOAD_SPECS = [
    NodeSpec(id=_spec_id(eid), fn=fetch_one, kind="download")
    for eid in ENTITY_IDS
]

# One published Delta table per chart. Each chart's raw parquet is already typed
# (pyarrow inferred entity/code -> string, year -> int64, value cols -> double),
# so the transform is a thin pass-through: publish the chart's natural wide table.
TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{s.id}-transform",
        deps=[s.id],
        sql=f'SELECT * FROM "{s.id}"',
    )
    for s in DOWNLOAD_SPECS
]
