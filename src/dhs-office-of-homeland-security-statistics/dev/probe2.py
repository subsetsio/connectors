from subsets_utils import get, configure_http
UA="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
url="https://ohss.dhs.gov/topics/immigration/yearbook"
xlsx="https://ohss.dhs.gov/sites/default/files/2024-10/24-1011_ohss_immigration-enforcement-and-legal-processes-tables-june-2024_2.xlsx"

def trial(name, **kw):
    for u in (url, xlsx):
        try:
            r=get(u, timeout=(10,60), **kw)
            print(name, u.split("/")[-1][:30], r.status_code, len(r.content))
        except Exception as e:
            print(name, u.split("/")[-1][:30], "ERR", type(e).__name__)

trial("default")
trial("ua_only", headers={"User-Agent":UA})
trial("full", headers={
    "User-Agent":UA,
    "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language":"en-US,en;q=0.9",
})
