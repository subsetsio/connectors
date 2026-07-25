"""KOF Swiss Economic Institute connector — node module.

Source: KOF Time Series Database API v2 (https://tsdb-api.kof.ethz.ch/v2/).
Each accepted subset is a public KOF "collection": a curated bundle of related
time series. One request, GET /collections/public/<name>/ts?access_type=public,
returns the entire bundle as a list of time series objects — full history, no
pagination.

Fetch shape: stateless full re-pull. The whole public corpus is ~59 small
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
import hashlib
import time

import pyarrow as pa

from subsets_utils import NodeSpec, get, save_raw_parquet, transient_retry

BASE = "https://tsdb-api.kof.ethz.ch/v2"

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


@transient_retry(attempts=8, min_wait=10, max_wait=180)
def _fetch_collection(name: str) -> dict:
    resp = get(
        f"{BASE}/collections/public/{name}/ts",
        params={"access_type": "public"},
        timeout=(10.0, 300.0),
    )
    resp.raise_for_status()
    return resp.json()


def _iter_observations(node_id: str, data):
    """Yield (series_key, obs_index, date, value) for v2 and legacy v1 shapes."""
    if isinstance(data, list):
        for series in data:
            if not isinstance(series, dict):
                raise ValueError(
                    f"{node_id}: expected time series object, got "
                    f"{type(series).__name__}"
                )
            series_key = series.get("ts_key")
            times = series.get("time")
            values = series.get("value")
            if not isinstance(series_key, str) or not series_key:
                raise ValueError(f"{node_id}: time series is missing ts_key")
            if not isinstance(times, list) or not isinstance(values, list):
                raise ValueError(f"{node_id}: {series_key!r} missing time/value arrays")
            if len(times) != len(values):
                raise ValueError(
                    f"{node_id}: {series_key!r} has {len(times)} time points but "
                    f"{len(values)} values"
                )
            for i, (date, val) in enumerate(zip(times, values, strict=True)):
                yield series_key, i, date, val
        return

    if isinstance(data, dict):
        if "error" in data and len(data) == 1:
            raise ValueError(f"{node_id}: API returned error envelope: {data['error']!r}")
        for series_key, observations in data.items():
            if not isinstance(observations, list):
                raise ValueError(
                    f"{node_id}: series {series_key!r} not a list (got "
                    f"{type(observations).__name__})"
                )
            for i, obs in enumerate(observations):
                yield series_key, i, obs.get("date"), obs.get("value")
        return

    raise ValueError(f"{node_id}: expected JSON array/object, got {type(data).__name__}")


def fetch_one(node_id: str) -> None:
    asset = node_id  # the runtime passes the spec id; it IS the asset name
    name = SPEC_TO_COLLECTION[node_id]
    stagger_s = int(hashlib.sha1(node_id.encode("utf-8")).hexdigest()[:2], 16) % 10
    time.sleep(stagger_s)
    data = _fetch_collection(name)

    series_keys = []
    obs_indices = []
    dates = []
    values = []
    for series_key, obs_index, date, val in _iter_observations(node_id, data):
        series_keys.append(series_key)
        obs_indices.append(obs_index)
        dates.append(date)
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
