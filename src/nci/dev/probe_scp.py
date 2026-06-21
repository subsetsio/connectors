import re
from subsets_utils import get
# raw incidence CSV (state level, all states)
url="https://statecancerprofiles.cancer.gov/incidencerates/index.php"
p=dict(stateFIPS="00",areatype="state",cancer="001",stage="999",race="00",sex="0",age="001",year="0",type="incd",sortVariableName="rate",sortOrder="desc",output="1")
r=get(url, params=p, timeout=(10,120)); r.raise_for_status()
txt=r.text
print("=== INCIDENCE CSV (first 1400 chars) ===")
print(txt[:1400])
print("\n=== last 600 chars (footnotes) ===")
print(txt[-600:])
print("\n=== total lines:", txt.count(chr(10)))
# discover cancer codes from the incidence options page
r2=get("https://statecancerprofiles.cancer.gov/incidencerates/", timeout=(10,120))
html=r2.text
# look for cancer select options
m=re.search(r'(?is)<select[^>]*name=["\']?cancer["\']?.*?</select>', html)
print("\n=== cancer select found:", bool(m))
if m:
    opts=re.findall(r'<option[^>]*value=["\']?([0-9]+)["\']?[^>]*>(.*?)</option>', m.group(0))
    print("n cancer options:", len(opts))
    for v,l in opts[:40]: print(f"  {v}  {re.sub('<[^>]+>','',l).strip()}")
