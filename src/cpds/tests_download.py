"""Health invariants for CPDS raw assets, run post-DAG inside the connector."""
from subsets_utils import load_raw_parquet, load_raw_ndjson


def test_main_nonempty_and_wide(spec_ids):
    """The main CPDS panel must hold its country-year rows and its wide
    indicator schema. A truncated download or a switched sheet shows up as
    too few rows or too few columns."""
    if "cpds-main" not in spec_ids:
        return
    table = load_raw_parquet("cpds-main")
    assert table.num_rows >= 1500, f"cpds-main: {table.num_rows} rows (expected >=1500)"
    assert table.num_columns >= 200, f"cpds-main: {table.num_columns} cols (expected >=200)"
    assert "year" in table.column_names and "country" in table.column_names


def test_government_composition_nonempty(spec_ids):
    """The government-composition long table must hold rows across all the
    per-country sheets. An empty payload means the workbook layout changed."""
    if "cpds-government-composition" not in spec_ids:
        return
    rows = load_raw_ndjson("cpds-government-composition")
    assert len(rows) >= 4000, f"cpds-government-composition: {len(rows)} rows (expected >=4000)"
    countries = {r.get("country") for r in rows}
    assert len(countries) >= 30, f"only {len(countries)} countries in gov-composition"
