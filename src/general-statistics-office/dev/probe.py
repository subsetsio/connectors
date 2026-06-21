import httpx
# Validate client against Statistics Finland PxWeb (known working POST)
fin_url = "https://pxdata.stat.fi/PXWeb/api/v1/en/StatFin/vtp/statfin_vtp_pxt_124l.px"
with httpx.Client(timeout=40, follow_redirects=True) as c:
    rm = c.get(fin_url)
    print("FIN meta GET:", rm.status_code, rm.headers.get("content-type","")[:20])
    meta = rm.json()
    q = [{"code":v["code"],"selection":{"filter":"top","values":["1"]}} for v in meta["variables"]]
    rd = c.post(fin_url, json={"query":q,"response":{"format":"json-stat2"}})
    j = rd.json()
    print("FIN data POST:", rd.status_code, "has value:", isinstance(j,dict) and "value" in j, "vals:", j.get("value") if isinstance(j,dict) else None)
