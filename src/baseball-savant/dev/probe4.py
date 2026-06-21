import io, csv, hashlib
from subsets_utils import get
def sig(url):
    t=get(url,timeout=(10,120)).text
    rdr=list(csv.reader(io.StringIO(t)))
    return len(rdr)-1, hashlib.md5(t.encode()).hexdigest()[:8], (rdr[0] if rdr else [])
# try alternative season params for bat-tracking
for q in ["type=batter&year=2023&season=2023","type=batter&season=2023","type=batter&startYear=2023&endYear=2023",
          "type=batter&year=2023&perspective=batter","type=batter&year=2024&min=q"]:
    n,d,h=sig(f"https://baseballsavant.mlb.com/leaderboard/bat-tracking?{q}&csv=true")
    print(f"bat-tracking [{q}]: rows={n} md5={d}")
# pitch-tempo alt
for q in ["year=2023&season=2023","season=2023","startYear=2023&endYear=2023","year=2024&min=5"]:
    n,d,h=sig(f"https://baseballsavant.mlb.com/leaderboard/pitch-tempo?{q}&csv=true")
    print(f"pitch-tempo [{q}]: rows={n} md5={d}")
