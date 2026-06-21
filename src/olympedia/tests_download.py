"""Health-invariant tests for the olympedia connector.

Run post-DAG, in-connector. They load each download node's raw asset via the
same loader the node used (save_raw_ndjson -> load_raw_ndjson) and assert the
data isn't silently degraded (empty payload, wrong shape, missing key columns).
"""
from subsets_utils import load_raw_ndjson

# Minimum row counts we expect per asset given what we observed while probing.
# Loose lower bounds: a healthy pull is far above these; tripping one means a
# page changed shape, parsing broke, or a fetch silently returned nothing.
MIN_ROWS = {
    "olympedia-editions": 60,
    "olympedia-countries": 300,
    "olympedia-sports": 100,
    "olympedia-medals-by-country": 100,
    "olympedia-medals-by-athlete": 10,
    "olympedia-participations": 20,
    "olympedia-age-records": 20,
    "olympedia-medal-table-by-edition": 1000,
    "olympedia-olympic-records": 5,
}


def test_all_raw_assets_nonempty(spec_ids):
    """Every download asset must hold rows; empty usually means the HTML
    layout changed or the request silently failed."""
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        assert rows, f"{sid}: raw ndjson has 0 rows"


def test_row_counts_reasonable(spec_ids):
    """Counts shouldn't collapse below the loose floors observed during probing."""
    for sid in spec_ids:
        floor = MIN_ROWS.get(sid)
        if floor is None:
            continue
        rows = load_raw_ndjson(sid)
        assert len(rows) >= floor, f"{sid}: {len(rows)} rows < expected floor {floor}"


def test_medal_tables_have_codes(spec_ids):
    """Medal-bearing assets must carry NOC codes — the join key. All-null
    noc_code means the country-link extraction broke."""
    for sid in ("olympedia-medals-by-country", "olympedia-medal-table-by-edition"):
        if sid not in spec_ids:
            continue
        rows = load_raw_ndjson(sid)
        with_code = sum(1 for r in rows if r.get("noc_code"))
        assert with_code > 0.9 * len(rows), (
            f"{sid}: only {with_code}/{len(rows)} rows have a noc_code"
        )
