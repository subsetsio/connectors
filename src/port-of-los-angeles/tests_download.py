"""Health invariants for Port of Los Angeles raw downloads."""

from subsets_utils import load_raw_parquet


HISTORICAL_ID = "port-of-los-angeles-historical-teu-statistics"

MIN_HTML_CELLS = {
    "port-of-los-angeles-automobile-statistics": 30,
    "port-of-los-angeles-breakbulk-statistics": 45,
    "port-of-los-angeles-container-statistics": 60,
    "port-of-los-angeles-cruise-statistics": 80,
    "port-of-los-angeles-facts-and-figures": 40,
    "port-of-los-angeles-tonnage-statistics": 200,
}


def test_raw_assets_nonempty(spec_ids):
    for spec_id in spec_ids:
        table = load_raw_parquet(spec_id)
        assert table.num_rows > 0, f"{spec_id}: raw parquet has 0 rows"
        assert table.num_columns >= 2, f"{spec_id}: raw parquet has too few columns"


def test_historical_teu_shape(spec_ids):
    if HISTORICAL_ID not in spec_ids:
        return
    table = load_raw_parquet(HISTORICAL_ID)
    assert table.num_rows >= 36, (
        f"{HISTORICAL_ID}: expected at least 36 annual rows, got {table.num_rows}"
    )
    assert set(table.column_names) == {"year", "teus_in_million"}


def test_html_pages_kept_table_cells(spec_ids):
    for spec_id, minimum in MIN_HTML_CELLS.items():
        if spec_id not in spec_ids:
            continue
        table = load_raw_parquet(spec_id)
        assert table.num_rows >= minimum, (
            f"{spec_id}: parsed {table.num_rows} cells, expected >= {minimum}"
        )
        assert "value" in table.column_names, f"{spec_id}: missing value column"
