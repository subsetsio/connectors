import sys; sys.path.insert(0,"src")
from subsets_utils import get
r=get("https://dataverse.nl/api/datasets/:persistentId/",params={"persistentId":"doi:10.34894/FABVLR"},timeout=60)
for f in r.json()["data"]["latestVersion"]["files"]:
    df=f["dataFile"]; print(df["id"], df.get("filename"), df.get("contentType"))
