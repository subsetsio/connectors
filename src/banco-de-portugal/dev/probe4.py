from subsets_utils import get
# fetch docs page raw to find spec/endpoint patterns
r=get("https://bpstat.bportugal.pt/data/docs", timeout=(10,60))
t=r.text
print("len",len(t))
import re
# find script srcs and any /data/ url patterns
for m in set(re.findall(r'(?:src|href)="([^"]+)"', t)):
    print("ASSET:",m)
print("---spec hints---")
for m in set(re.findall(r'(openapi[^"\']*|swagger[^"\']*|spec[^"\']*\.json|/data/v1/[a-z_{}/]+)', t)):
    print(m)
