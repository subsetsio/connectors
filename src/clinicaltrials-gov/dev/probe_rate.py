import os, sys, ssl, httpx, time
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import subsets_utils
import subsets_utils.http_client as hc
ctx = ssl.create_default_context(); ctx.set_ciphers("DEFAULT")
hc._client = httpx.Client(timeout=60, headers=hc._client_config["headers"], follow_redirects=True, verify=ctx)
B = "https://clinicaltrials.gov/api/v2/studies"

token=None; codes=[]; t0=time.time()
for i in range(25):
    p={"pageSize":1000,"fields":"NCTId"}
    if token: p["pageToken"]=token
    r=subsets_utils.get(B, params=p, timeout=(10,90))
    codes.append(r.status_code)
    if r.status_code==200:
        token=r.json().get("nextPageToken")
    if i==0:
        rl={k:v for k,v in r.headers.items() if "rate" in k.lower() or "retry" in k.lower()}
        print("rate headers:", rl)
dt=time.time()-t0
print(f"25 reqs(pageSize=1000) in {dt:.1f}s -> {25/dt*60:.0f} req/min; codes set: {sorted(set(codes))}; n200={codes.count(200)}")
