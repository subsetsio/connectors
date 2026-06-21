import io, csv
from subsets_utils import get

def fetch(url):
    r = get(url, timeout=(10,120))
    ct = r.headers.get("Content-Type","")
    return r.status_code, ct, r.text

def header_and_count(text):
    rdr = csv.reader(io.StringIO(text))
    rows = list(rdr)
    return (rows[0] if rows else []), max(0, len(rows)-1)

# 1. expected_statistics across a year that exists and an early year
for y in (2024, 2016, 2015):
    u=f"https://baseballsavant.mlb.com/leaderboard/expected_statistics?type=batter&year={y}&csv=true"
    sc,ct,t=fetch(u); h,n=header_and_count(t)
    print(f"exp_stats {y}: {sc} ct={ct[:20]} rows={n} hdr0={h[:4]}")

# 2. bat-tracking in a pre-existence year (2019) -> empty? error?
for y in (2024, 2019):
    u=f"https://baseballsavant.mlb.com/leaderboard/bat-tracking?attackZone=&batSide=&type=batter&year={y}&csv=true"
    sc,ct,t=fetch(u); h,n=header_and_count(t)
    print(f"bat-tracking {y}: {sc} ct={ct[:20]} rows={n} hdr0={h[:3]}")

# 3. does 'year' appear in header for statcast (exit velo) board?
u="https://baseballsavant.mlb.com/leaderboard/statcast?type=batter&year=2024&csv=true"
sc,ct,t=fetch(u); h,n=header_and_count(t)
print(f"statcast board hdr has year? {'year' in h} cols={len(h)} sample={h[:6]}")

# 4. statcast pitch search one day: shape & rowcount, content-type
u="https://baseballsavant.mlb.com/statcast_search/csv?all=true&type=details&player_type=pitcher&game_date_gt=2023-07-04&game_date_lt=2023-07-04"
sc,ct,t=fetch(u); h,n=header_and_count(t)
print(f"statcast_search 1day: {sc} ct={ct[:25]} rows={n} cols={len(h)} game_date_in_hdr={'game_date' in h}")

# 5. off-season day -> empty?
u="https://baseballsavant.mlb.com/statcast_search/csv?all=true&type=details&player_type=pitcher&game_date_gt=2024-01-15&game_date_lt=2024-01-15"
sc,ct,t=fetch(u); h,n=header_and_count(t)
print(f"statcast_search offseason: {sc} ct={ct[:25]} rows={n} textlen={len(t)}")
