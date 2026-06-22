import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from subsets_utils import get_client
SDMX_CSV="application/vnd.sdmx.data+csv;version=1.0.0"
client=get_client()

# 1) series keys only
url="https://api.statistiken.bundesbank.de/rest/data/BBBK7/Q.?detail=serieskeysonly"
with client.stream("GET",url,headers={"Accept":SDMX_CSV},timeout=(15,300)) as resp:
    print("serieskeysonly status",resp.status_code)
    if resp.status_code==200:
        hdr=None; keys=[]; idx={}
        for line in resp.iter_lines():
            if hdr is None:
                hdr=line.lstrip("﻿").split(";"); idx={c:i for i,c in enumerate(hdr)}; 
                print("hdr",hdr); continue
            f=line.split(";")
            keys.append(f[idx["BBK_ID"]])
        print("num series",len(keys))
        print("sample",keys[:5])
        # second-dim values (after freq)
        second=[k.split(".",2)[1] if k.count(".")>=1 else None for k in keys]
        # actually BBK_ID = full key e.g. BBBK7.Q.<rest>? check
        print("sample full keys parsed:")
        for k in keys[:3]: print("  ",k, "parts", k.split("."))
