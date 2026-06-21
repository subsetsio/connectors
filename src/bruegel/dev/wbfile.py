import httpx, urllib.parse, sys
fileurl="https://www.bruegel.org/sites/default/files/2026-06/REER_database_ver14Jun2026.zip"
page="https://www.bruegel.org/dataset/global-trade-tracker"

def cdx(u):
    r=httpx.get("https://web.archive.org/cdx/search/cdx",
        params={"url":u,"output":"json","limit":"-8","filter":"statuscode:200","fl":"timestamp,original,statuscode,mimetype"},
        timeout=60)
    print("CDX", u, "->", r.status_code)
    try:
        rows=r.json()
        for row in rows[1:]:
            print("   ", row)
        return rows
    except Exception as e:
        print("   parse err", e, r.text[:200]); return []

# 1: does wayback have the exact reer zip?
cdx(fileurl)
# 2: prefix search for any reer zip ever archived
print("=== prefix REER ===")
cdx("bruegel.org/sites/default/files/*REER*")
