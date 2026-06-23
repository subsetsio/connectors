import requests
UA="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
try:
    r=requests.get("https://ohss.dhs.gov/topics/immigration/yearbook",headers={"User-Agent":UA},timeout=60)
    print("requests", r.status_code, len(r.content))
except Exception as e:
    print("requests ERR", type(e).__name__, str(e)[:80])
