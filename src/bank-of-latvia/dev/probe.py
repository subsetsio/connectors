import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent/"src"))
import subsets_utils as su
import re, sys

TID = "115"  # daily exchange rate (small)
url = f"https://statdb.bank.lv/LB/Data/{TID}?lang=en"
print("GET", url)
try:
    r = su.get(url, timeout=(15.0, 180.0))
    print("status", r.status_code, "len", len(r.text))
    html = r.text
    for f in ("__VIEWSTATE","__VIEWSTATEGENERATOR","__EVENTVALIDATION"):
        m = re.search(r'id="%s" value="([^"]*)"' % f, html)
        print(f, "found" if m else "MISSING", (m.group(1)[:30]+"...") if m else "")
    # show export controls present
    print("lnkCsv present:", "lnkCsv" in html)
    print("cookies:", dict(r.cookies))
except Exception as e:
    print("ERR", type(e).__name__, str(e)[:200])
