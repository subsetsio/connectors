from subsets_utils import load_raw_ndjson


def test_raw_assets_have_rows(spec_ids):
    for spec_id in spec_ids:
        rows = load_raw_ndjson(spec_id)
        assert rows, f"{spec_id}: raw NDJSON has no rows"


def test_product_ids_present(spec_ids):
    for spec_id in spec_ids:
        rows = load_raw_ndjson(spec_id)
        missing = [idx for idx, row in enumerate(rows[:1000]) if not row.get("product_id")]
        assert not missing, f"{spec_id}: sampled rows missing product_id: {missing[:10]}"
