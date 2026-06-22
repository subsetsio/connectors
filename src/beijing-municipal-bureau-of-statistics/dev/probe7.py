import subsets_utils as su
def t(method, u, **kw):
    f = su.post if method=="POST" else su.get
    try:
        r=f(u, timeout=(10,30), **kw)
        print(method, u.split('gov.cn')[1], r.status_code, r.headers.get("content-type"), "len", len(r.text))
        print("  ", repr(r.text[:250]))
    except Exception as e:
        print(method, u, "ERR", type(e).__name__, e)

H="https://hgk.tjj.beijing.gov.cn"
for ns in ["/query/","/query/queryReport/","/query/queryres/queryreport/"]:
    t("POST", H+ns+"QueryReportAction!queryDataSortType")
print("--- report viewer (seeds session) ---")
t("GET", H+"/query/queryReport/queryReportAction?method=queryHtmlStyle&queryCondition.reportNumber=60Y-1-03-N&queryCondition.objectType=04&queryCondition.objectCode=0100&yhid=guest&netType=2")
