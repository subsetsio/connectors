import re
from subsets_utils import get
TOOL="https://www.cedefop.europa.eu/en/tools/skills-forecast"
HOST="https://www.cedefop.europa.eu/"
def slug(path):
    f=path.rsplit("/",1)[-1].replace(".json.gz","")
    return re.sub(r"^skills?-?20\d\d-?","",f).strip("-")
h=get(TOOL, timeout=(10,120)).text
folder=re.search(r'skillsForecastDataFolder"\s*:\s*"([^"]+)"',h).group(1).replace("\\/","/")
js=[m.group(1).replace("&amp;","&") for m in re.finditer(r'src="(/files/js/js_[^"]+)"',h)]
hay="".join(get(HOST+u,timeout=(10,120)).text for u in js)
paths=sorted(set(re.findall(r"/skills-20\d\d/[A-Za-z0-9_\-]+/[A-Za-z0-9_\-]+\.json\.gz",hay)))
iso=[]
for c,_ in re.findall(r'<option[^>]+value="([a-z]{2,4})"[^>]*>([^<]+)</option>',h):
    if c not in iso: iso.append(c)
print("folder",folder,"npaths",len(paths),"niso",len(iso))
# resolve country-occupations
ent="country-occupations"
tgt=[p for p in paths if slug(p)==ent]
eu=[p for p in paths if slug(p)==ent+"-eu"]
print("target",tgt,"eu",eu)
import json as J
arr=J.loads(get(HOST+folder+tgt[0],timeout=(10,120)).text)
rec=arr[0]
dims=[k for k in rec if not re.fullmatch(r'\d{4}',str(k))]
yrs=[k for k in rec if re.fullmatch(r'\d{4}',str(k))]
print("dims",dims,"nyears",len(yrs),"rows",len(arr),"sampleval",rec[yrs[0]],type(rec[yrs[0]]).__name__)
# templated
tp=sorted(set(re.findall(r'(/skills-20\d\d/[A-Za-z0-9_\-]+/[A-Za-z0-9_\-]+-)(?=")',hay)))
tp=[t for t in tp if not any(p.startswith(t) for p in paths)]
print("templ",tp)
so=J.loads(get(HOST+folder+tp[0]+iso[0]+".json.gz",timeout=(10,120)).text)
print("sector-occ iso",iso[0],"rows",len(so),"cols",list(so[0].keys())[:4])
