from subsets_utils import post, get
import json

def fetch(lang, db, tid):
    url = f"https://pxweb.nso.gov.vn/api/v1/{lang}/{db}/{tid}"
    r = post(url, json={"query": [], "response": {"format": "json-stat2"}}, timeout=(10,120))
    r.raise_for_status()
    return r.json()

# English table E07.09 (Industry, energy)
d = fetch("en", "Industry", "E07.09.px")
print("=== E07.09 json-stat2 keys:", list(d.keys()))
print("class:", d.get("class"), "| id(dims):", d.get("id"), "| size:", d.get("size"))
print("label:", d.get("label"))
for dim in d["id"]:
    cat = d["dimension"][dim]["category"]
    labels = list(cat["label"].items())[:3]
    print(f"  dim {dim!r} label={d['dimension'][dim].get('label')!r} ncat={len(cat['label'])} sample={labels}")
print("value len:", len(d["value"]), "sample:", d["value"][:5])
print("value types:", set(type(v).__name__ for v in d["value"][:50]))
print()
# Vietnamese table V02.01 (Population)
import urllib.parse
d2 = fetch("vi", urllib.parse.quote("Dân số và lao động"), "V02.01.px")
print("=== V02.01 dims:", d2.get("id"), "size:", d2.get("size"))
for dim in d2["id"]:
    print(f"  dim {dim!r} label={d2['dimension'][dim].get('label')!r}", "sample:", list(d2['dimension'][dim]['category']['label'].items())[:2])
print("value sample:", d2["value"][:5])
print("any None in values?", any(v is None for v in d2["value"]))
