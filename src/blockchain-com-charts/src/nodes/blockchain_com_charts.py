"""Blockchain.com Charts connector.

One published time series per chart slug. Each chart is fetched in full from the
Blockchain.com Charts API in a single request:

    GET https://api.blockchain.info/charts/<slug>?timespan=all&sampled=false&format=json

The response carries metadata (name/unit/period/description) plus
`values: [{x: <unix seconds>, y: <float>}, ...]` — the entire history. We store the
raw (x, y) pairs as parquet and let the transform cast x→timestamp and project value.

Fetch shape: stateless full re-pull (shape 1). Each series is small (thousands to a
few hundred thousand points, a single small JSON), there is no incremental/`since`
filter on this API, and re-pulling picks up any upstream revisions for free.
"""

import pyarrow as pa

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    save_raw_parquet,
    transient_retry,
)
from constants import ENTITY_IDS

SLUG = "blockchain-com-charts"
BASE_URL = "https://api.blockchain.info/charts/"

# x = observation time (unix seconds), y = metric value. Stable across every chart.
SCHEMA = pa.schema([
    ("x", pa.int64()),
    ("y", pa.float64()),
])


@transient_retry()
def _fetch_chart(slug: str) -> list[dict]:
    resp = get(
        f"{BASE_URL}{slug}",
        params={"timespan": "all", "sampled": "false", "format": "json"},
        timeout=(10.0, 120.0),
    )
    resp.raise_for_status()
    doc = resp.json()
    if doc.get("status") != "ok":
        # The API answers 200 with a status envelope; a non-ok status for a slug we
        # expect to exist is a real error, not a transient one — fail loudly.
        raise AssertionError(f"{slug}: unexpected chart status {doc.get('status')!r}")
    values = doc.get("values")
    if not isinstance(values, list) or not values:
        raise AssertionError(f"{slug}: empty or missing values array")
    return values


def fetch_one(node_id: str) -> None:
    asset = node_id  # the runtime passes the spec id; it IS the asset name
    slug = node_id[len(SLUG) + 1:]  # strip "blockchain-com-charts-" prefix
    values = _fetch_chart(slug)
    table = pa.Table.from_pylist(
        [{"x": int(p["x"]), "y": float(p["y"])} for p in values],
        schema=SCHEMA,
    )
    save_raw_parquet(table, asset)


DOWNLOAD_SPECS = [
    NodeSpec(
        id=f"{SLUG}-{eid.lower().replace('_', '-')}",
        fn=fetch_one,
        kind="download",
    )
    for eid in ENTITY_IDS
]

# One published Delta table per chart: a clean (timestamp, value) time series.
# Each chart carries its own unit/meaning, so it is its own table (the table name
# is the metric); the transform is a thin parse-and-type pass.
TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{s.id}-transform",
        deps=[s.id],
        sql=f'''
            SELECT
                CAST(to_timestamp(x) AS TIMESTAMP) AS timestamp,
                CAST(y AS DOUBLE)                  AS value
            FROM "{s.id}"
            WHERE y IS NOT NULL
            ORDER BY timestamp
        ''',
    )
    for s in DOWNLOAD_SPECS
]
