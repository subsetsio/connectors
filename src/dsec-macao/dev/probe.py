from subsets_utils import post
URL="https://www.dsec.gov.mo/TimeSeriesApi/App/IndicatorValue/LatestSameEndPeriodv3"
def fetch(body):
    return post(URL, json=body, timeout=(10,120)).json()["Value"]

# 9029 yearly-only: clean single-period request
clean = fetch({"indicator_ids":["9029"],"language":"en-us","types":["VAL"],"dataPeriods":["Yearly"],"fromYear":1900,"toYear":2026})[0]["dsecIndicatorData"]
clean_nonnull=[r for r in clean if r["IndicatorValue"] is not None]
print("9029 CLEAN Yearly: total",len(clean),"nonnull",len(clean_nonnull))
print("  sample:", [(r["Year"],r["PeriodID"],r["IndicatorValue"]) for r in clean_nonnull[:4]])

# 9029 under broadcast all4
bc = fetch({"indicator_ids":["9029","9020"],"language":"en-us","types":["VAL","VAL"],"dataPeriods":["Yearly","Quarterly","Monthly","ThreeConsecutiveMonths"],"fromYear":1900,"toYear":2026})[0]["dsecIndicatorData"]
bc_nonnull=[r for r in bc if r["IndicatorValue"] is not None]
print("9029 BROADCAST all4: total",len(bc),"nonnull",len(bc_nonnull))
print("  nonnull sample:", [(r["Year"],r["PeriodID"],r["IndicatorValue"]) for r in bc_nonnull[:6]])
print("  distinct PeriodIDs among nonnull:", sorted(set(r["PeriodID"] for r in bc_nonnull), key=lambda x:(x is None,x)))
