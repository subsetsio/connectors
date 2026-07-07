"""Health-invariant tests for the Banguat connector raw assets.

These run post-DAG, in-connector, through the subsets_utils loaders — they
catch silent degradation (empty payloads, a SOAP endpoint that switched to
returning empty arrays) that file-existence alone misses.
"""

from subsets_utils import load_raw_ndjson


def test_exchange_rates_nonempty():
    rows = load_raw_ndjson("banco-de-guatemala-exchange-rates")
    assert len(rows) > 0, "exchange_rates: TipoCambioRango returned 0 rows"
    assert any(r.get("fecha") for r in rows), "exchange_rates: no rate dates present"
