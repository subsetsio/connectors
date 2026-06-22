import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from subsets_utils import get_client, get
SDMX_CSV="application/vnd.sdmx.data+csv;version=1.0.0"
client=get_client()
def head(url, accept=SDMX_CSV, n=3):
    try:
        with client.stream("GET",url,headers={"Accept":accept},timeout=(15,180)) as resp:
            print(f"  -> {resp.status_code}  {url}")
            if resp.status_code==200:
                rows=0
                for line in resp.iter_lines():
                    if rows<n: print("     ",line[:160])
                    rows+=1
                    if rows>3_000_000: break
                print("     total lines:",rows)
    except Exception as e:
        print("  ERR",type(e).__name__,e, url)

print("A serieskeysonly variants:")
head("https://api.statistiken.bundesbank.de/rest/data/BBBK7?detail=serieskeysonly")
head("https://api.statistiken.bundesbank.de/rest/data/BBBK7/Q?detail=serieskeysonly")
head("https://api.statistiken.bundesbank.de/rest/data/BBBK7/all?detail=serieskeysonly")
print("B availableconstraint:")
for acc in ["application/xml"]:
    r=get("https://api.statistiken.bundesbank.de/rest/availableconstraint/BBBK7", headers={"Accept":acc}, timeout=(15,120))
    print("  availableconstraint status",r.status_code,"len",len(r.content))
    print("   ",r.text[:300])
