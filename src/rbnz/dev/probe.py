import sys, os, time
os.chdir("/Users/nathansnellaert/Documents/hardened/connectors/src/rbnz"); sys.path.insert(0,"src")
import nodes.rbnz as R
R._try_live=lambda u:None
for code in ["D10","D12","S50","D9","D30","F5","R3"]:
    print(code, "group:", R._group_candidates(code))
    t0=time.time(); rows=[]
    for opt,stems in R.SERIES_OPTIONS[code].items():
        for s in stems:
            rows+=R._parse_workbook(R._download_stem(code,s),code,opt,s)
    print(f"   rows={len(rows)} ({time.time()-t0:.1f}s)")
