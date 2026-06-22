"""Statistics Poland (GUS) — Local Data Bank (BDL) connector.

Mechanism: BDL REST API (https://bdl.stat.gov.pl/api/v1/). Each rank-accepted
entity is a BDL *thematic group* (G-level subject, e.g. ``G7`` POPULATION). A
group has no variables of its own; its data lives in its P-level subgroups, each
of which exposes a set of statistical *variables*. For every group we:

  1. enumerate its P subgroups (``/subjects?parent-id=G...``),
  2. enumerate the variables under each subgroup (``/variables?subject-id=P...``),
  3. fetch the **national (Poland)** time series for those variables in batches
     via ``/data/by-unit/{POLAND}?var-id=...`` — one request returns the full
     year/value series for up to ~50 variables.

Scope is deliberately **national level only** (BDL territorial unit
``000000000000`` = POLAND). BDL publishes the same characteristics down to the
locality level (4,694 units), but full territorial coverage would be hundreds of
thousands of requests against a hard rate limit; the national series is the
broadly-useful headline indicator and keeps a full refresh to ~900 requests.
Every accepted group was verified to carry national-level values.

Fetch shape: **stateless full re-pull** (shape 1). The whole national corpus for
a group is small and re-fetched every run; no watermark/cursor.

Rate limits (BDL): anonymous 5 req/s, 100/15min, 1000/12h, 10000/7days; with a
registered key (sent as the ``X-ClientId`` header, read from env ``BDL_API_KEY``)
500/15min, 5000/12h. We pace to ~4 req/s and lean on ``transient_retry`` to ride
out the rolling-window 429s when running anonymously.
"""

import os

import pyarrow as pa
from ratelimit import limits, sleep_and_retry

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    save_raw_parquet,
    transient_retry,
)
from constants import ENTITY_IDS

BASE = "https://bdl.stat.gov.pl/api/v1"
SLUG = "statistics-poland"
PREFIX = f"{SLUG}-"
POLAND = "000000000000"          # BDL territorial unit id for the national total
PAGE_SIZE = 100                  # BDL max page size
VAR_BATCH = 50                   # var-ids per /data/by-unit request

SCHEMA = pa.schema([
    ("group_id", pa.string()),
    ("subject_id", pa.string()),
    ("variable_id", pa.int64()),
    ("variable_name", pa.string()),
    ("n1", pa.string()),
    ("n2", pa.string()),
    ("n3", pa.string()),
    ("n4", pa.string()),
    ("n5", pa.string()),
    ("measure_unit", pa.string()),
    ("measure_unit_id", pa.int64()),
    ("year", pa.int32()),
    ("value", pa.float64()),
    ("attr_id", pa.int32()),
])


def _headers():
    key = os.environ.get("BDL_API_KEY") or os.environ.get("BDL_CLIENT_ID")
    return {"X-ClientId": key} if key else {}


@sleep_and_retry
@limits(calls=4, period=1)        # ~80% of the anonymous 5 req/s ceiling
def _throttle():
    return None


@transient_retry(attempts=15, min_wait=5, max_wait=300)
def _api(path, params):
    """One GET against the BDL API. Retries 429/5xx/network with backoff — the
    long max_wait lets an anonymous run sit out a blown 15-minute window."""
    _throttle()
    p = {"format": "json", "lang": "en", **params}
    resp = get(f"{BASE}/{path}", params=p, headers=_headers(), timeout=(10.0, 120.0))
    resp.raise_for_status()
    return resp.json()


def _paged(path, params, *, key):
    """Iterate every record across the BDL page envelope. ``key`` is the result
    list key (always 'results' here); pagination is pinned to totalRecords."""
    page = 0
    while True:
        body = _api(path, {**params, "page": page, "page-size": PAGE_SIZE})
        results = body.get(key, []) or []
        for rec in results:
            yield rec
        total = body.get("totalRecords", 0)
        size = body.get("pageSize", PAGE_SIZE) or PAGE_SIZE
        if not results or (page + 1) * size >= total:
            break
        page += 1
        if page > 10_000:
            raise RuntimeError(f"pagination runaway on {path} params={params}")


def _variable_name(v):
    parts = [v.get(f"n{i}") for i in range(1, 6)]
    parts = [p for p in parts if p]
    return " - ".join(parts) if parts else None


def _batched(seq, size):
    for i in range(0, len(seq), size):
        yield seq[i:i + size]


def fetch_one(node_id: str) -> None:
    asset = node_id                                  # the spec id IS the asset name
    group_id = node_id[len(PREFIX):].upper()         # 'statistics-poland-g7' -> 'G7'

    # 1+2. Walk the group's P subgroups and collect their variables' metadata.
    var_meta = {}
    for sub in _paged("subjects", {"parent-id": group_id}, key="results"):
        sub_id = sub["id"]
        for v in _paged("variables", {"subject-id": sub_id}, key="results"):
            vid = v["id"]
            var_meta[vid] = {
                "subject_id": sub_id,
                "variable_name": _variable_name(v),
                "n1": v.get("n1"), "n2": v.get("n2"), "n3": v.get("n3"),
                "n4": v.get("n4"), "n5": v.get("n5"),
                "measure_unit": v.get("measureUnitName"),
                "measure_unit_id": v.get("measureUnitId"),
            }

    # 3. National time series for those variables, batched by var-id.
    rows = []
    for chunk in _batched(list(var_meta), VAR_BATCH):
        for res in _paged(
            f"data/by-unit/{POLAND}", {"var-id": chunk}, key="results"
        ):
            vid = res.get("id")
            meta = var_meta.get(vid)
            if meta is None:
                continue
            for obs in res.get("values", []):
                year = obs.get("year")
                rows.append({
                    "group_id": group_id,
                    "subject_id": meta["subject_id"],
                    "variable_id": int(vid),
                    "variable_name": meta["variable_name"],
                    "n1": meta["n1"], "n2": meta["n2"], "n3": meta["n3"],
                    "n4": meta["n4"], "n5": meta["n5"],
                    "measure_unit": meta["measure_unit"],
                    "measure_unit_id": meta["measure_unit_id"],
                    "year": int(year) if year is not None else None,
                    "value": obs.get("val"),
                    "attr_id": obs.get("attrId"),
                })

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

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{s.id}-transform",
        deps=[s.id],
        sql=f'''
            SELECT
                CAST(year AS INTEGER)                  AS year,
                make_date(CAST(year AS INTEGER), 1, 1) AS date,
                variable_id,
                variable_name,
                n1, n2, n3, n4, n5,
                measure_unit,
                CAST(value AS DOUBLE)                  AS value,
                attr_id
            FROM "{s.id}"
            WHERE value IS NOT NULL AND year IS NOT NULL
        ''',
    )
    for s in DOWNLOAD_SPECS
]
