"""Health invariants for the DG ECFIN Business & Consumer Surveys raw downloads."""
from subsets_utils import load_raw_parquet

# Core columns every SDMX-CSV dataflow must carry; if the format drifts or the
# trailing-field handling breaks, these disappear.
_REQUIRED = {"REF_AREA", "ACTIVITY", "FREQ", "TIME_PERIOD", "OBS_VALUE"}

# Each BCS dataflow is a long panel (countries x dimensions x decades of
# monthly/quarterly obs); a few-hundred rows means the fetch was truncated.
_MIN_ROWS = 500


def test_all_raw_assets_nonempty(spec_ids):
    for sid in spec_ids:
        t = load_raw_parquet(sid)
        assert t.num_rows >= _MIN_ROWS, f"{sid}: {t.num_rows} rows < {_MIN_ROWS}"


def test_core_columns_present(spec_ids):
    for sid in spec_ids:
        cols = set(load_raw_parquet(sid).column_names)
        missing = _REQUIRED - cols
        assert not missing, f"{sid}: missing core columns {missing} (have {cols})"


def test_no_stray_trailing_column(spec_ids):
    """The unnamed trailing CSV field must be dropped, not landed as a column."""
    for sid in spec_ids:
        cols = load_raw_parquet(sid).column_names
        stray = [c for c in cols if c.startswith("_extra")]
        assert not stray, f"{sid}: stray trailing columns leaked: {stray}"


def test_obs_value_has_numbers(spec_ids):
    """OBS_VALUE is stored as string; at least some must parse as floats."""
    for sid in spec_ids:
        t = load_raw_parquet(sid)
        vals = t.column("OBS_VALUE").to_pylist()[:2000]
        parsed = 0
        for v in vals:
            try:
                float(v)
                parsed += 1
            except (TypeError, ValueError):
                pass
        assert parsed > 0, f"{sid}: no parseable OBS_VALUE in first {len(vals)} rows"
