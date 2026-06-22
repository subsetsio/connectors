import io, json
import pandas as pd
from subsets_utils import get

CATALOG_URL = "https://raw.githubusercontent.com/us-cbo/cbo-data/main/catalog.json"
RAW_BASE = "https://raw.githubusercontent.com/us-cbo/cbo-data/main/"
ENTITY_IDS = ["automatic_stabilizers","demographic","economic_projections","historical_budget",
 "historical_economic","long_term_budget","long_term_economic","revenue_detail",
 "spending_detail","tax_parameters","ten_year_budget","trust_fund"]

cat = get(CATALOG_URL, timeout=60).json()
ds_by_id = {d.get("identifier"): d for d in cat.get("datasets", [])}

for eid in ENTITY_IDS:
    d = ds_by_id.get(eid)
    dists = d.get("distribution", [])
    print("="*70)
    print(f"{eid}: {len(dists)} distributions")
    file_types = sorted(set(str(x.get("file_type")) for x in dists))
    vintages = sorted(set(str(x.get("vintage")) for x in dists))
    print(f"  file_types={file_types}")
    print(f"  vintages={vintages[:6]}{'...' if len(vintages)>6 else ''}")
    # sample one distribution per file_type
    seen_ft = set()
    for dist in dists:
        ft = str(dist.get("file_type"))
        if ft in seen_ft: continue
        seen_ft.add(ft)
        url = RAW_BASE + dist.get("downloadURL")
        try:
            df = pd.read_csv(io.StringIO(get(url, timeout=120).text))
        except Exception as e:
            print(f"  [{ft}] ERROR {e}")
            continue
        print(f"  [{ft}] cols={list(df.columns)} rows={len(df)}")
        print(f"        dtypes={ {c:str(t) for c,t in df.dtypes.items()} }")
        print(f"        sample={df.head(2).to_dict(orient='records')}")
