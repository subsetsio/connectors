import re, json
from subsets_utils import get, configure_http
from parser import parse_workbook
configure_http(headers={"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36","Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8","Accept-Language":"en-US,en;q=0.9"})
BASE="https://www.cbe.org.eg"
CATS={"099EFD590A274C8F9259740B4FE96AAD":"cbe","F016705643D24C51959577587914DA5C":"domestic-debt","2596CC0C64D5474C865C49E48A24D483":"external-debt","DEF6421CA1354B128A1113D7A5BBFC66":"gdp","909707CDAD5C47529817D6146659E054":"interest-rates","A6ACD7B25BE64045A90660B320ECFA32":"investments","623F34508AE148C1969795A8F78FDA49":"time-series","B928771A1D1A4550A1B08F9386DDC0FA":"tourism","F0324992E95741438C789A669E5194F4":"foreign-trade","3EB4667B01F04C41ADCF7D96039037A4":"stock","F9F37F0E98A54C3684790C4037AA4BE3":"banking-survey","232131B16F15454BB1E1933B2BFEB041":"bop","706A9057F8454F7284BE8143070D88C4":"inflation","97805EA8534C4134B65BDE9621E187AF":"state-budget"}
def hrefs(g):
    h=get(f"{BASE}/en/economic-research/time-series/downloadlist?category={g}",timeout=(10,120)).text
    return re.findall(r'href="(/-/media/project/cbe/listing/time-series/[^"]+?\.xlsx)"',h)
def tag_years(fn):
    ys=[int(y) for y in re.findall(r'(?:19|20)\d{2}',fn)]
    y0,y1=(ys[0],ys[-1]) if ys else (None,None)
    low=fn.lower()
    ft="monthly" if "month" in low else "quarterly" if "quart" in low else "annual" if ("annual" in low or "year" in low) else None
    return ft,y0,y1
bad=[]
for g,cs in CATS.items():
    by={}
    for h in hrefs(g): by.setdefault(h.split('/')[-2],[]).append(h)
    for ds,files in by.items():
        files.sort()
        # test latest 1 file
        h=files[-1]; fn=h.split('/')[-1]
        ft,y0,y1=tag_years(fn)
        try:
            content=get(BASE+h,timeout=(10,120)).content
            rows=parse_workbook(content,y0,y1,ft)
        except Exception as e:
            rows=[]; print("ERR",ds,e)
        nd=sum(1 for x in rows if x['date'])
        flag="" if rows else "  <<< EMPTY"
        print(f"{cs:14s} {ds[:42]:42s} files={len(files):3d} rows={len(rows):5d} dated={nd:5d}{flag}")
        if not rows: bad.append((cs,ds,fn))
print("\nEMPTY DATASETS:",len(bad))
for b in bad: print(" ",b)
