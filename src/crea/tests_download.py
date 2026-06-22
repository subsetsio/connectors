"""Health invariants for the CREA HPI raw asset, run post-DAG in-connector."""

from subsets_utils import load_raw_parquet


def test_raw_nonempty(spec_ids):
    """The HPI parquet must hold rows. An empty payload usually means the ZIP
    layout or sheet headers changed and parsing silently produced nothing."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert len(table) > 0, f"{sid}: raw parquet has 0 rows"


def test_hpi_has_values(spec_ids):
    """Every row carries at least an index or a benchmark price; both columns
    all-null would mean the value columns stopped being parsed."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        cols = table.column_names
        assert "hpi_index" in cols and "benchmark_price" in cols, f"{sid}: missing value columns"
        hpi_nonnull = table.column("hpi_index").null_count < len(table)
        bm_nonnull = table.column("benchmark_price").null_count < len(table)
        assert hpi_nonnull or bm_nonnull, f"{sid}: hpi_index and benchmark_price are entirely null"


def test_multiple_geographies(spec_ids):
    """We expect dozens of geographies; a single one means sheet enumeration
    collapsed to the first sheet only."""
    import pyarrow.compute as pc
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        n = len(pc.unique(table.column("geography")))
        assert n >= 40, f"{sid}: only {n} distinct geographies; expected ~60"
