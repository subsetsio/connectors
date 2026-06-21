import re
from subsets_utils import get
for code in ["SDT03","STO04","SPO18"]:
    html = get(f"https://www.statistics.gr/en/statistics/-/publication/{code}/-", timeout=(10,60)).text
    insts = re.findall(r'INSTANCE_([A-Za-z0-9]+)[^"]*?documentID=(\d+)', html)
    print(code, "len(html)=",len(html), "n_docs=",len(insts))
    seen=set()
    for inst,did in insts:
        if (inst,did) in seen: continue
        seen.add((inst,did))
        print("   ", inst, did)
