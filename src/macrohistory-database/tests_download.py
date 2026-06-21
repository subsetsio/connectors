from subsets_utils import load_raw_parquet


def test_panel_nonempty(spec_ids):
    """The JST panel raw parquet must carry the full country-year panel. A
    truncated download or a switched-out file would collapse the row count."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert len(table) >= 2000, f"{sid}: only {len(table)} rows; expected the full panel (~2700)"


def test_panel_schema(spec_ids):
    """Header drift in the workbook would silently change the columns; assert
    the identifier columns and a few flagship series survive."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        cols = set(table.column_names)
        required = {"year", "country", "iso", "gdp", "cpi", "pop", "eq_tr", "housing_tr"}
        missing = required - cols
        assert not missing, f"{sid}: missing expected columns {sorted(missing)}"
        assert len(cols) >= 50, f"{sid}: only {len(cols)} columns; expected ~59"


def test_panel_coverage(spec_ids):
    """18 advanced economies since 1870 — guard against a partial parse that
    drops countries or the historical depth."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        d = table.to_pydict()
        countries = {c for c in d["country"] if c}
        years = [y for y in d["year"] if y is not None]
        assert len(countries) >= 15, f"{sid}: only {len(countries)} countries; expected ~18"
        assert min(years) <= 1875, f"{sid}: earliest year {min(years)}; expected ~1870"
