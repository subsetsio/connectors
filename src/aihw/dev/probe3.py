from subsets_utils import get
import json
MYH="https://myhospitalsapi.aihw.gov.au/api/v1"
H={"Accept":"application/json"}
for top in [5000, 1000, 500]:
    d=get(f"{MYH}/flat-data-extract/MYH-ADM", headers=H, params={"top":top,"skip":0}, timeout=(10,120)).json()
    print("top",top,"->", list(d.keys()) if isinstance(d,dict) else type(d), str(d)[:200])
