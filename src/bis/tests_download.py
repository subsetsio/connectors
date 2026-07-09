"""Post-DAG health invariants for the BIS connector.

These run in-connector after the download nodes. They catch silent degradation
a file-existence check misses: empty payloads, a topic that switched to a layout
with no observations, or obs values that failed to parse to numbers.

Memory discipline: the largest BIS topics (locational/consolidated banking, debt
securities) decompress to multi-GB Arrow tables. `load_raw_parquet()` would
materialise the whole table in memory — loading every topic fully (and once per
test) peaks at ~15 GB and OOM-kills the 16 GB GitHub runner, which surfaces as a
cancelled job even though the DAG already finished. Instead we stream each topic
exactly once through DuckDB over a local path (see `raw_parquet_localpath`'s
docstring), computing all invariants as scalar aggregates so peak memory stays
in the low hundreds of MB regardless of topic size.
"""
import functools

import duckdb
import pyarrow.parquet as pq

from subsets_utils import raw_parquet_localpath

# Every topic carries its own SDMX dimension columns, so only the identity /
# observation spine is common across all 27.
EXPECTED_COLUMNS = {
    "dataflow",
    "series_key",
    "freq",
    "time_period",
    "period_start",
    "obs_value",
}


def _raw_ids(spec_ids):
    """Download spec ids only — the harness passes every DAG node id (downloads
    *and* `-transform` nodes), but raw Parquet exists solely for downloads."""
    return [sid for sid in spec_ids if not sid.endswith("-transform")]


@functools.lru_cache(maxsize=None)
def _stats(sid):
    """One memory-bounded pass over a topic's raw Parquet.

    Returns scalar aggregates + the column set — never the table itself. The
    schema comes from the Parquet footer (no data scanned); the row/obs/time
    counts stream through DuckDB. Cached per sid so the four invariant tests
    below share a single pass (and a single tempfile download in cloud mode).
    """
    with raw_parquet_localpath(sid) as path:
        cols = set(pq.read_schema(path).names)
        rows, non_null_obs, nonempty_tp = duckdb.sql(
            f"""
            SELECT
                count(*),
                count(obs_value),
                count(*) FILTER (WHERE length(time_period) > 0)
            FROM read_parquet('{path}')
            """
        ).fetchone()
    return {
        "rows": rows,
        "cols": cols,
        "non_null_obs": non_null_obs,
        "nonempty_tp": nonempty_tp,
    }


def test_all_raw_assets_nonempty(spec_ids):
    """Every topic's raw Parquet should hold rows — a 0-row asset usually means
    the bulk file moved, the zip layout changed, or the CSV parsed to nothing."""
    for sid in _raw_ids(spec_ids):
        assert _stats(sid)["rows"] > 0, f"{sid}: raw parquet has 0 rows"


def test_schema_is_uniform(spec_ids):
    """Every topic must normalise to the fixed long schema; a missing column
    means the SDMX flat layout drifted and normalisation silently dropped it."""
    for sid in _raw_ids(spec_ids):
        missing = EXPECTED_COLUMNS - _stats(sid)["cols"]
        assert not missing, f"{sid}: missing columns {missing}"


def test_has_parsable_observations(spec_ids):
    """Each topic must carry at least one non-null numeric observation. All-null
    obs_value points at an OBS_VALUE column the parser failed to locate."""
    for sid in _raw_ids(spec_ids):
        assert _stats(sid)["non_null_obs"] > 0, f"{sid}: every obs_value is null"


def test_time_period_populated(spec_ids):
    """time_period anchors every observation; a fully-empty column means the
    TIME_PERIOD column index was misread."""
    for sid in _raw_ids(spec_ids):
        assert _stats(sid)["nonempty_tp"] > 0, f"{sid}: time_period is empty for all rows"
