import urllib.parse, httpx
page="https://www.bruegel.org/dataset/global-trade-tracker"
fileurl="https://www.bruegel.org/sites/default/files/2026-06/2026-06-16%20Global%20trade%20tracker.xlsx"
zipurl="https://www.bruegel.org/sites/default/files/2026-06/REER_database_ver14Jun2026.zip"
def t(name,url):
    try:
        r=httpx.get(url,timeout=90,follow_redirects=True)
        print(f"{name}: {r.status_code} bytes={len(r.content)}")
        return r
    except Exception as e:
        print(f"{name}: ERR {type(e).__name__}: {str(e)[:80]}")
# allorigins raw
t("allorigins-page", "https://api.allorigins.win/raw?url="+urllib.parse.quote(page,safe=''))
t("allorigins-file", "https://api.allorigins.win/raw?url="+urllib.parse.quote(fileurl,safe=''))
t("allorigins-zip5MB", "https://api.allorigins.win/raw?url="+urllib.parse.quote(zipurl,safe=''))
# corsproxy.io
t("corsproxy-page", "https://corsproxy.io/?url="+urllib.parse.quote(page,safe=''))
# jina reader (text only)
t("jina-page", "https://r.jina.ai/"+page)
