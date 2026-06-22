import io, time, json
import pandas as pd
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
    for att in range(5):
        j=post(SEARCH,data=data,headers={"X-Requested-With":"XMLHttpRequest"},timeout=180).json()
        if j.get("IsSuccessful"): return j
        time.sleep(2)
    return j
def examine(tid,sd,ed,label):
    j=call(tid,sd,ed)
    tv=j.get("TableView") or ""
    print(f"\n==== {label} t{tid} ok={j.get('IsSuccessful')} tvlen={len(tv)} ====")
    if not tv: return
    dfs=pd.read_html(io.StringIO(tv))
    df=dfs[0]
    print("  shape",df.shape," ncol_levels=",df.columns.nlevels)
    print("  first col name:",df.columns[0])
    print("  sample cols[1:4]:",list(df.columns[1:4]))
    print("  last col:",df.columns[-1])
    print("  row0 idx val:",df.iloc[0,0]," row0 vals[1:5]:",list(df.iloc[0,1:5]))
examine(81,"1960-01-01","2030-12-31","ANNUAL")
examine(5,"1960-01-01","2030-12-31","QUARTERLY")
examine(50,"1960-01-01","2030-12-31","MONTHLY")
examine(48,"2010-01-01","2026-12-31","DAILY")
