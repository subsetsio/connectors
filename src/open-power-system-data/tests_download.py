"""Health-invariant tests for the OPSD connector.

Each download node writes one parquet raw asset (a full CSV snapshot converted to
typed parquet). These checks catch silent degradation that file-existence alone
misses: an empty/truncated download, or a CSV that parsed to zero columns.
"""

from subsets_utils import load_raw_parquet


def test_all_raw_assets_nonempty(spec_ids):
    """Every OPSD table is a full snapshot with rows; an empty parquet means the
    endpoint changed shape, returned an error page, or the download truncated."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert len(table) > 0, f"{sid}: raw parquet has 0 rows"


def test_all_raw_assets_have_columns(spec_ids):
    """A real OPSD CSV has many columns (13-656). Zero/one column usually means
    the delimiter sniff failed or an error body got parsed as a single cell."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert table.num_columns >= 2, (
            f"{sid}: parsed to {table.num_columns} column(s); expected a real tabular CSV"
        )
