from subsets_utils import load_raw_parquet


def test_country_panel_shape(spec_ids):
    """The country panel must hold a broad multi-country, multi-century span.
    A collapse to a handful of rows means the sheet parse or download broke."""
    sid = "maddison-project-country-panel"
    if sid not in spec_ids:
        return
    t = load_raw_parquet(sid)
    assert t.num_rows > 20000, f"{sid}: only {t.num_rows} rows; expected >20k"
    assert set(t.column_names) == {"countrycode", "country", "region", "year", "gdppc", "pop"}, \
        f"{sid}: unexpected columns {t.column_names}"
    countries = set(t.column("countrycode").to_pylist())
    assert len(countries) >= 150, f"{sid}: only {len(countries)} country codes; expected >=150"
    nonnull = sum(1 for v in t.column("gdppc").to_pylist() if v is not None)
    assert nonnull > 10000, f"{sid}: only {nonnull} non-null gdppc values"


def test_regional_aggregates_shape(spec_ids):
    """Regional aggregates must cover the 8 Maddison regions plus World and
    carry real gdppc values; an unpivot regression would drop regions or values."""
    sid = "maddison-project-regional-aggregates"
    if sid not in spec_ids:
        return
    t = load_raw_parquet(sid)
    assert t.num_rows > 50, f"{sid}: only {t.num_rows} rows"
    assert set(t.column_names) == {"region", "year", "gdppc", "pop"}, \
        f"{sid}: unexpected columns {t.column_names}"
    regions = set(t.column("region").to_pylist())
    assert "World" in regions, f"{sid}: missing World region; got {regions}"
    assert len(regions) >= 9, f"{sid}: only {len(regions)} regions; expected >=9"
    nonnull = sum(1 for v in t.column("gdppc").to_pylist() if v is not None)
    assert nonnull > 50, f"{sid}: only {nonnull} non-null gdppc values"
