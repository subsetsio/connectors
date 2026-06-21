from subsets_utils import get
# adm2 header + size via range request
for lvl in [4,5,6]:
    u=f"https://storage.googleapis.com/global-surface-water-stats/hydrobasins{lvl}-all-2018.csv"
    r=get(u, headers={"Range":"bytes=0-300"}, timeout=(10,120))
    print("basins",lvl, r.status_code, r.text.splitlines()[:3])
# adm2 header only
r=get("https://storage.googleapis.com/global-surface-water-stats/gaul2-all-2018.csv", headers={"Range":"bytes=0-400"}, timeout=(10,120))
print("adm2 status", r.status_code)
print(r.text.splitlines()[:3])
