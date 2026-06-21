"""Health-invariant tests for the PPAC connector raw assets.

Run post-DAG inside the connector. They catch silent degradation that file
existence alone misses: an AjaxController page that started returning an empty
result, an XLSX whose layout shifted so the parser found no data rows, or a
value column that arrived entirely non-numeric.
"""

from subsets_utils import load_raw_parquet

# raw assets carrying a numeric `value` column (REST long tables + xlsx melts)
_VALUE_ASSETS = [
    "ppac-consumption-products-wise",
    "ppac-production-petroleum-products",
    "ppac-prices-international-prices-of-crude-oil",
    "ppac-production-indigenous-crude-oil",
    "ppac-import-export",
    "ppac-natural-gas-production",
    "ppac-natural-gas-consumption",
    "ppac-production-crude-processing",
    "ppac-consumption-active-domestic-customers",
    "ppac-consumption-state-wise-pmuy-data",
    "ppac-consumption-state-wise",
    "ppac-natural-gas-import",
]


def test_all_raw_assets_nonempty(spec_ids):
    """Every download spec's raw asset should hold rows. An empty payload means
    the page/endpoint changed shape or the parser stopped matching."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert len(table) > 0, f"{sid}: raw parquet has 0 rows"


def test_value_columns_have_numbers(spec_ids):
    """Tables with a `value` column must have at least one non-null number —
    guards against a column that silently became all-null after a layout shift."""
    for sid in _VALUE_ASSETS:
        if sid not in spec_ids:
            continue
        table = load_raw_parquet(sid)
        col = table.column("value")
        assert col.null_count < len(col), f"{sid}: value column is entirely null"


def test_refinery_capacity_has_capacity(spec_ids):
    sid = "ppac-infrastructure-installed-refinery-capacity"
    if sid in spec_ids:
        table = load_raw_parquet(sid)
        col = table.column("capacity")
        assert col.null_count < len(col), f"{sid}: capacity column is entirely null"
