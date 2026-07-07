from subsets_utils import load_raw_file


def test_all_statec_csv_assets_nonempty(spec_ids):
    for spec_id in spec_ids:
        text = load_raw_file(spec_id, extension="csv")
        lines = [line for line in text.splitlines() if line.strip()]
        assert len(lines) >= 2, f"{spec_id}: CSV has no data rows"
        assert "OBS_VALUE" in lines[0], f"{spec_id}: CSV header is missing OBS_VALUE"
