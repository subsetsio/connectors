import io, csv, hashlib
from subsets_utils import get
def fetch(url):
    r=get(url,timeout=(10,120)); return r.text
def sig(t):
    rdr=list(csv.reader(io.StringIO(t)))
    h=rdr[0] if rdr else []
    return len(rdr)-1, hashlib.md5(t.encode()).hexdigest()[:8], h

# statcast exit-velo board (no year col): compare years + no-year + check for year col
for y in ("2024","2023","2018","2015"):
    n,d,h=sig(fetch(f"https://baseballsavant.mlb.com/leaderboard/statcast?type=batter&year={y}&csv=true"))
    print(f"statcast y={y}: rows={n} md5={d} hasyear={'year' in h}")
n,d,h=sig(fetch("https://baseballsavant.mlb.com/leaderboard/statcast?type=batter&csv=true"))
print(f"statcast no-year: rows={n} md5={d} cols={len(h)} hdr={h[:6]}")

# does statcast board accept start/end season params?
n,d,h=sig(fetch("https://baseballsavant.mlb.com/leaderboard/statcast?type=batter&year=2021&min_season=2015&max_season=2024&csv=true"))
print(f"statcast range params: rows={n} md5={d} hasyear={'year' in h}")

# arm-strength (likely starts 2020) early year
for y in ("2024","2020","2016"):
    n,d,h=sig(fetch(f"https://baseballsavant.mlb.com/leaderboard/arm-strength?type=Fielder&year={y}&csv=true"))
    print(f"arm-strength y={y}: rows={n} md5={d} hasyear={'year' in h}")
