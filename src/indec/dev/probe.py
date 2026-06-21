from subsets_utils import get
from urllib.parse import urljoin

BASE = "https://apis.datos.gob.ar"
start = "/series/api/dump/sspm/series-tiempo-metadatos.csv"

def resolve(url, max_hops=6):
    cur = urljoin(BASE, url)
    for _ in range(max_hops):
        r = get(cur, follow_redirects=False, timeout=(10,60))
        if r.status_code in (301,302,303,307,308):
            loc = r.headers["location"]
            cur = urljoin(cur, loc)
            print("  ->", r.status_code, cur[:120])
            continue
        return cur, r
    raise RuntimeError("too many redirects")

print("=== resolving metadatos ===")
final, r = resolve(start)
print("FINAL status", r.status_code, "ctype", r.headers.get("content-type"), "len", len(r.content))
if r.status_code == 200:
    text = r.content.decode("utf-8", errors="replace")
    lines = text.splitlines()
    print("nlines", len(lines))
    print("HEADER:", lines[0][:400])
    print("ROW1:", lines[1][:400])
