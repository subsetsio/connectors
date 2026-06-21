import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import json, re
from subsets_utils import get

# (1) full header JSON for 4625 - look for column labels / titles
r = get("https://statistique.quebec.ca/pls/ken/ken411_data_explt_v2.p_retrn_header?p_id_tabl=4625", timeout=(10,60))
cfg = json.loads(r.text)
print("top keys:", list(cfg.keys()))
tc = cfg.get("tableConfig",{})
print("tableConfig keys:", list(tc.keys()))
# look for any list of column descriptors with labels
def find_labels(o,p=''):
    if isinstance(o,dict):
        for k,v in o.items():
            if k.lower() in ('columns','colonnes','header','entetes','titles','titres','labels','colmodel','fields') and isinstance(v,(list,dict)):
                print(f"  LABELS at {p}/{k}: {json.dumps(v,ensure_ascii=False)[:400]}")
            find_labels(v,p+'/'+k)
    elif isinstance(o,list):
        for i,v in enumerate(o[:3]): find_labels(v,p+f'[{i}]')
find_labels(cfg)
# is there a separate endpoint p_retrn_entete / labels? print other procs? skip.

# show header CSV via a 'header' proc if exists - the p_retrn_header gave config; the COLUMN labels for the data:
# Check 'boldField' and 'sort'
print("dataSource:", json.dumps(tc.get('dataSource',{}),ensure_ascii=False)[:300])
