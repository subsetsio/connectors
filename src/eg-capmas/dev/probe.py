import time, sys
from subsets_utils import get

BASE = "https://www.capmas.gov.eg:8080/api"
H = {"lo": "en"}

def g(path):
    r = get(f"{BASE}/{path}", headers=H, timeout=(10.0, 60.0))
    r.raise_for_status()
    return r.json()

# Get tree, gather (indicatorId, subSubjectId) pairs from a couple of subSubjects
tree = g("Subject/HasData")["data"]
pairs = []
for main in tree:
    for ss in main.get("subSubjects", []):
        ssid = ss["id"]
        d = g(f"Subject/SubSubjectWithIndicator/{ssid}")["data"]
        for p in d.get("publicationWithIndicators", []):
            for ind in p.get("indicators", []):
                pairs.append((ind["indicatorId"], ssid))
        if len(pairs) >= 60:
            break
    if len(pairs) >= 60:
        break

print(f"collected {len(pairs)} indicator pairs; now timing 50 sequential IndicatorFilter calls")
t0 = time.time()
ok = 0; empty = 0; fail = 0; pts = 0
for i, (iid, ssid) in enumerate(pairs[:50]):
    try:
        d = g(f"Indicator/IndicatorFilter?IndicatorId={iid}&SubSubjectId={ssid}")["data"]
        ok += 1
        npts = sum(len(s.get("data", [])) for s in d)
        pts += npts
        if not d: empty += 1
    except Exception as e:
        fail += 1
        print(f"  [{i}] FAIL iid={iid}: {type(e).__name__}: {str(e)[:80]}")
    if i % 10 == 9:
        el = time.time() - t0
        print(f"  {i+1} done in {el:.1f}s -> {(i+1)/el:.2f} req/s, ok={ok} empty={empty} fail={fail} pts={pts}")
el = time.time() - t0
print(f"TOTAL 50 calls in {el:.1f}s = {50/el:.2f} req/s; ok={ok} empty={empty} fail={fail} total_points={pts}")
