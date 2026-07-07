"""Post-DAG health invariants for WHO GHO raw downloads."""

from subsets_utils import load_raw_parquet


def test_indicators_catalog_nonempty(spec_ids):
    if "who-indicators" not in spec_ids:
        return
    table = load_raw_parquet("who-indicators")
    assert table.num_rows >= 1000, (
        f"who-indicators: only {table.num_rows} rows; expected >=1000"
    )
    assert table.column("IndicatorCode").null_count == 0, (
        "who-indicators: null IndicatorCode values present"
    )


def test_values_corpus_substantial(spec_ids):
    if "who-values" not in spec_ids:
        return
    table = load_raw_parquet("who-values")
    assert table.num_rows >= 1_000_000, (
        f"who-values: only {table.num_rows} rows; expected >=1,000,000"
    )
    assert table.column("IndicatorCode").null_count == 0, (
        "who-values: null IndicatorCode values present"
    )


def test_values_have_many_indicators_and_numbers(spec_ids):
    if "who-values" not in spec_ids:
        return
    table = load_raw_parquet("who-values")
    indicators = set(table.column("IndicatorCode").to_pylist()[:500000])
    assert len(indicators) >= 500, (
        f"who-values: only {len(indicators)} distinct indicators in head sample"
    )
    numeric = table.column("NumericValue").to_pylist()[:500000]
    assert any(v is not None for v in numeric), (
        "who-values: NumericValue is all-null in head sample"
    )
