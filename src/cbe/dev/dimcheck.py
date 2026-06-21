import re, collections
from subsets_utils import get, configure_http
from parser import parse_workbook
configure_http(headers={"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36","Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8","Accept-Language":"en-US,en;q=0.9"})
BASE="https://www.cbe.org.eg"
def hrefs(g): 
    h=get(f"{BASE}/en/economic-research/time-series/downloadlist?category={g}",timeout=(10,120)).text
    return re.findall(r'href="(/-/media/project/cbe/listing/time-series/[^"]+?\.xlsx)"',h)
def tyr(fn):
    ys=[int(y) for y in re.findall(r'(?:19|20)\d{2}',fn)]; y0,y1=(ys[0],ys[-1]) if ys else (None,None)
    low=fn.lower(); ft="monthly" if "month" in low else "quarterly" if "quart" in low else "annual" if ("annual" in low or "year" in low) else None
    return ft,y0,y1
# GDP factor cost constant - check dimension
for ds,g in [("gdp-at-factor-cost-constant","DEF6421CA1354B128A1113D7A5BBFC66"),("cpi","706A9057F8454F7284BE8143070D88C4")]:
    fs=sorted(x for x in hrefs(g) if x.split('/')[-2]==ds)
    fn=fs[-1].split('/')[-1]; ft,y0,y1=tyr(fn)
    rows=parse_workbook(get(BASE+fs[-1],timeout=(10,120)).content,y0,y1,ft)
    dims=collections.Counter(r['dimension'] for r in rows)
    print(f"\n{ds}: {len(rows)} rows; dims={dict(dims)}")
    # uniqueness of (indicator,dimension,freq,date)
    keys=collections.Counter((r['indicator_en'],r['dimension'],r['frequency'],str(r['date'])) for r in rows)
    dup=sum(1 for k,v in keys.items() if v>1)
    print("  dup keys:",dup,"of",len(keys))
    for r in rows[:3]: print("   ",{k:r[k] for k in('indicator_en','dimension','date','value')})
