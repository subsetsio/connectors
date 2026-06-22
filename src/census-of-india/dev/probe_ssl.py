import ssl, certifi, httpx, io
pem = open("dev/emint.pem").read()
ctx = ssl.create_default_context(cafile=certifi.where())
ctx.load_verify_locations(cadata=pem)
with httpx.Client(verify=ctx, follow_redirects=True, timeout=60,
                  headers={"User-Agent":"DataIntegrations/1.0"}) as c:
    r=c.get("https://censusindia.gov.in/nada/index.php/api/catalog/search?tab_type=table&ps=2&page=1")
    print("catalog", r.status_code, "found", r.json()["result"]["found"])
    m=c.get("https://censusindia.gov.in/nada/index.php/metadata/export/42526/json")
    j=m.json(); print("metadata", m.status_code, "xlsx:", j["resources"][0]["filename"].rsplit("/",1)[-1][:40])
    # download a small file
    u=None
    for res in j["resources"]:
        if res["filename"].lower().endswith((".xlsx",".xls")): u=res["filename"]; break
    d=c.get(u); print("download", d.status_code, "bytes", len(d.content), "head", d.content[:4])
