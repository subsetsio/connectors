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
def inds(tid):return [n['data']['indicator_id'] for n in nodes if n['data']['set_type']==4 and n['data']['table_id']==tid]
def call(tid,sd,ed):
    data={"model[TableId]":str(tid),"model[StartDate]":sd,"model[EndDate]":ed,"model[IndicatorIds][]":[str(i) for i in inds(tid)]}
    for att in range(5):
        j=post(SEARCH,data=data,headers={"X-Requested-With":"XMLHttpRequest"},timeout=180).json()
        if j.get("IsSuccessful"): return j
        time.sleep(2)
    return j

def parse_tv(tv):
    doc=lh.fromstring(tv)
    tbl=doc.xpath('//table[@id="sm_view_grid"]')
    if not tbl: return None,None
    tbl=tbl[0]
    head_rows=tbl.xpath('.//thead/tr')
    grid={}; occ=set(); nrows=len(head_rows)
    for r,tr in enumerate(head_rows):
        c=0
        for th in tr.xpath('./th|./td'):
            while (r,c) in occ: c+=1
            cs=int(th.get('colspan',1)); rs=int(th.get('rowspan',1))
            txt=th.text_content().strip()
            for dr in range(rs):
                for dc in range(cs):
                    occ.add((r+dr,c+dc)); grid[(r+dr,c+dc)]=txt
            c+=cs
    ncols=(max((c for (_,c) in grid), default=0))+1
    col_parts={col:[grid.get((r,col),'') for r in range(nrows)] for col in range(ncols)}
    # body
    body=tbl.xpath('.//tbody/tr') or [tr for tr in tbl.xpath('./tr')]
    return col_parts, body

j=call(81,"1960-01-01","2030-12-31")
cp,body=parse_tv(j["TableView"])
print("ANNUAL ncols",len(cp),"nbody",len(body))
print("col_parts[0]",cp[0]," col_parts[1]",cp[1]," last",cp[len(cp)-1])
# row0 (Agriculture)
cells=body[0].xpath('./th|./td')
print("body0 ncell",len(cells)," name",cells[0].text_content().strip())
# find col with header '2023'
c2023=[c for c,p in cp.items() if p and p[-1]=='2023']
print("2023 col idx",c2023)
ci=c2023[0]
print("Agriculture 2023 (cell idx ci):", cells[ci].text_content().strip())
# monthly check
j=call(50,"1960-01-01","2030-12-31")
cp,body=parse_tv(j["TableView"])
print("\nMONTHLY ncols",len(cp),"nbody",len(body)," col1parts",cp[1]," col12parts",cp[12])
cells=body[0].xpath('./th|./td'); print("body0 name",cells[0].text_content().strip(),"ncell",len(cells))
# daily check
j=call(48,"2010-01-01","2026-12-31")
cp,body=parse_tv(j["TableView"])
print("\nDAILY ncols",len(cp),"nbody",len(body)," col1parts",cp[1]," col2parts",cp[2])
cells=body[0].xpath('./th|./td'); print("body0 name",cells[0].text_content().strip(),"ncell",len(cells))
