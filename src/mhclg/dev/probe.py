from subsets_utils import get
import json

def content(base_path):
    r = get(f"https://www.gov.uk/api/content/{base_path}", timeout=(10,120))
    r.raise_for_status()
    return r.json()

for bp in [
    "government/statistical-data-sets/live-tables-on-homelessness",
    "government/statistical-data-sets/local-authority-housing-statistics-open-data",
    "government/statistics/english-indices-of-deprivation-2025",
]:
    print("="*80); print(bp)
    try:
        d = content(bp)
    except Exception as e:
        print("ERR", type(e).__name__, e); continue
    det = d.get("details", {})
    atts = det.get("attachments", [])
    print("document_type:", d.get("document_type"), " attachments:", len(atts))
    from collections import Counter
    print("content_types:", Counter(a.get("content_type") for a in atts))
    for a in atts[:6]:
        print("  -", a.get("content_type"), "|", a.get("filename"), "|", a.get("title","")[:60])
