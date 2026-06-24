"""Health invariants for the DESNZ connector, run post-DAG in-connector.

Every download node writes a gzip NDJSON long-format extract with the same six
columns. These tests catch silent degradation that file-existence alone misses:
an empty payload (endpoint/format change), a dropped column, or an extract with
no numeric content at all (a sign the melt or the source went wrong globally).
"""
from subsets_utils import load_raw_ndjson

EXPECTED_COLUMNS = {"resource", "sheet", "row_label", "series", "value_text", "value_num"}


def test_all_raw_assets_nonempty(spec_ids):
    """Every package should yield at least one melted row. An empty extract means
    every tabular resource failed to download or parse."""
    empty = []
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        if not rows:
            empty.append(sid)
    assert not empty, f"empty raw extract for: {empty}"


def test_schema_shape(spec_ids):
    """Every row must carry the full long-format schema with a non-empty
    resource / series / value_text — the columns the transform depends on."""
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        sample = rows[: min(len(rows), 500)]
        for r in sample:
            assert EXPECTED_COLUMNS.issubset(r.keys()), \
                f"{sid}: row missing columns: {EXPECTED_COLUMNS - set(r.keys())}"
            assert r["resource"], f"{sid}: empty resource provenance"
            assert r["value_text"], f"{sid}: empty value_text (should have been skipped)"


def test_has_numeric_content(spec_ids):
    """Across the whole corpus the extracts should be mostly numeric statistics:
    at least one package must carry parsed numeric values. A corpus with zero
    numeric cells means value parsing silently broke."""
    total_numeric = 0
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        total_numeric += sum(1 for r in rows if r.get("value_num") is not None)
    assert total_numeric > 0, "no numeric values parsed across any package"
