from subsets_utils import post
import urllib.parse

def fetch(lang, db, tid_noext):
    url = f"https://pxweb.nso.gov.vn/api/v1/{lang}/{db}/{tid_noext}"
    r = post(url, json={"query": [], "response": {"format": "json-stat2"}}, timeout=(10,120))
    r.raise_for_status()
    return r.json()

d = fetch("en", "Industry", "E07.09")
print("=== E07.09 keys:", list(d.keys()))
print("class:", d.get("class"), "id:", d.get("id"), "size:", d.get("size"))
for dim in d["id"]:
    dd = d["dimension"][dim]
    print(f"  dim {dim!r} label={dd.get('label')!r} ncat={len(dd['category']['label'])} sample={list(dd['category']['label'].items())[:2]}")
print("value len:", len(d["value"]), "sample:", d["value"][:5], "types:", set(type(v).__name__ for v in d["value"]))
print("status field present?", "status" in d, d.get("status") if "status" in d else "")
print()
d2 = fetch("vi", urllib.parse.quote("Dân số và lao động"), "V02.01")
print("=== V02.01 id:", d2.get("id"), "size:", d2.get("size"))
for dim in d2["id"]:
    dd = d2["dimension"][dim]
    print(f"  dim {dim!r} label={dd.get('label')!r} sample={list(dd['category']['label'].items())[:2]}")
print("value sample:", d2["value"][:5], "Nones:", sum(1 for v in d2['value'] if v is None))
