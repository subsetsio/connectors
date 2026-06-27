"""Health invariants for ListenBrainz raw assets — catch silent degradation
(empty payloads, a single window slipping through, format drift) that mere file
existence would miss."""

from subsets_utils import load_raw_ndjson


def test_all_raw_assets_nonempty(spec_ids):
    """Every endpoint must yield rows; an empty payload usually means the API
    changed shape or every window 204'd."""
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        assert rows, f"{sid}: raw ndjson has 0 rows"


def test_rows_carry_range(spec_ids):
    """Every row must be tagged with its aggregation window — the column the
    transforms partition on."""
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        missing = sum(1 for r in rows if not r.get("range"))
        assert missing == 0, f"{sid}: {missing} rows missing 'range' tag"


def test_multiple_windows_present(spec_ids):
    """We request six rolling windows; if only one comes back the others are
    silently 204'ing (or the loop broke). Allow some windows to be uncomputed
    but require at least two so a total collapse trips this."""
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        ranges = {r.get("range") for r in rows}
        assert len(ranges) >= 2, f"{sid}: only windows {ranges} present; expected several"
