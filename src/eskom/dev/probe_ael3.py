import re
from subsets_utils import get
html = get("https://www.eskom.co.za/dataportal/emissions/ael/", timeout=(10,60)).text
for kw in ['iframe','Embed','embed']:
    for m in re.finditer(kw, html):
        i=m.start()
        seg=re.sub(r'\s+',' ', html[i-120:i+260])
        print(f"[{kw}@{i}] {seg}")
        print('-'*60)
        break  # first occurrence each
# look for any guid token (powerbi resourceKey style) or base64 view token anywhere
toks = re.findall(r'eyJ[A-Za-z0-9=_\-]{20,}', html)
print("base64 eyJ tokens:", toks[:3])
guids = re.findall(r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}', html)
print("guids:", list(dict.fromkeys(guids))[:6])
