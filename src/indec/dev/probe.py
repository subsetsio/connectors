import io, zipfile, csv
from subsets_utils import get

BASE = "https://apis.datos.gob.ar/series/api/dump/sspm"

# 1. metadatos CSV (series catalog)
print("=== metadatos head ===")
r = get(f"{BASE}/series-tiempo-metadatos.csv", timeout=(10,180))
print("status", r.status_code, "len", len(r.content), "ctype", r.headers.get("content-type"))
text = r.content.decode("utf-8", errors="replace")
lines = text.splitlines()
print("nlines", len(lines))
print("HEADER:", lines[0])
for l in lines[1:3]:
    print("ROW:", l[:300])
