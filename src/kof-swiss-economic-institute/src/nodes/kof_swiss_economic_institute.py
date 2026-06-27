"""KOF Swiss Economic Institute — KOF Datenservice public time-series collections.

Catalog connector. Each rank-active entity is a *collection* of the KOF
Datenservice public API (`/api/v1/public`). One download node per collection
fetches the whole collection in a single request
(`GET /public/collections/<id>?mime=json`), which returns
`{series_key: [{date: 'YYYY-MM', value: <num|null>}, ...], ...}`, and flattens it
into long-format rows (series_key, date, value). One SQL transform per collection
publishes that long table.

Fetch shape: **stateless full re-pull** (shape 1). The public API exposes no
incremental/`since` filter and no whole-corpus bulk dump; the per-collection
response is small (largest seen ~14MB / ~313k rows for globidx_v2020), so we
re-fetch each collection in full every run and overwrite. Revisions and late
corrections are picked up for free.
"""

import pyarrow as pa

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    transient_retry,
    save_raw_parquet,
)
from constants import ENTITY_IDS

SLUG = "kof-swiss-economic-institute"
PREFIX = SLUG + "-"
BASE = "https://datenservice.kof.ethz.ch/api/v1/public"

# Long-format contract: one row per (series_key, date). value is float64 — the
# API mixes int/float/null per observation; from_pylist coerces ints to float
# and keeps nulls (real gaps in the series).
SCHEMA = pa.schema(
    [
        ("series_key", pa.string()),
        ("date", pa.string()),
        ("value", pa.float64()),
    ]
)


def _collection_id(node_id: str) -> str:
    """Recover the upstream collection id from a download node id.

    Spec ids are f"{SLUG}-{entity_id.lower().replace('_','-')}"; entity ids
    contain only underscores and dots (no hyphens), so the reverse is a literal
    prefix strip plus '-' -> '_'.
    """
    return node_id[len(PREFIX):].replace("-", "_")


@transient_retry()
def _fetch_collection(collection_id: str) -> dict:
    resp = get(
        f"{BASE}/collections/{collection_id}",
        params={"mime": "json"},
        timeout=(10.0, 300.0),
    )
    resp.raise_for_status()
    return resp.json()


def fetch_one(node_id: str) -> None:
    asset = node_id  # the runtime passes the spec id; it IS the asset name
    collection_id = _collection_id(node_id)
    data = _fetch_collection(collection_id)

    rows = []
    for series_key, observations in data.items():
        if not isinstance(observations, list):
            # Defensive: every series in the public collections endpoint is an
            # observation list; skip anything that isn't rather than crashing.
            continue
        for obs in observations:
            if not isinstance(obs, dict):
                continue
            rows.append(
                {
                    "series_key": series_key,
                    "date": obs.get("date"),
                    "value": obs.get("value"),
                }
            )

    table = pa.Table.from_pylist(rows, schema=SCHEMA)
    save_raw_parquet(table, asset)


DOWNLOAD_SPECS = [
    NodeSpec(
        id=f"{SLUG}-{eid.lower().replace('_', '-')}",
        fn=fetch_one,
        kind="download",
    )
    for eid in ENTITY_IDS
]

# One published Delta table per collection: parse the 'YYYY-MM' month string to a
# first-of-month DATE, type value as DOUBLE, drop gap rows (null value).
TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{s.id}-transform",
        deps=[s.id],
        sql=f'''
            SELECT
                series_key,
                CAST(date || '-01' AS DATE) AS date,
                CAST(value AS DOUBLE)       AS value
            FROM "{s.id}"
            WHERE value IS NOT NULL
              AND date IS NOT NULL
        ''',
    )
    for s in DOWNLOAD_SPECS
]
