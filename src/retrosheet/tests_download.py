"""Health invariants for Retrosheet raw CSV downloads."""

import gzip

from subsets_utils import load_raw_file

_MIN_LINES = {
    "retrosheet-allplayers": 100000,
    "retrosheet-ballparks": 200,
    "retrosheet-batting": 1000000,
    "retrosheet-biofile": 20000,
    "retrosheet-coaches": 1000,
    "retrosheet-fielding": 1000000,
    "retrosheet-gameinfo": 200000,
    "retrosheet-managers": 1000,
    "retrosheet-pitching": 1000000,
    "retrosheet-plays": 10000000,
    "retrosheet-relatives": 100,
    "retrosheet-teams": 1000,
    "retrosheet-teamstats": 400000,
    "retrosheet-umpires": 1000,
}


def _csv_lines(spec_id: str) -> list[str]:
    raw = load_raw_file(spec_id, extension="csv.gz", binary=True)
    text = gzip.decompress(raw).decode("utf-8-sig", errors="replace")
    return text.splitlines()


def test_all_raw_csvs_have_headers_and_rows(spec_ids):
    """Every raw asset should be a gzipped CSV with a header and data rows."""
    for spec_id in spec_ids:
        lines = _csv_lines(spec_id)
        assert len(lines) >= 2, f"{spec_id}: CSV has no data rows"
        assert "," in lines[0], f"{spec_id}: first line does not look like a CSV header"


def test_expected_line_floors(spec_ids):
    """Loose row floors catch truncated ZIP extraction or accidental subset files."""
    for spec_id in spec_ids:
        floor = _MIN_LINES.get(spec_id)
        if floor is None:
            continue
        line_count = len(_csv_lines(spec_id))
        assert line_count >= floor, f"{spec_id}: got {line_count} lines, expected >= {floor}"


def test_core_headers_present(spec_ids):
    expected_fragments = {
        "retrosheet-gameinfo": ("game",),
        "retrosheet-plays": ("game",),
        "retrosheet-batting": ("game",),
        "retrosheet-pitching": ("game",),
        "retrosheet-fielding": ("game",),
        "retrosheet-teamstats": ("game",),
        "retrosheet-biofile": ("id",),
    }
    for spec_id in spec_ids:
        fragments = expected_fragments.get(spec_id)
        if not fragments:
            continue
        header = _csv_lines(spec_id)[0].lower()
        missing = [fragment for fragment in fragments if fragment not in header]
        assert not missing, f"{spec_id}: header missing expected fragments {missing}: {header}"
