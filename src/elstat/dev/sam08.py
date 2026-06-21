from subsets_utils import get
for url in ["https://www.statistics.gr/en/statistics/-/publication/SAM08/-",
            "https://www.statistics.gr/el/statistics/-/publication/SAM08/-"]:
    r=get(url,timeout=(10,60))
    html=r.text
    print(url)
    print("  status", r.status_code, "len", len(html), "final_url", str(r.url))
    print("  has documentID:", "documentID=" in html, "| has 'publication':", "/publication/" in html)
    # title
    import re
    t=re.search(r'<title>([^<]*)</title>',html)
    print("  title:", t.group(1) if t else None)
