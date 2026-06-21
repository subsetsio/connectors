"""Health-invariant tests for the National Records of Scotland connector.

Run post-DAG, in-connector, against the raw assets via subsets_utils loaders.
Catch silent degradation that file-existence alone misses: empty payloads,
truncated crawls, or a measure-value column that lost all its numbers.
"""
from subsets_utils import load_raw_parquet


def test_all_raw_assets_nonempty(spec_ids):
    """Every cube must publish observations. An empty parquet means the SPARQL
    crawl returned nothing (endpoint format/scheme change or a silent timeout)."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert len(table) > 0, f"{sid}: raw parquet has 0 rows"


def test_value_column_present_and_numeric(spec_ids):
    """Each cube row carries a measure value that parses as a number for the
    overwhelming majority of rows; a column that is entirely non-numeric means
    we grabbed the wrong object in the measureType join."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert "value" in table.column_names, f"{sid}: missing 'value' column"
        assert "measure_type" in table.column_names, f"{sid}: missing 'measure_type'"
        vals = table.column("value").to_pylist()
        numeric = 0
        for v in vals:
            if v is None or v == "":
                continue
            try:
                float(v)
                numeric += 1
            except (TypeError, ValueError):
                pass
        assert numeric > 0, f"{sid}: no numeric values in 'value' column"
