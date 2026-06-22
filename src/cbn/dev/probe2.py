import re, json
from subsets_utils import get, post
NAV = "https://statistics.cbn.gov.ng/data-nav-items/dataset-nav-tree"
SEARCH = "https://statistics.cbn.gov.ng/data-browser/search-data-by-table"
def nav_nodes():
    html = get(NAV, headers={"X-Requested-With":"XMLHttpRequest"}, timeout=120).text
    i = html.find('"data":'); s = html.find('[', i); depth=0
    for j in range(s,len(html)):
        if html[j]=='[':depth+=1
        elif html[j]==']':
            depth-=1
            if depth==0: e=j+1;break
    return json.loads(html[s:e])
nodes = nav_nodes()
il=[(n['data']['indicator_id'], n['text'].strip()) for n in nodes if n['data']['set_type']==4 and n['data']['table_id']==50]
data={"model[TableId]":"50","model[StartDate]":"1960-01-01","model[EndDate]":"2030-12-31","model[IndicatorIds][]":[str(i) for i,_ in il]}
r=post(SEARCH,data=data,headers={"X-Requested-With":"XMLHttpRequest"},timeout=180)
j=r.json()
cv=j["ChartView"]
print("LEN",len(cv))
k=cv.find("loadChart")
print(repr(cv[k:k+600]))
print("=== TableView head ===")
print(j["TableView"][:1200])
