"""Health-invariant tests for the Banguat connector raw assets.

These run post-DAG, in-connector, through the subsets_utils loaders — they
catch silent degradation (empty payloads, a SOAP endpoint that switched to
returning empty arrays) that file-existence alone misses.
"""

from subsets_utils import load_raw_parquet, load_raw_ndjson


def test_variables_nonempty():
    table = load_raw_parquet("banco-de-guatemala-variables")
    assert len(table) > 0, "variables: raw parquet has 0 rows (VariablesDisponibles empty?)"


def test_values_nonempty():
    rows = load_raw_ndjson("banco-de-guatemala-values")
    assert len(rows) > 0, "values: 0 observations (all Info* calls returned empty?)"
    # every row must identify its variable and frequency
    bad = [r for r in rows if not r.get("variable_id") or not r.get("frequency")]
    assert not bad, f"values: {len(bad)} rows missing variable_id/frequency"


def test_exchange_rates_nonempty():
    rows = load_raw_ndjson("banco-de-guatemala-exchange-rates")
    assert len(rows) > 0, "exchange_rates: TipoCambioRango returned 0 rows"
    assert any(r.get("fecha") for r in rows), "exchange_rates: no rate dates present"
