import sys, json
sys.path.insert(0,"src")
from nodes.central_statistical_bureau import _get_json, _post_json, BASE
path="TIR/AT/ATD/ATD060m"
meta=_get_json(BASE+path)
def one(v): return v["values"][0]
# pin small vars to one value, ask CN6Z = all
q={"query":[
  {"code":"FLOW","selection":{"filter":"item","values":[meta["variables"][0]["values"][0]]}},
  {"code":"CN6Z","selection":{"filter":"all","values":["*"]}},
  {"code":"COUNTRY","selection":{"filter":"item","values":[meta["variables"][2]["values"][0]]}},
  {"code":"ContentsCode","selection":{"filter":"item","values":[meta["variables"][3]["values"][0]]}},
  {"code":"TIME","selection":{"filter":"item","values":[meta["variables"][4]["values"][-1]]}},
],"response":{"format":"json-stat2"}}
from subsets_utils import post
r=post(BASE+path, json=q, timeout=(10,180))
print("status", r.status_code)
print(r.text[:400])
