"""Health invariants for the Opportunity Insights raw downloads.

Each download parses its source CSV into a typed Arrow table (DuckDB full-file
type detection) and saves it as parquet. A healthy fetch produces a non-empty
table with at least one column; an empty / truncated payload (host hiccup,
format switch, redirect to an HTML error page) yields zero rows or zero columns,
which is what these catch.
"""

from subsets_utils import load_raw_parquet


def test_all_raw_parquets_have_rows(spec_ids):
    bad = []
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        if table.num_rows == 0 or table.num_columns == 0:
            bad.append((sid, table.num_rows, table.num_columns))
    assert not bad, f"{len(bad)} raw parquets are empty (rows, cols): {bad[:10]}"
