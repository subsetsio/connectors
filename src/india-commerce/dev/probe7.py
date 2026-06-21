import re
from subsets_utils import get
BASE="https://trade-analytics.commerce.gov.in"
for pg in ["public/country","public/indiaTrade"]:
    html=get(f"{BASE}/{pg}",timeout=(10,90)).text
    yrs=sorted({int(v) for v in re.findall(r'<option[^>]*value="(20\d{2})"', html)})
    print(pg,"year options:",yrs)
