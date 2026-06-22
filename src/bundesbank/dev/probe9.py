import sys, os, time, json, re
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from subsets_utils import get_client
SDMX_CSV="application/vnd.sdmx.data+csv;version=1.0.0"
client=get_client()
url="https://api.statistiken.bundesbank.de/rest/data/BBBK7/Q."
for i in range(8):
    t=time.time()
    with client.stream("GET",url,headers={"Accept":SDMX_CSV},timeout=(15,300)) as resp:
        st=resp.status_code
        if st==200:
            rows=sum(1 for _ in resp.iter_lines())
            print(f"try{i} 200 rows={rows} after {time.time()-t:.1f}s"); break
        body=b"".join(resp.iter_bytes()).decode("utf-8","replace")
        m=re.search(r'Progress: ([\d.]+)%', body)
        eta=re.search(r'([\d.]+) Minutes', body)
        print(f"try{i} {st} progress={m.group(1) if m else '?'}% eta={eta.group(1) if eta else '?'}min")
    time.sleep(30)
