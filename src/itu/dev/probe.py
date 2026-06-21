import io
import zipfile
import csv
import time
from subsets_utils import get

BASE = "https://api.datahub.itu.int/v2"


def _download_csv(codesid, country_ids):
    cids = ",".join(str(c) for c in country_ids)
    url = f"{BASE}/data/download"
    for i in range(5):
        r = get(url, params={"codesid": codesid, "countriesid": cids, "startyear": 1960}, timeout=(10, 120))
        body = r.content
        if body[:2] == b"PK":
            zf = zipfile.ZipFile(io.BytesIO(body))
            name = zf.namelist()[0]
            text = zf.read(name).decode("utf-8-sig")
            return list(csv.DictReader(io.StringIO(text)))
        print(f"  [try {i}] non-zip body ({len(body)}b): {body[:90]!r}")
        time.sleep(2 * (i + 1))
    return None


# country list
countries = get(f"{BASE}/country/all", timeout=(10, 60)).json()
cids = [c["CountryID"] for c in countries]
print("countries:", len(countries), "sample:", {k: countries[0][k] for k in ("CountryID", "IsoCode", "ShortName")})
print("country keys:", sorted(countries[0].keys()))
print("regions sample:", countries[0]["Regions"][:1])

# quantitative indicator
print("\n=== quantitative codesid=8965 ===")
rows = _download_csv(8965, cids)
print("rows:", len(rows), "cols:", list(rows[0].keys()))
print("sample:", rows[0])

# qualitative / governance indicator - pick a Trust/Governance codeID
print("\n=== getcategories: find a Governance base indicator ===")
cats = get(f"{BASE}/dictionaries/getcategories", timeout=(10, 60)).json()
gov = None
for c in cats:
    if c["category"] in ("Governance", "Trust"):
        for sc in c["subCategory"]:
            for it in sc["items"]:
                if not it.get("isCollection"):
                    gov = it
                    break
            if gov:
                break
    if gov:
        break
print("governance indicator:", gov["codeID"], gov["label"])
rows2 = _download_csv(gov["codeID"], cids)
print("rows:", len(rows2) if rows2 else None)
if rows2:
    print("cols:", list(rows2[0].keys()))
    print("sample:", rows2[0])
    # distinct dataValue types
    vals = [r["dataValue"] for r in rows2[:20]]
    print("sample dataValues:", vals)
