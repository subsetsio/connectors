from subsets_utils import get
url = "https://www.sidc.be/SILSO/DATA/SN_d_tot_V2.0.txt"
r = get(url, headers={"Range": "bytes=0-1023", "Accept-Encoding": "identity"}, timeout=(30.0,180.0))
print("status:", r.status_code)
for k in ("Accept-Ranges","Content-Range","Content-Length","Content-Encoding"):
    print(f"  {k}: {r.headers.get(k)}")
print("body bytes returned:", len(r.content))
