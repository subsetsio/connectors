from subsets_utils import post, get
import json, urllib.parse

url = "https://pxweb.nso.gov.vn/api/v1/en/Industry/E07.09"
for q in ([], [{"code":"Year","selection":{"filter":"all","values":["*"]}}]):
    r = post(url, json={"query": q, "response": {"format": "json-stat2"}}, timeout=(10,120))
    body = r.json()
    print(f"query={q!r} -> status {r.status_code}, type {type(body).__name__}, head {str(body)[:200]}")
print()
# try WITH .px but maybe needs the select-all; recheck status via subsets_utils
r2 = post("https://pxweb.nso.gov.vn/api/v1/en/Industry/E07.09.px", json={"query":[],"response":{"format":"json-stat2"}}, timeout=(10,60))
print(".px empty:", r2.status_code, r2.headers.get("content-type"))
