from subsets_utils import load_raw_ndjson


def test_all_raw_assets_nonempty(spec_ids):
    """Every Port-of-LA dataset is a small static table; an empty payload means
    the Socrata endpoint changed format, moved, or the resource was retired."""
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        assert len(rows) > 0, f"{sid}: raw ndjson has 0 rows"


def test_expected_row_floor(spec_ids):
    """Per-dataset row counts observed during probing. A sharp drop (e.g. a
    truncated download returning page 1 only, or a silent schema swap) trips
    this. Floors are loose — ~10% below observed counts."""
    floors = {
        "port-of-la-2t3h-my34": 5,   # 2005-2012 annual emissions
        "port-of-la-38a8-tm7u": 30,  # 36 annual TEU rows
        "port-of-la-5a4i-e2zs": 30,  # short-ton annual series
        "port-of-la-i9rh-q5gx": 30,  # 38 MMRT annual rows
        "port-of-la-jmt8-y5rm": 20,  # 25 cruise-passenger years
        "port-of-la-tsuv-4rgh": 80,  # 93 monthly TEU rows
    }
    for sid in spec_ids:
        floor = floors.get(sid)
        if floor is None:
            continue
        rows = load_raw_ndjson(sid)
        assert len(rows) >= floor, f"{sid}: {len(rows)} rows < expected floor {floor}"
