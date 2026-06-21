from subsets_utils import get
import io, csv, json

CKAN="https://data.gov.au/data/api/3/action"
MYH="https://myhospitalsapi.aihw.gov.au/api/v1"

def res_url(rid):
    r=get(f"{CKAN}/resource_show", params={"id":rid}, timeout=(10,60))
    r.raise_for_status()
    return r.json()["result"]["url"]

# probe a few CKAN CSV headers
for rid,label in [("edcbc14c-ba7c-44ae-9d4f-2622ad3fafe0","GRIM"),
                  ("7e4d5726-8daa-4c14-8a46-96b701e8b3ca","ACIM Rates"),
                  ("3b7d81af-943f-447d-9d64-9ce220be35e7","MORT_2"),
                  ("88399d53-d55c-466c-8f4a-6cb965d24d6d","HealthExp"),
                  ("c7edfa08-7bc9-404d-8f2b-22bcd0425021","Youth"),
                  ("5c536ecc-316a-4206-9984-bd1b3b8982b9","NDSHS")]:
    try:
        u=res_url(rid)
        resp=get(u, timeout=(10,120))
        resp.raise_for_status()
        text=resp.content.decode("utf-8-sig", errors="replace")
        rdr=csv.reader(io.StringIO(text))
        hdr=next(rdr)
        row1=next(rdr, None)
        n=sum(1 for _ in rdr)+2
        print(f"\n== {label} ({rid[:8]}) url={u[-40:]}")
        print("  header:", hdr)
        print("  row1:", row1)
        print("  approx_rows:", n)
    except Exception as e:
        print(f"\n== {label} ERR {type(e).__name__}: {e}")
