"""Health-invariant tests for the GEM download nodes — run post-DAG, in-connector.

Catch silent degradation that file-existence alone misses: empty payloads,
truncated downloads, the .sav parse falling back to garbage, or the economy
identity columns coming back blank.
"""

from subsets_utils import load_raw_parquet

EXPECTED_COLS = {
    "year", "economy_code", "economy_name", "economy_iso",
    "indicator", "variable", "label", "value",
}


def _download_ids(spec_ids):
    """The harness passes every spec that ran; transforms publish Delta tables,
    not raw parquet, so restrict the raw-asset checks to the download nodes."""
    return [s for s in spec_ids if not s.endswith("-transform")]


def test_raw_assets_nonempty(spec_ids):
    """Every survey's reshaped long table should hold many rows."""
    for sid in _download_ids(spec_ids):
        table = load_raw_parquet(sid)
        assert len(table) > 1000, f"{sid}: only {len(table)} rows — download/parse likely truncated"


def test_raw_schema(spec_ids):
    """The long-format schema must be stable across runs."""
    for sid in _download_ids(spec_ids):
        cols = set(load_raw_parquet(sid).column_names)
        missing = EXPECTED_COLS - cols
        assert not missing, f"{sid}: missing columns {missing}"


def test_value_and_year_populated(spec_ids):
    """value must always be present (nulls are dropped) and years must be plausible."""
    for sid in _download_ids(spec_ids):
        df = load_raw_parquet(sid).to_pandas()
        assert df["value"].notna().all(), f"{sid}: null values leaked through reshape"
        assert df["indicator"].notna().all(), f"{sid}: null indicator key"
        assert df["year"].between(1990, 2100).all(), f"{sid}: implausible survey year"
        assert df["economy_name"].notna().mean() > 0.5, f"{sid}: most economy names are blank"
        assert df["indicator"].nunique() >= 10, f"{sid}: too few distinct indicators"
