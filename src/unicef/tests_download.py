"""Health invariants for the UNICEF raw assets (run post-DAG, in-connector)."""
from subsets_utils import load_raw_parquet

# Universal tidy columns every normalized asset must carry.
_REQUIRED_COLS = {"ref_area", "indicator", "time_period", "obs_value"}


def test_all_raw_assets_nonempty(spec_ids):
    """Every dataflow must yield at least one observation. An empty asset means
    the CSV endpoint changed format, the dataflow was retired, or the stream
    truncated before the first row."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert table.num_rows > 0, f"{sid}: raw parquet has 0 rows"


def test_assets_have_universal_columns(spec_ids):
    """Each asset carries the universal tidy columns. If normalization silently
    drifted (header aliases stopped matching), these go missing."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        missing = _REQUIRED_COLS - set(table.column_names)
        assert not missing, f"{sid}: asset missing columns {missing}"


def test_ref_area_and_time_mostly_present(spec_ids):
    """ref_area and time_period are the backbone of every SDMX observation;
    a flow where they are overwhelmingly null signals a header-mapping break."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        n = table.num_rows
        area_nulls = table.column("ref_area").null_count
        time_nulls = table.column("time_period").null_count
        assert (n - area_nulls) >= 0.5 * n, f"{sid}: ref_area mostly null ({area_nulls}/{n})"
        assert (n - time_nulls) >= 0.5 * n, f"{sid}: time_period mostly null ({time_nulls}/{n})"
