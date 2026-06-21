"""Health invariants for the Global Forest Watch raw assets.

Each download writes a tidy country-level parquet. These checks catch silent
degradation the file-existence check misses: an endpoint that switched format or
started returning an empty / single-country payload.
"""

from subsets_utils import load_raw_parquet

# Asset id -> a column that MUST be present (the country/grouping key proves the
# expected schema came back, not just some bytes).
_KEY_COLUMN = {
    "global-forest-watch-fao-forest-extent": "iso",
    "global-forest-watch-fao-forest-change": "iso",
    "global-forest-watch-fao-forestry-employment": "iso",
    "global-forest-watch-gadm--tcl--iso-change": "iso",
    "global-forest-watch-gadm--tcl--iso-summary": "iso",
    "global-forest-watch-carbonflux-iso-summary": "iso",
    "global-forest-watch-gadm--integrated-alerts--iso-daily-alerts": "iso",
    "global-forest-watch-wri-global-power-plant-database": "country",
    "global-forest-watch-gfw-universal-mill-list": "mill_name",
}


def test_all_raw_assets_nonempty(spec_ids):
    """Every spec's raw asset should hold rows. Empty usually means the query
    silently failed or the dataset version had no data."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert table.num_rows > 0, f"{sid}: raw parquet has 0 rows"


def test_expected_key_column_present(spec_ids):
    """The grouping/country key must survive — guards against a schema or
    column-quoting regression in the download SQL."""
    for sid in spec_ids:
        col = _KEY_COLUMN.get(sid)
        if col is None:
            continue
        table = load_raw_parquet(sid)
        assert col in table.column_names, (
            f"{sid}: expected column '{col}' missing; got {table.column_names}"
        )


def test_country_coverage_plausible(spec_ids):
    """The country-keyed datasets should span many countries, not one. A
    collapse to a handful of isos means the source paginated/truncated."""
    for sid in ("global-forest-watch-gadm--tcl--iso-change",
                "global-forest-watch-fao-forest-extent"):
        if sid not in spec_ids:
            continue
        table = load_raw_parquet(sid)
        n_iso = len(set(table.column("iso").to_pylist()))
        assert n_iso >= 50, f"{sid}: only {n_iso} distinct iso codes; expected >=50"
