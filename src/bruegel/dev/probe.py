"""Probe: for each entity, scrape the dataset page, resolve the download
link(s), download, and report file type + (for Excel) sheet names/shapes."""
import io, re, sys, zipfile, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from subsets_utils import get

ENTITIES = {
    "2026-european-energy-crisis-fiscal-response-tracker": "/dataset/2026-european-energy-crisis-fiscal-response-tracker",
    "china-economic-database": "/dataset/china-economic-database",
    "divisia-monetary-aggregates-euro-area": "/dataset/divisia-monetary-aggregates-euro-area",
    "eu-labour-market-outlook-dashboard": "/dataset/eu-labour-market-outlook-dashboard",
    "eu-renewables-value-tracker": "/dataset/eu-renewables-value-tracker",
    "european-clean-tech-tracker": "/dataset/european-clean-tech-tracker",
    "european-natural-gas-demand-tracker": "/dataset/european-natural-gas-demand-tracker",
    "european-natural-gas-imports": "/dataset/european-natural-gas-imports",
    "global-and-regional-gini-coefficients-income-inequality": "/dataset/global-and-regional-gini-coefficients-income-inequality",
    "global-trade-tracker": "/dataset/global-trade-tracker",
    "real-effective-exchange-rates-for-178-countries-a-new-database": "/publications/datasets/real-effective-exchange-rates-for-178-countries-a-new-database",
    "russian-foreign-trade-tracker": "/dataset/russian-foreign-trade-tracker",
    "sovereign-bond-holdings": "/dataset/sovereign-bond-holdings",
    "us-foreign-military-sales": "/dataset/us-foreign-military-sales",
}
BASE = "https://www.bruegel.org"
FILE_RE = re.compile(r'href="((?:https?://[^"]+)?/(?:sites/default|system)/files/[^"]+\.(?:xlsx|xls|csv|zip))"', re.I)

def resolve(path):
    html = get(BASE + path, timeout=(10, 60)).text
    links = []
    for m in FILE_RE.finditer(html):
        u = m.group(1)
        if not u.startswith("http"):
            u = BASE + u
        if u not in links:
            links.append(u)
    return links

only = sys.argv[1] if len(sys.argv) > 1 else None
for eid, path in ENTITIES.items():
    if only and only not in eid:
        continue
    print("="*100)
    print("ENTITY:", eid)
    try:
        links = resolve(path)
    except Exception as e:
        print("  resolve ERROR:", type(e).__name__, e); continue
    print("  links:", len(links))
    for u in links:
        print("   -", u)
    if not links:
        continue
    u = links[0]
    try:
        content = get(u, timeout=(10, 120)).content
    except Exception as e:
        print("  download ERROR:", type(e).__name__, e); continue
    print(f"  downloaded {len(content)} bytes from {u.rsplit('/',1)[-1]}")
    members = []
    if u.lower().endswith(".zip"):
        z = zipfile.ZipFile(io.BytesIO(content))
        for n in z.namelist():
            print("   zip member:", n, z.getinfo(n).file_size)
        members = [(n, z.read(n)) for n in z.namelist() if n.lower().endswith((".xlsx",".xls",".csv"))]
    else:
        ext = u.lower().rsplit(".",1)[-1]
        members = [(u.rsplit("/",1)[-1], content)]
    import pandas as pd
    for name, data in members[:6]:
        print("  FILE:", name)
        if name.lower().endswith(".csv"):
            try:
                df = pd.read_csv(io.BytesIO(data), nrows=5)
                print("    csv cols:", list(df.columns)[:20], "shape~", df.shape)
            except Exception as e:
                print("    csv ERROR:", e)
            continue
        try:
            xl = pd.ExcelFile(io.BytesIO(data))
            print("    sheets:", xl.sheet_names)
            for sh in xl.sheet_names[:12]:
                try:
                    df = xl.parse(sh, header=None, nrows=8)
                    print(f"      [{sh}] shape={df.shape}")
                    # show first 3 rows compactly
                    for ri in range(min(3, len(df))):
                        vals = [str(v)[:18] for v in df.iloc[ri].tolist()[:8]]
                        print("        r%d:"%ri, vals)
                except Exception as e:
                    print(f"      [{sh}] parse ERROR:", e)
        except Exception as e:
            print("    excel ERROR:", type(e).__name__, e)
