import os, re, collections
from subsets_utils import get

KEY = os.environ.get("DATA_GOV_IN_API_KEY", "579b464db66ec23bdd000001cdd3946e44ce4aad7209ff7b23ac571b")
LISTS = "https://api.data.gov.in/lists"
RES = "https://api.data.gov.in/resource/{}"

def lists_page(offset, limit=1000):
    p = {"api-key": KEY, "format": "json", "filters[active]": "1",
         "notfilters[source]": "visualize.data.gov.in", "filters[title]": "HMIS",
         "limit": str(limit), "offset": str(offset)}
    return get(LISTS, params=p, timeout=(10, 120)).json()

# enumerate all
recs = []
off = 0
while True:
    d = lists_page(off)
    r = d.get("records", [])
    recs.extend(r)
    total = int(d.get("total") or 0)
    off += 1000
    if not r or off >= total:
        break
print("total HMIS resources:", len(recs), "(reported", total, ")")

# classify by title
def fy(t):
    m = re.search(r"for\s+(\d{4})[-/](\d{2,4})", t or "", re.I)
    return f"{m.group(1)}-{m.group(2)}" if m else None

allindia = [r for r in recs if re.search(r"\bof\s+all\s+india\b", r.get("title",""), re.I)]
print("All-India resources:", len(allindia))
years = collections.Counter(fy(r.get("title","")) for r in recs)
print("years:", dict(sorted((k,v) for k,v in years.items() if k)))
print("titles missing FY:", sum(1 for r in recs if not fy(r.get("title",""))))

# distinct title shapes (strip geo + year)
shapes = collections.Counter()
for r in recs:
    t = r.get("title","")
    t2 = re.sub(r"\bof\s+.+?\s+for\s+\d{4}[-/]\d{2,4}", "of <GEO> for <FY>", t, flags=re.I)
    t2 = re.sub(r"\d{4}[-/]\d{2,4}", "<FY>", t2)
    shapes[t2] += 1
print("title shapes:")
for s,c in shapes.most_common(15):
    print("  ", c, s[:90])

# sample several resources: total rows + n fields
print("sample resource sizes:")
import random
for r in (allindia[:3] + recs[:2] + recs[-2:]):
    rid = r["index_name"]
    d = get(RES.format(rid), params={"api-key": KEY, "format": "json", "limit": "1"}, timeout=(10,120)).json()
    print("  ", r["title"][:55], "| total", d.get("total"), "| nfields", len(d.get("field",[])))
