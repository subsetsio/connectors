import re
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
    import json;return json.loads(html[s:e])
nodes=nav_nodes()
def inds(tid):return [n['data']['indicator_id'] for n in nodes if n['data']['set_type']==4 and n['data']['table_id']==tid]
def call(tid,sd,ed):
    data={"model[TableId]":str(tid),"model[StartDate]":sd,"model[EndDate]":ed,"model[IndicatorIds][]":[str(i) for i in inds(tid)]}
    return post(SEARCH,data=data,headers={"X-Requested-With":"XMLHttpRequest"},timeout=180).json()
def show_thead(tid,sd,ed,label):
    tv=call(tid,sd,ed).get("TableView") or ""
    th=re.search(r'<thead>(.*?)</thead>',tv,re.S)
    print(f"\n===== {label} t{tid} thead =====")
    if not th: print(" no thead; tvlen",len(tv)); return
    rows=re.findall(r'<tr>(.*?)</tr>',th.group(1),re.S)
    print(" header rows:",len(rows))
    for ri,row in enumerate(rows):
        cells=re.findall(r'<th([^>]*)>(.*?)</th>',row,re.S)
        simp=[]
        for attr,txt in cells[:18]:
            cs=re.search(r"colspan='?(\d+)'?",attr); rs=re.search(r"rowspan='?(\d+)'?",attr)
            t=re.sub(r'<[^>]+>','',txt).strip()
            simp.append((t,'c'+cs.group(1) if cs else '', 'r'+rs.group(1) if rs else ''))
        print(f"  row{ri} ({len(cells)} cells):",simp[:18])
    # first body row
    tb=re.search(r'</thead>(.*?)</table>',tv,re.S)
    r0=re.search(r'<tr>(.*?)</tr>',tb.group(1),re.S) if tb else None
    if r0:
        tds=re.findall(r'<t[dh][^>]*>(.*?)</t[dh]>',r0.group(1),re.S)
        print("  body row0 first cells:",[re.sub(r'<[^>]+>','',x).strip() for x in tds[:10]])
show_thead(81,"1960-01-01","2030-12-31","ANNUAL")
show_thead(5,"1960-01-01","2030-12-31","QUARTERLY")
show_thead(50,"1960-01-01","2030-12-31","MONTHLY")
show_thead(48,"2015-01-01","2026-06-30","DAILY")
