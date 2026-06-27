"""Health-invariant tests for the OpenPowerlifting raw download.

Catch silent degradation a file-exists check misses: a truncated download, a
header/format change upstream, or the corpus quietly shrinking to a fraction of
its real size.
"""
from subsets_utils import load_raw_parquet

CORE_COLUMNS = {
    "Name", "Sex", "Event", "Equipment", "Place", "Federation",
    "Date", "MeetCountry", "MeetName", "TotalKg",
}


def test_results_nonempty(spec_ids):
    """Empty raw usually means the endpoint changed format or the zip was
    truncated mid-download."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert len(table) > 0, f"{sid}: raw parquet has 0 rows"


def test_results_core_columns_present(spec_ids):
    """The denormalized CSV header is stable; missing core columns means the
    schema drifted and the transform's casts would break."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        missing = CORE_COLUMNS - set(table.column_names)
        assert not missing, f"{sid}: missing expected columns {sorted(missing)}"


def test_results_scale(spec_ids):
    """The full corpus is ~3.96M rows. A drop below 3M means the download was
    truncated or only a partial file was published."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert len(table) >= 3_000_000, (
            f"{sid}: only {len(table)} rows; expected >=3M (truncated download?)"
        )
