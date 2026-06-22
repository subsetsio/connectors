import time, json, io
from subsets_utils import get
BASE = "https://opendata.centralbank.ie"

def show(pid):
    for a in range(10):
        r = get(f"{BASE}/api/3/action/package_show?id={pid}&_={a}", timeout=(10,120))
        rec = json.loads(r.content.decode("utf-8","replace"))["result"]
        if rec.get("name") == pid:
            return rec
        time.sleep(0.4)
    raise RuntimeError(pid)

for pid in ["holders-of-long-term-irish-government-bonds","payment-fraud-statistics",
            "monthly-card-payment-statistics","ncid-part-4-claim-settlements",
            "quarterly-financial-accounts","securities-issues-of-irish-companies"]:
    rec = show(pid)
    print(f"\n===== {pid}")
    for r in rec.get("resources", []):
        url = r.get("url")
        try:
            head = get(url, timeout=(10,120)).content[:300].decode("utf-8","replace").splitlines()[0]
        except Exception as e:
            head = f"ERR {e}"
        print(f"  [{r.get('name')!r}] header: {head}")
