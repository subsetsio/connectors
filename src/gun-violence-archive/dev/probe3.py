import io
import re
import pandas as pd
from subsets_utils import get

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
      "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36")
BASE = "https://www.gunviolencearchive.org"
H = {"User-Agent": UA}


def uuid_for(slug):
    html = get(f"{BASE}/{slug}", headers=H, timeout=30).text
    return re.search(r"query/([a-f0-9-]{36})", html).group(1)


def page_ids(uuid, n):
    r = get(f"{BASE}/query/{uuid}/export-api", params={"page": n}, headers=H, timeout=30)
    for t in pd.read_html(io.StringIO(r.text)):
        if any("Incident ID" in str(c) for c in t.columns):
            return tuple(t["Incident ID"])
    return tuple()


def last_page(slug):
    """Binary search the highest page index that differs from its successor."""
    uuid = uuid_for(slug)
    # exponential upper bound
    hi = 1
    while page_ids(uuid, hi) != page_ids(uuid, hi + 1):
        hi *= 2
        if hi > 4096:
            break
    lo = 0
    # invariant: page(hi) == page(hi+1) (in clamp); find smallest such boundary
    while lo < hi:
        mid = (lo + hi) // 2
        if page_ids(uuid, mid) == page_ids(uuid, mid + 1):
            hi = mid
        else:
            lo = mid + 1
    return lo  # last real page index


for slug in ["accidental-child-deaths", "accidental-deaths", "officer-involved-shootings"]:
    lp = last_page(slug)
    print(f"{slug}: last_page={lp}, ~{(lp+1)*25} incidents")
