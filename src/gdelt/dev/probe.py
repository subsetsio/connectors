import io, zipfile
from subsets_utils import get
# Use masterfilelist (posted files), take a recent export url (not the very last, which may race)
ml = get("http://data.gdeltproject.org/gdeltv2/masterfilelist.txt", timeout=(10,180)).text
export_urls = [ln.split()[2] for ln in ml.splitlines() if len(ln.split())>=3 and ".export." in ln.split()[2]]
url = export_urls[-5]
print("url:", url, "total export files:", len(export_urls))
r = get(url, timeout=(10,120)); r.raise_for_status()
zf = zipfile.ZipFile(io.BytesIO(r.content))
rows = [ln.split("\t") for ln in zf.read(zf.namelist()[0]).decode("utf-8","replace").splitlines() if ln]
print("rows:", len(rows), "ncols:", len(rows[0]))
r0 = rows[0]
labels = {0:"gid",1:"day",28:"root",29:"quad",30:"gold",31:"nment",33:"nart",34:"tone",53:"act_fips"}
for i,l in labels.items(): print(i, l, repr(r0[i]))
from collections import Counter
print("quad:", Counter(r[29] for r in rows))
print("roots:", sorted(set(r[28] for r in rows))[:15])
print("null country:", sum(1 for r in rows if not r[53]), "/", len(rows))
print("event_days:", Counter(r[1] for r in rows).most_common(3))
