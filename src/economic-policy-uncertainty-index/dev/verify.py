import sys, json
sys.path.insert(0,"src")
from utils import parse_index_file
mapping=json.load(open("dev/mapping.json"))
bad=[]; total=0
for eid,fn in mapping.items():
    content=open("dev/files/"+fn,"rb").read()
    try:
        rows=parse_index_file(content, fn)
    except Exception as e:
        import traceback; traceback.print_exc(); print("ERR",fn,e); bad.append(fn); continue
    if not rows: print("ZERO",fn); bad.append(fn); continue
    total+=len(rows)
    dts=sorted(set(d for d,_,_ in rows)); ser=set(s for _,s,_ in rows)
    # sanity: no series name longer than 120 chars (would signal a note leaked in)
    longs=[s for s in ser if len(s)>120]
    flag=" LONGSERIES!" if longs else ""
    print(f"OK {eid}: rows={len(rows)} series={len(ser)} {dts[0]}..{dts[-1]}{flag}")
    if longs: print("    e.g.", longs[0][:160])
print(f"\nTOTAL rows={total} files_ok={len(mapping)-len(bad)} BAD={bad}")
