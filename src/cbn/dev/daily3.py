import time, json, re
from subsets_utils import get, post
NAV="https://statistics.cbn.gov.ng/data-nav-items/dataset-nav-tree"
SEARCH="https://statistics.cbn.gov.ng/data-browser/search-data-by-table"
def nav_nodes():
    h=get(NAV,headers={"X-Requested-With":"XMLHttpRequest"},timeout=120).text
    i=h.find('"data":');s=h.find('[',i);d=0
    for j in range(s,len(h)):
        if h[j]=='[':d+=1
        elif h[j]==']':
            d-=1
            if d==0:e=j+1;break
    return json.loads(h[s:e])
nodes=nav_nodes()
def inds(tid):return [n['data']['indicator_id'] for n in nodes if n['data']['set_type']==4 and n['data']['table_id']==tid]
def call(tid,ids,sd,ed):
    data={"model[TableId]":str(tid),"model[StartDate]":sd,"model[EndDate]":ed,"model[IndicatorIds][]":[str(i) for i in ids]}
    for _ in range(5):
        j=post(SEARCH,data=data,headers={"X-Requested-With":"XMLHttpRequest"},timeout=200).json()
        if j.get("IsSuccessful"):return j
        if 'Invalid' in (j.get('Error')or''):return j
        time.sleep(1.5)
    return j
j=call(48,inds(48),"2020-06-01","2020-06-30")
tv=j["TableView"]
th=re.search(r'<thead>(.*?)</thead>',tv,re.S).group(1)
trs=re.findall(r'<tr[^>]*>(.*?)</tr>',th,re.S)
print("header tr count",len(trs))
for ri,tr in enumerate(trs):
    cells=re.findall(r'<th[^>]*>(.*?)</th>',tr,re.S)
    print(f" row{ri} ncells={len(cells)} sample:",[re.sub(r'<[^>]+>','',c).strip() for c in cells[:8]])
# body row0
tb=re.search(r'</thead>(.*?)</table>',tv,re.S).group(1)
r0=re.search(r'<tr[^>]*>(.*?)</tr>',tb,re.S).group(1)
tds=re.findall(r'<t[dh][^>]*>(.*?)</t[dh]>',r0,re.S)
print("body0 ncells",len(tds),"vals:",[re.sub(r'<[^>]+>','',x).strip() for x in tds[:12]])
