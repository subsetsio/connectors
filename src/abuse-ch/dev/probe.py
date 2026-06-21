import json, io, zipfile
from subsets_utils import get

def head(url, n=12, container="plain"):
    r = get(url, timeout=(10,120))
    print("==", url, r.status_code, "len", len(r.content))
    if container == "zip":
        zf = zipfile.ZipFile(io.BytesIO(r.content))
        m = zf.namelist()[0]
        print("  member:", m)
        data = zf.read(m).decode("utf-8","replace")
        for line in data.splitlines()[:n]:
            print("  ", line[:200])
    else:
        for line in r.text.splitlines()[:n]:
            print("  ", line[:200])

# feodo JSON
r = get("https://feodotracker.abuse.ch/downloads/ipblocklist.json", timeout=(10,120))
arr = json.loads(r.text)
print("== feodo json rows:", len(arr))
print("  keys:", sorted(arr[0].keys()))
print("  sample:", json.dumps(arr[0], indent=0)[:400])

head("https://sslbl.abuse.ch/blacklist/sslblacklist.csv", n=12)
head("https://urlhaus.abuse.ch/downloads/csv/", n=12, container="zip")
