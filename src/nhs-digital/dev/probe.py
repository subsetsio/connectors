import re, io
from subsets_utils import get

CKAN="https://ckan.publishing.service.gov.uk/api/3/action"
DATA_EXT=re.compile(r"\.(csv|xlsx|xls|zip)$", re.I)

def live_files(pkg):
    r=get(f"{CKAN}/package_show", params={"id":pkg}, timeout=60).json()["result"]
    out=[]
    for res in r["resources"]:
        u=res.get("url") or ""
        base=u.split("?")[0]
        if "files.digital.nhs.uk" in u and DATA_EXT.search(base):
            out.append((res.get("format"), u))
    return out

for pkg in ["national-diabetes-inpatient-safety-audit-ndisa-2018-2021",
            "general_pharmaceutical_services",
            "nhs-outcomes-framework-indicators",
            "prescribing-by-gp-practice-presentation-level",
            "national-diabetes-audit-2020-21-type-1-diabetes"]:
    fs=live_files(pkg)
    print(f"\n===== {pkg}: {len(fs)} live files")
    for fmt,u in fs[:4]:
        # HEAD-ish: get content-length via range request
        try:
            resp=get(u, headers={"Range":"bytes=0-2047"}, timeout=60)
            cl=resp.headers.get("Content-Range") or resp.headers.get("Content-Length")
            ext=u.split("?")[0].rsplit(".",1)[-1].lower()
            print(f"  [{fmt}] cl={cl} ext={ext} url=...{u[-60:]}")
            if ext=="csv":
                head=resp.content[:600].decode("utf-8","replace").splitlines()[:3]
                for line in head: print("       |", line[:140])
        except Exception as e:
            print("  ERR", type(e).__name__, str(e)[:80], u[-50:])
