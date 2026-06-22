import re, json, time
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
def parse(cv):
    out=[];idxs=[m.start() for m in re.finditer(r'loadChart\(',cv)]
    for k,st in enumerate(idxs):
        seg=cv[st:idxs[k+1] if k+1<len(idxs) else len(cv)]
        mn=re.search(r'name:"([^"]*)"',seg);md=re.search(r'data:\[([^\]]*)\]',seg)
        if not(mn and md):continue
        rest=seg[md.end():];mc=re.search(r'\[([^\]]*)\]',rest)
        cats=[c.strip().strip('"') for c in mc.group(1).split(',')] if mc and mc.group(1).strip() else []
        vals=[None if v.strip() in('','null') else float(v) for v in md.group(1).split(',')]
        out.append((mn.group(1),vals,cats))
    return out
def call(tid,sd,ed):
    data={"model[TableId]":str(tid),"model[StartDate]":sd,"model[EndDate]":ed,"model[IndicatorIds][]":[str(i) for i in inds(tid)]}
    return post(SEARCH,data=data,headers={"X-Requested-With":"XMLHttpRequest"},timeout=180).json()
j=call(48,"2015-01-01","2026-06-30")
ser=parse(j["ChartView"])
nm,vals,cats=ser[0]
nn=[(c,v) for c,v in zip(cats,vals) if v is not None]
print("t48 daily series0",nm,"n_cats",len(cats),"label_sample",cats[:3],cats[-2:])
print("  first_nonnull",nn[:2],"last_nonnull",nn[-2:],"n_nonnull",len(nn))
print("window cap search for t48:")
for sd,ed in [("2002-01-01","2026-06-30"),("2006-01-01","2026-06-30"),("1999-01-01","2026-06-30"),("2010-01-01","2030-12-31")]:
    j2=call(48,sd,ed);print(f"  {sd}..{ed}: ok={j2.get('IsSuccessful')} DCount={j2.get('DCount')}");time.sleep(1)
