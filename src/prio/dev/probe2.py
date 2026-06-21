import re, io, zipfile, urllib.parse
from subsets_utils import get
import pandas as pd

IDS = ["1","3","4","5","6","7","8","10","11","16","20","23","31","32","34","35","36","37","39","40"]
DATA_EXT_PRIORITY = ["csv","xlsx","xls","dta","sav","tab","txt","dat"]

def links(html):
    seen=set(); res=[]
    for m in re.finditer(r'cdn\.cloud\.prio\.org/files/([0-9a-f-]+)/([^"?\\]+)', html):
        u,f = m.group(1), urllib.parse.unquote(m.group(2))
        if (u,f) in seen: continue
        seen.add((u,f)); res.append((u,f))
    return res

def ext(name): 
    return name.rsplit(".",1)[-1].lower() if "." in name else ""

def pick(files):
    # files: list of (name). return best data file name by priority, else None
    for e in DATA_EXT_PRIORITY:
        for name in files:
            if ext(name)==e: return name
    return None

def dl(uuid, fname):
    url = f"https://cdn.cloud.prio.org/files/{uuid}/{urllib.parse.quote(fname)}"
    return get(url, timeout=(10,120)).content

for i in IDS:
    try:
        html = get(f"https://www.prio.org/data/{i}", timeout=(10,60)).text
        ls = links(html)
        names = [f for _,f in ls]
        # pick top-level data file (prefer non-zip data; if none, pick a zip)
        chosen = pick([n for n in names if ext(n)!="zip"])
        zipname = None
        if chosen is None:
            zipname = next((n for n in names if ext(n)=="zip"), None)
        # map name->uuid
        umap = {f:u for u,f in ls}
        report = f"/data/{i}: "
        if chosen:
            content = dl(umap[chosen], chosen)
            report += f"FILE={chosen} ({len(content)//1024}KB)"
            print(report); 
        elif zipname:
            content = dl(umap[zipname], zipname)
            zf = zipfile.ZipFile(io.BytesIO(content))
            members = [m for m in zf.namelist() if not m.endswith("/")]
            datam = pick(members)
            report += f"ZIP={zipname} -> member={datam}  | all={[m.rsplit('/',1)[-1] for m in members][:8]}"
            print(report)
        else:
            print(report+"NO DATA FILE  names="+str(names))
    except Exception as e:
        print(f"/data/{i}: ERR {type(e).__name__}: {e}")
