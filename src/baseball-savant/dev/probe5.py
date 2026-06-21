import io, csv, hashlib
from subsets_utils import get
def sig(url):
    t=get(url,timeout=(10,120)).text
    rdr=list(csv.reader(io.StringIO(t)))
    return len(rdr)-1, hashlib.md5(t.encode()).hexdigest()[:8], (rdr[0][:4] if rdr else [])
print("bat-tracking date-range:")
for y in ("2025","2024","2023","2022"):
    n,d,h=sig(f"https://baseballsavant.mlb.com/leaderboard/bat-tracking?attackZone=&batSide=&type=batter&dateStart={y}-01-01&dateEnd={y}-12-31&csv=true")
    print(f"  {y}: rows={n} md5={d}")
print("pitch-tempo date-range:")
for y in ("2024","2020","2016"):
    n,d,h=sig(f"https://baseballsavant.mlb.com/leaderboard/pitch-tempo?dateStart={y}-01-01&dateEnd={y}-12-31&csv=true")
    print(f"  {y}: rows={n} md5={d}")
# does pitch-tempo even have a date filter? check its form
