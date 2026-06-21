"""Post-run health invariants for the MoSPI connector.

These run in-connector after the DAG, seeing raw via subsets_utils loaders.
They catch silent degradation that file existence alone misses: an indicator
list that quietly returned empty, a sanitisation regression, or a dataset whose
schema collapsed to a single column.
"""

from subsets_utils import list_raw_files, load_raw_ndjson


def test_all_raw_assets_written(spec_ids):
    """Every download spec must have produced a raw NDJSON file."""
    for sid in spec_ids:
        files = list_raw_files(f"{sid}.ndjson*")
        assert files, f"{sid}: no raw ndjson file written"


def test_small_dataset_shape(spec_ids):
    """AISHE is small and stable (indicator/year/state/value). Loading it fully
    is cheap and confirms rows are sanitised dicts carrying a real value."""
    sid = "mospi-aishe-getaisherecords"
    if sid not in spec_ids:
        return
    rows = load_raw_ndjson(sid)
    assert len(rows) >= 100, f"{sid}: only {len(rows)} rows; indicator enumeration likely broke"
    sample = rows[0]
    assert isinstance(sample, dict) and sample, f"{sid}: empty/!dict row"
    assert all(
        all(c.isalnum() or c == "_" for c in k) for k in sample
    ), f"{sid}: unsanitised column name in {list(sample)}"
    assert "value" in sample, f"{sid}: expected a 'value' column, got {list(sample)}"


def test_index_dataset_has_index_column(spec_ids):
    """A flagship index dataset (WPI) must carry its measure column, else the
    transform's TRY_CAST would silently publish all-null."""
    sid = "mospi-wpi-getwpirecords"
    if sid not in spec_ids:
        return
    rows = load_raw_ndjson(sid)
    assert len(rows) >= 1000, f"{sid}: only {len(rows)} rows; base-year loop likely broke"
    assert "index_value" in rows[0], f"{sid}: missing index_value column, got {list(rows[0])}"
