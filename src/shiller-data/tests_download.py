from subsets_utils import load_raw_parquet


WORKBOOK_SPECS = {
    "shiller-data-long-term-market-volatility",
    "shiller-data-us-home-prices",
    "shiller-data-us-stock-markets-cape",
}


def test_all_raw_assets_nonempty(spec_ids):
    for spec_id in spec_ids:
        table = load_raw_parquet(spec_id)
        assert table.num_rows > 0, f"{spec_id}: raw table has 0 rows"


def test_workbook_assets_have_period_rows(spec_ids):
    for spec_id in sorted(set(spec_ids) & WORKBOOK_SPECS):
        table = load_raw_parquet(spec_id)
        periods = [v for v in table.column("period_value").to_pylist() if v is not None]
        assert len(periods) >= 100, f"{spec_id}: too few parsed period rows"
        assert max(periods) >= 2023, f"{spec_id}: workbook appears stale/truncated"


def test_repeat_sales_cities_present(spec_ids):
    spec_id = "shiller-data-repeat-sales-house-prices"
    if spec_id not in spec_ids:
        return
    table = load_raw_parquet(spec_id)
    cities = set(table.column("city").to_pylist())
    assert cities == {"Atlanta", "Chicago", "Dallas", "Oakland"}
    assert table.num_rows >= 35000
