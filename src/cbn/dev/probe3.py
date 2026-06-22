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

def parse_chart(cv):
    out=[]
    idxs=[m.start() for m in re.finditer(r'loadChart\(',cv)]
    for k,st in enumerate(idxs):
        seg=cv[st: idxs[k+1] if k+1<len(idxs) else len(cv)]
        mn=re.search(r'name:"([^"]*)"',seg)
        md=re.search(r'data:\[([^\]]*)\]',seg)
        if not (mn and md):continue
        rest=seg[md.end():]
        mc=re.search(r'\[([^\]]*)\]',rest)
        cats=[c.strip().strip('"') for c in mc.group(1).split(',')] if mc and mc.group(1).strip() else []
        vals=[]
        for v in md.group(1).split(','):
            v=v.strip()
            if v in ('','null','undefined'):vals.append(None)
            else:
                try:vals.append(float(v))
                except:vals.append(None)
        out.append((mn.group(1),vals,cats))
    return out

for tid in [81,5,50,12,48,45]:
    il=inds(tid)
    data={"model[TableId]":str(tid),"model[StartDate]":"1960-01-01","model[EndDate]":"2030-12-31","model[IndicatorIds][]":[str(i) for i,_ in il]}
    j=post(SEARCH,data=data,headers={"X-Requested-With":"XMLHttpRequest"},timeout=180).json()
    series=parse_chart(j.get("ChartView") or "")
    print(f"\n== t{tid} {j.get('Title','')[:55]} | inds={len(il)} series={len(series)} ==")
    if series:
        nm,vals,cats=series[0]
        print("  series0:",nm[:40]," n_vals=",len(vals)," n_cats=",len(cats))
        print("  cats[:4]=",cats[:4]," cats[-3:]=",cats[-3:])
        nonnull=[(c,v) for c,v in zip(cats,vals) if v is not None]
        print("  first_nonnull=",nonnull[:2]," last_nonnull=",nonnull[-2:])
