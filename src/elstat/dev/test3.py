import re, io, json, collections
from subsets_utils import get
import pandas as pd

# 1) Test Range request for cheap classification
url="https://www.statistics.gr/en/statistics?p_p_id=documents_WAR_publicationsportlet_INSTANCE_Mr0GiQJSgPHd&p_p_lifecycle=2&p_p_cacheability=cacheLevelPage&_documents_WAR_publicationsportlet_INSTANCE_Mr0GiQJSgPHd_javax.faces.resource=document&_documents_WAR_publicationsportlet_INSTANCE_Mr0GiQJSgPHd_ln=downloadResources&_documents_WAR_publicationsportlet_INSTANCE_Mr0GiQJSgPHd_documentID=225240&_documents_WAR_publicationsportlet_INSTANCE_Mr0GiQJSgPHd_locale=en"
r = get(url, headers={"Range":"bytes=0-0"}, timeout=(10,30))
print("Range GET status:", r.status_code, "len(body):", len(r.content),
      "| cd:", r.headers.get("content-disposition"), "| ct:", r.headers.get("content-type"))

# 2) language suffix distribution from the doc_map
dm = json.load(open("dev/doc_map.json"))
langs = collections.Counter()
for c,docs in dm.items():
    if not docs: continue
    for ct,fn in docs:
        if ct in ("application/vnd.openxmlformats-officedocument.spreadsheetml.sheet","application/vnd.ms-excel"):
            m = re.search(r'_([A-Za-z?]{2})\.xl', fn)
            langs[m.group(1) if m else "none"]+=1
print("Excel filename language suffixes:", dict(langs))

# 3) Parse an .xls TS (SEL15 docID 115314) and a non-TS xlsx (SHE06)
def docurl(inst, did):
    return (f"https://www.statistics.gr/en/statistics?p_p_id=documents_WAR_publicationsportlet_INSTANCE_{inst}"
            f"&p_p_lifecycle=2&p_p_cacheability=cacheLevelPage"
            f"&_documents_WAR_publicationsportlet_INSTANCE_{inst}_javax.faces.resource=document"
            f"&_documents_WAR_publicationsportlet_INSTANCE_{inst}_ln=downloadResources"
            f"&_documents_WAR_publicationsportlet_INSTANCE_{inst}_documentID={did}"
            f"&_documents_WAR_publicationsportlet_INSTANCE_{inst}_locale=en")

r2 = get(docurl("Mr0GiQJSgPHd","115314"), timeout=(10,90))
print("\nSEL15 .xls fn:", r2.headers.get("content-disposition"))
xls = pd.read_excel(io.BytesIO(r2.content), header=None, dtype=str, sheet_name=None)
for sh, df in xls.items():
    print(f"  sheet {sh!r} shape={df.shape}")
    print(df.head(12).fillna("").to_string(max_colwidth=16))
    break
