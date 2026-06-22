import io, time, json
import pandas as pd
from subsets_utils import get, post
pd.set_option('display.max_columns',10); pd.set_option('display.width',200)
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
# annual t81: verify 2023 nominal ~229912
j=call(81,"1960-01-01","2030-12-31")
df=pd.read_html(io.StringIO(j["TableView"]))[0]
print("ANNUAL columns[:5]:",list(df.columns[:5]))
print(df.iloc[:3,:6].to_string())
print("nrows",len(df),"  iloc[0,0]=",repr(df.iloc[0,0]),"iloc[1,0]=",repr(df.iloc[1,0]))
# locate 2023 col
print("2023 col present:", '2023' in [str(c) for c in df.columns])
sub=df[['Indicators','2023']] if '2023' in df.columns else None
print(sub.head(3).to_string() if sub is not None else "no 2023")
