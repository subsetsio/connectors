import httpx
body = {"query": [], "response": {"format": "json-stat2"}}
tests = [
  ("POST", "https://pxweb.nso.gov.vn/pxweb/api/v1/en/Industry/E07.09.px"),
  ("POST", "https://pxweb.nso.gov.vn/PXWeb/api/v1/en/Industry/E07.09.px"),
  ("POST", "https://pxweb.nso.gov.vn/api/v1/en/Industry/E07.09.px."),
  ("GET",  "https://pxweb.nso.gov.vn/api/v1/en/Industry/E07.09.px."),
]
with httpx.Client(timeout=30, follow_redirects=False) as c:
    for m, u in tests:
        try:
            r = c.request(m, u, json=body if m=="POST" else None)
            loc = r.headers.get("location","")
            print(f"{m} {u[28:]:45} -> {r.status_code} {r.headers.get('content-type','')[:20]} loc={loc[:80]}")
        except Exception as e:
            print(f"{m} {u[28:]:45} -> ERR {e}")
    # follow the .px. redirect
    r = c.post("https://pxweb.nso.gov.vn/api/v1/en/Industry/E07.09.px.", json=body)
    print("redirect target:", r.headers.get("location"))
