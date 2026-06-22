from subsets_utils import load_raw_parquet


def test_raw_nonempty(spec_ids):
    """Exchange-rate raw must hold many rows; an empty/tiny payload means the
    SOAP windows came back empty (auth/endpoint/format change)."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert len(table) > 1000, f"{sid}: only {len(table)} raw rows"


def test_currency_coverage(spec_ids):
    """Grupo 0 enumerates ~40 currencies/units; if we see far fewer the
    multi-code query or currency enumeration silently degraded."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        distinct = set(table.column("moneda").to_pylist())
        distinct.discard(None)
        assert len(distinct) >= 20, f"{sid}: only {len(distinct)} distinct currencies"


def test_rates_present(spec_ids):
    """At least one of buy/sell rate must be populated on the vast majority of
    rows; an all-null rate column means the TCC/TCV parse broke."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        tcc = table.column("tcc").to_pylist()
        nonnull = sum(1 for v in tcc if v is not None)
        assert nonnull > 0.5 * len(tcc), f"{sid}: only {nonnull}/{len(tcc)} rows have a buy rate"
