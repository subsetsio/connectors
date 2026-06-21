import re, subsets_utils as su
UA = "subsets.io data connector (contact: nathansnellaert@gmail.com)"
su.configure_http(headers={"User-Agent": UA})
r = su.get("https://download.bls.gov/pub/time.series/ce/", timeout=(10,60))
# parse listing: size + href
rows = re.findall(r'(\d+)\s+<A HREF="([^"]+)">', r.text)
data = [(int(sz), href) for sz,href in rows if re.search(r'/ce\.data\.', href)]
data.sort(reverse=True)
print("num data files:", len(data))
for sz,h in data[:5]: print(f"{sz/1e6:8.1f}MB {h}")
print("total MB:", sum(s for s,_ in data)/1e6)
# also check a value that may be non-numeric: scan small survey for '-'
r2 = su.get("https://download.bls.gov/pub/time.series/jt/jt.data.1.AllItems", timeout=(10,120))
import collections
vals=[l.split('\t')[3].strip() for l in r2.text.split('\n')[1:5000] if l.count('\t')>=4]
nonnum=[v for v in vals if not re.match(r'^-?\d+\.?\d*$', v)]
print("sample nonnumeric values:", collections.Counter(nonnum).most_common(5))
