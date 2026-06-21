import html, json
import subsets_utils as su

BASE="https://data.rbi.org.in/CIMS_Gateway_DBIE/GATEWAY/SERVICES"
H={"Content-Type":"application/json","datatype":"application/json","channelkey":"key1","Origin":"https://data.rbi.org.in","Referer":"https://data.rbi.org.in/DBIE/"}

# 1. prime cookie
r0=su.get("https://data.rbi.org.in/DBIE/", timeout=(10,60))
print("prime status", r0.status_code, "set-cookie?", "TS01" in r0.headers.get("set-cookie",""))
# 2. session token
r1=su.post(f"{BASE}/security_generateSessionToken", headers=H, content=b'{"body":{}}', timeout=(10,60))
print("token status", r1.status_code, "auth hdr:", r1.headers.get("authorization"))
sid=r1.headers.get("authorization")
hd=dict(H); hd["authorization"]=sid
# 3. fx reserves (does cookie persist automatically?)
body=json.dumps({"body":{"currencyCode":"USD","reserveCode":"FCA","fromDate":"2024-01-01 00:00:00","toDate":"2026-06-18 00:00:00","frequency":"Weekly"}})
r2=su.post(f"{BASE}/dbie_foreignExchangeReserves", headers=hd, content=body.encode(), timeout=(10,120))
j=json.loads(html.unescape(r2.text).encode('utf-8','replace').decode())
print("fx status:", j["header"].get("status"))
rl=j.get("body",{}).get("resultList",[])
print("fx rows:", len(rl))
if rl: print("fx sample:", json.dumps(rl[0],ensure_ascii=False)[:300])
# 4. policy rates
r3=su.post(f"{BASE}/dbie_getPublicationDataImpala", headers=hd, content=b'{"body":{}}', timeout=(10,60))
j3=json.loads(html.unescape(r3.text).encode('utf-8','replace').decode())
print("rates status:", j3["header"].get("status"))
res=j3.get("body",{}).get("result",[])
print("rates rows:", len(res))
if res: print("rates sample:", json.dumps(res[:3],ensure_ascii=False)[:400])
