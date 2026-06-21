import sys, os, json
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
sys.path.insert(0, os.path.dirname(__file__))
from urllib.parse import quote
from subsets_utils import get
from parser import parse_workbook

BASE = "https://www.centralbankmalta.org"
paths = json.load(open("/tmp/cbm_paths.json"))

results = {}
fails = []
zero = []
for eid, path in sorted(paths.items()):
    url = BASE + quote(path)
    ext = path.rsplit(".", 1)[-1].lower()
    try:
        r = get(url, timeout=(10, 120))
        r.raise_for_status()
        rows = parse_workbook(r.content, ext)
        results[eid] = len(rows)
        if len(rows) == 0:
            zero.append(eid)
    except Exception as e:
        fails.append((eid, repr(e)[:120]))
        results[eid] = -1

print("TOTAL files:", len(paths))
print("FAILED fetch/parse:", len(fails))
for eid, e in fails:
    print("  FAIL", eid, e)
print("ZERO rows:", len(zero), zero)
print()
print("row counts (sorted asc):")
for eid, n in sorted(results.items(), key=lambda kv: kv[1]):
    print(f"  {n:7d}  {eid}")
