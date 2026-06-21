from subsets_utils import get
base="http://tjnj.gdstats.gov.cn:8080/tjnj/2025/directory"
for u in ["06/excel/06-08.xls","06/html/06-08.htm","06/excel/06-07.xls","06/excel/06-09.xls"]:
    r=get(f"{base}/{u}",timeout=(10,60))
    head=r.content[:16]
    print(f"{u:22} status={r.status_code} bytes={len(r.content)} ctype={r.headers.get('content-type')} head={head}")
