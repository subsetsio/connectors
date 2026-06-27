"""Health invariants for the Open PageRank raw download.

One asset: the Top 10 Million Domains ranking, full-pulled each run. The corpus
is ~10M rows; a large shortfall signals a truncated transfer or a changed source
format, not normal fluctuation.
"""

from subsets_utils import load_raw_parquet

# Floor well below the ~10M true size, but far above any plausible partial read.
_MIN_ROWS = 1_000_000


def test_raw_nonempty(spec_ids):
    """The raw parquet must hold rows."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert len(table) > 0, f"{sid}: raw parquet has 0 rows"


def test_corpus_size(spec_ids):
    """The ranking should carry ~millions of rows — guards a truncated download."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert len(table) >= _MIN_ROWS, (
            f"{sid}: only {len(table)} rows, expected >= {_MIN_ROWS} "
            "(possible truncated transfer or format change)"
        )


def test_columns_and_ranges(spec_ids):
    """Schema is (rank, domain, open_page_rank); domains non-null and Open
    PageRank within the documented 0-10 scale."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert set(table.column_names) == {"rank", "domain", "open_page_rank"}, (
            f"{sid}: unexpected columns {table.column_names}"
        )
        domain = table.column("domain")
        assert domain.null_count == 0, f"{sid}: {domain.null_count} null domains"
        import pyarrow.compute as pc

        opr = table.column("open_page_rank")
        assert pc.min(opr).as_py() >= 0.0, f"{sid}: Open PageRank below 0"
        assert pc.max(opr).as_py() <= 10.0, f"{sid}: Open PageRank above 10"
