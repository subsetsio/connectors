import time, httpx
from subsets_utils import get
URL="https://data.gov.au/data/api/3/action/package_show?id=forests-of-australia-2023"
ok=resets=other=0
for i in range(15):
    try:
        r=get(URL,timeout=(15,60)); r.raise_for_status(); ok+=1
    except httpx.ReadError as e:
        resets+=1
    except Exception as e:
        other+=1; print("other",type(e).__name__,str(e)[:50])
    time.sleep(0.4)
print(f"ok={ok} resets={resets} other={other}")
