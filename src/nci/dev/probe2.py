import json
from subsets_utils import get
BASE = "https://seer.cancer.gov/statistics-network/explorer/source/content_writers/"
def r5(**params):
    r = get(BASE + "render_region_5.php", params=params, timeout=(10,120))
    r.raise_for_status()
    b = r.json()
    return json.loads(b) if isinstance(b,str) else b

def show(tag, **p):
    print(f"\n===== {tag} :: {p} =====")
    try:
        d = r5(**p)
        info = d.get("info",{})
        print("INFO key-order:", info.get("key-order"))
        print("INFO data-fields:", info.get("data-fields"))
        print("INFO x-axis:", info.get("x-axis"), "| y-axis:", info.get("y-axis"))
        data = d.get("data",{})
        print("DATA keys (count=%d):"%len(data), list(data.keys())[:8])
        for k,v in list(data.items())[:2]:
            ds = v.get("data_series") if isinstance(v,dict) else v
            print(f"  {k}: first row={ds[0] if ds else None}  nrows={len(ds) if ds else 0}")
    except Exception as e:
        print("ERR", type(e).__name__, e)

# incidence with compareBy=sex, all sexes -> expect 3 series
show("INCIDENCE site=1 gt=1 compareBy=sex all", site=1, data_type=1, graph_type=1, compareBy="sex",
     chk_sex_1=1, chk_sex_3=1, chk_sex_2=1, rate_type=2, race=1, age_range=1, subtype=1)
# survival
show("SURVIVAL site=1 gt=5 compareBy=sex", site=1, data_type=4, graph_type=5, compareBy="sex",
     chk_sex_1=1, chk_sex_3=1, chk_sex_2=1, race=1, age_range=1, relative_survival_interval=5)
# prevalence
show("PREVALENCE site=1 gt=1 compareBy=sex", site=1, data_type=5, graph_type=1, compareBy="sex",
     chk_sex_1=1, chk_sex_3=1, chk_sex_2=1, age_range=1)
# risk
show("RISK site=1 gt=1 compareBy=sex", site=1, data_type=6, graph_type=1, compareBy="sex",
     chk_sex_1=1, chk_sex_3=1, chk_sex_2=1, race=1, age_range=300, stat_type=10)
