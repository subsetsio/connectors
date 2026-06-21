import json
from subsets_utils import get

UA = {"User-Agent": "subsets.io-connector-probe/1.0 (nathan@subsets.io)"}

# 1. sitematrix: list of all wikimedia projects
print("=== sitematrix ===")
r = get("https://www.wikidata.org/w/api.php",
        params={"action": "sitematrix", "format": "json", "smtype": "language", "smstate": "all"},
        headers=UA, timeout=(10, 60))
print("status", r.status_code)
sm = r.json()["sitematrix"]
count = int(sm["count"])
print("count field:", count)
# structure: numeric keys -> {code, name, site:[{url, dbname, code, ...}]}
hosts = []
for k, v in sm.items():
    if k in ("count", "specials"):
        continue
    for site in v.get("site", []):
        url = site.get("url", "")
        if url.startswith("https://"):
            hosts.append(url[len("https://"):])
# specials
for site in sm.get("specials", []):
    url = site.get("url", "")
    if url.startswith("https://"):
        hosts.append(url[len("https://"):])
print("total host entries:", len(hosts))
print("sample hosts:", hosts[:8])
wikipedias = [h for h in hosts if h.endswith(".wikipedia.org")]
print("wikipedia hosts:", len(wikipedias), wikipedias[:5])

# 2. all-projects support on pageviews
print("\n=== all-projects pageviews ===")
r = get("https://wikimedia.org/api/rest_v1/metrics/pageviews/aggregate/all-projects/all-access/all-agents/monthly/2024010100/2024030100",
        headers=UA, timeout=(10, 60))
print("status", r.status_code, r.text[:200])

# 3. 404 for a small/nonexistent wiki on unique-devices
print("\n=== 404 behavior tiny wiki ===")
for proj in ["aa.wikipedia", "zzzzz.wikipedia"]:
    r = get(f"https://wikimedia.org/api/rest_v1/metrics/unique-devices/{proj}/all-sites/monthly/2024010100/2024030100",
            headers=UA, timeout=(10, 60))
    print(proj, r.status_code, r.text[:150])

# 4. project segment with vs without .org on editors
print("\n=== project segment forms ===")
for proj in ["en.wikipedia", "en.wikipedia.org"]:
    r = get(f"https://wikimedia.org/api/rest_v1/metrics/edits/aggregate/{proj}/all-editor-types/all-page-types/monthly/2024010100/2024030100",
            headers=UA, timeout=(10, 60))
    print(proj, r.status_code, r.text[:120])
