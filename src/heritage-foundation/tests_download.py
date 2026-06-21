"""Health invariants for the Heritage Foundation raw asset.

The single download node melts every Index edition into one long parquet. These
catch silent degradation a file-exists check would miss: a host going dark
(missing whole editions), the Excel layout changing (no rows / no components),
or scores parsing to garbage.
"""

from subsets_utils import load_raw_parquet


def test_raw_nonempty_and_long(spec_ids):
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert table.num_rows > 10000, f"{sid}: only {table.num_rows} rows; an edition host likely went dark"
        cols = set(table.column_names)
        assert {"year", "country", "component", "score"} <= cols, f"{sid}: unexpected columns {cols}"


def test_edition_coverage(spec_ids):
    """We expect ~18 editions (2009-2026). Far fewer means a host stopped serving."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        years = set(table.column("year").to_pylist())
        assert min(years) <= 2009, f"{sid}: earliest edition is {min(years)}, expected <=2009"
        assert len(years) >= 15, f"{sid}: only {len(years)} editions; expected ~18"


def test_overall_component_present(spec_ids):
    """Every edition carries an 'overall' index value; if the slug vanished, the
    header classifier broke."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        components = set(table.column("component").to_pylist())
        assert "overall" in components, f"{sid}: no 'overall' component — header mapping broke"
        assert "property_rights" in components, f"{sid}: no 'property_rights' — header mapping broke"


def test_scores_in_range(spec_ids):
    """Index scores are 0-100. A value outside that means we read the wrong column
    (e.g. a rank or a country id) as a score."""
    import pyarrow.compute as pc
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        scores = table.column("score")
        non_null = pc.drop_null(scores)
        if len(non_null) == 0:
            raise AssertionError(f"{sid}: every score is null")
        lo = pc.min(non_null).as_py()
        hi = pc.max(non_null).as_py()
        assert 0 <= lo and hi <= 100, f"{sid}: scores out of 0-100 range ({lo}..{hi})"
