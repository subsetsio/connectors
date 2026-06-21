import re, subsets_utils as su
UA = "subsets.io data connector (contact: nathansnellaert@gmail.com)"
su.configure_http(headers={"User-Agent": UA})
for s in ["cm","kv","nb","nd","mp","ws","wm","su","or"]:
    try:
        r = su.get(f"https://download.bls.gov/pub/time.series/{s}/", timeout=(10,60))
        files = re.findall(r'<A HREF="[^"]*/('+s+r'\.data\.[^"]+)">', r.text)
        print(f"{s}: status={r.status_code} ndata={len(files)} sample={files[:2]}")
    except Exception as e:
        print(s, "ERR", type(e).__name__, e)
