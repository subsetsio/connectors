import subsets_utils as su

# Try the base domain and a few path variants
urls = [
  "https://hgk.tjj.beijing.gov.cn/",
  "https://hgk.tjj.beijing.gov.cn/query/queryres/queryreport/QueryReportAction!queryDataSortType",
  "https://hgk.tjj.beijing.gov.cn/query/queryReport/queryReportAction?method=queryDataSortType",
]
for u in urls:
    try:
        r = su.get(u, timeout=(10,30))
        print("GET", u, r.status_code, r.headers.get("content-type"), "len", len(r.text))
        print(r.text[:300].replace("\n"," "))
    except Exception as e:
        print("GET", u, "ERR", type(e).__name__, e)
    print()
