"""Post-DAG health invariants — catch silent degradation (empty payloads,
truncated downloads, format drift) that file-existence alone misses."""
from subsets_utils import load_raw_parquet, list_raw_files


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


def test_values_batches_nonempty(spec_ids):
    """The firehose writes one parquet batch per chunk of indicators. At least
    one batch must exist for this run and carry real, non-null observations."""
    batches = list_raw_files("world-bank-values-*.parquet")
    assert batches, "values: no batch parquet files were written"
    total = 0
    for rel in batches:
        asset_id = rel[: -len(".parquet")]
        table = load_raw_parquet(asset_id)
        total += len(table)
        assert table.column("value").null_count < len(table), (
            f"values batch {asset_id}: every value is null"
        )
    assert total > 0, "values: all batches empty"
