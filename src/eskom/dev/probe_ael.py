import re
from subsets_utils import get
html = get("https://www.eskom.co.za/dataportal/emissions/ael/", timeout=(10,60)).text
print("len", len(html))
for pat in [r'app\.powerbi\.com/view\?r=[A-Za-z0-9=_\-]+', r'powerbi\.com[^"\' ]{0,80}', r'<iframe[^>]*src="[^"]+"', r'datawrapper|flourish|tableau|public\.tableau']:
    m = re.findall(pat, html, re.I)
    print(pat, "->", list(dict.fromkeys(m))[:4])
