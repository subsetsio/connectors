"""Health invariants for Kobe Customs raw assets.

These run post-DAG in-connector and load raw via subsets_utils, so they catch
silent degradation (empty payloads, listing/format drift, parser regressions)
that mere file-existence checks miss.
"""

from subsets_utils import load_raw_parquet


def test_all_raw_assets_nonempty(spec_ids):
    """Every statistic-type must yield numeric observations. A 0-row asset means
    the listing layout changed, a ZIP 404'd, or the .xls parser broke."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert len(table) > 0, f"{sid}: raw parquet has 0 rows"


def test_multi_year_coverage(spec_ids):
    """Each type publishes several years (finalized annual series). If a type
    collapses to a single year, year discovery on the listing page broke."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        years = set(table.column("year").to_pylist())
        assert len(years) >= 2, f"{sid}: only years {sorted(years)} (expected multi-year)"
        assert max(years) >= 2024, f"{sid}: stale max year {max(years)}"


def test_values_finite_and_labeled(spec_ids):
    """Values must be real numbers and most cells must carry a reconstructed
    row label — an all-null label column means the melt lost the label axis."""
    import math
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        vals = table.column("value").to_pylist()
        assert all(v is not None and math.isfinite(v) for v in vals[:5000]), \
            f"{sid}: non-finite/null values present"
        labels = table.column("row_label").to_pylist()
        labeled = sum(1 for x in labels if x)
        assert labeled >= 0.5 * len(labels), \
            f"{sid}: only {labeled}/{len(labels)} cells have a row label"
