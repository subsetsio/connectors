from subsets_utils import get
from datetime import datetime

BASE = "https://custom.resbank.co.za/SarbWebApi/WebIndicators"

def clean_val(v):
    if v is None:
        return None
    s = v.replace(" ", "").replace(" ", "").replace(",", ".")
    try:
        return float(s)
    except ValueError:
        return None

def clean_date(p):
    if not p:
        return None
    try:
        return datetime.strptime(p, "%Y/%m/%d %H:%M:%S").date()
    except ValueError:
        return None

for dt in ["MRGEI", "CDACA", "MRDMA"]:
    data = get(f"{BASE}/ReleaseOfSelectedData/MonthlyIndicatorsAll/{dt}", timeout=300.0).json()
    n = len(data)
    vbad = [d.get("Value") for d in data if clean_val(d.get("Value")) is None]
    dbad = [d.get("Period") for d in data if clean_date(d.get("Period")) is None]
    codes = len({d.get("TimeSeriesCode") for d in data})
    print(f"{dt}: rows={n} series={codes} value_unparsed={len(vbad)} date_unparsed={len(dbad)}")
    if vbad:
        print("   sample bad values:", list({repr(x) for x in vbad})[:8])
