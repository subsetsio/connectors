import os, sys, ssl, httpx
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import subsets_utils
import subsets_utils.http_client as hc

def install_client():
    ctx = ssl.create_default_context()
    ctx.set_ciphers("DEFAULT")
    if hc._client is not None:
        hc._client.close()
    hc._client = httpx.Client(
        timeout=hc._client_config["timeout"],
        headers=hc._client_config["headers"],
        follow_redirects=True,
        verify=ctx,
    )

install_client()
r = subsets_utils.get("https://clinicaltrials.gov/api/v2/studies",
                      params={"pageSize": 2, "fields": "NCTId,Conditions", "countTotal": "true"},
                      timeout=(10, 60))
print("subsets_utils.get ->", r.status_code)
d = r.json()
print("totalCount", d.get("totalCount"), "nextToken?", "nextPageToken" in d)
import json
print(json.dumps(d["studies"][0], indent=2)[:1200])
