from subsets_utils import get
for did in ["trade","uk-business-by-enterprises-and-local-units","cpih01","labour-market","gdp-to-four-decimal-places","uk-spending-on-cards","ashe-tables-20","TS001","ST001","retail-sales-index"]:
    try:
        d=get(f"https://api.beta.ons.gov.uk/v1/datasets/{did}",timeout=(10,60)).json()
        lv=d["links"]["latest_version"]["href"]
        v=get(lv,timeout=(10,60)).json()
        csz=v.get("downloads",{}).get("csv",{}).get("size")
        print(f"{did:50s} csv_bytes={csz}")
    except Exception as e:
        print(did,"ERR",e)
