import json
from subsets_utils import get
BASE = "https://seer.cancer.gov/statistics-network/explorer/source/content_writers/"
def r5(**p):
    r = get(BASE+"render_region_5.php", params=p, timeout=(10,120)); r.raise_for_status()
    b=r.json(); return json.loads(b) if isinstance(b,str) else b
def reg2(site,dt):
    r=get(BASE+"render_region_2_controls.php", params={"site":site,"data_type":dt}, timeout=(10,120)); r.raise_for_status(); return r.json()
def show(tag,**p):
    print(f"\n== {tag} {p} ==")
    try:
        d=r5(**p); info=d.get("info",{}); data=d.get("data",{})
        print("key-order:",info.get("key-order"),"| data-fields:",info.get("data-fields"),"| x:",info.get("x-axis"))
        print("nkeys:",len(data),"keys:",list(data.keys())[:4])
        for k,v in list(data.items())[:1]:
            ds=v.get("data_series"); print(" ",k,"nrows:",len(ds),"first:",ds[0],"last:",ds[-1])
    except Exception as e: print("ERR",type(e).__name__,e)
print("graph_types for mortality site=1:", reg2(1,2))
print("graph_types for prelim site=1:", reg2(1,3))
show("MORTALITY site=1 gt=1", site=1,data_type=2,graph_type=1,compareBy="sex",chk_sex_1=1,chk_sex_3=1,chk_sex_2=1,race=1,age_range=1)
show("PRELIM gt=1", site=1,data_type=3,graph_type=1,compareBy="sex",chk_sex_1=1,chk_sex_3=1,chk_sex_2=1,rate_type=2,race=1,age_range=1,subtype=1)
show("PRELIM gt=10", site=1,data_type=3,graph_type=10,compareBy="sex",chk_sex_1=1,chk_sex_3=1,chk_sex_2=1,rate_type=2,race=1,age_range=1,subtype=1)
# survival with all stages
show("SURVIVAL all stages", site=1,data_type=4,graph_type=5,compareBy="sex",chk_sex_1=1,race=1,age_range=1,relative_survival_interval=5,chk_stage_101=1,chk_stage_104=1,chk_stage_105=1,chk_stage_106=1,chk_stage_107=1)
