from subsets_utils import get, get_client
SDMX = {"Accept":"application/vnd.sdmx.data+csv;version=1.0.0"}
for flow in ["BBBK13","BBBK20","BBBP2","BBDG1","BBXP1"]:
    for path in [f"BBK,{flow},1.0", f"{flow}/all", f"{flow}/", f"BBK,{flow}"]:
        try:
            r = get(f"https://api.statistiken.bundesbank.de/rest/data/{path}", headers=SDMX, timeout=(15,120))
            print(f"{flow} [{path}]: {r.status_code} bytes={len(r.content) if r.status_code==200 else '-'}")
            if r.status_code==200: break
        except Exception as e:
            print(f"{flow} [{path}]: EXC {str(e)[:50]}")
