"""Health invariants for Baker Hughes raw downloads.

Catch silent degradation the file-exists check misses: empty payloads, a current
report that stopped updating (rotating-UUID discovery picked a stale file), a
parser that quietly produced the wrong shape.
"""
from datetime import date

from subsets_utils import load_raw_parquet

WEEKLY = "baker-hughes-na-rig-count-weekly"
MONTHLY = "baker-hughes-na-rig-count-monthly"
WW = "baker-hughes-worldwide-rig-count-monthly"
STATE_HIST = "baker-hughes-na-state-rig-count-historical-weekly"
WW_HIST = "baker-hughes-worldwide-rig-count-historical-monthly"


def test_all_raw_assets_nonempty(spec_ids):
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert len(table) > 0, f"{sid}: raw parquet has 0 rows"


def test_na_weekly_is_fresh_and_granular(spec_ids):
    """The NA weekly report is released weekly; if discovery picked a stale
    file the max publish_date would lag badly. Also assert the granular columns
    are present and non-trivial."""
    if WEEKLY not in spec_ids:
        return
    t = load_raw_parquet(WEEKLY)
    cols = set(t.column_names)
    assert {"country", "basin", "trajectory", "publish_date", "rig_count"} <= cols, \
        f"NA weekly missing expected columns: {cols}"
    dates = [d for d in t.column("publish_date").to_pylist() if d]
    assert dates, "NA weekly has no publish_date values"
    # The report restates full history from 2024; latest week should be recent.
    latest = max(dates)
    cutoff = (date.today().replace(day=1)).isoformat()[:7]  # this month, YYYY-MM
    assert latest[:7] >= (date(date.today().year, max(1, date.today().month - 2), 1)).isoformat()[:7], \
        f"NA weekly latest publish_date {latest} is stale (>2 months old) -- discovery may have picked an old file"
    assert len(t) > 5000, f"NA weekly only {len(t)} rows -- expected tens of thousands"


def test_countries_present(spec_ids):
    if WEEKLY not in spec_ids:
        return
    t = load_raw_parquet(WEEKLY)
    countries = set(t.column("country").to_pylist())
    up = {str(c).upper() for c in countries}
    assert any("UNITED STATES" in c or c == "US" for c in up), f"no US rows: {up}"
    assert any("CANADA" in c for c in up), f"no Canada rows: {up}"


def test_worldwide_regions(spec_ids):
    if WW not in spec_ids:
        return
    t = load_raw_parquet(WW)
    regions = {str(r) for r in t.column("region").to_pylist()}
    assert len(regions) >= 4, f"worldwide: expected several regions, got {regions}"
    assert len(t) > 500, f"worldwide only {len(t)} rows"


def test_state_historical_shape(spec_ids):
    if STATE_HIST not in spec_ids:
        return
    t = load_raw_parquet(STATE_HIST)
    cats = {str(c) for c in t.column("category").to_pylist()}
    assert {"Land", "Offshore", "Total"} <= cats, f"state hist categories incomplete: {cats}"
    dates = [d for d in t.column("date").to_pylist() if d]
    assert min(dates) < "2005-01-01", f"state hist should reach back to ~2000, earliest is {min(dates)}"
    assert len(t) > 20000, f"state hist only {len(t)} rows"


def test_worldwide_historical_shape(spec_ids):
    if WW_HIST not in spec_ids:
        return
    t = load_raw_parquet(WW_HIST)
    dates = [d for d in t.column("date").to_pylist() if d]
    assert min(dates) < "2008-01-01", f"ww hist should reach back well before 2008, earliest {min(dates)}"
    assert len(t) > 1000, f"ww hist only {len(t)} rows"
