import time, json, collections
from lxml import html as lh
from subsets_utils import get, post
NAV="https://statistics.cbn.gov.ng/data-nav-items/dataset-nav-tree"
SEARCH="https://statistics.cbn.gov.ng/data-browser/search-data-by-table"
EU=json.load(open("/Users/nathansnellaert/Documents/hardened/data/sources/cbn/work/entity_union.json"))
ids=EU if isinstance(EU,list) else list(EU.get("entities",EU).keys() if isinstance(EU.get("entities",EU),dict) else EU)
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
    for att in range(4):
        j=post(SEARCH,data=data,headers={"X-Requested-With":"XMLHttpRequest"},timeout=180).json()
        if j.get("IsSuccessful"): return j
        if 'No data' not in (j.get('Error') or ''): time.sleep(1.2); continue
        return j
    return j
def headcols(tv):
    doc=lh.fromstring(tv); t=doc.xpath('//table[@id="sm_view_grid"]')
    if not t:return None
    t=t[0]; hr=t.xpath('.//thead/tr'); grid={};occ=set();nr=len(hr)
    for r,tr in enumerate(hr):
        c=0
        for th in tr.xpath('./th|./td'):
            while (r,c) in occ:c+=1
            cs=int(th.get('colspan',1));rs=int(th.get('rowspan',1));tx=th.text_content().strip()
            for dr in range(rs):
                for dc in range(cs):occ.add((r+dr,c+dc));grid[(r+dr,c+dc)]=tx
            c+=cs
    nc=max((c for(_,c)in grid),default=0)+1
    return nr,nc,[grid.get((r,1),'')for r in range(nr)]
fmt=collections.Counter(); needchunk=[]
for eid in sorted(ids,key=lambda x:int(x.split('-')[1])):
    tid=int(eid.split('-')[1])
    j=call(tid,"1960-01-01","2030-12-31")
    if not j.get("IsSuccessful"):
        # try chunk
        jc=call(tid,"2000-01-01","2019-12-31")
        ok2=jc.get("IsSuccessful")
        needchunk.append(tid)
        print(f"t{tid:>3} WIDE-FAIL err={j.get('Error')!r} chunk2000-2019_ok={ok2}")
        j=jc if ok2 else j
        if not ok2: continue
    hc=headcols(j.get("TableView") or "")
    if not hc: print(f"t{tid} parse-fail"); continue
    nr,nc,c1=hc
    sample="|".join(c1)
    fmt[(nr,sample)]+=1
    print(f"t{tid:>3} levels={nr} ncols={nc} col1={c1}")
    time.sleep(0.2)
print("\nformat histogram:")
for k,v in fmt.items(): print("  ",k,"->",v)
print("need chunking:",needchunk)
