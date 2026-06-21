"""Bank of Canada — observations subset.

Long-format values across every series, one row per (series_id, date). Fetched
per series via /observations/<series>/json — the only path that yields a clean,
non-overlapping long format with full coverage of ungrouped series.

Fetch shape: stateless full re-pull. The Valet API has no all-corpus bulk dump,
so this node walks all ~15,600 series each refresh and re-pulls full history —
this catches revisions and late corrections for free (no stored watermark to go
stale). Because that is a large crawl, observations raw is written as a sequence
of parquet batches (one per chunk of series); the transform globs every batch
and de-duplicates, so an interrupted prior run that left stale batch files
cannot corrupt the published table. No incremental delta filter is used: a
single long-format node spanning all series cannot key one watermark per series,
and the per-series start_date filter would not reduce the request count (still
one request per series).

The series list this crawl walks is re-fetched here internally from
/lists/series/json — the observations subset depends on the live series list.
"""
import logging

import httpx
import pyarrow as pa

from subsets_utils import NodeSpec, SqlNodeSpec, save_raw_parquet

from utils import BASE, _fetch_json, _is_permanent_client_error

log = logging.getLogger("bank-of-canada")

# Series are fetched one request each; group them into parquet batches so a
# single in-memory table never holds the whole corpus. ~200 series per batch
# keeps each file comfortably in RAM while avoiding thousands of tiny files.
OBS_CHUNK = 200

# value kept as the raw string the API returns ("1.3977", "", "..."); the
# transform TRY_CASTs to DOUBLE and drops the non-numeric rows.
OBS_SCHEMA = pa.schema([
    ("series_id", pa.string()),
    ("obs_date", pa.string()),
    ("value", pa.string()),
])


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
        rows.append({
            "series_id": series_id,
            "obs_date": obs.get("d"),
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


DOWNLOAD_SPECS = [
    NodeSpec(id="bank-of-canada-observations", fn=fetch_observations, kind="download"),
]

TRANSFORM_SPECS = [
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
