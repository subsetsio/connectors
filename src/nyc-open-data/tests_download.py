"""Health-invariant tests for the NYC Open Data connector.

Run post-DAG, in-connector. They guard against silent mass degradation —
the Socrata export switching format, auth throttling, or pagination breaking —
without failing on the handful of genuinely-empty or deleted upstream datasets
that a 1100-dataset portal inevitably contains.
"""

from subsets_utils import load_raw_parquet


def test_majority_assets_nonempty(spec_ids):
    """Across a portal this size a few datasets are legitimately empty/deleted,
    but if MOST raw assets are empty the export endpoint or our parsing broke."""
    checked = 0
    nonempty = 0
    for sid in spec_ids:
        try:
            table = load_raw_parquet(sid)
        except FileNotFoundError:
            continue
        checked += 1
        if table.num_rows > 0:
            nonempty += 1
    assert checked > 0, "no raw parquet assets found at all"
    assert nonempty >= 0.5 * checked, (
        f"only {nonempty}/{checked} raw assets have rows; "
        "the bulk-CSV export or DuckDB parse likely degraded"
    )


def test_assets_have_columns(spec_ids):
    """Every materialized asset must carry at least one normalized column.
    A 0-column table means the CSV header was lost or normalize_names produced
    nothing — a parsing regression, not an upstream emptiness."""
    bad = []
    for sid in spec_ids:
        try:
            table = load_raw_parquet(sid)
        except FileNotFoundError:
            continue
        if table.num_columns == 0:
            bad.append(sid)
    assert not bad, f"{len(bad)} assets have 0 columns (e.g. {bad[:5]})"
