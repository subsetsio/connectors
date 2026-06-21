import sys
sys.path.insert(0,"src")
from nodes.central_statistical_bureau import _get_json, BASE
from subsets_utils import post
path="TIR/AT/ATD/ATD060m"
meta=_get_json(BASE+path)
q={"query":[
  {"code":"FLOW","selection":{"filter":"item","values":[meta["variables"][0]["values"][0]]}},
  {"code":"CN6Z","selection":{"filter":"all","values":["*"]}},
  {"code":"COUNTRY","selection":{"filter":"item","values":[meta["variables"][2]["values"][0]]}},
  {"code":"ContentsCode","selection":{"filter":"item","values":[meta["variables"][3]["values"][0]]}},
  {"code":"TIME","selection":{"filter":"item","values":[meta["variables"][4]["values"][-1]]}},
],"response":{"format":"json-stat2"}}
js=post(BASE+path, json=q, timeout=(10,180)).json()
n=len(js["dimension"]["CN6Z"]["category"]["index"])
print("CN6Z codes returned:", n, "size:", js["size"])
# Now try filter all on CN6Z with 2 countries to see if cells limit or maxValues matters
