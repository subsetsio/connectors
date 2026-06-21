"""Health-invariant tests for the INDEC raw assets.

Run post-DAG inside the connector; they load raw through subsets_utils so they
behave identically locally and in the cloud. They catch silent degradation that
file-existence alone misses: empty payloads, a broken source filter, or the
values stream collapsing to a single series.
"""

from subsets_utils import load_raw_parquet


def test_series_catalog_nonempty():
    """The series catalog should hold ~9,500 INDEC series. A near-empty table
    means the dataset_source filter or /search pagination broke."""
    t = load_raw_parquet("indec-indec-series")
    assert t.num_rows >= 3000, f"series catalog has only {t.num_rows} rows"
    sources = set(t.column("dataset_source").to_pylist())
    assert sources == {"Instituto Nacional de Estadística y Censos (INDEC)"}, (
        f"catalog leaked non-INDEC sources: {sources}"
    )


def test_values_nonempty_and_multi_series():
    """Long-format values should cover many series and many observations. A
    tiny table or a single distinct series means the /series fan-out broke."""
    t = load_raw_parquet("indec-indec-values")
    assert t.num_rows >= 100_000, f"values has only {t.num_rows} rows"
    distinct = len(set(t.column("series_id").to_pylist()))
    assert distinct >= 3000, f"values covers only {distinct} distinct series"


def test_values_have_finite_numbers():
    """Values must be real numbers (not all-null / not NaN poisoned)."""
    import math
    t = load_raw_parquet("indec-indec-values")
    sample = t.column("value").to_pylist()[:5000]
    assert sample, "no values present"
    assert all(v is not None and math.isfinite(v) for v in sample), (
        "values contain null/NaN/inf in the first 5000 rows"
    )
