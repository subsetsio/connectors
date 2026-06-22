import io, pandas as pd
from subsets_utils import get

FILES = {
    "coups-annual": "CSPCoupsAnnualv2021.xls",
    "coups-list": "CSPCoupsListv2021.xls",
    "high-casualty-terrorist-bombings": "HCTBSep2021list.xls",
    "mepv-annual": "MEPVv2018.xls",
    "mepv-episodes": "MEPV2012ex.xls",
    "pitf-adverse-regime-change": "PITF Adverse Regime Change 2018.xls",
    "pitf-ethnic-war": "PITF Ethnic War 2018.xls",
    "pitf-geno-politicide": "PITF GenoPoliticide 2018.xls",
    "pitf-revolutionary-war": "PITF Revolutionary War 2018.xls",
    "polity5-annual": "p5v2018.xls",
    "polity5-case": "p5v2018d.xls",
    "state-fragility-index": "SFIv2018.xls",
}
BASE = "https://www.systemicpeace.org/inscr/"
import urllib.parse
for eid, fn in FILES.items():
    url = BASE + urllib.parse.quote(fn)
    try:
        r = get(url, timeout=(10,120))
        r.raise_for_status()
        head = r.content[:8]
        df = pd.read_excel(io.BytesIO(r.content))
        print(f"=== {eid}  [{fn}]  bytes={len(r.content)}  magic={head!r}")
        print(f"    shape={df.shape}")
        print(f"    cols={list(df.columns)[:40]}")
        print(f"    dtypes={ {c:str(t) for c,t in list(df.dtypes.items())[:40]} }")
        print(df.head(2).to_string()[:1200])
    except Exception as e:
        print(f"=== {eid} [{fn}] ERROR {type(e).__name__}: {e}")
    print()
