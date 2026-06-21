import httpx
body = {"query": [], "response": {"format": "json-stat2"}}
# The PxWeb v1 API on this build: GET .px = metadata. Test alternate data routes.
tests = [
 ("POST","https://pxweb.nso.gov.vn/api/v1/en/Industry/E07.09.px",{"q":body}),
 # method override header
 ("GET","https://pxweb.nso.gov.vn/api/v1/en/Industry/E07.09.px",{"h":{"X-HTTP-Method-Override":"POST"},"q":None}),
 # PUT
 ("PUT","https://pxweb.nso.gov.vn/api/v1/en/Industry/E07.09.px",{"q":body}),
 # px source file likely static under PXWeb resources
 ("GET","https://pxweb.nso.gov.vn/Resources/PX/Databases/Industry/E07.09.px",{"q":None}),
 ("GET","https://pxweb.nso.gov.vn/PXWeb/Resources/PX/Databases/Industry/E07.09.px",{"q":None}),
]
with httpx.Client(timeout=30, follow_redirects=False) as c:
    for m,u,opt in tests:
        try:
            r = c.request(m,u,json=opt.get("q") if m in ("POST","PUT") else None, headers=opt.get("h"))
            print(f"{m:5} {u[28:]:55} -> {r.status_code} {r.headers.get('content-type','')[:22]} {r.headers.get('location','')[:40]}")
        except Exception as e:
            print(f"{m:5} {u[28:]:55} -> ERR {type(e).__name__}")
