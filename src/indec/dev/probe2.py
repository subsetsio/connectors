from subsets_utils import get
from urllib.parse import urljoin
import requests, httpx

BASE = "https://apis.datos.gob.ar"
start = "/series/api/dump/sspm/series-tiempo-metadatos.csv"

# get the presigned location via subsets (no follow)
def presigned(path):
    cur = urljoin(BASE, path)
    for _ in range(6):
        r = get(cur, follow_redirects=False, timeout=(10,60))
        if r.status_code in (301,302,303,307,308):
            cur = urljoin(cur, r.headers["location"]); continue
        return cur
    raise RuntimeError

loc = presigned(start)
print("presigned:", loc[:130])

# A) requests, follow redirects from the start url
ra = requests.get(urljoin(BASE,start), timeout=120)
print("A requests full-chain:", ra.status_code, len(ra.content), ra.headers.get("content-type"))

# B) httpx follow_redirects from start
try:
    rb = httpx.get(urljoin(BASE,start), follow_redirects=True, timeout=120)
    print("B httpx full-chain:", rb.status_code, len(rb.content))
except Exception as e:
    print("B err", e)

if ra.status_code==200:
    lines = ra.content.decode("utf-8","replace").splitlines()
    print("nlines", len(lines)); print("HEADER:", lines[0][:400]); print("ROW1:", lines[1][:400])
