import os, re, json
from subsets_utils import get

KEY = os.environ.get("DATA_GOV_IN_API_KEY", "579b464db66ec23bdd000001cdd3946e44ce4aad7209ff7b23ac571b")
LISTS = "https://api.data.gov.in/lists"
RES = "https://api.data.gov.in/resource/{}"

def lists_all():
    recs, off = [], 0
    while True:
        p = {"api-key": KEY, "format": "json", "filters[active]": "1",
             "notfilters[source]": "visualize.data.gov.in", "filters[title]": "HMIS",
             "limit": "1000", "offset": str(off)}
        d = get(LISTS, params=p, timeout=(10,120)).json()
        r = d.get("records", []); recs += r
        total = int(d.get("total") or 0); off += 1000
        if not r or off >= total: break
    return recs

recs = lists_all()
ai = [r for r in recs if re.search(r"\bof\s+all\s+india\b", r.get("title",""), re.I)]
ai.sort(key=lambda r: r.get("title",""))
print("All-India item-wise reports:", len(ai))
for r in ai:
    print("  ", r["index_name"], "|", r["title"])

def dump(rid, label):
    d = get(RES.format(rid), params={"api-key": KEY, "format": "json", "limit": "2"}, timeout=(10,120)).json()
    print("\n===", label, "=== total", d.get("total"))
    print("fields:", [f["id"] for f in d.get("field",[])])
    print("row0:", json.dumps(d.get("records",[{}])[0]))

# a 17-col (old) and a 69-col (new) All-India report
old = next(r for r in ai if "2008-09" in r["title"])
new = next(r for r in ai if "2019-20" in r["title"])
dump(old["index_name"], "OLD "+old["title"])
dump(new["index_name"], "NEW "+new["title"])
