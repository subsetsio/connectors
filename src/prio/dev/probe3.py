import re, io, zipfile, urllib.parse
from subsets_utils import get

def links(html):
    seen=set(); res=[]
    for m in re.finditer(r'cdn\.cloud\.prio\.org/files/([0-9a-f-]+)/([^"?\\]+)', html):
        u,f = m.group(1), urllib.parse.unquote(m.group(2))
        if (u,f) in seen: continue
        seen.add((u,f)); res.append((u,f))
    return res
def dl(uuid, fname):
    return get(f"https://cdn.cloud.prio.org/files/{uuid}/{urllib.parse.quote(fname)}", timeout=(10,180)).content
def allnames(i):
    html=get(f"https://www.prio.org/data/{i}", timeout=(10,60)).text
    ls=links(html); return ls
def zipmembers(uuid,fname):
    c=dl(uuid,fname); zf=zipfile.ZipFile(io.BytesIO(c))
    return [(m.filename, m.file_size) for m in zf.infolist() if not m.is_dir() and not m.filename.split('/')[-1].startswith('._') and '__MACOSX' not in m.filename]

for i in ["11","20"]:
    print(f"\n##### /data/{i} ALL LINKS #####")
    for u,f in allnames(i): print("  ",f)

for i,zipfn in [("40","priogrid_300_05deg_yearly.zip"),("40","priogrid_3_0_1_05deg_yearly.zip"),
                ("39","OMG_Stata.zip"),("39","OMG_R.zip"),("6","USD 20 Data.zip")]:
    print(f"\n##### /data/{i} ZIP={zipfn} #####")
    ls=allnames(i); umap={f:u for u,f in ls}
    if zipfn not in umap: print("  (not found, links:", [f for _,f in ls],")"); continue
    try:
        for name,size in zipmembers(umap[zipfn], zipfn)[:30]:
            print(f"   {size:>12,}  {name}")
    except Exception as e:
        print("  ERR", e)
