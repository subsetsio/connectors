"""Post-DAG health invariants for the Central Bank of Malta connector.

Each download spec parses one CBM Excel table into a long-format parquet of
(sheet, section_label, row_label, series, value). These tests catch silent
degradation that file-existence checks miss: empty parses, a column that
stopped carrying numbers, or a parser that collapsed to a single junk row.
"""
from subsets_utils import load_raw_parquet


def test_all_raw_assets_nonempty(spec_ids):
    """Every table must parse to rows. An empty parse means the file changed
    layout, returned an error page, or the parser stopped recognising it."""
    empty = []
    for sid in spec_ids:
        try:
            n = len(load_raw_parquet(sid))
        except Exception as e:  # noqa: BLE001 - report which asset failed to load
            empty.append(f"{sid} (load error: {e!r})")
            continue
        if n == 0:
            empty.append(f"{sid} (0 rows)")
    assert not empty, f"{len(empty)} assets empty/unloadable: {empty[:10]}"


def test_values_are_finite_numbers(spec_ids):
    """The value column must hold real, mostly non-null numbers. An all-null
    value column means parsing matched headers but not data cells."""
    import math

    bad = []
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        if len(table) == 0:
            continue
        vals = table.column("value").to_pylist()
        nonnull = [v for v in vals if v is not None]
        if not nonnull:
            bad.append(f"{sid}: all-null values")
            continue
        if any(isinstance(v, float) and (math.isnan(v) or math.isinf(v)) for v in nonnull):
            bad.append(f"{sid}: NaN/Inf in values")
    assert not bad, f"value-quality failures: {bad[:10]}"


def test_series_labels_present(spec_ids):
    """Every row should carry a non-empty `series` (the column-header lineage).
    Blank series across an asset means header detection failed for it."""
    bad = []
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        if len(table) == 0:
            continue
        series = table.column("series").to_pylist()
        if all((s is None or s == "") for s in series):
            bad.append(sid)
    assert not bad, f"assets with no series labels: {bad[:10]}"
