"""Health invariants for Realtime Inequality raw assets.

Each spec writes NDJSON. These catch silent degradation that file-existence
alone misses: empty/truncated payloads, a backfill that lost the 1976 history,
or the source quietly dropping the income/wealth columns.
"""

from subsets_utils import load_raw_ndjson

# Minimum rows per asset — well below observed counts (~28.9k / ~10.9k / ~11.3k
# / ~603) but high enough that a truncated or single-page fetch trips.
_MIN_ROWS = {
    "realtime-inequality-online-database": 20000,
    "realtime-inequality-online-database-labor": 8000,
    "realtime-inequality-online-database-demographics": 8000,
    "realtime-inequality-online-database-popul-deflator": 400,
}

# A column every row of the asset must carry — guards against the source
# renaming/dropping its core measures.
_REQUIRED_COL = {
    "realtime-inequality-online-database": "wealth",
    "realtime-inequality-online-database-labor": "labor_income",
    "realtime-inequality-online-database-demographics": "demo_type",
    "realtime-inequality-online-database-popul-deflator": "pop_adults",
}


def test_raw_assets_have_expected_volume(spec_ids):
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        assert len(rows) >= _MIN_ROWS[sid], (
            f"{sid}: {len(rows)} rows, expected >= {_MIN_ROWS[sid]} — likely truncated"
        )


def test_required_columns_and_keys_present(spec_ids):
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        sample = rows[0]
        assert "year" in sample and "month" in sample, f"{sid}: missing year/month keys"
        col = _REQUIRED_COL[sid]
        assert col in sample, f"{sid}: missing expected column {col!r}"


def test_history_reaches_1976(spec_ids):
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        years = [r["year"] for r in rows if isinstance(r.get("year"), (int, float))]
        assert years, f"{sid}: no numeric year values"
        assert min(years) <= 1976, f"{sid}: earliest year {min(years)}, expected <= 1976"
