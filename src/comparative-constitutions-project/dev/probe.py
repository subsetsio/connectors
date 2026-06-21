import io, re, zipfile, collections
from subsets_utils import get

r = get("https://www.constituteproject.org/service/constitutions?lang=en", timeout=(10,120))
data = r.json()
print("constitutions count:", len(data))
allkeys = set()
for rec in data: allkeys |= set(rec.keys())
print("union keys:", sorted(allkeys))
types = collections.defaultdict(collections.Counter)
for rec in data:
    for k in allkeys:
        types[k][type(rec.get(k)).__name__] += 1
for k in sorted(allkeys):
    print(f"  {k}: {dict(types[k])}")

page = get("https://comparativeconstitutionsproject.org/download-data/", timeout=(10,120)).text
def resolve(heading):
    i = re.search(heading, page); sub = page[i.end():]
    return re.search(r'href="(https://[^"]*box\.com/shared/static/[^"]+\.zip)"', sub).group(1)
cce_url = resolve(r"Chronology of Constitutional Events")
cnc_url = resolve(r"Characteristics of National Constitutions")
print("CCE url tail:", cce_url.split('/')[-1], "| CNC url tail:", cnc_url.split('/')[-1])
blob = get(cce_url, timeout=(10,300)).content
print("CCE zip bytes:", len(blob))
with zipfile.ZipFile(io.BytesIO(blob)) as zf:
    csvs = [n for n in zf.namelist() if n.lower().endswith(".csv") and "macosx" not in n.lower() and "_small" not in n.lower()]
    print("CCE csv members:", csvs)
    print("CCE header:", zf.read(csvs[0]).split(b"\n",1)[0][:300])
