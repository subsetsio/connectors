import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from subsets_utils import get_client
SDMX_CSV="application/vnd.sdmx.data+csv;version=1.0.0"
client=get_client()
for code in ["A","D","H","M","Q","W"]:
    # full request (no lastNObs) — measure status + bytes for first chunk
    url=f"https://api.statistiken.bundesbank.de/rest/data/BBBK7/{code}."
    try:
        with client.stream("GET",url,headers={"Accept":SDMX_CSV},timeout=(15,300)) as resp:
            st=resp.status_code
            nbytes=0; nrows=0
            if st==200:
                for i,line in enumerate(resp.iter_lines()):
                    nbytes+=len(line)
                    nrows+=1
                    if nrows>2_000_000: break
            print(f"freq={code} status={st} rows={nrows} approx_bytes={nbytes}")
    except Exception as e:
        print(f"freq={code} ERROR {type(e).__name__}: {e}")
