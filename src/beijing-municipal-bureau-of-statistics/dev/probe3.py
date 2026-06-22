import subsets_utils as su
B = "https://hgk.tjj.beijing.gov.cn/ww/"
def t(method, path, **kw):
    u=B+path
    f = su.post if method=="POST" else su.get
    try:
        r=f(u, timeout=(10,30), **kw)
        print(method, path, r.status_code, r.headers.get("content-type"), "len", len(r.text))
        print(repr(r.text[:600]))
    except Exception as e:
        print(method, path, "ERR", type(e).__name__, e)
    print()

t("GET","MenuItemAction!queryMenu")
t("POST","QueryReportAction!queryDataSortType")
t("POST","SubjectReportAction!queryLevelOneSubjectList", data={"dataSortType":"01"})
