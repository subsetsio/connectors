import sys, os, re
sys.path.insert(0, os.path.join(os.path.dirname(__file__),"..","src"))
from subsets_utils import get
r=get("https://www.bancentral.gov.do/Home/GetContentForRender",
      data="id=2536", headers={"Content-Type":"application/x-www-form-urlencoded","X-Requested-With":"XMLHttpRequest"},
      timeout=(10,60))
print("status",r.status_code,"len",len(r.text))
links=sorted(set(re.findall(r'https://cdn\.bancentral\.gov\.do/[^\"\'<> ]+\.(?:xls|xlsx)', r.text, re.I)))
bac=[l for l in links if 'diariasBAC' in l or 'diariasbac' in l.lower()]
print('total links',len(links),'BAC links',len(bac))
for l in bac[:6]: print('  ',l)
