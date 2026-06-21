import json
from subsets_utils import get

BASE = "https://seer.cancer.gov/statistics-network/explorer/source/content_writers/"

def r5(**params):
    r = get(BASE + "render_region_5.php", params=params, timeout=(10,120))
    r.raise_for_status()
    body = r.json()
    if isinstance(body, str):
        body = json.loads(body)
    return body

def controls(region, **params):
    r = get(BASE + f"render_region_{region}_controls.php", params=params, timeout=(10,120))
    r.raise_for_status()
    return r.json()

# data types available for site=1
print("=== data_types for site=1 (region2 options) ===")
print(controls(2, site=1, data_type=1))

DT = {"1":"incidence","2":"mortality","3":"prelim_incidence","4":"survival","5":"prevalence","6":"risk"}
for dt in ["1","2","3","4","5","6"]:
    print(f"\n=== data_type={dt} ({DT[dt]}) graph_types (region3 options) ===")
    try:
        print(controls(3, site=1, data_type=dt, graph_type=1))
    except Exception as e:
        print("ERR", type(e).__name__, e)
