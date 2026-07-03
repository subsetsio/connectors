"""Post-DAG health invariants — catch silent degradation (empty payloads,
truncated downloads, format drift) that file-existence alone misses."""
from subsets_utils import load_raw_parquet


def test_countries_nonempty(spec_ids):
    """The country reference table should hold ~200-300 rows; a collapse to a
    handful means the catalog endpoint changed shape or paging broke."""
    table = load_raw_parquet("world-bank-countries")
    assert len(table) >= 200, f"countries: only {len(table)} rows (expected >=200)"
    assert table.column("id").null_count == 0, "countries: null id present"


def test_indicators_nonempty(spec_ids):
    """The indicator catalog is ~29.5k records; far fewer means the /indicator
    enumeration broke or stopped after page 1."""
    table = load_raw_parquet("world-bank-indicators")
    assert len(table) >= 10000, f"indicators: only {len(table)} rows (expected >=10000)"
    assert table.column("id").null_count == 0, "indicators: null id present"


def test_values_nonempty(spec_ids):
    """The WDI bulk archive unpivots to millions of long-format observations.
    A collapse to a handful means the bulk CSV changed shape, the ZIP member
    was renamed, or the unpivot dropped everything."""
    table = load_raw_parquet("world-bank-values")
    assert len(table) >= 1_000_000, (
        f"values: only {len(table)} rows (expected >=1,000,000)"
    )
    assert table.column("value").null_count == 0, "values: null value present"
    assert table.column("indicator_code").null_count == 0, "values: null indicator_code"
