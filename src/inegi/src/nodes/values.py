"""INEGI BISE long-format observation stream.

The long-format observation stream across all ~31,817 BISE indicators at
national coverage (geo 00). Indicator ids are batched 10-per-request (the
documented cap) and streamed to one parquet asset.

Refresh model: stateless full re-pull. INEGI exposes no incremental/since
filter and revises history in place, so every run re-fetches the whole corpus
and overwrites. The values stream is bounded (~3.2k batched requests) and
finishes in one run; it is streamed row-group-by-row-group so memory stays
flat. Per-batch 400/401 (ErrorCode 100/110 = "no national data for these ids")
is handled by bisecting the batch and dropping the ids that genuinely have no
national observation — it is NOT an auth failure and is not retried.
"""

import pyarrow as pa
import pyarrow.parquet as pq  # noqa: F401  (writer type ref)

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    raw_parquet_writer,
)
from utils import _BASE, _catalog_codes, _get, _token

_BATCH_SIZE = 10            # documented multi-indicator cap
_FLUSH_ROWS = 50_000        # row-group flush threshold for the values stream

_VALUES_SCHEMA = pa.schema([
    ("indicator_id", pa.string()),
    ("topic_id", pa.string()),
    ("freq_id", pa.string()),
    ("unit_id", pa.string()),
    ("unit_mult", pa.string()),
    ("source_id", pa.string()),
    ("last_update", pa.string()),
    ("time_period", pa.string()),
    ("obs_value", pa.string()),
    ("obs_status", pa.string()),
    ("obs_exception", pa.string()),
    ("obs_note", pa.string()),
    ("cober_geo", pa.string()),
])


def _chunked(seq, size):
    for i in range(0, len(seq), size):
        yield seq[i:i + size]


def _fetch_series(ids: list) -> list:
    """Fetch national-level series for a list of indicator ids.

    A "good" response is HTTP 200 with an `application/json` body carrying a
    `Series` array. Everything else is a data/shape failure for THIS id set:
      * 400/401 (ErrorCode 100/110) — one or more ids have no national data;
      * 200 text/html — the URL exceeded the server's length limit and it
        returned the SPA "not found" shell instead of JSON;
      * 200 JSON but an error array / no Series.
    In every such case we bisect to isolate the offending ids and drop the
    single ids that genuinely have no national observation. These are data
    conditions, not transport errors, so they are never retried."""
    url = f"{_BASE}/INDICATOR/{','.join(ids)}/es/00/false/BISE/2.0/{_token()}?type=json"
    resp = _get(url)
    ctype = resp.headers.get("content-type", "")
    if resp.status_code == 200 and ctype.startswith("application/json"):
        body = resp.json()
        if isinstance(body, dict) and isinstance(body.get("Series"), list):
            return body["Series"]
        # JSON error array or unexpected shape -> treat as no-data, isolate.
    elif resp.status_code not in (200, 400, 401):
        # Genuinely unexpected status -> surface it.
        resp.raise_for_status()
        return []

    # Data failure for this id set: bisect, or drop a lone no-data id.
    if len(ids) == 1:
        return []
    mid = len(ids) // 2
    return _fetch_series(ids[:mid]) + _fetch_series(ids[mid:])


def _series_rows(series: list):
    for s in series:
        indicator_id = s.get("INDICADOR")
        topic_id = s.get("TOPIC")
        freq_id = s.get("FREQ")
        unit_id = s.get("UNIT")
        unit_mult = s.get("UNIT_MULT")
        source_id = s.get("SOURCE")
        last_update = s.get("LASTUPDATE")
        for o in s.get("OBSERVATIONS", []) or []:
            yield {
                "indicator_id": indicator_id,
                "topic_id": topic_id,
                "freq_id": freq_id,
                "unit_id": unit_id,
                "unit_mult": unit_mult,
                "source_id": source_id,
                "last_update": last_update,
                "time_period": o.get("TIME_PERIOD"),
                "obs_value": o.get("OBS_VALUE"),
                "obs_status": o.get("OBS_STATUS"),
                "obs_exception": o.get("OBS_EXCEPTION"),
                "obs_note": o.get("OBS_NOTE"),
                "cober_geo": o.get("COBER_GEO"),
            }


def fetch_values(node_id: str) -> None:
    """Stream the long-format observation table across every BISE indicator at
    national coverage. Full re-pull, streamed in 50k-row groups to one parquet."""
    ids = sorted(c["value"] for c in _catalog_codes("CL_INDICATOR"))
    if not ids:
        raise RuntimeError("CL_INDICATOR returned no indicator ids")

    buf = []
    with raw_parquet_writer(node_id, _VALUES_SCHEMA) as writer:
        for chunk in _chunked(ids, _BATCH_SIZE):
            series = _fetch_series(chunk)
            buf.extend(_series_rows(series))
            if len(buf) >= _FLUSH_ROWS:
                writer.write_table(pa.Table.from_pylist(buf, schema=_VALUES_SCHEMA))
                buf = []
        if buf:
            writer.write_table(pa.Table.from_pylist(buf, schema=_VALUES_SCHEMA))


DOWNLOAD_SPECS = [
    NodeSpec(id="inegi-values", fn=fetch_values, kind="download"),
]


TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="inegi-values-transform",
        deps=["inegi-values"],
        sql='''
            SELECT
                indicator_id,
                topic_id,
                freq_id,
                unit_id,
                source_id,
                time_period,
                CAST(obs_value AS DOUBLE) AS value,
                obs_status,
                cober_geo AS coverage_geo,
                last_update
            FROM "inegi-values"
            WHERE obs_value IS NOT NULL
              AND TRY_CAST(obs_value AS DOUBLE) IS NOT NULL
        ''',
    ),
]
