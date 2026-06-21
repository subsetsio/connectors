import io, csv, hashlib
from subsets_utils import get
def sig(url):
    r=get(url,timeout=(10,120)); t=r.text; ct=r.headers.get("Content-Type","")[:18]
    rdr=list(csv.reader(io.StringIO(t)))
    h=rdr[0] if rdr else []
    return len(rdr)-1, hashlib.md5(t.encode()).hexdigest()[:8], ct, [c.strip('"﻿ ') for c in h[:5]]
print("pitch-movement no pitch_type:", sig("https://baseballsavant.mlb.com/leaderboard/pitch-movement?year=2024&csv=true"))
print("pitch-movement pitch_type=FF:", sig("https://baseballsavant.mlb.com/leaderboard/pitch-movement?year=2024&pitch_type=FF&csv=true"))
print("pitch-arsenals 2024:", sig("https://baseballsavant.mlb.com/leaderboard/pitch-arsenals?year=2024&type=avg_speed&csv=true"))
print("pitch-arsenals 2017:", sig("https://baseballsavant.mlb.com/leaderboard/pitch-arsenals?year=2017&type=avg_speed&csv=true"))
print("sprint_speed 2024:", sig("https://baseballsavant.mlb.com/leaderboard/sprint_speed?year=2024&position=&team=&min_season=2024&max_season=2024&csv=true"))
print("sprint_speed 2016:", sig("https://baseballsavant.mlb.com/leaderboard/sprint_speed?year=2016&position=&team=&min_season=2016&max_season=2016&csv=true"))
print("active-spin 2024:", sig("https://baseballsavant.mlb.com/leaderboard/active-spin?year=2024_spin-based&csv=true"))
print("active-spin 2016:", sig("https://baseballsavant.mlb.com/leaderboard/active-spin?year=2016_spin-based&csv=true"))
print("running_splits 2016:", sig("https://baseballsavant.mlb.com/leaderboard/running_splits?type=raw&bats=&year=2016&position=&team=&min=5&csv=true"))
