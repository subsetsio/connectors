import re, time
import lxml.html
from subsets_utils import get

def chart_nav(url, kind):
    r = get(url, timeout=(10.0, 60.0))
    if r.status_code != 200:
        return r.status_code, None, None, 0
    doc = lxml.html.fromstring(r.text)
    hrefs = [a.get("href") for a in doc.xpath("//a[@href]")]
    pat = re.compile(rf"/box-office-chart/{kind}/(\d{{4}})/(\d{{2}})/(\d{{2}})$")
    dates = sorted(set("/".join(m.groups()) for h in hrefs if h for m in [pat.search(h)] if m))
    # rows in first table
    nrows = 0
    for t in doc.xpath("//table"):
        rr = t.xpath(".//tr")
        if len(rr) > 3:
            nrows = len(rr) - 1; break
    return r.status_code, dates[:3], dates[-3:], nrows

# daily nav links from a recent page
print("daily 2026/06/19:", chart_nav("https://www.the-numbers.com/box-office-chart/daily/2026/06/19", "daily"))
# how old does daily go?
for d in ["2015/06/19", "2005/06/17", "2000/06/16", "1997/06/20"]:
    s, lo, hi, n = chart_nav(f"https://www.the-numbers.com/box-office-chart/daily/{d}", "daily")
    print(f"daily {d}: status={s} rows={n}")

# rate test: 10 sequential daily fetches
t0 = time.time()
ok = 0
import datetime
base = datetime.date(2024, 1, 1)
for i in range(10):
    d = base + datetime.timedelta(days=i)
    u = f"https://www.the-numbers.com/box-office-chart/daily/{d.year}/{d.month:02d}/{d.day:02d}"
    r = get(u, timeout=(10.0, 60.0))
    if r.status_code == 200: ok += 1
dt = time.time() - t0
print(f"10 fetches in {dt:.1f}s ({10/dt:.1f}/s), ok={ok}")
