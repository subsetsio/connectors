from subsets_utils import get
import io, zipfile, csv, json

# A) Check GitHub release assets — are individual CSVs downloadable, or only the ZIP?
r = get("https://api.github.com/repos/Economic/data/releases/latest", timeout=(10,60))
print("release status", r.status_code)
if r.status_code == 200:
    d = r.json()
    print("tag:", d.get("tag_name"))
    for a in d.get("assets", []):
        print("  asset:", a["name"], a["size"], a["browser_download_url"])

# B) Try a per-indicator CSV on economic.github.io/data
for cand in [
    "https://economic.github.io/data/ceo_pay_ratio.csv",
    "https://economic.github.io/data/data/ceo_pay_ratio.csv",
]:
    try:
        rr = get(cand, timeout=(10,60))
        print("GHpages", cand, rr.status_code, rr.headers.get("content-type"), len(rr.content))
    except Exception as e:
        print("GHpages", cand, "ERR", e)
