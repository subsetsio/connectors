"""Health invariants for the ECB raw downloads.

Each spec writes one streamed parquet asset (one SDMX dataflow). These catch
silent degradation that file-existence alone misses: empty payloads, a flow that
quietly switched format, or numeric observation columns that stopped parsing.
"""
from subsets_utils import load_raw_parquet

EXPECTED_COLUMNS = {
    "series_key", "freq", "time_period", "obs_value",
    "obs_status", "title", "unit", "unit_mult", "decimals",
}


def test_all_raw_assets_nonempty(spec_ids):
    """Every flow's raw parquet should hold observations. Empty usually means
    the endpoint switched format or the flow was withdrawn."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert len(table) > 0, f"{sid}: raw parquet has 0 rows"


def test_schema_is_curated(spec_ids):
    """The normalised curated schema must be present on every asset, so the
    transform's column references can't silently drift."""
    for sid in spec_ids:
        cols = set(load_raw_parquet(sid).schema.names)
        missing = EXPECTED_COLUMNS - cols
        assert not missing, f"{sid}: missing curated columns {missing}"


def test_observations_are_numeric(spec_ids):
    """Each flow should carry at least some parseable numeric OBS_VALUE — a flow
    whose values stopped casting to a number publishes an empty subset."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        numeric = 0
        for v in table.column("obs_value").to_pylist():
            if v is None:
                continue
            try:
                float(v)
            except ValueError:
                continue
            numeric += 1
            if numeric > 0:
                break
        assert numeric > 0, f"{sid}: no numeric obs_value found"
