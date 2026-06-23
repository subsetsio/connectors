import json
from subsets_utils import get

BASE = "https://www.federalregister.gov/api/v1"

# 1) agencies
r = get(BASE + "/agencies.json", timeout=(10, 120))
ag = r.json()
print("AGENCIES status", r.status_code, "count", len(ag))
print("agency[0] keys:", sorted(ag[0].keys()))
print("agency[0] sample:", {k: ag[0][k] for k in ("id","name","short_name","slug","parent_id","agency_url")})
print("null parent_id count:", sum(1 for a in ag if a.get("parent_id") is None))
print("ids non-null:", sum(1 for a in ag if a.get("id") is not None), "of", len(ag))

# 2) documents one year, one page, selected fields
fields = ["document_number","type","subtype","title","abstract","publication_date",
          "signing_date","citation","page_length","start_page","end_page","agencies",
          "html_url","pdf_url","raw_text_url","president"]
params = [("conditions[publication_date][year]","2024"),
          ("per_page","2"),("order","oldest")]
for f in fields:
    params.append(("fields[]", f))
r = get(BASE + "/documents.json", params=params, timeout=(10,120))
d = r.json()
print("\nDOCUMENTS status", r.status_code)
print("top keys:", sorted(d.keys()))
print("count:", d.get("count"), "total_pages:", d.get("total_pages"))
print("next_page_url:", d.get("next_page_url"))
res = d["results"]
print("result[0] keys:", sorted(res[0].keys()))
print(json.dumps(res[0], indent=2, default=str)[:2500])
