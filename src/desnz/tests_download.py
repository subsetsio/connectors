"""Health invariants for the DESNZ connector, run post-DAG in-connector.

Every download node writes a gzip NDJSON long-format extract with the same six
columns. These tests catch silent degradation that file-existence alone misses:
an empty payload (endpoint/format change), a dropped column, or an extract with
no numeric content at all.

The big packages melt to tens of millions of rows (multi-GB compressed), so the
extracts MUST be read by streaming a bounded prefix — never `load_raw_ndjson`,
which materializes the whole asset and would OOM the runner.
"""
import json

from subsets_utils import raw_reader

EXPECTED_COLUMNS = {"resource", "sheet", "row_label", "series", "value_text", "value_num"}


def _iter_prefix(sid, limit):
    """Yield up to `limit` parsed rows from the head of an asset's ndjson.gz,
    streaming so we never hold the whole (possibly multi-GB) file in memory."""
    with raw_reader(sid, "ndjson.gz", mode="rt", compression="gzip") as f:
        for i, line in enumerate(f):
            if i >= limit:
                break
            line = line.strip()
            if line:
                yield json.loads(line)


def test_all_raw_assets_nonempty(spec_ids):
    """Every package should yield at least one melted row. An empty extract means
    every tabular resource failed to download or parse."""
    empty = []
    for sid in spec_ids:
        first = next(_iter_prefix(sid, 1), None)
        if first is None:
            empty.append(sid)
    assert not empty, f"empty raw extract for: {empty}"


def test_schema_shape(spec_ids):
    """Every row must carry the full long-format schema with a non-empty
    resource / value_text — the columns the transform depends on."""
    for sid in spec_ids:
        for r in _iter_prefix(sid, 500):
            assert EXPECTED_COLUMNS.issubset(r.keys()), \
                f"{sid}: row missing columns: {EXPECTED_COLUMNS - set(r.keys())}"
            assert r["resource"], f"{sid}: empty resource provenance"
            assert r["value_text"], f"{sid}: empty value_text (should have been skipped)"


def test_has_numeric_content(spec_ids):
    """The extracts are statistical workbooks: parsed numeric values must appear.
    Scan a bounded prefix of each asset and stop at the first numeric — a corpus
    with zero numeric cells means value parsing silently broke."""
    for sid in spec_ids:
        for r in _iter_prefix(sid, 5000):
            if r.get("value_num") is not None:
                return
    raise AssertionError("no numeric values parsed across any package prefix")
