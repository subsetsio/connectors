"""Health-invariant tests for the ISC-GEM connector raw assets."""

from subsets_utils import load_raw_parquet


def test_raw_nonempty_and_large(spec_ids):
    """The full ISC-GEM catalogue is ~74k events; a tiny or empty payload means
    pagination broke after page 1 or the FDSN mirror changed silently."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert len(table) >= 50000, f"{sid}: only {len(table)} rows; expected ~74k"


def test_raw_ids_unique_and_prefixed(spec_ids):
    """Event ids must be unique (no offset-page overlap) and iscgem-prefixed
    (proves we pulled the ISC-GEM catalogue, not a fallback default catalog)."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        ids = table.column("id").to_pylist()
        assert len(ids) == len(set(ids)), f"{sid}: duplicate event ids in raw"
        assert all(i and i.startswith("iscgem") for i in ids), \
            f"{sid}: found event ids not prefixed 'iscgem'"


def test_raw_has_core_columns(spec_ids):
    """The FDSN CSV column set must be intact — a format switch drops these."""
    expected = {"id", "time", "latitude", "longitude", "mag", "magType", "updated"}
    for sid in spec_ids:
        cols = set(load_raw_parquet(sid).column_names)
        missing = expected - cols
        assert not missing, f"{sid}: raw missing columns {missing}"
