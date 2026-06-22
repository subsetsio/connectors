import ssl, certifi, httpx, json, re, collections
pem=open("dev/emint.pem").read()
ctx=ssl.create_default_context(cafile=certifi.where()); ctx.load_verify_locations(cadata=pem)
C=httpx.Client(verify=ctx, follow_redirects=True, timeout=120, headers={"User-Agent":"DataIntegrations/1.0"})
def gk(idno): return re.sub(r"(-\d+)+$","",idno)
TARGETS={"PC01_A01","PC01_A02","PC11_A01","PC11_A02","PC11_A11"}
rows=[]
p=1
while True:
    r=C.get(f"https://censusindia.gov.in/nada/index.php/api/catalog/search?tab_type=table&ps=1000&page={p}").json()["result"]
    b=r["rows"]
    if not b: break
    rows+=b
    if len(rows)>=int(r["found"]): break
    p+=1
print("enumerated",len(rows))
members=collections.defaultdict(list)
for x in rows:
    k=gk(x["idno"])
    if k in TARGETS: members[k].append(x)
def excel_url(id_):
    j=C.get(f"https://censusindia.gov.in/nada/index.php/metadata/export/{id_}/json").json()
    for res in j["resources"]:
        fn=res["filename"]
        if fn.lower().split("?")[0].endswith((".xlsx",".xls")): return fn
    return None
TC={"PC01_A01":("2001","A-01"),"PC01_A02":("2001","A-02"),"PC11_A01":("2011","A-01"),
    "PC11_A02":("2011","A-02"),"PC11_A11":("2011","A-11")}
out={}
for k in sorted(TARGETS):
    ms=sorted(members[k], key=lambda x:x["idno"])
    urls=[]
    for m in ms:
        u=excel_url(m["id"])
        if u: urls.append(u)
    y,tc=TC[k]
    out[k]={"census_year":y,"table_code":tc,"title":ms[0]["title"] if ms else k,"urls":urls}
    print(k,"members",len(ms),"excel_urls",len(urls))
# write constants.py
with open("src/constants.py","w") as f:
    f.write('"""Baked entity->member-file map for the Census of India connector.\n\n')
    f.write("Generated from the NADA catalog: each accepted census table (entity) maps to\n")
    f.write("the stable Excel download URLs of its per-geography member files. URLs carry\n")
    f.write("persistent resource ids. Data, not logic.\n\"\"\"\n\n")
    f.write("ENTITY_IDS = "+json.dumps(sorted(TARGETS))+"\n\n")
    f.write("ENTITY_FILES = "+json.dumps(out, indent=1, ensure_ascii=False)+"\n")
print("wrote src/constants.py")
