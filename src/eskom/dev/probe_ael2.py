import re
from subsets_utils import get
html = get("https://www.eskom.co.za/dataportal/emissions/ael/", timeout=(10,60)).text
for pat in [r'data-[a-z-]*src="[^"]+"', r'iframe', r'<table', r'wpDataTable|tablepress|wp-block-table', r'https?://[^"\' ]+\.(?:csv|xlsx|json)', r'embed', r'\.pbix|powerbi']:
    m = re.findall(pat, html, re.I)
    print(repr(pat), "->", list(dict.fromkeys(m))[:5], "count", len(m))
# show a chunk around 'AEL' / 'emission'
i = html.lower().find('atmospheric')
print("--- around 'atmospheric' ---")
print(re.sub(r'\s+',' ', html[i-200:i+600]) if i>=0 else "not found")
