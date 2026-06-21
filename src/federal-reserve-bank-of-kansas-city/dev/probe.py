import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import sys
from subsets_utils import get, configure_http

BROWSER_UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
configure_http(headers={"User-Agent": BROWSER_UA, "Accept": "text/html,application/xhtml+xml,*/*"})

def probe(url, **kw):
    try:
        r = get(url, timeout=(10, 60), **kw)
        print(f"  -> {r.status_code} | {r.headers.get('content-type','?')} | {len(r.content)} bytes")
        return r
    except Exception as e:
        print(f"  -> ERROR {type(e).__name__}: {e}")
        return None

print("=== FRED fredgraph.csv (keyless) KCFSI ===")
r = probe("https://fred.stlouisfed.org/graph/fredgraph.csv?id=KCFSI")
if r is not None and r.status_code == 200:
    print("  head:", r.text[:200].replace("\n","\\n"))

print("=== FRED fredgraph.csv LMCI series ===")
for sid in ("FRBKCLMCILA","FRBKCLMCIM"):
    print(f"-- {sid}")
    r = probe(f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={sid}")
    if r is not None and r.status_code==200:
        print("  head:", r.text[:160].replace("\n","\\n"))

print("=== KC Fed manufacturing landing page ===")
r = probe("https://www.kansascityfed.org/surveys/manufacturing-survey/")
if r is not None and r.status_code==200:
    import re
    links = re.findall(r'href="([^"]+\.(?:xls|xlsx))"', r.text, re.I)
    print("  xls links:", links[:10])
    # also documents links
    docs = re.findall(r'(/documents/\d+/[^"\']+)', r.text)
    print("  /documents/ refs:", docs[:15])
