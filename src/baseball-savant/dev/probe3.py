import io, csv, hashlib
from subsets_utils import get
def sig(url):
    t=get(url,timeout=(10,120)).text
    rdr=list(csv.reader(io.StringIO(t)))
    h=rdr[0] if rdr else []
    return len(rdr)-1, hashlib.md5(t.encode()).hexdigest()[:8], ('year' in h)
for y in ("2025","2024","2023","2022","2019","2015"):
    n,d,hy=sig(f"https://baseballsavant.mlb.com/leaderboard/bat-tracking?attackZone=&batSide=&type=batter&year={y}&csv=true")
    print(f"bat-tracking y={y}: rows={n} md5={d} hasyearcol={hy}")
print("---pitch-tempo (has year col? entity_id...)---")
for y in ("2024","2016","2014"):
    n,d,hy=sig(f"https://baseballsavant.mlb.com/leaderboard/pitch-tempo?year={y}&csv=true")
    print(f"pitch-tempo y={y}: rows={n} md5={d} hasyearcol={hy}")
print("---poptime (catcher, no year col)---")
for y in ("2024","2015","2014"):
    n,d,hy=sig(f"https://baseballsavant.mlb.com/leaderboard/poptime?year={y}&csv=true")
    print(f"poptime y={y}: rows={n} md5={d} hasyearcol={hy}")
