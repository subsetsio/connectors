import time, json
from lxml import html as lh
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
def indinfo(tid):return [(n['data']['indicator_id'],n['text'].strip()) for n in nodes if n['data']['set_type']==4 and n['data']['table_id']==tid]
def call(tid,ids,sd,ed):
    data={"model[TableId]":str(tid),"model[StartDate]":sd,"model[EndDate]":ed,"model[IndicatorIds][]":[str(i) for i in ids]}
    for _ in range(5):
        j=post(SEARCH,data=data,headers={"X-Requested-With":"XMLHttpRequest"},timeout=200).json()
        if j.get("IsSuccessful"):return j
        if 'Invalid' in (j.get('Error')or''):return j
        time.sleep(1.5)
    return j
def datecols(tv):
    doc=lh.fromstring(tv);t=doc.xpath('//table[@id="sm_view_grid"]')[0]
    hr=t.xpath('.//thead/tr');grid={};occ=set();nr=len(hr)
    for r,tr in enumerate(hr):
        c=0
        for th in tr.xpath('./th|./td'):
            while (r,c) in occ:c+=1
            cs=int(th.get('colspan',1));rs=int(th.get('rowspan',1));tx=th.text_content().strip()
            for dr in range(rs):
                for dc in range(cs):occ.add((r+dr,c+dc));grid[(r+dr,c+dc)]=tx
            c+=cs
    nc=max((c for(_,c)in grid),default=0)+1
    return [grid.get((nr-1,col),'') for col in range(1,nc)]
info=indinfo(48);ids=[i for i,_ in info]
for sd,ed,lbl in [("2020-06-01","2020-06-30","single Jun2020"),("2020-06-01","2020-12-31","Jun-Dec2020"),("2023-03-15","2023-04-20","mid-mar to apr")]:
    j=call(48,ids,sd,ed)
    dc=datecols(j["TableView"]) if j.get("IsSuccessful") else []
    print(f"{lbl} [{sd}..{ed}]: ok={j.get('IsSuccessful')} ndatecols={len(dc)} first={dc[:2]} last={dc[-2:]}")
