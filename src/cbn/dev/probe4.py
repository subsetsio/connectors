import re, json
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
def inds(tid):return [(n['data']['indicator_id'],n['text'].strip()) for n in nodes if n['data']['set_type']==4 and n['data']['table_id']==tid]
for tid in [5,48]:
    il=inds(tid)
    data={"model[TableId]":str(tid),"model[StartDate]":"1960-01-01","model[EndDate]":"2030-12-31","model[IndicatorIds][]":[str(i) for i,_ in il]}
    r=post(SEARCH,data=data,headers={"X-Requested-With":"XMLHttpRequest"},timeout=180)
    j=r.json()
    print(f"\n##### t{tid} http={r.status_code} IsSuccessful={j.get('IsSuccessful')} Error={j.get('Error')!r} DCount={j.get('DCount')} TitleLen={len(j.get('Title') or '')}")
    cv=j.get("ChartView") or ""
    print("  ChartView len",len(cv)," count loadChart:",cv.count("loadChart"))
    k=cv.find("loadChart")
    if k>=0: print("  near loadChart:",repr(cv[k:k+200]))
    # maybe data in 'series' or other format. show snippet of cv around 'data:'
    kd=cv.find("data:")
    print("  near data::",repr(cv[kd-60:kd+160]) if kd>=0 else "no data:")
