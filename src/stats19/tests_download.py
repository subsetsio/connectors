from subsets_utils import list_raw_fragments, raw_asset_exists


MIN_COMPRESSED_BYTES = {
    "stats19-collisions": 250_000_000,
    "stats19-vehicles": 250_000_000,
    "stats19-casualties": 150_000_000,
}


def test_raw_csv_assets_exist(spec_ids):
    for spec_id in spec_ids:
        assert raw_asset_exists(spec_id, "csv.gz"), f"{spec_id}: missing raw csv.gz"


def test_raw_csv_assets_have_expected_size(spec_ids):
    for spec_id in spec_ids:
        fragments = list_raw_fragments(spec_id, "csv.gz")
        full = fragments.get("full")
        assert full, f"{spec_id}: missing committed full fragment"
        size = int(full.get("size") or 0)
        expected = MIN_COMPRESSED_BYTES[spec_id]
        assert size >= expected, f"{spec_id}: got {size} bytes, expected >= {expected}"
