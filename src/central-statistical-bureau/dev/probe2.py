from subsets_utils import get, post
base="https://data.stat.gov.lv/api/v1/en/OSP_PUB/"
path="POP/IR/IRS/IRS010"
m=get(base+path, timeout=(10,60)).json()
tvar=[v for v in m["variables"] if v["code"]=="TIME"][0]
# chunked item query: only 3 time values, all indicators/contents
q={"query":[
   {"code":"INDICATOR","selection":{"filter":"all","values":["*"]}},
   {"code":"ContentsCode","selection":{"filter":"all","values":["*"]}},
   {"code":"TIME","selection":{"filter":"item","values":tvar["values"][-3:]}},
 ],"response":{"format":"json-stat2"}}
r=post(base+path, json=q, timeout=(10,120))
js=r.json()
print("chunk status",r.status_code,"size",js["size"],"nvalues",len(js["value"]))
print("updated:", js.get("updated"))
print("TIME labels:", list(js["dimension"]["TIME"]["category"]["label"].items()))
