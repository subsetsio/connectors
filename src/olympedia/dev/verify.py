import sys, re, time
sys.path.insert(0, "src")
import lxml.html as LH
from nodes import olympedia as M

def head(label, rows, n=3):
    print("=" * 60); print(label, "n=", len(rows))
    for r in rows[:n]:
        print("  ", r)

# editions (single fetch, parse)
eds = M._parse_editions(M._doc("/editions"))
head("editions", eds)
print("  categories:", sorted(set(e["category"] for e in eds)))
print("  seasons:", sorted(set(str(e["season"]) for e in eds)))
print("  total editions to scrape for medal table:", len(eds))
time.sleep(3)

# countries via direct parse logic
doc = M._doc("/countries"); tables = doc.xpath("//table")
crows = []
for section, tbl in zip(("modern","ancient"), tables[:2]):
    for tr in tbl.xpath(".//tr"):
        tds = tr.xpath("./td")
        if len(tds) < 2: continue
        code=(tds[0].text_content() or "").strip(); country=(tds[1].text_content() or "").strip()
        if not code or not country: continue
        glyph = LH.tostring(tds[2], encoding="unicode") if len(tds)>=3 else ""
        crows.append({"noc_code":code,"country":country,"competed_modern":"glyphicon-ok" in glyph,"section":section})
head("countries", crows)
print("  competed_modern true count:", sum(1 for r in crows if r["competed_modern"]))
time.sleep(3)

head("medals_by_athlete", M._simple_stat_rows("/statistics/medal/athlete",
    [("athlete",0),("noc_code",1),("gold",2),("silver",3),("bronze",4),("total",5)]))
time.sleep(3)

# medals_by_country (uses _noc_from_row + _ints_in_row)
doc = M._doc("/statistics/medal/country"); tbl = doc.xpath("//table")[0]
mc=[]
for tr in tbl.xpath(".//tr"):
    tds=tr.xpath("./td")
    if len(tds)<5: continue
    code,name=M._noc_from_row(tr); nums=M._ints_in_row(tds)
    if not code or len(nums)<4: continue
    g,s,b,t=nums[-4:]; mc.append({"noc_code":code,"country":name,"gold":g,"silver":s,"bronze":b,"total":t})
head("medals_by_country", mc)
time.sleep(3)

# one edition medal table
doc = M._doc("/editions/63"); tbl=M._find_medal_table(doc)
print("=== edition 63 medal table found:", tbl is not None)
mrows=[]
for tr in tbl.xpath(".//tr"):
    tds=tr.xpath("./td")
    if len(tds)<5: continue
    code,name=M._noc_from_row(tr); nums=M._ints_in_row(tds)
    if not code or len(nums)<4: continue
    g,s,b,t=nums[-4:]; mrows.append({"noc":code,"name":name,"g":g,"s":s,"b":b,"t":t})
head("edition63 medal rows", mrows)
time.sleep(3)

# records
index=M._doc("/records"); disc={}
for a in index.xpath('//a[contains(@href,"/records/sport/")]'):
    m=re.search(r"/records/sport/([A-Za-z0-9]+)$", a.get("href") or "")
    if m: disc[m.group(1)]=(a.text_content() or "").strip()
print("=== record disciplines:", disc)
time.sleep(3)
doc=M._doc("/records/sport/ARC"); t0=doc.xpath("//table")[0]
rr=[]
for tr in t0.xpath(".//tr"):
    tds=tr.xpath("./td")
    if len(tds)<8: continue
    rr.append({"event":(tds[0].text_content() or '').strip()[:30],"rec":(tds[1].text_content() or '').strip(),"noc":(tds[3].text_content() or '').strip(),"rank":(tds[7].text_content() or '').strip()})
head("ARC records (table0)", rr)
