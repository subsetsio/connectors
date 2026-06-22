from subsets_utils import get, post
url="https://bank.stat.gl/api/v1/en/Greenland/AL/AL10/ALXALK.px"
meta=get(url,timeout=(10,60)).json()
print("TITLE",meta["title"])
for v in meta["variables"]:
    print("  var",v["code"],"text=",v["text"],"nvals=",len(v.get("values") or []),"time=",v.get("time"),"elim=",v.get("elimination"))
# small query: all values via wildcard
q={"query":[{"code":v["code"],"selection":{"filter":"all","values":["*"]}} for v in meta["variables"]],"response":{"format":"json-stat2"}}
js=post(url,json=q,timeout=(10,120)).json()
print("KEYS",list(js.keys()))
print("id",js["id"],"size",js["size"])
print("role",js.get("role"))
print("nvalues",len(js["value"]),"sample",js["value"][:5])
# show one dimension category shape
d0=js["id"][0]
print("dim",d0,"category keys",list(js["dimension"][d0]["category"].keys()))
