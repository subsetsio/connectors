from subsets_utils import get_client

ACCEPT = {"Accept":"application/vnd.sdmx.data+csv;version=1.0.0"}
bad = ["BBBK13","BBBK20","BBBP2","BBDG1","BBXP1","BBBK7","BBFFDIPV","BBKRT","BBSIS"]
client = get_client()
for flow in bad:
    url=f"https://api.statistiken.bundesbank.de/rest/data/{flow}"
    try:
        with client.stream("GET", url, headers=ACCEPT, timeout=(15,300)) as r:
            status=r.status_code
            first=None; nlines=0
            if status==200:
                for line in r.iter_lines():
                    if nlines==0: first=line[:80]
                    nlines+=1
                    if nlines>=3: break
            print(f"{flow}: status={status} firstline={first!r}")
    except Exception as e:
        print(f"{flow}: EXC {type(e).__name__}: {str(e)[:80]}")
