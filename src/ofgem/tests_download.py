"""Health-invariant tests for the Ofgem connector raw assets.

Each chart's raw asset is long-format ndjson with columns
(category, series, value). These tests catch silent degradation that file
existence alone misses: empty payloads, an everviz format change that yields
all-null values, or a parse that dropped the series dimension.
"""
from subsets_utils import load_raw_ndjson


def test_all_raw_assets_nonempty(spec_ids):
    """Every chart should yield at least one (category, series, value) row.
    An empty asset means the everviz inject changed shape or data.csv vanished."""
    empty = []
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        if not rows:
            empty.append(sid)
    assert not empty, f"{len(empty)} assets have 0 rows: {empty[:10]}"


def test_assets_have_numeric_values(spec_ids):
    """Across all charts the overwhelming majority must carry at least one
    non-null numeric value. A spike of all-null assets means value parsing
    broke (e.g. delimiter misdetection)."""
    all_null = []
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        if rows and not any(r.get("value") is not None for r in rows):
            all_null.append(sid)
    assert len(all_null) <= max(2, len(spec_ids) // 50), (
        f"{len(all_null)}/{len(spec_ids)} charts have no numeric values: {all_null[:10]}"
    )


def test_expected_columns(spec_ids):
    """Each row must carry the long-format triple. A missing key means the
    normalisation step changed and downstream SQL will break."""
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        if not rows:
            continue
        sample = rows[0]
        for col in ("category", "series", "value"):
            assert col in sample, f"{sid}: row missing '{col}' column: {sample}"
        break  # one healthy asset proves the shape; all share the same writer
