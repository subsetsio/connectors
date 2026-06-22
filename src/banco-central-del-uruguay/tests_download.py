"""Health-invariant tests for the BCU connector — run post-DAG, in-connector."""

from subsets_utils import load_raw_parquet


def test_raw_nonempty(spec_ids):
    """The exchange-rate raw asset must hold many rows. An empty/tiny payload
    means the SOAP enumeration or the windowed crawl silently broke."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert len(table) > 1000, f"{sid}: raw parquet has only {len(table)} rows"


def test_multiple_currencies(spec_ids):
    """We expect a broad currency universe (group 1 lists ~31). If only a
    handful show up, the currency-code list collapsed to one/few codes."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        n = len(set(table.column("codigo_iso").to_pylist()))
        assert n >= 20, f"{sid}: only {n} distinct currencies; expected >=20"


def test_rates_positive(spec_ids):
    """Buy rates are UYU-per-unit and must be strictly positive."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        tcc = [v for v in table.column("tcc").to_pylist() if v is not None]
        assert tcc, f"{sid}: no non-null tcc values"
        assert min(tcc) > 0, f"{sid}: found a non-positive buy rate ({min(tcc)})"
