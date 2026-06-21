"""Health invariants for the BLS bulk flat-file download assets.

Catches silent degradation that file-existence alone misses: empty/truncated
payloads, the 403-on-bad-UA quirk silently yielding an HTML error body, and the
stable 5-column observation schema drifting.
"""
from subsets_utils import load_raw_parquet

_EXPECTED_COLS = {"series_id", "year", "period", "value", "footnote_codes"}


def test_all_raw_assets_nonempty(spec_ids):
    """Every survey asset must hold observation rows. Empty usually means the
    listing parse failed or the endpoint returned an HTML error body."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert len(table) > 0, f"{sid}: raw parquet has 0 rows"


def test_schema_stable(spec_ids):
    """The tab-delimited observation schema is stable across every survey."""
    for sid in spec_ids:
        cols = set(load_raw_parquet(sid).column_names)
        assert cols == _EXPECTED_COLS, f"{sid}: unexpected columns {cols}"


def test_values_mostly_numeric(spec_ids):
    """Raw `value` is kept as string (for '-' sentinels), but the overwhelming
    majority must parse as numbers — a wholesale failure signals a format shift
    (e.g. wrong delimiter, shifted columns)."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        vals = table.column("value").to_pylist()
        sample = vals[:5000]
        numeric = 0
        for v in sample:
            try:
                float(v)
                numeric += 1
            except (TypeError, ValueError):
                pass
        assert numeric >= 0.5 * len(sample), (
            f"{sid}: only {numeric}/{len(sample)} sampled values numeric"
        )
