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
def bodynames(tv):
    doc=lh.fromstring(tv);tt=doc.xpath('//table[@id="sm_view_grid"]')
    if not tt:return []
    t=tt[0]
    return [r.xpath('./th|./td')[0].text_content().strip() for r in (t.xpath('.//tbody/tr') or t.xpath('./tr'))]
for tid in [42,20,31,44,77,25]:
    info=indinfo(tid);ids=[i for i,_ in info];names=[n for _,n in info]
    j=call(tid,ids,"1960-01-01","2030-12-31")
    bn=bodynames(j.get("TableView")or"")
    aligned = (len(bn)==len(names) and bn==names)
    print(f"t{tid}: sent={len(ids)} body={len(bn)} exact_aligned={aligned}")
    if not aligned and len(bn)==len(names):
        # show first mismatch
        for k,(a,b) in enumerate(zip(bn,names)):
            if a!=b: print("   first mismatch at",k,repr(a),"vs",repr(b)); break
    time.sleep(0.5)
