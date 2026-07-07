from subsets_utils import list_raw_fragments, raw_asset_exists


EXPECTED_MIN_FRAGMENTS = {
    "opm-accessions": 200,
    "opm-employment": 150,
    "opm-separations": 200,
}


def test_raw_assets_exist(spec_ids):
    for spec_id in spec_ids:
        assert raw_asset_exists(spec_id, "parquet"), f"{spec_id}: raw parquet asset missing"


def test_expected_fragment_counts(spec_ids):
    for spec_id in spec_ids:
        fragments = list_raw_fragments(spec_id, "parquet")
        min_count = EXPECTED_MIN_FRAGMENTS[spec_id]
        assert len(fragments) >= min_count, (
            f"{spec_id}: got {len(fragments)} fragments, expected at least {min_count}"
        )


def test_fragments_nonempty(spec_ids):
    for spec_id in spec_ids:
        fragments = list_raw_fragments(spec_id, "parquet")
        empty = [name for name, meta in fragments.items() if meta.get("size", 0) <= 0]
        assert not empty, f"{spec_id}: empty raw fragments: {empty[:5]}"
