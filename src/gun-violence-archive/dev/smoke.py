import sys, time
sys.path.insert(0, "src")
import nodes.gun_violence_archive as m
from subsets_utils import configure_http
configure_http(headers={"User-Agent": m.BROWSER_UA})
uuid, name = m._discover_report("accidental-teen-deaths")
print("discovered:", name, uuid)
t0 = time.time()
for p in range(3):
    r = m._get(f"{m.BASE}/query/{uuid}/export-api", params={"page": p})
    df = m._parse_page(r.text)
    print(f"page {p}: status={r.status_code} rows={0 if df is None else len(df)} elapsed={time.time()-t0:.1f}s")
