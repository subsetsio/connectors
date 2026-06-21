"""Health-invariant tests for the Correlates of War connector.

Run post-DAG, in-connector, against the raw assets the download nodes wrote
(via the same subsets_utils loader). Catches silent degradation that a file
existing can't: empty payloads, truncated/mis-parsed CSVs, single-column blobs
(a sign the delimiter or encoding fell over).
"""

from subsets_utils import load_raw_parquet


def test_all_raw_assets_nonempty(spec_ids):
    """Every download spec's raw parquet should hold rows."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert len(table) > 0, f"{sid}: raw parquet has 0 rows"


def test_all_raw_assets_multicolumn(spec_ids):
    """Every COW table is multi-column; a single column means the CSV parse
    collapsed (wrong delimiter / un-normalized line endings / bad encoding)."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert table.num_columns >= 2, (
            f"{sid}: only {table.num_columns} column(s) — likely a CSV parse failure"
        )
