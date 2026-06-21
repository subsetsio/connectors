import sys
sys.path.insert(0, "src")
from subsets_utils import get

DOIS = {
 "fabvlr":"10.34894/FABVLR","qt5bcc":"10.34894/QT5BCC","inzbf2":"10.34894/INZBF2",
 "aeax1f":"10.34894/AEAX1F","lch4ca":"10.34894/LCH4CA","e7mvox":"10.34894/E7MVOX",
 "imkxnt":"10.34894/IMKXNT","a7axdn":"10.34894/A7AXDN","pj2m1c":"10.34894/PJ2M1C",
 "xdtauz":"10.34894/XDTAUZ","6gdd7q":"10.34894/6GDD7Q",
}
for k,doi in DOIS.items():
    r = get("https://dataverse.nl/api/datasets/:persistentId/",
            params={"persistentId":"doi:"+doi}, timeout=60)
    r.raise_for_status()
    files = r.json()["data"]["latestVersion"]["files"]
    print(f"\n=== {k}  {doi}  ({len(files)} files) ===")
    for f in files:
        df=f["dataFile"]
        print(f"  id={df['id']:>8}  {df.get('filesize',0):>12}  {df.get('contentType','')[:45]:45}  {df.get('filename','')}")
