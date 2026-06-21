"""Health-invariant tests for the Central Bank of Sri Lanka connector.

Each raw asset is the long-format melt of one ESS statistical workbook, written
as NDJSON. These tests catch silent degradation the file-existence check misses:
empty/truncated downloads, a layout change that breaks the melt, or the value
parser ceasing to produce numbers.
"""

from subsets_utils import load_raw_ndjson


def test_all_raw_assets_nonempty(spec_ids):
    """Every workbook must melt to at least a handful of long rows. An empty or
    near-empty asset means the xlsx download failed or the source layout changed
    so the melt produced nothing."""
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        assert len(rows) >= 5, f"{sid}: only {len(rows)} melted rows (expected >=5)"


def test_value_parsing_works(spec_ids):
    """Across the corpus the melt must yield genuine numeric values. If the value
    parser silently stopped (e.g. number format changed), this trips."""
    numeric = 0
    for sid in spec_ids:
        for r in load_raw_ndjson(sid):
            if r.get("value") is not None:
                numeric += 1
                break
    frac = numeric / len(spec_ids) if spec_ids else 0
    assert frac >= 0.95, (
        f"only {numeric}/{len(spec_ids)} assets have any numeric value "
        f"({frac:.0%}); value parsing likely degraded"
    )


def test_schema_shape(spec_ids):
    """Every melted row must carry the expected long-format keys."""
    expected = {"row_label", "col_label", "period_year", "value", "value_text"}
    for sid in spec_ids[:20]:
        for r in load_raw_ndjson(sid)[:50]:
            missing = expected - set(r)
            assert not missing, f"{sid}: row missing keys {missing}"
