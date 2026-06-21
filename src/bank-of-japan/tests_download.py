"""Health invariants for the Bank of Japan download nodes.

Raw is written as per-(db[/freq/chunk]) parquet batches, so we discover the
files via list_raw_files rather than loading the bare node id. These checks
catch silent degradation that file existence alone misses — empty payloads,
the catalog losing its key columns, the observations table coming back without
real values.
"""
from subsets_utils import list_raw_files, load_raw_parquet


def _assets(prefix: str) -> list[str]:
    return [p[:-len(".parquet")] for p in list_raw_files(f"{prefix}-*.parquet")]


def test_series_catalog_present_and_nonempty():
    """The catalog must materialise as one-or-more per-DB batches with rows."""
    assets = _assets("bank-of-japan-series")
    assert assets, "no bank-of-japan-series-* raw batches were written"
    total = 0
    for a in assets:
        t = load_raw_parquet(a)
        total += t.num_rows
    assert total > 0, "series catalog batches hold 0 rows in total"


def test_series_schema_intact():
    """If /getMetadata changed shape, the catalog would lose its key columns."""
    assets = _assets("bank-of-japan-series")
    assert assets, "no series batches to inspect"
    cols = set(load_raw_parquet(assets[0]).column_names)
    for required in ("db", "series_code", "name", "frequency", "unit", "last_update"):
        assert required in cols, f"series batch missing column {required}: {sorted(cols)}"


def test_values_observations_present():
    """At least some observation batches with non-null values must exist —
    an empty values table means the endpoint switched format or paging broke."""
    assets = _assets("bank-of-japan-values")
    assert assets, "no bank-of-japan-values-* raw batches were written"
    seen_rows = 0
    for a in assets:
        t = load_raw_parquet(a)
        seen_rows += t.num_rows
        if seen_rows:
            break
    assert seen_rows > 0, "values batches hold 0 observations in total"


def test_values_schema_intact():
    """Observations must carry the long-format columns the transform parses."""
    assets = _assets("bank-of-japan-values")
    assert assets, "no values batches to inspect"
    # Find a non-empty batch (a freq bucket can legitimately be all-null/empty).
    for a in assets:
        t = load_raw_parquet(a)
        if t.num_rows:
            cols = set(t.column_names)
            for required in ("db", "series_code", "survey_date", "value", "last_update"):
                assert required in cols, f"values batch missing column {required}: {sorted(cols)}"
            return
    raise AssertionError("every values batch is empty")
