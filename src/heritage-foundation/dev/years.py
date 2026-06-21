from subsets_utils import get
AZURE = "https://indexdotnet.azurewebsites.net/index/excel/{y}/index{y}_data.xls"
STATIC = "https://static.heritage.org/index/data/{y}/{y}_indexofeconomicfreedom_data.xlsx"
def ok(url):
    try:
        r = get(url, timeout=(8,60))
    except Exception as e:
        return None
    ct = r.headers.get("content-type","").lower()
    return r.status_code == 200 and "html" not in ct
found = []
for y in range(2009, 2029):
    src = "static" if ok(STATIC.format(y=y)) else ("azure" if ok(AZURE.format(y=y)) else None)
    if src: found.append((y, src))
print("editions found:", len(found))
print([f"{y}:{s}" for y,s in found])
