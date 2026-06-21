import json
from subsets_utils import get

# Probe a few datasets to understand observation shape, measures, attributes.
for ds in ["DS_COEFF_EURO_FRANC", "DD_CNA_AGREGATS", "DS_IPC_PRINC", "DS_ELECTORAL"]:
    r = get(f"https://api.insee.fr/melodi/data/{ds}", params={"maxResult": 3, "page": 1},
            headers={"Accept": "application/json"}, timeout=(10, 120))
    d = r.json()
    obs = d.get("observations", [])
    print("====", ds, "status", r.status_code, "n_obs_page", len(obs))
    print("paging:", json.dumps(d.get("paging")))
    for o in obs[:2]:
        print("  dims:", json.dumps(o.get("dimensions"), ensure_ascii=False))
        print("  measures:", json.dumps(o.get("measures"), ensure_ascii=False))
        print("  attributes:", json.dumps(o.get("attributes"), ensure_ascii=False))
        print("  top-keys:", list(o.keys()))
