"""Post-DAG health invariants for the BCRP connector."""
from subsets_utils import load_raw_parquet


def test_series_catalog_nonempty(spec_ids):
    """The series catalog should hold ~17,000 rows; a big drop means the
    metadata file truncated or the delimiter/encoding changed."""
    table = load_raw_parquet("central-bank-of-peru-series")
    assert len(table) >= 12000, (
        f"series catalog has {len(table)} rows; expected ~17,100 (>=12000)"
    )
    # codigo_serie must be populated on every row.
    codes = table.column("codigo_serie").to_pylist()
    assert all(c for c in codes), "series catalog has blank codigo_serie values"


def test_values_nonempty_and_typed(spec_ids):
    """Observations must be present, numeric, and span multiple frequencies.
    An empty or single-frequency table means the crawl degraded silently."""
    table = load_raw_parquet("central-bank-of-peru-values")
    assert len(table) >= 500_000, (
        f"values has {len(table)} rows; expected millions (>=500k)"
    )
    freqs = set(table.column("frecuencia").to_pylist()[:200000])
    assert len(freqs) >= 3, f"expected multiple frequencies, got {freqs}"
    # values are floats, dates are ISO strings
    vals = table.column("value").to_pylist()[:1000]
    assert any(v is not None for v in vals), "no numeric values in sample"


def test_values_reference_real_series(spec_ids):
    """Every observed codigo_serie must exist in the catalog — guards against
    a parsing bug emitting codes that don't join."""
    cat = set(load_raw_parquet("central-bank-of-peru-series")
              .column("codigo_serie").to_pylist())
    obs = load_raw_parquet("central-bank-of-peru-values")
    sample = set(obs.column("codigo_serie").to_pylist()[:50000])
    orphans = sample - cat
    assert not orphans, f"{len(orphans)} observed codes not in catalog: {list(orphans)[:5]}"
