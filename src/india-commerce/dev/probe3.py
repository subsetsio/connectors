import json
from subsets_utils import get
BASE="https://trade-analytics.commerce.gov.in"
def supply(flow,year,cc="WRD"):
    u=f"{BASE}/public/country/getIndiaSupplyDataPublic?impexptype={flow}&calyear={year}&hscode=HS2&commocode=HS&countryCode={cc}&region=COUNTRY&regionCode=&qeCodes=ALL&pcCodes=ALL&yeartype=cal&finyear=&currency=USD"
    r=get(u,timeout=(10,90)); d=r.json()
    labels=d.get('label',[]); vals=d.get('value',[])
    tot=sum(float(v['value']) for v in vals if v.get('value') not in (None,''))
    return labels,vals,tot

for y in [2017,2020,2024,2025,2026]:
    lab,val,tot=supply("Export",y)
    print(f"WRD Export {y}: chapters={len(lab)} total_usd_mn={tot:,.0f}  first={lab[0]['label'][:30] if lab else None} v0={val[0] if val else None}")
lab,val,tot=supply("Import",2024)
print(f"WRD Import 2024: chapters={len(lab)} total={tot:,.0f}")

# bilateral WRD returns year list?
r=get(f"{BASE}/public/country/bilateralMonthlyDataPublic?indi=yearly&countryCode=WRD&year=2025&region=COUNTRY&regionCode=&regionCodetd=&currency=USD",timeout=(10,90))
d=r.json(); print("\nbilateral WRD arrays:",len(d),"years:",[x['label'] for x in d[0]])
print("exp:",[round(float(x['value'])) for x in d[1]])
print("imp:",[round(float(x['value'])) for x in d[2]])
print("bal:",[round(float(x['value'])) for x in d[3]] if len(d)>3 else "NONE")

# state years
for y in [2017,2018,2025,2026]:
    r=get(f"{BASE}/public/indiaTrade/getStateWiseTableData?year={y}&type=Export&currency=USD",timeout=(10,90))
    d=r.json(); print(f"state Export {y}: rows={len(d)} sample={d[0] if d else None}")
