from subsets_utils import post
import urllib.parse

def fetch(lang, db, tid):
    # tid like "E07.09.px" -> uppercase extension to bypass IIS static handler
    base, ext = tid.rsplit(".", 1)
    url = f"https://pxweb.nso.gov.vn/api/v1/{lang}/{db}/{base}.{ext.upper()}"
    r = post(url, json={"query": [], "response": {"format": "json-stat2"}}, timeout=(10,120))
    r.raise_for_status()
    return r.json()

d = fetch("en", "Industry", "E07.09.px")
print("type:", type(d).__name__, "keys:", list(d.keys()) if isinstance(d,dict) else "LIST")
print("class:", d.get("class"), "id:", d.get("id"), "size:", d.get("size"), "label:", d.get("label"))
for dim in d["id"]:
    dd = d["dimension"][dim]
    print(f"  dim {dim!r} label={dd.get('label')!r} ncat={len(dd['category']['label'])} sample={list(dd['category']['label'].items())[:2]}")
print("value len:", len(d["value"]), "sample:", d["value"][:6], "types:", set(type(v).__name__ for v in d["value"]))
print()
d2 = fetch("vi", urllib.parse.quote("Dân số và lao động"), "V02.01.px")
print("V02.01 id:", d2.get("id"), "size:", d2.get("size"))
for dim in d2["id"]:
    dd = d2["dimension"][dim]
    print(f"  dim {dim!r} label={dd.get('label')!r} sample={list(dd['category']['label'].items())[:2]}")
print("vals:", d2["value"][:5], "Nones:", sum(1 for v in d2['value'] if v is None), "/", len(d2['value']))
# combined dim id like V02.03-07 multi-table check
d3 = fetch("vi", urllib.parse.quote("Đầu tư"), "V04.11.px")
print("V04.11 dims:", d3.get("id"), "size:", d3.get("size"))
