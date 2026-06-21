from subsets_utils import get
import httpx

BASE = "https://apis.datos.gob.ar/series/api/dump/sspm"
url = f"{BASE}/series-tiempo-metadatos.csv"

# Step 1: get the 302 without following
r = get(url, follow_redirects=False, timeout=(10,60))
print("step1 status", r.status_code)
loc = r.headers.get("location")
print("location:", loc[:160] if loc else None)

# Step 2a: subsets get on the location
r2 = get(loc, timeout=(10,120))
print("2a subsets.get status", r2.status_code, "ctype", r2.headers.get("content-type"), "len", len(r2.content))

# Step 2b: raw httpx with the literal URL, no param re-encoding
with httpx.Client(timeout=120) as c:
    r3 = c.get(loc)
    print("2b httpx literal status", r3.status_code, "len", len(r3.content))
