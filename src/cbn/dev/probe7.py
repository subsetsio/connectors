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
j=call(48,"2006-01-01","2026-06-30")
print("t48 2006-2026 DCount(nonnull reported)=",j["DCount"])
ser=parse(j["ChartView"])
print("n loadChart series=",len(ser),"distinct names=",len(set(s[0] for s in ser)))
tot_nonnull=sum(1 for _,vals,_ in ser for v in vals if v is not None)
allcats=set(c for _,_,cats in ser for c in cats)
print("parsed nonnull points=",tot_nonnull," distinct dates across series=",len(allcats))
# per name, sum
from collections import defaultdict
byname=defaultdict(int)
for nm,vals,_ in ser: byname[nm]+=sum(1 for v in vals if v is not None)
print("sample per-name nonnull:",dict(list(byname.items())[:6]))
print("cats range:",sorted(allcats)[:2],sorted(allcats)[-2:])
