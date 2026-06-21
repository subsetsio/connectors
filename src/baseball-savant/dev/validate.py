import sys, types
import nodes.baseball_savant as m

# capture save_raw_ndjson instead of writing to production raw
captured = {}
def fake_save(rows, asset_id, **kw):
    captured[asset_id] = list(rows)
    return f"mem://{asset_id}"
m.save_raw_ndjson = fake_save

# 1. year-honoring board with both player types
m.fetch_leaderboard("baseball-savant-expected-statistics")
rows = captured["baseball-savant-expected-statistics"]
yrs = sorted({r.get("_requested_year") for r in rows})
pts = sorted({r.get("_player_type") for r in rows})
print(f"expected-statistics: {len(rows)} rows, years={yrs}, player_types={pts}")
print("  sample:", {k:rows[0][k] for k in list(rows[0])[:6]})

# 2. snapshot board (ignores year)
m.fetch_leaderboard("baseball-savant-pitch-tempo")
rows = captured["baseball-savant-pitch-tempo"]
yrs = sorted({r.get("_requested_year") for r in rows}, key=lambda x:(x is None,x))
print(f"pitch-tempo: {len(rows)} rows, _requested_year set={yrs}")

# 3. a fielding board (Fielder type, starts later years)
m.fetch_leaderboard("baseball-savant-arm-strength")
rows = captured["baseball-savant-arm-strength"]
yrs = sorted({r.get("_requested_year") for r in rows})
print(f"arm-strength: {len(rows)} rows, years={yrs}")

# 4. statcast single window helpers
from datetime import date
txt = m._fetch_csv_text("https://baseballsavant.mlb.com/statcast_search/csv?all=true&type=details&player_type=pitcher&game_date_gt=2023-07-04&game_date_lt=2023-07-06")
parsed = m._parse_csv(txt)
typed = m._typed_rows(parsed)
print(f"statcast 3-day window: rows={len(typed)} cols={len(typed[0])} game_date={typed[0]['game_date']} rel_speed_type={type(typed[0]['release_speed']).__name__}")
