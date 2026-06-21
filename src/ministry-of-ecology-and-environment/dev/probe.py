from datetime import datetime, timedelta
from subsets_utils import post

BASE = "https://air.cnemc.cn:18007"
H = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "X-Requested-With": "XMLHttpRequest",
    "Origin": BASE,
    "Referer": BASE + "/",
    "Accept": "application/json, text/javascript, */*; q=0.01",
}

live = post(f"{BASE}/HourChangesPublish/GetAllAQIPublishLive", headers=H, data=b"", timeout=(10, 120)).json()
print("LIVE count:", len(live))
print("LIVE keys:", sorted(live[0].keys()))
print("LIVE sample TimePoint:", live[0]["TimePoint"], "->", live[0]["TimePointStr"])
tps = set(r["TimePoint"] for r in live)
print("LIVE distinct TimePoints:", len(tps))

# history for a specific past hour
for back in (2, 24, 47):
    hr = (datetime.utcnow() + timedelta(hours=8)).replace(minute=0, second=0, microsecond=0) - timedelta(hours=back)
    ds = hr.strftime("%Y-%m-%d %H:00:00")
    r = post(f"{BASE}/HourChangesPublish/GetAQIHistoryByConditionHis", headers={**H, "Content-Type": "application/x-www-form-urlencoded"}, data={"date": ds}, timeout=(10, 120))
    try:
        j = r.json()
    except Exception as e:
        print(f"HIST back={back} ({ds}): status={r.status_code} non-json len={len(r.text)}")
        continue
    tset = set(x.get("TimePointStr") for x in j) if j else set()
    print(f"HIST back={back} ({ds} Beijing): rows={len(j)} distinct_TimePointStr={len(tset)} sample={list(tset)[:3]}")
