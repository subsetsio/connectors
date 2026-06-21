import re, json, io, sys
from concurrent.futures import ThreadPoolExecutor
from subsets_utils import get
import openpyxl

union = json.load(open("/Users/nathansnellaert/Documents/hardened/data/sources/elstat/work/entity_union.json"))
codes = union if isinstance(union, list) else list(union)
print("total codes:", len(codes), file=sys.stderr)

TS_INSTANCE = "Mr0GiQJSgPHd"
PUB = "https://www.statistics.gr/en/statistics/-/publication/{code}/-"
DOC_RE = re.compile(
    r'documents_WAR_publicationsportlet_INSTANCE_([A-Za-z0-9]+)[^"]*?documentID=(\d+)',
)

def scan(code):
    try:
        html = get(PUB.format(code=code), timeout=(10,60)).text
    except Exception as e:
        return code, "ERR", []
    ts = []
    seen=set()
    for m in DOC_RE.finditer(html):
        inst, did = m.group(1), m.group(2)
        if inst == TS_INSTANCE and did not in seen:
            seen.add(did); ts.append(did)
    return code, "OK", ts

results = {}
with ThreadPoolExecutor(max_workers=8) as ex:
    for code, status, ts in ex.map(scan, codes):
        results[code] = (status, ts)

no_ts = [c for c,(s,t) in results.items() if s=="OK" and not t]
errs = [c for c,(s,t) in results.items() if s=="ERR"]
has_ts = [c for c,(s,t) in results.items() if t]
import statistics
counts = [len(t) for c,(s,t) in results.items() if t]
print("HAS_TS:", len(has_ts))
print("NO_TS:", len(no_ts), no_ts)
print("ERRS:", len(errs), errs)
print("TS doc-count distribution: min/median/max:", min(counts), statistics.median(counts), max(counts))
print("multi-TS (>1):", sum(1 for c in counts if c>1))
json.dump({c:t for c,(s,t) in results.items()}, open("dev/ts_map.json","w"))
