import requests
URL = "https://clinicaltrials.gov/api/v2/studies"
P = {"pageSize": 1, "fields": "NCTId"}

# requests normally sends Title-Case header names -> 200. Force lowercase wire names.
s = requests.Session()
# requests preserves the case you give it for custom headers; clear defaults and set lowercase
s.headers.clear()
s.headers.update({
    "user-agent": "python-httpx/0.28.1",
    "accept": "*/*",
    "accept-encoding": "gzip, deflate",
    "connection": "keep-alive",
})
r = s.get(URL, params=P, timeout=30)
print("requests LOWERCASE headers ->", r.status_code)

# control: Title-Case
s2 = requests.Session()
r2 = s2.get(URL, params=P, timeout=30)
print("requests default Title-Case ->", r2.status_code)
