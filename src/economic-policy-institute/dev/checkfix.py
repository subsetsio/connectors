import io, zipfile, sys
sys.path.insert(0, "src")
from subsets_utils import get
from nodes.economic_policy_institute import _member_for, _member_indicator
from constants import INDICATOR_NAMES
r = get("https://github.com/Economic/data/releases/latest/download/epi_swa_data_library.zip", timeout=(10,300))
zf = zipfile.ZipFile(io.BytesIO(r.content))
for eid in ["hourly_wage_mean","hourly_wage_median","ceo_pay_ratio"]:
    print(eid, "->", _member_for(zf, eid), "| name in csv:", repr(_member_indicator(zf, _member_for(zf, eid))), "| expected:", repr(INDICATOR_NAMES[eid]))
# verify ALL 37 resolve
from constants import ENTITY_IDS
bad=[e for e in ENTITY_IDS if _member_indicator(zf,_member_for(zf,e))!=INDICATOR_NAMES[e]]
print("unresolved/mismatch:", bad)
