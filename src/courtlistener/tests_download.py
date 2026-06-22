"""Post-DAG health invariants for the CourtListener bulk connector.

Each download node streams one bulk CSV table into an all-string Parquet raw
asset. These checks catch silent degradation file-existence alone misses: an
empty/truncated download, or a payload that lost its header (so the `id` primary
key column vanished)."""

from subsets_utils import load_raw_parquet


def test_all_raw_assets_nonempty(spec_ids):
    """Every bulk table should hold rows. 0 rows means the S3 object was empty,
    the range/stream truncated, or the bz2 decode produced nothing."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert table.num_rows > 0, f"{sid}: raw parquet has 0 rows"


def test_all_raw_assets_have_id(spec_ids):
    """Every CourtListener bulk table is keyed by an `id` column. Its absence
    means the CSV header was dropped or the columns shifted."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert "id" in table.column_names, f"{sid}: missing 'id' column ({table.column_names[:6]}...)"
