from subsets_utils import get, post
import json

base = "https://data.stat.gov.lv/api/v1/en/OSP_PUB/"
# small table: IRS010 metadata
path = "POP/IR/IRS/IRS010"
m = get(base+path, timeout=(10,60)).json()
print("=== META title ===", m["title"])
for v in m["variables"]:
    print(f"  var code={v['code']!r} text={v.get('text')!r} nvals={len(v['values'])} elimination={v.get('elimination')} time={v.get('time')}")
# build all-* query, json-stat2
query = {"query":[{"code":v["code"],"selection":{"filter":"all","values":["*"]}} for v in m["variables"]],
         "response":{"format":"json-stat2"}}
import math
total=1
for v in m["variables"]: total*=len(v["values"])
print("total cells:", total)
r = post(base+path, json=query, timeout=(10,120))
print("POST status", r.status_code, "ctype", r.headers.get("content-type"))
js = r.json()
print("json-stat keys:", list(js.keys()))
print("class", js.get("class"), "dims order", js.get("id"), "size", js.get("size"))
print("role", js.get("role"))
# show one dimension structure
firstdim = js["id"][0]
dd = js["dimension"][firstdim]
print("dim", firstdim, "label", dd.get("label"))
print("  category.index sample:", dict(list(dd["category"]["index"].items())[:3]))
print("  category.label sample:", dict(list(dd["category"]["label"].items())[:3]))
print("value len", len(js["value"]), "sample values", js["value"][:5])
