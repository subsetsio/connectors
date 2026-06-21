import re
from subsets_utils import get
import httpx
# Test HEAD
url="https://www.statistics.gr/en/statistics?p_p_id=documents_WAR_publicationsportlet_INSTANCE_Mr0GiQJSgPHd&p_p_lifecycle=2&p_p_cacheability=cacheLevelPage&_documents_WAR_publicationsportlet_INSTANCE_Mr0GiQJSgPHd_javax.faces.resource=document&_documents_WAR_publicationsportlet_INSTANCE_Mr0GiQJSgPHd_ln=downloadResources&_documents_WAR_publicationsportlet_INSTANCE_Mr0GiQJSgPHd_documentID=225240&_documents_WAR_publicationsportlet_INSTANCE_Mr0GiQJSgPHd_locale=en"
try:
    r = httpx.head(url, follow_redirects=True, timeout=30)
    print("HEAD status", r.status_code)
    print("  content-type:", r.headers.get("content-type"))
    print("  content-disposition:", r.headers.get("content-disposition"))
    print("  content-length:", r.headers.get("content-length"))
except Exception as e:
    print("HEAD err", e)

# Look for portlet section headings in STO04 page (instance VBZOni0vs5VJ)
html = get("https://www.statistics.gr/en/statistics/-/publication/STO04/-", timeout=(10,60)).text
for inst in ["VBZOni0vs5VJ","0qObWqzRnXSG","qDQ8fBKKo4lN"]:
    # find portlet boundary text: search for the instance's portlet-title
    idx = html.find(f"INSTANCE_{inst}")
    # search backwards for a heading
    pre = html[max(0,idx-1500):idx]
    titles = re.findall(r'portlet-title-text[^>]*>([^<]+)<', pre)
    heads = re.findall(r'<h[1-6][^>]*>([^<]+)</h[1-6]>', pre)
    print(inst, "titles:", titles[-2:], "heads:", heads[-3:])
