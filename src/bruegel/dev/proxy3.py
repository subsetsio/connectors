import httpx, urllib.parse
page="https://www.bruegel.org/dataset/global-trade-tracker"
xlsx="https://www.bruegel.org/sites/default/files/2026-06/2026-06-16%20Global%20trade%20tracker.xlsx"
zipurl="https://www.bruegel.org/sites/default/files/2026-06/REER_database_ver14Jun2026.zip"
def t(name,url,want_html=False):
    try:
        r=httpx.get(url,timeout=120,follow_redirects=True)
        sig = r.text[:70].replace("\n"," ") if want_html else f"bytes={len(r.content)} magic={r.content[:4]!r}"
        print(f"{name}: {r.status_code} {sig}")
    except Exception as e:
        print(f"{name}: ERR {type(e).__name__}: {str(e)[:80]}")
q=lambda u: urllib.parse.quote(u,safe='')
# codetabs wants the raw url (already-encoded) as quest; encode the whole thing once
t("codetabs-page", "https://api.codetabs.com/v1/proxy/?quest="+q(page), True)
t("codetabs-xlsx", "https://api.codetabs.com/v1/proxy/?quest="+q(xlsx))
t("codetabs-zip",  "https://api.codetabs.com/v1/proxy/?quest="+q(zipurl))
# allorigins retry (may be transient 522)
t("allorigins-xlsx","https://api.allorigins.win/raw?url="+q(xlsx))
