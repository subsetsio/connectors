"""Bank of Canada — Valet REST connector (https://www.bankofcanada.ca/valet).

Three published subsets, one DOWNLOAD_SPEC each:

  - groups        reference catalog of ~2,400 named series groups (/lists/groups/json)
  - series        reference catalog of ~15,600 individual time series (/lists/series/json)
  - observations  long-format values across every series, one row per (series_id, date),
                  fetched per series via /observations/<series>/json

Each is a stateless full re-pull. Observations re-walks all series each refresh
(no all-corpus bulk dump exists) and is written as a sequence of parquet batches
(one per chunk of series) that the transform globs back together and de-dups, so
an interrupted prior run leaving stale batch files cannot corrupt the table.
"""
import logging

import httpx
import pyarrow as pa

from subsets_utils import NodeSpec, SqlNodeSpec, save_raw_parquet

from utils import BASE, _fetch_json, _is_permanent_client_error

log = logging.getLogger("bank-of-canada")


# --------------------------------------------------------------------------- #
# groups
# --------------------------------------------------------------------------- #
GROUPS_SCHEMA = pa.schema([
    ("group_id", pa.string()),
    ("label", pa.string()),
    ("description", pa.string()),
])


def fetch_groups(node_id: str) -> None:
    asset = node_id
    payload = _fetch_json(f"{BASE}/lists/groups/json")
    groups = payload["groups"]
    rows = [
        {
            "group_id": gid,
            "label": (meta.get("label") or "").strip() or None,
            "description": (meta.get("description") or "").strip() or None,
        }
        for gid, meta in groups.items()
    ]
    assert rows, "groups list returned no entries"
    table = pa.Table.from_pylist(rows, schema=GROUPS_SCHEMA)
    save_raw_parquet(table, asset)


# --------------------------------------------------------------------------- #
# series
# --------------------------------------------------------------------------- #
SERIES_SCHEMA = pa.schema([
    ("series_id", pa.string()),
    ("label", pa.string()),
    ("description", pa.string()),
])


def fetch_series(node_id: str) -> None:
    asset = node_id
    payload = _fetch_json(f"{BASE}/lists/series/json")
    series = payload["series"]
    rows = [
        {
            "series_id": sid,
            "label": (meta.get("label") or "").strip() or None,
            "description": (meta.get("description") or "").strip() or None,
        }
        for sid, meta in series.items()
    ]
    assert rows, "series list returned no entries"
    table = pa.Table.from_pylist(rows, schema=SERIES_SCHEMA)
    save_raw_parquet(table, asset)


# --------------------------------------------------------------------------- #
# observations
# --------------------------------------------------------------------------- #
# Series are fetched one request each; group them into parquet batches so a
# single in-memory table never holds the whole corpus. ~200 series per batch
# keeps each file comfortably in RAM while avoiding thousands of tiny files.
OBS_CHUNK = 200

# Valet observations are NOT all date-indexed. Each observation object carries
# the series' own key plus exactly one INDEX key naming what the row is keyed
# by. Measured over a 400-series sample of the catalog:
#
#   d        81%   a date          -> true time series (FX rates, yields, ...)
#   k        16%   a category label -> survey cross-tabs (BOS/CES/CSCE), e.g.
#                                      {"k": "Size of price changes", ...}
#   <x>_id    3%   an entity id     -> bond_id, tbill_id, or_id, sr_id, tr_id,
#                                      bapf_id, pmmp_id, sl_id, dom_dbt_id, ...
#
# So we record the index GENERICALLY: obs_index_key names the upstream key,
# obs_index carries its value. Hardcoding "d" would null out the index for ~19%
# of series and silently destroy their row identity. The set of *_id keys is
# open-ended, so nothing here enumerates it.
#
# value kept as the raw string the API returns ("1.3977", "", "...", and for
# some k-indexed series plain text like "eSwatini (Swaziland)"); transforms
# TRY_CAST and drop the non-numeric rows.
OBS_SCHEMA = pa.schema([
    ("series_id", pa.string()),
    ("obs_index_key", pa.string()),
    ("obs_index", pa.string()),
    ("value", pa.string()),
])

# When an observation exposes more than one candidate index key, prefer the
# temporal one, then the category one; otherwise take the lowest name so the
# choice never depends on JSON key order.
_INDEX_PREFERENCE = ("d", "k")


def _observation_index(obs: dict, series_id: str) -> tuple[str, str] | None:
    """The (key_name, value) this observation is indexed by, or None if the
    payload carries no index at all (row identity would be unrecoverable)."""
    candidates = [k for k in obs if k != series_id]
    if not candidates:
        return None
    for preferred in _INDEX_PREFERENCE:
        if preferred in candidates:
            return preferred, obs[preferred]
    return (key := min(candidates)), obs[key]


def _list_series_ids() -> list[str]:
    payload = _fetch_json(f"{BASE}/lists/series/json")
    ids = list(payload["series"].keys())
    assert ids, "series list returned no entries"
    return sorted(ids)


def _series_observations(series_id: str) -> list[dict]:
    """Full history for one series as long-format rows, or [] if the series
    is gone (permanent 4xx) — a single dead series must not kill the crawl."""
    url = f"{BASE}/observations/{series_id}/json"
    try:
        payload = _fetch_json(url)
    except httpx.HTTPStatusError as exc:
        if _is_permanent_client_error(exc):
            log.warning("skip series %s: %s %s", series_id, exc.response.status_code, url)
            return []
        raise
    rows = []
    for obs in payload.get("observations", []):
        cell = obs.get(series_id)
        if not cell:
            continue
        value = cell.get("v")
        if value is None:
            continue
        index = _observation_index(obs, series_id)
        if index is None:
            log.warning("skip unindexed observation for series %s: %s", series_id, obs)
            continue
        index_key, index_value = index
        if index_value is None:
            continue
        rows.append({
            "series_id": series_id,
            "obs_index_key": index_key,
            "obs_index": str(index_value),
            "value": value,
        })
    return rows


def fetch_observations(node_id: str) -> None:
    # node_id == "bank-of-canada-observations"; raw is written as batches named
    # "<node_id>-<NNNNN>", which the transform's view globs back together.
    series_ids = _list_series_ids()
    for batch_idx in range(0, len(series_ids), OBS_CHUNK):
        chunk = series_ids[batch_idx:batch_idx + OBS_CHUNK]
        rows: list[dict] = []
        for sid in chunk:
            rows.extend(_series_observations(sid))
        if not rows:
            continue
        batch_key = f"{batch_idx // OBS_CHUNK:05d}"
        asset = f"{node_id}-{batch_key}"
        table = pa.Table.from_pylist(rows, schema=OBS_SCHEMA)
        save_raw_parquet(table, asset)


# --------------------------------------------------------------------------- #
# specs
# --------------------------------------------------------------------------- #
DOWNLOAD_SPECS = [
    NodeSpec(id="bank-of-canada-groups", fn=fetch_groups, kind="download"),
    NodeSpec(id="bank-of-canada-series", fn=fetch_series, kind="download"),
    NodeSpec(id="bank-of-canada-observations", fn=fetch_observations, kind="download"),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="bank-of-canada-groups-transform",
        deps=["bank-of-canada-groups"],
        sql='''
            SELECT
                group_id,
                label,
                description
            FROM "bank-of-canada-groups"
            WHERE group_id IS NOT NULL
        ''',
    ),
    SqlNodeSpec(
        id="bank-of-canada-series-transform",
        deps=["bank-of-canada-series"],
        sql='''
            SELECT
                series_id,
                label,
                description
            FROM "bank-of-canada-series"
            WHERE series_id IS NOT NULL
        ''',
    ),
    SqlNodeSpec(
        id="bank-of-canada-observations-transform",
        deps=["bank-of-canada-observations"],
        sql='''
            SELECT DISTINCT
                series_id,
                TRY_CAST(obs_date AS DATE)  AS date,
                TRY_CAST(value AS DOUBLE) AS value
            FROM "bank-of-canada-observations"
            WHERE series_id IS NOT NULL
              AND obs_date IS NOT NULL
              AND TRY_CAST(obs_date AS DATE) IS NOT NULL
              AND TRY_CAST(value AS DOUBLE) IS NOT NULL
        ''',
    ),
]
