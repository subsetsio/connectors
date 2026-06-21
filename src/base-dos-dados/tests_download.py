"""Health invariants for the Base dos Dados raw assets.

Each raw asset is the source one-click CSV, parsed with robust options and
persisted as typed parquet (see the node module for why we normalize at
download time). These catch silent degradation that file-existence alone
misses: an empty payload, an unreadable parquet, or a table with columns but
no data rows.
"""

from subsets_utils import load_raw_parquet


def test_raw_assets_are_nonempty_parquet(spec_ids):
    """Every asset must load as parquet with >=1 column and >=1 data row."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert table.num_columns >= 1, f"{sid}: parquet has no columns"
        assert table.num_rows >= 1, (
            f"{sid}: parquet has {table.num_rows} rows; expected >=1"
        )
