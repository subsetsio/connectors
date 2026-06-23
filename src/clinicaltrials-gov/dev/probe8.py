import os, sys, ssl, httpx
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import subsets_utils
import subsets_utils.http_client as hc
ctx = ssl.create_default_context(); ctx.set_ciphers("DEFAULT")
hc._client = httpx.Client(timeout=30, headers=hc._client_config["headers"], follow_redirects=True, verify=ctx)
B = "https://clinicaltrials.gov/api/v2/studies"

# try field variants
for fields in ["NCTId,Conditions", "NCTId,Condition", "protocolSection.conditionsModule.conditions"]:
    r = subsets_utils.get(B, params={"pageSize": 1, "fields": fields}, timeout=(10,60))
    print(repr(fields), "->", r.status_code, r.text[:160] if r.status_code!=200 else "OK")
