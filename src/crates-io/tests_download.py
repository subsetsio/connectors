"""Health invariants for the crates.io raw assets.

Catch silent degradation a truncated/format-changed dump would cause: empty
tables, missing kept columns, or a crates table that lost its joined downloads.
"""
from subsets_utils import load_raw_parquet

# Minimum row counts well below current reality but far above a degraded run.
_MIN_ROWS = {
    "crates-io-crates": 100_000,
    "crates-io-versions": 500_000,
    "crates-io-dependencies": 1_000_000,
    "crates-io-version-downloads-daily": 500_000,
    "crates-io-categories": 50,
}

_REQUIRED_COLS = {
    "crates-io-crates": {"id", "name", "downloads", "created_at"},
    "crates-io-versions": {"id", "crate_id", "num", "yanked"},
    "crates-io-dependencies": {"id", "version_id", "crate_id", "kind"},
    "crates-io-version-downloads-daily": {"version_id", "date", "downloads"},
    "crates-io-categories": {"id", "slug", "category", "crates_cnt"},
}


def test_raw_assets_nonempty(spec_ids):
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        floor = _MIN_ROWS.get(sid, 1)
        assert len(table) >= floor, f"{sid}: {len(table)} rows < expected {floor}"


def test_required_columns_present(spec_ids):
    for sid in spec_ids:
        cols = set(load_raw_parquet(sid).column_names)
        need = _REQUIRED_COLS.get(sid, set())
        missing = need - cols
        assert not missing, f"{sid}: missing columns {missing} (have {sorted(cols)})"
