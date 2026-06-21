import re, io, zipfile, urllib.parse
from subsets_utils import get
def links(html):
    seen=set(); res=[]
    for m in re.finditer(r'cdn\.cloud\.prio\.org/files/([0-9a-f-]+)/([^"?\\]+)', html):
        u,f=m.group(1),urllib.parse.unquote(m.group(2))
        if (u,f) in seen: continue
        seen.add((u,f)); res.append((u,f))
    return res
def dl(u,f): return get(f"https://cdn.cloud.prio.org/files/{u}/{urllib.parse.quote(f)}", timeout=(10,180)).content
def members(u,f):
    zf=zipfile.ZipFile(io.BytesIO(dl(u,f)))
    return [(m.filename,m.file_size) for m in zf.infolist() if not m.is_dir() and not m.filename.split('/')[-1].startswith('._') and '__MACOSX' not in m.filename]

for i in ["11","20"]:
    ls=links(get(f"https://www.prio.org/data/{i}", timeout=(10,60)).text)
    print(f"\n##### /data/{i} links #####")
    for u,f in ls: print("   ",f)

for i,zf in [("11","PETRODATA v12.zip"),("20","polyarchy v2 data.zip"),("20","polyarchy v11.zip")]:
    ls=links(get(f"https://www.prio.org/data/{i}", timeout=(10,60)).text)
    umap={f:u for u,f in ls}
    # find a zip whose name contains the key
    cand=[f for f in umap if zf.lower() in f.lower() or f.lower()==zf.lower()]
    if not cand:
        cand=[f for f in umap if f.lower().endswith('.zip')]
    for c in cand[:1]:
        print(f"\n##### /data/{i} ZIP={c} #####")
        try:
            for n,s in members(umap[c],c)[:25]: print(f"   {s:>12,}  {n}")
        except Exception as e: print("  ERR",e)
