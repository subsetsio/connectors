"""Health invariants for SDES DiDo raw CSV assets."""

from subsets_utils import load_raw_file


def test_all_raw_csv_assets_nonempty(spec_ids):
    empty = []
    for sid in spec_ids:
        content = load_raw_file(sid, extension="csv", binary=True)
        if len(content) < 20:
            empty.append(sid)
    assert not empty, f"{len(empty)} raw CSV assets are empty/truncated: {empty[:5]}"


def test_raw_csv_assets_have_headers(spec_ids):
    missing_header = []
    for sid in spec_ids:
        content = load_raw_file(sid, extension="csv", binary=True)
        first_line = content.splitlines()[0].decode("utf-8-sig", errors="replace")
        if ";" not in first_line and "," not in first_line:
            missing_header.append((sid, first_line[:120]))
    assert not missing_header, f"CSV header not detected: {missing_header[:5]}"
