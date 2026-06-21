import sys; sys.path.insert(0,"src")
import io, pandas as pd
import nodes.groningen_growth_and_development_centre as N
from constants import DATASETS

def grab(eid):
    c=DATASETS[eid]
    fid=N._resolve_file_id(c["doi"], c["file"])
    return N._download_datafile(fid), c

# monkeypatch _finish to NOT save, just report
def fake_finish(df, asset):
    d=df.copy()
    d["value"]=pd.to_numeric(d["value"],errors="coerce")
    d=d.dropna(subset=["value"])
    print(f"   -> {asset}: rows={len(d)} cols={list(d.columns)}")
    if "year" in d.columns and len(d):
        print(f"      year {int(d['year'].min())}..{int(d['year'].max())}")
N._finish=fake_finish

for eid in ["10.34894-inzbf2","10.34894-aeax1f","10.34894-lch4ca","10.34894-e7mvox",
            "10.34894-a7axdn","10.34894-pj2m1c","10.34894-xdtauz","10.34894-imkxnt"]:
    print(f"\n### {eid} ({DATASETS[eid]['parser']})")
    content,cfg=grab(eid)
    N._PARSERS[cfg["parser"]](content, cfg["params"], N.SLUG+"-"+eid)
