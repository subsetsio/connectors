from subsets_utils import get
print(get("https://bpstat.bportugal.pt/api/static/drf-yasg/redoc-init.41348b1afc50.js", timeout=(10,60)).text[:500])
print("=====TRY SPEC URLS=====")
for u in ["https://bpstat.bportugal.pt/data/docs/?format=openapi",
          "https://bpstat.bportugal.pt/data/?format=openapi",
          "https://bpstat.bportugal.pt/data/swagger.json",
          "https://bpstat.bportugal.pt/data/swagger/?format=openapi"]:
    r=get(u, timeout=(10,60))
    print(u, r.status_code, r.headers.get("content-type"), len(r.content))
