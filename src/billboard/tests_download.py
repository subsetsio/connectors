"""Health-invariant tests for the Billboard Hot 100 raw download.

Run post-DAG inside the connector; loads raw via the same loader the download
node used (save_raw_parquet). Catches silent degradation the file-existence
check misses: truncated downloads, format switches, broken pagination.
"""
from subsets_utils import load_raw_parquet


def test_raw_nonempty(spec_ids):
    """The full history is ~354k rows. A near-empty payload means the mirror
    changed format or the fetch was truncated."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert len(table) >= 300_000, f"{sid}: only {len(table)} rows, expected >=300k"


def test_rank_bounds(spec_ids):
    """Chart positions are 1-100; anything outside means a schema/mapping break."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        ranks = table.column("rank").to_pylist()
        assert min(ranks) >= 1 and max(ranks) <= 100, (
            f"{sid}: rank out of [1,100] range (min={min(ranks)}, max={max(ranks)})"
        )


def test_full_history_span(spec_ids):
    """Coverage must reach from the 1958 inception to recent years. A truncated
    span signals the mirror served a partial file (e.g. recent.json)."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        dates = table.column("chart_date").to_pylist()
        assert min(dates) <= "1958-08-04", f"{sid}: earliest chart {min(dates)} > inception"
        assert max(dates) >= "2024-01-01", f"{sid}: latest chart {max(dates)} too old"
