import re, json, time
from subsets_utils import get, post
NAV="https://statistics.cbn.gov.ng/data-nav-items/dataset-nav-tree"
SEARCH="https://statistics.cbn.gov.ng/data-browser/search-data-by-table"
def nav_nodes():
    html=get(NAV,headers={"X-Requested-With":"XMLHttpRequest"},timeout=120).text
    i=html.find('"data":');s=html.find('[',i);depth=0
    for j in range(s,len(html)):
        if html[j]=='[':depth+=1
        elif html[j]==']':
            depth-=1
            if depth==0:e=j+1;break
    return json.loads(html[s:e])
nodes=nav_nodes()
def inds(tid):return [n['data']['indicator_id'] for n in nodes if n['data']['set_type']==4 and n['data']['table_id']==tid]
def call(tid,sd,ed):
    data={"model[TableId]":str(tid),"model[StartDate]":sd,"model[EndDate]":ed,"model[IndicatorIds][]":[str(i) for i in inds(tid)]}
    j=post(SEARCH,data=data,headers={"X-Requested-With":"XMLHttpRequest"},timeout=180).json()
    return j.get("IsSuccessful"), j.get("DCount"), (j.get("ChartView") or "").count("loadChart"), j.get("Error")
print("repeat t5 (1960-2030):")
for n in range(4):
    print("  ",call(5,"1960-01-01","2030-12-31")); time.sleep(1)
print("t48 daily windows:")
for sd,ed in [("1960-01-01","2030-12-31"),("2015-01-01","2026-06-30"),("2024-01-01","2024-12-31"),("2024-12-01","2024-12-31")]:
    print(f"  {sd}..{ed}:",call(48,sd,ed)); time.sleep(1)
