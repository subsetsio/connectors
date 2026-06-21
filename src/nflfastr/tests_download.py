"""Post-DAG health invariants for the nflfastR connector.

These run in-connector after the download nodes and load raw through the same
subsets_utils loader the fetch fn used. They catch silent degradation that file
existence alone misses — empty payloads, truncated downloads, a release whose
parquet assets vanished.
"""

from subsets_utils import load_raw_parquet


def test_all_raw_assets_nonempty(spec_ids):
    """Every entity's combined raw parquet must hold rows. An empty payload
    means the release layout changed or every season file failed to download."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert table.num_rows > 0, f"{sid}: raw parquet has 0 rows"
        assert table.num_columns > 0, f"{sid}: raw parquet has 0 columns"


def test_play_by_play_is_wide(spec_ids):
    """play-by-play is the flagship nflfastR table — ~370 advanced-metric
    columns and seasons back to 1999. A thin/short pbp means the union dropped
    files or only the latest season landed."""
    sid = "nflfastr-play-by-play"
    if sid not in spec_ids:
        return
    table = load_raw_parquet(sid)
    assert table.num_columns >= 300, f"{sid}: expected ~370 columns, got {table.num_columns}"
    assert table.num_rows >= 800_000, f"{sid}: expected >=800k plays across seasons, got {table.num_rows}"
    assert "season" in table.column_names, f"{sid}: missing 'season' column"
