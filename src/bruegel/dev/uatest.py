import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import subsets_utils as su
# 1) per-request header override
r = su.get("https://httpbin.org/headers", headers={"User-Agent":"CHROME-OVERRIDE","Accept":"text/html"}, timeout=30)
print("per-request override -> sent UA:", r.json()["headers"].get("User-Agent"))
# 2) configure_http then plain get
su.configure_http(headers={"User-Agent":"CONFIGURED-UA","Accept":"text/html"})
r2 = su.get("https://httpbin.org/headers", timeout=30)
print("configure_http     -> sent UA:", r2.json()["headers"].get("User-Agent"))
