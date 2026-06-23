from subsets_utils import post
URL="https://www.dsec.gov.mo/TimeSeriesApi/App/IndicatorValue/LatestSameEndPeriodv3"
def call(label, body):
    r=post(URL, json=body, timeout=(10,120)); d=r.json()
    v=d.get("Value"); n=len(v) if isinstance(v,list) else v
    print(f"[{label}] Status={d['Status']} nInd={n}", "" if d['Status']=="OK" else (d.get('Debug_msg') or '')[:90])
    return d
# parallel arrays: dataPeriods per id
call("batch2 parallel periods", {"indicator_ids":["9029","9031"],"language":"en-us","types":["VAL","VAL"],"dataPeriods":["Yearly","Yearly"],"fromYear":1980,"toYear":2026})
# parallel arrays with all-periods each via nested? try types parallel only
call("batch2 types parallel, periods1", {"indicator_ids":["9029","9031"],"language":"en-us","types":["VAL","VAL"],"dataPeriods":["Yearly"],"fromYear":1980,"toYear":2026})
d=call("batch2 parallel both", {"indicator_ids":["9029","9031"],"language":"en-us","types":["VAL","VAL"],"dataPeriods":["Yearly","Yearly"],"fromYear":1980,"toYear":2026})
if d['Status']=="OK":
    for ind in d['Value']:
        print("   id",ind['indicatorId'],"rows",len(ind['dsecIndicatorData']))
