"""Health-invariant tests for the AHRQ (MEPS PUF) connector.

These run post-DAG, in-connector, against the raw parquet each download node
wrote. They catch silent degradation that mere file-existence misses: an
endpoint that started returning an HTML error page, a truncated/empty xlsx, or
a format switch that yields a single junk column.
"""
from subsets_utils import load_raw_parquet


def test_all_raw_assets_nonempty(spec_ids):
    """Every PUF should parse to a non-empty microdata table. MEPS public-use
    files all carry thousands of survey records; 0 rows means the download or
    xlsx parse silently broke."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert len(table) > 0, f"{sid}: raw parquet has 0 rows"


def test_assets_are_wide_microdata(spec_ids):
    """MEPS PUFs are wide survey microdata — even the narrowest event files
    carry well over a dozen variables. A table that collapsed to 1-2 columns
    signals the xlsx was misread (e.g. an HTML error page parsed as one cell)."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert table.num_columns >= 5, (
            f"{sid}: only {table.num_columns} columns; expected wide microdata"
        )
