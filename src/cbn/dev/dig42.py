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
    for _ in range(4):
        j=post(SEARCH,data=data,headers={"X-Requested-With":"XMLHttpRequest"},timeout=200).json()
        if j.get("IsSuccessful"):return j
        if 'Invalid' in (j.get('Error')or''):return j
        time.sleep(1.2)
    return j
info=indinfo(42);ids=[i for i,_ in info]
j=call(42,ids,"1960-01-01","2030-12-31")
print("ok",j.get("IsSuccessful"),"DCount",j.get("DCount"),"tvlen",len(j.get("TableView")or""))
tv=j["TableView"];doc=lh.fromstring(tv);t=doc.xpath('//table[@id="sm_view_grid"]')[0]
allrows=t.xpath('.//tbody/tr') or t.xpath('./tr')
print("tbody tr count",len(allrows))
# all tr in table
print("all tr in table",len(t.xpath('.//tr')))
# cells per row
for r in allrows[:20]:
    cells=r.xpath('./th|./td')
    print("  ncell",len(cells),"name",cells[0].text_content().strip()[:45])
