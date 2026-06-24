"""Health invariants for the FBSP Anuário download nodes.

Each raw asset is one Anuário data table parsed to long form. These catch silent
degradation the file-existence check misses: empty payloads, a parser that
stopped finding state rows, or year/value columns going non-numeric.
"""

from subsets_utils import load_raw_parquet


def test_all_raw_assets_nonempty(spec_ids):
    """Every accepted table must parse to rows. 0 rows means the workbook layout
    changed or the sheet match broke."""
    for sid in spec_ids:
        t = load_raw_parquet(sid)
        assert len(t) > 0, f"{sid}: raw parquet has 0 rows"


def test_geography_and_years_sane(spec_ids):
    """Each table is a UF-by-year cross-tab: it should span several distinct
    Brazilian geographies and plausible years."""
    for sid in spec_ids:
        t = load_raw_parquet(sid).to_pydict()
        geos = set(t["geography"])
        assert len(geos) >= 5, f"{sid}: only {len(geos)} distinct geographies"
        years = [y for y in t["year"] if y is not None]
        assert years, f"{sid}: no year values"
        assert all(1990 <= y <= 2030 for y in years), f"{sid}: year out of range"


def test_values_present(spec_ids):
    """The value column carries the statistic; an all-null column means the
    column index drifted."""
    for sid in spec_ids:
        vals = load_raw_parquet(sid).to_pydict()["value"]
        assert any(v is not None for v in vals), f"{sid}: all values null"
