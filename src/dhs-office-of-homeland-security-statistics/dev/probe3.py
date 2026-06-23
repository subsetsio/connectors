from subsets_utils import get
UA="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
url="https://ohss.dhs.gov/topics/immigration/yearbook"
r=get(url, timeout=(10,60), headers={
    "User-Agent":UA,
    "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language":"en-US,en;q=0.9",
    "Accept-Encoding":"gzip, deflate, br",
    "Sec-Fetch-Dest":"document","Sec-Fetch-Mode":"navigate","Sec-Fetch-Site":"none",
    "Upgrade-Insecure-Requests":"1","Connection":"keep-alive",
})
print("status", r.status_code)
print("resp headers:")
for k,v in r.headers.items(): print("  ",k,":",v[:80])
print("body[:600]:")
print(r.text[:600])
