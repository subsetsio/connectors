import json
from subsets_utils import get

REPOS = {
    "systema_globalis": "https://raw.githubusercontent.com/open-numbers/ddf--gapminder--systema_globalis/master",
    "fasttrack": "https://raw.githubusercontent.com/open-numbers/ddf--gapminder--fasttrack/master",
}

for repo, base in REPOS.items():
    dp = get(base + "/datapackage.json", timeout=(10, 120)).json()
    resources = dp.get("resources", [])
    print(f"\n=== {repo}: {len(resources)} resources ===")
    # Look at datapoints resources
    dps = []
    for r in resources:
        path = r.get("path", "")
        if "datapoints" in path:
            pk = r.get("schema", {}).get("primaryKey")
            dps.append((path, pk))
    print(f"datapoints resources: {len(dps)}")
    for path, pk in dps[:5]:
        print("  ", path, "PK=", pk)
    # distinct primaryKey shapes
    from collections import Counter
    shapes = Counter(tuple(pk) if isinstance(pk, list) else (pk,) for _, pk in dps)
    print("PK shapes:", dict(shapes))
    # one non-geo-time example fields
    for r in resources:
        if "datapoints" in r.get("path", ""):
            fields = [f["name"] for f in r.get("schema", {}).get("fields", [])]
            print("  sample fields:", fields, "path=", r["path"])
            break

# concepts columns per repo
for repo, base in REPOS.items():
    txt = get(base + "/ddf--concepts.csv", timeout=(10, 120)).text
    header = txt.splitlines()[0]
    print(f"\n{repo} concepts header: {header}")
