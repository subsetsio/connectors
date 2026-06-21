import re, json
from subsets_utils import get
UA=("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36")
SHARE="https://airtable.com/appzVzSeINK1S3EVR/shroOenW19l1m3w0H/tblxearKzw8W7ViN8"
H={"User-Agent":UA,"x-airtable-application-id":"appzVzSeINK1S3EVR","x-airtable-inter-service-client":"webClient","x-requested-with":"XMLHttpRequest","x-time-zone":"America/New_York","x-user-locale":"en","Accept":"application/json"}
html=get(SHARE,headers={"User-Agent":UA},timeout=60).text
url="https://airtable.com"+re.search(r'urlWithParams:\s*"([^"]+)"',html).group(1).encode().decode("unicode_escape")
t=get(url,headers=H,timeout=180).json()["data"]["table"]
for c in t["columns"]:
    if c["type"] in ("select","multiSelect"):
        print("===",c["name"],"type=",c["type"])
        print("  keys:",list(c.keys()))
        to=c.get("typeOptions") or {}
        print("  typeOptions keys:",list(to.keys()))
        ch=to.get("choices") or to.get("choiceOrder")
        print("  choices sample:",json.dumps(ch)[:300] if ch else to)
        break
# dump full column object for one select to see exact path
for c in t["columns"]:
    if c["name"]=="race":
        print("\nFULL race column:", json.dumps(c)[:800])
        break
