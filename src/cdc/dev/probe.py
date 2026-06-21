import subsets_utils as su
import httpx

ids = ["24w5-nppr", "2den-c3u2", "29hc-w46k"]
for did in ids:
    url = f"https://data.cdc.gov/api/views/{did}/rows.csv?accessType=DOWNLOAD"
    try:
        # stream to get headers + first chunk only
        r = su.get(url, timeout=(10,120))
        cl = r.headers.get("Content-Length")
        ct = r.headers.get("Content-Type")
        cd = r.headers.get("Content-Disposition")
        body = r.content
        print(did, "status", r.status_code, "CT", ct, "len_bytes", len(body), "CL", cl)
        head = body[:300].decode("utf-8","replace")
        print("  head:", head.replace("\n","\\n")[:280])
        print("  nlines~", body.count(b"\n"))
    except Exception as e:
        print(did, "ERR", type(e).__name__, e)
