"""CBO connector — Congressional Budget Office Open Data Repository.

Source: the official machine-readable mirror of CBO's Budget and Economic Data
at github.com/us-cbo/cbo-data. A root catalog.json (DCAT / project-open-data)
lists 13 datasets; we publish the 12 the accept step accepted. Each dataset has
several distributions (a CSV per release-vintage x file_type); a distribution's
downloadURL is repo-relative and fetched from raw.githubusercontent.com.

Shape: stateless full re-pull. The whole corpus is ~40MB across ~80 CSVs, so
there is no watermark and no cursor — every run re-reads the catalog and
re-fetches every distribution, which picks up revised vintages for free.

The CSVs are NOT uniformly shaped. Most are tidy long (date, variable, value),
some carry an extra estimate_type/section column, and a few (demographic,
spending_detail, long_term_economic's lfp_rates) are wide per-file_type tables
with their own dimension columns. Column names even drift across vintages of one
dataset (migration: people -> number_of_people; ss_area_population: marital ->
marital_status). So we impose no schema: each download fetches every
distribution of one dataset, tags rows with their vintage + file_type, takes the
union of all columns (missing -> null), and writes one NDJSON asset. Values are
left as the CSV's own text; the transform stage casts.

Two NDJSON measures applied at fetch time so the runtime's read_json_auto (no
union_by_name, default sample window) infers the asset cleanly:
  1. Uniform keys — every row carries every column of the union, so a row's key
     set never depends on which distribution it came from.
  2. Sample priming — the first PRIME_ROWS rows of every distribution are
     hoisted to the front of the file, so each column has a non-null value
     inside the sample window (a column null throughout the window is inferred
     as JSON, which leaks quotes into the published strings).
"""

from __future__ import annotations

import csv
import io
import re

from subsets_utils import (
    MaintainSpec,
    NodeSpec,
    get,
    raw_asset_exists,
    record_source_signature,
    save_raw_ndjson,
    source_unchanged,
    transient_retry,
)

from constants import ENTITY_IDS

RAW_BASE = "https://raw.githubusercontent.com/us-cbo/cbo-data/main/"
CATALOG_URL = RAW_BASE + "catalog.json"

# First N rows of each distribution hoisted to the file head so every column is
# typed within read_json_auto's default sample window.
PRIME_ROWS = 50

# The repo carries ~80 CSVs across 13 datasets today. A single dataset fanning
# out past this many distributions means CBO changed how it partitions releases,
# and the per-entity full re-pull is no longer the right shape.
MAX_DISTRIBUTIONS = 500

_VINTAGE_RE = re.compile(r"^\d{4}-\d{2}$")


@transient_retry()
def _fetch_catalog():
    resp = get(CATALOG_URL, timeout=(10.0, 60.0))
    resp.raise_for_status()
    return resp


@transient_retry()
def _fetch_csv(url: str) -> str:
    resp = get(url, timeout=(10.0, 180.0))
    resp.raise_for_status()
    return resp.text


def _entity_from_node_id(node_id: str) -> str:
    """`cbo-historical-economic` -> `historical_economic` (the catalog id)."""
    return node_id[len("cbo-"):].replace("-", "_")


def _vintage_date(vintage: str | None) -> str | None:
    """The release month as an ISO date, so freshness compares as a date."""
    return f"{vintage}-01" if _VINTAGE_RE.match(vintage or "") else None


def fetch_one(node_id: str) -> None:
    """Fetch every distribution of one CBO dataset into a single NDJSON asset."""
    asset = node_id
    entity = _entity_from_node_id(node_id)

    catalog_resp = _fetch_catalog()
    catalog = catalog_resp.json()

    datasets = {d.get("identifier"): d for d in catalog.get("datasets", [])}
    if entity not in datasets:
        raise RuntimeError(
            f"{asset}: dataset {entity!r} is no longer listed in the CBO catalog "
            f"(listed: {sorted(k for k in datasets if k)})"
        )

    distributions = datasets[entity].get("distribution") or []
    if not distributions:
        raise RuntimeError(f"{asset}: dataset {entity!r} lists no distributions")
    if len(distributions) > MAX_DISTRIBUTIONS:
        raise RuntimeError(
            f"{asset}: {len(distributions)} distributions exceeds the "
            f"{MAX_DISTRIBUTIONS} safety cap — the release partitioning changed"
        )

    # Rows per distribution, plus the stable first-seen union of their columns.
    per_dist: list[list[dict]] = []
    all_cols: list[str] = ["vintage", "vintage_date", "file_type"]
    for dist in distributions:
        download_url = dist.get("downloadURL")
        if not download_url:
            raise RuntimeError(f"{asset}: distribution missing downloadURL: {dist}")
        vintage = dist.get("vintage")
        tags = {
            "vintage": vintage,
            "vintage_date": _vintage_date(vintage),
            "file_type": dist.get("file_type"),
        }
        reader = csv.DictReader(io.StringIO(_fetch_csv(RAW_BASE + download_url)))
        for col in reader.fieldnames or []:
            if col not in all_cols:
                all_cols.append(col)
        per_dist.append([{**tags, **record} for record in reader])

    rows = [
        [{col: record.get(col) for col in all_cols} for record in records]
        for records in per_dist
    ]
    if not any(rows):
        raise RuntimeError(f"{asset}: {len(distributions)} distributions yielded 0 rows")

    head = [r for records in rows for r in records[:PRIME_ROWS]]
    tail = [r for records in rows for r in records[PRIME_ROWS:]]
    save_raw_ndjson(head + tail, asset)
    record_source_signature(asset, CATALOG_URL, response=catalog_resp)


def _node_id(entity: str) -> str:
    return f"cbo-{entity.lower().replace('_', '-')}"


DOWNLOAD_SPECS = [
    NodeSpec(id=_node_id(entity), fn=fetch_one, kind="download")
    for entity in ENTITY_IDS
]

# catalog.json is the repo's single index: it is rewritten whenever any dataset
# gains a vintage, so its ETag is a conservative change signal for every asset
# (it can over-fetch, it can never falsely skip).
MAINTAIN_SPECS = [
    MaintainSpec(
        asset_id=spec.id,
        description=(
            f"Re-fetch when {CATALOG_URL} changes (ETag). CBO republishes each "
            "dataset on its own schedule, anchored on the twice-yearly baseline "
            "(Jan/Feb and a mid-year update) per https://www.cbo.gov/data/budget-economic-data"
        ),
        check=lambda aid: source_unchanged(aid, CATALOG_URL) and raw_asset_exists(aid, "ndjson.zst"),
    )
    for spec in DOWNLOAD_SPECS
]
