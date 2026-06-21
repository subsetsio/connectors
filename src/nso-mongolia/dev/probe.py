import json, urllib.parse
from subsets_utils import get, post

BASE = "https://data.1212.mn/api/v1/en/NSO"
path = ["Population, household", "1_Population, household"]
table = "DT_NSO_0300_027V1.px"
url = BASE + "/" + "/".join(urllib.parse.quote(s, safe="") for s in path) + "/" + urllib.parse.quote(table, safe="")
print("URL", url)

meta = get(url, timeout=(10,120)).json()
print("TITLE", meta["title"])
for v in meta["variables"]:
    print("VAR", v["code"], "|", v["text"], "| n=", len(v["values"]), "| sample", v["valueTexts"][:3])

body = {"query":[{"code":v["code"],"selection":{"filter":"all","values":["*"]}} for v in meta["variables"]],
        "response":{"format":"json-stat2"}}
r = post(url, json=body, timeout=(10,120))
print("POST status", r.status_code)
js = r.json()
print("keys", list(js.keys()))
print("id", js.get("id"), "size", js.get("size"))
print("value type", type(js.get("value")), "len", len(js["value"]) if isinstance(js["value"],list) else "dict")
print("value sample", js["value"][:5] if isinstance(js["value"],list) else list(js["value"].items())[:5])
dimcode = js["id"][0]
dim = js["dimension"][dimcode]
print("dim0 label", dim.get("label"))
print("dim0 category index", dim["category"]["index"])
print("dim0 category label", dim["category"]["label"])
