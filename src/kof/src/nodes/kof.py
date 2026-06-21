"""KOF Swiss Economic Institute connector — node module.

Source: KOF Datenservice REST API v1 (https://datenservice.kof.ethz.ch/api/v1/),
the /public/* namespace (no auth). Each accepted subset is a public KOF
"collection": a curated bundle of related time series. One request,
GET /public/collections/<name>?format=json, returns the entire bundle as
{series_key: [{date, value}, ...]} — full history, no pagination.

Fetch shape: stateless full re-pull. The whole public corpus is ~44 small
collections (largest ~13MB / ~310k observations), so we re-fetch each
collection in full every run and overwrite — revisions and late corrections
are picked up for free. No watermark, no cursor.

Raw is flattened to long format (series_key, obs_index, date, value) and
stored as parquet. The transform normalizes the mixed-grain date string
('YYYY', 'YYYY-MM', 'YYYY-MM-DD') to a DATE and publishes one Delta table per
collection.

Note on granularity: the JSON endpoint reports every date as 'YYYY-MM' (or
'YYYY' / 'YYYY-MM-DD'); for daily series (e.g. the Stringency Index, the Job
Tracker) the day component is dropped upstream, so many observations within a
series share the same month string. `obs_index` is the 0-based position of the
observation within its series — it keeps each row addressable and preserves the
intra-month cadence without inventing day labels the source did not provide.
"""
import pyarrow as pa

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    save_raw_parquet,
    transient_retry,
)

BASE = "https://datenservice.kof.ethz.ch/api/v1/public"

# The entity union — public KOF collections scored at/above the publish
# threshold by the rank stage. Copied verbatim from
# data/sources/kof/work/entity_union.json.
from constants import ENTITY_IDS


def _spec_id(entity_id: str) -> str:
    return f"kof-{entity_id.lower().replace('_', '-')}"


# Spec id -> original collection name. The id transform (lowercase, '_'->'-')
# is lossy, so we recover the real collection name to call the API.
SPEC_TO_COLLECTION = {_spec_id(eid): eid for eid in ENTITY_IDS}

SCHEMA = pa.schema([
    ("series_key", pa.string()),
    ("obs_index", pa.int64()),
    ("date", pa.string()),
    ("value", pa.float64()),
])


@transient_retry()
def _fetch_collection(name: str) -> dict:
    resp = get(
        f"{BASE}/collections/{name}",
        params={"format": "json"},
        timeout=(10.0, 300.0),
    )
    resp.raise_for_status()
    return resp.json()


def fetch_one(node_id: str) -> None:
    asset = node_id  # the runtime passes the spec id; it IS the asset name
    name = SPEC_TO_COLLECTION[node_id]
    data = _fetch_collection(name)

    if not isinstance(data, dict):
        raise ValueError(f"{node_id}: expected JSON object, got {type(data).__name__}")
    # The API returns {"error": "..."} (HTTP 200) for an unknown/empty collection.
    # For an accepted subset that is a hard failure, not an empty table.
    if "error" in data and len(data) == 1:
        raise ValueError(f"{node_id}: API returned error envelope: {data['error']!r}")

    series_keys = []
    obs_indices = []
    dates = []
    values = []
    for series_key, observations in data.items():
        if not isinstance(observations, list):
            raise ValueError(
                f"{node_id}: series {series_key!r} not a list (got "
                f"{type(observations).__name__})"
            )
        for i, obs in enumerate(observations):
            val = obs.get("value")
            series_keys.append(series_key)
            obs_indices.append(i)
            dates.append(obs.get("date"))
            values.append(float(val) if val is not None else None)

    table = pa.table(
        {
            "series_key": series_keys,
            "obs_index": obs_indices,
            "date": dates,
            "value": values,
        },
        schema=SCHEMA,
    )
    save_raw_parquet(table, asset)


DOWNLOAD_SPECS = [
    NodeSpec(id=_spec_id(eid), fn=fetch_one, kind="download")
    for eid in ENTITY_IDS
]


# One published Delta table per collection: long-format (series_key, period,
# date, value). The date string is mixed-grain — 'YYYY' (annual), 'YYYY-MM'
# (monthly/quarterly), 'YYYY-MM-DD' (daily) — normalized to a DATE here while
# the original string is preserved as `period`. Null observations are dropped.
def _transform_sql(download_id: str) -> str:
    return f'''
        SELECT
            series_key,
            obs_index,
            date AS period,
            CASE
                WHEN length(date) = 4  THEN try_strptime(date || '-01-01', '%Y-%m-%d')
                WHEN length(date) = 7  THEN try_strptime(date || '-01', '%Y-%m-%d')
                ELSE                        try_strptime(date, '%Y-%m-%d')
            END::DATE AS date,
            CAST(value AS DOUBLE) AS value
        FROM "{download_id}"
        WHERE value IS NOT NULL
    '''


TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{s.id}-transform",
        deps=[s.id],
        sql=_transform_sql(s.id),
    )
    for s in DOWNLOAD_SPECS
]
