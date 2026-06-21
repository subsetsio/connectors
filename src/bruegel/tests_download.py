"""Health-invariant tests for the Bruegel connector.

Each dataset is parsed from a bespoke Excel/JSON layout, so the dominant silent
failure is a source re-publishing with a shifted header / renamed sheet that
yields an empty or degenerate table. These tests load each raw NDJSON asset back
through subsets_utils and assert it carries a plausible number of rows.
"""
from subsets_utils import load_raw_ndjson

# Loose per-asset floors — well below observed counts, tight enough that a broken
# parse (0/1 rows) trips. Observed (Jun 2026): trade ~150k, reer ~410k, gas-imports
# ~16k, gini ~5.8k, labour ~73k, divisia ~8k, russian ~20k, sovereign ~1.7k,
# fms ~1.2k, renewables ~678, gas-demand ~5.3k, energy-crisis ~52.
_MIN_ROWS = {
    "bruegel-2026-european-energy-crisis-fiscal-response-tracker": 20,
    "bruegel-divisia-monetary-aggregates-euro-area": 2000,
    "bruegel-eu-labour-market-outlook-dashboard": 20000,
    "bruegel-eu-renewables-value-tracker": 200,
    "bruegel-european-natural-gas-demand-tracker": 1500,
    "bruegel-european-natural-gas-imports": 5000,
    "bruegel-global-and-regional-gini-coefficients-income-inequality": 2000,
    "bruegel-global-trade-tracker": 50000,
    "bruegel-real-effective-exchange-rates-for-178-countries-a-new-database": 100000,
    "bruegel-russian-foreign-trade-tracker": 8000,
    "bruegel-sovereign-bond-holdings": 800,
    "bruegel-us-foreign-military-sales": 500,
    "bruegel-china-economic-database": 100,
    "bruegel-european-clean-tech-tracker": 100,
}


def test_all_raw_assets_nonempty(spec_ids):
    """Every download spec's raw NDJSON must hold rows."""
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        assert rows, f"{sid}: raw NDJSON has 0 rows"


def test_row_counts_plausible(spec_ids):
    """Each asset clears its loose floor — guards against a shifted-header parse
    that silently returns a near-empty table."""
    for sid in spec_ids:
        floor = _MIN_ROWS.get(sid)
        if floor is None:
            continue
        n = len(load_raw_ndjson(sid))
        assert n >= floor, f"{sid}: only {n} rows (<{floor}); parse likely degraded"


def test_rows_have_values(spec_ids):
    """Every asset's rows must carry at least one non-null field beyond keys —
    catches an all-null melt."""
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        sample = rows[: min(200, len(rows))]
        assert any(any(v is not None for v in r.values()) for r in sample), \
            f"{sid}: first {len(sample)} rows are entirely null"
