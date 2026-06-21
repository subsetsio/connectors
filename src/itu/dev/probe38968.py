from subsets_utils import get
BASE="https://api.datahub.itu.int/v2"
cids=[c["CountryID"] for c in get(f"{BASE}/country/all",timeout=(10,60)).json()]
for label,ids in [("2-countries",cids[:2]),("all-countries",cids)]:
    s=",".join(str(x) for x in ids)
    r=get(f"{BASE}/data/download",params={"codesid":38968,"countriesid":s,"startyear":1960},timeout=(10,180))
    print(label,"status",r.status_code,"len",len(r.content),"head",r.content[:80])
