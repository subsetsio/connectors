import sys, json
sys.path.insert(0, "src")
from nodes.central_statistical_bureau import _plan_blocks, _iter_rows, _get_json, _post_json, BASE
path="POP/IR/IRS/IRS010"
meta=_get_json(BASE+path)
blocks=_plan_blocks(meta["variables"])
print("n blocks:", len(blocks))
# fetch first block and parse
b=blocks[0]
q={"query":[{"code":c,"selection":{"filter":"item","values":v}} for c,v in b.items()],"response":{"format":"json-stat2"}}
js=_post_json(BASE+path,q)
rows=list(_iter_rows(js))
print("rows:", len(rows))
print("sample row:", rows[0])
cols=set()
for r in rows: cols|=set(r.keys())
print("columns:", sorted(cols))
