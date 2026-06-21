from subsets_utils import get
for ref in ["STC,DF_18100001", "CCEI,GHG_IPCC_TABLE"]:
    url=f"https://energy-information.canada.ca/sdmx/rest/data/{ref}/"
    r=get(url, headers={"Accept":"text/csv"}, timeout=(10,180))
    ct=r.headers.get("content-type")
    print("===",ref, r.status_code, "ct=",ct, "len", len(r.text))
    lines=r.text.splitlines()
    print("header:", lines[0][:400] if lines else "(empty)")
    for l in lines[1:3]:
        print("  row:", l[:300])
    print("nrows:", len(lines)-1)
