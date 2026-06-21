import re, io, zipfile, urllib.parse
from subsets_utils import get

IDS = ["1","3","4","5","6","7","8","10","11","16","20","23","31","32","34","35","36","37","39","40"]

def links(html):
    out=[]
    for m in re.finditer(r'cdn\.cloud\.prio\.org/files/([0-9a-f-]+)/([^"?\\]+)', html):
        uuid, fname = m.group(1), urllib.parse.unquote(m.group(2))
        out.append((uuid, fname))
    # dedup preserve order
    seen=set(); res=[]
    for u,f in out:
        if (u,f) in seen: continue
        seen.add((u,f)); res.append((u,f))
    return res

for i in IDS:
    html = get(f"https://www.prio.org/data/{i}", timeout=(10,60)).text
    ls = links(html)
    # the FIRST link is usually the primary/newest version
    print(f"\n=== /data/{i}  ({len(ls)} files) ===")
    for j,(u,f) in enumerate(ls[:4]):
        print(f"  [{j}] {f}")
    if not ls:
        print("  NO FILES")
