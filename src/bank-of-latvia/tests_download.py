"""Health-invariant tests for the Bank of Latvia connector.

Run post-DAG inside the connector, reading raw through subsets_utils so they
behave identically locally and in the cloud. They catch the silent failure modes
of the INTS postback export + pivot melt: an empty parse, a postback that quietly
returned the HTML page, or values that failed to coerce to numbers.
"""
from subsets_utils import load_raw_parquet

_EXPECTED_COLS = {"table_id", "row_label", "period", "value"}


def test_all_raw_nonempty(spec_ids):
    """Every table's melted parquet must hold rows. Empty usually means the
    postback re-rendered the page instead of exporting, or the layout changed."""
    bad = []
    for sid in spec_ids:
        try:
            t = load_raw_parquet(sid)
        except FileNotFoundError:
            bad.append(f"{sid}: missing")
            continue
        if t.num_rows == 0:
            bad.append(f"{sid}: 0 rows")
    assert not bad, "empty/missing raw: " + "; ".join(bad[:10])


def test_schema_stable(spec_ids):
    """Every table melts to the same long schema; value must be floating point."""
    bad = []
    for sid in spec_ids:
        try:
            t = load_raw_parquet(sid)
        except FileNotFoundError:
            continue
        cols = set(t.column_names)
        if cols != _EXPECTED_COLS:
            bad.append(f"{sid}: cols={sorted(cols)}")
            continue
        import pyarrow as pa
        if not pa.types.is_floating(t.schema.field("value").type):
            bad.append(f"{sid}: value not float ({t.schema.field('value').type})")
    assert not bad, "schema problems: " + "; ".join(bad[:10])


def test_periods_present(spec_ids):
    """Each table should label its observations with a non-empty period for the
    bulk of rows — an all-empty period column means header detection broke."""
    bad = []
    for sid in spec_ids:
        try:
            t = load_raw_parquet(sid)
        except FileNotFoundError:
            continue
        periods = t.column("period").to_pylist()
        nonempty = sum(1 for p in periods if p and p.strip())
        if periods and nonempty == 0:
            bad.append(sid)
    assert not bad, "all-empty period column for: " + ", ".join(bad[:10])
