"""Health-invariant tests for the ATO connector, run post-DAG in-connector.

These catch silent degradation that file-existence misses: empty/truncated
datastore pulls, and the income_year tag being lost during the per-year union.
"""

from subsets_utils import load_raw_parquet


def test_all_raw_assets_nonempty(spec_ids):
    """Every entity has a flat CSV edition — a 0-row raw asset means the
    resource download URL changed or the CSV was silently truncated."""
    empty = []
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        if len(table) == 0:
            empty.append(sid)
    assert not empty, f"{len(empty)} raw assets are empty: {empty[:10]}"


def test_income_year_column_present(spec_ids):
    """Every asset carries the income_year column (its value may be null for
    single-edition tables). A missing column means the tag step was dropped."""
    bad = []
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        if "income_year" not in table.column_names:
            bad.append(sid)
    assert not bad, f"{len(bad)} assets missing income_year column: {bad[:10]}"
