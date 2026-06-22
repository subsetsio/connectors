import re, json
from subsets_utils import get, post

NAV = "https://statistics.cbn.gov.ng/data-nav-items/dataset-nav-tree"
SEARCH = "https://statistics.cbn.gov.ng/data-browser/search-data-by-table"

def nav_nodes():
    html = get(NAV, headers={"X-Requested-With":"XMLHttpRequest"}, timeout=120).text
    i = html.find('"data":'); s = html.find('[', i); depth=0
    for j in range(s,len(html)):
        if html[j]=='[':depth+=1
        elif html[j]==']':
            depth-=1
            if depth==0: e=j+1;break
    return json.loads(html[s:e])

nodes = nav_nodes()
def inds(tid):
    return [(n['data']['indicator_id'], n['text'].strip()) for n in nodes if n['data']['set_type']==4 and n['data']['table_id']==tid]

CALL = re.compile(r'loadChart\(\s*parseInt\(\s*[\'"](\d+)[\'"]\s*\)\s*,\s*"([^"]+)"\s*,\s*(\[.*?\])\s*,\s*(\[[^\]]*\])\s*\)', re.S)

for tid in [50, 5, 48, 12, 45]:
    il = inds(tid)
    data = {"model[TableId]": str(tid), "model[StartDate]":"1960-01-01", "model[EndDate]":"2030-12-31",
            "model[IndicatorIds][]": [str(i) for i,_ in il]}
    r = post(SEARCH, data=data, headers={"X-Requested-With":"XMLHttpRequest"}, timeout=180)
    j = r.json()
    cv = j.get("ChartView") or ""
    calls = CALL.findall(cv)
    print(f"\n==== table {tid}: {j.get('Title','')[:65]} | inds={len(il)} | DCount={j.get('DCount')} | calls={len(calls)} ====")
    for ct, cont, sjson, cats in calls[:1]:
        cats_list = json.loads(cats)
        # series json: [{name:"..",data:[..]}] -> quote keys
        sj = re.sub(r'(\{|,)\s*(name|data)\s*:', lambda m: f'{m.group(1)}"{m.group(2)}":', sjson)
        ser = json.loads(sj)
        print("  chartType=",ct," n_labels=",len(cats_list)," labels[:8]=",cats_list[:8])
        print("  labels[-4:]=",cats_list[-4:])
        print("  series name=",ser[0]['name'][:50]," n_data=",len(ser[0]['data'])," data[:6]=",ser[0]['data'][:6])
        # nulls?
        nnull = sum(1 for v in ser[0]['data'] if v is None)
        print("  nulls_in_first_series=",nnull, " sample_types=", set(type(v).__name__ for v in ser[0]['data']))
