"""Health-invariant tests run post-DAG inside the connector. They load raw
through subsets_utils (identical local and cloud) and catch silent degradation
that mere file-existence checks miss."""

from subsets_utils import load_raw_ndjson


def test_all_raw_assets_nonempty(spec_ids):
    """Every download spec's raw ndjson must hold records. An empty payload
    means the workbook URL changed, the layout broke our header detection, or
    the download truncated."""
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        assert len(rows) > 0, f"{sid}: raw ndjson has 0 records"


def test_records_well_formed(spec_ids):
    """Every melted record carries the long-format keys and a non-empty
    row_label/measure. Guards against the extractor emitting blank dimensions if
    a header/label column shifts."""
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        sample = rows[: min(len(rows), 200)]
        for r in sample:
            for k in ("sheet", "row_dim", "row_label", "measure", "value_text"):
                assert k in r, f"{sid}: record missing key {k!r}: {r}"
            assert r["row_label"], f"{sid}: empty row_label in {r}"
            assert r["measure"], f"{sid}: empty measure in {r}"
            assert r["value_text"] not in (None, ""), f"{sid}: empty value_text in {r}"


def test_some_numeric_values(spec_ids):
    """EDR datasets are statistical tables — across all assets the great
    majority of cells are numeric. If value_num is null everywhere, numeric
    parsing silently broke (e.g. values arrived as formatted strings)."""
    total = 0
    numeric = 0
    for sid in spec_ids:
        for r in load_raw_ndjson(sid):
            total += 1
            if r.get("value_num") is not None:
                numeric += 1
    assert total > 0, "no records across any asset"
    frac = numeric / total
    assert frac >= 0.6, f"only {frac:.1%} of {total} cells numeric; expected >=60%"
