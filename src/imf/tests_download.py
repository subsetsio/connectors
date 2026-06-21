"""Health-invariant tests for the IMF connector raw assets.

Each dataflow is fetched as an all-string Parquet. These catch silent
degradation a file-exists check misses: empty payloads, missing the
OBS_VALUE/TIME_PERIOD columns (format switch), or a value column that is
entirely non-numeric (wrong endpoint / HTML error body parsed as CSV).
"""

from subsets_utils import load_raw_parquet


def test_all_raw_assets_nonempty(spec_ids):
    """Every dataflow's raw parquet should hold rows. An empty payload means the
    endpoint changed shape, returned an error body, or the wildcard query broke."""
    empty = []
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        if table.num_rows == 0:
            empty.append(sid)
    assert not empty, f"{len(empty)} raw assets have 0 rows: {empty[:10]}"


def test_core_observation_columns_present(spec_ids):
    """SDMX-CSV always carries TIME_PERIOD and OBS_VALUE. Their absence means the
    response was not the expected flat SDMX-CSV (format/accept-header drift)."""
    missing = []
    for sid in spec_ids:
        cols = set(load_raw_parquet(sid).column_names)
        if "TIME_PERIOD" not in cols or "OBS_VALUE" not in cols:
            missing.append(sid)
    assert not missing, f"{len(missing)} assets missing TIME_PERIOD/OBS_VALUE: {missing[:10]}"


def test_obs_value_mostly_numeric(spec_ids):
    """OBS_VALUE is stored as a string in raw but must parse as numbers. If a
    sample of a dataflow has no parseable values, we fetched the wrong thing."""
    bad = []
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        col = table.column("OBS_VALUE").slice(0, 1000).to_pylist()
        parseable = 0
        for v in col:
            if v in (None, ""):
                continue
            try:
                float(v)
                parseable += 1
            except (TypeError, ValueError):
                pass
        if parseable == 0:
            bad.append(sid)
    assert not bad, f"{len(bad)} assets have no numeric OBS_VALUE in first 1000 rows: {bad[:10]}"
