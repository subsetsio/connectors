import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import httpx
URL="https://www.bruegel.org/dataset/global-trade-tracker"
for label, ua in [("default-DI","DataIntegrations/1.0"), ("chrome","Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36")]:
    try:
        r=httpx.get(URL, headers={"User-Agent":ua,"Accept":"text/html","Accept-Language":"en-US,en;q=0.9"}, timeout=30, follow_redirects=True)
        print(label, r.status_code, "len", len(r.text), "| cf-mitigated:", r.headers.get("cf-mitigated"), "| server:", r.headers.get("server"))
    except Exception as e:
        print(label, "ERR", type(e).__name__, e)
# also test the static file URL directly
fr=httpx.get("https://www.bruegel.org/sites/default/files/2026-06/2026-06-16%20Global%20trade%20tracker.xlsx", headers={"User-Agent":"DataIntegrations/1.0"}, timeout=60, follow_redirects=True)
print("static-file default-UA:", fr.status_code, "bytes", len(fr.content))
