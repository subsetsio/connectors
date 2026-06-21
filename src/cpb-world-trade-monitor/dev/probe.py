"""Probe: download latest WTM xlsx via subsets_utils.get, parse with stdlib."""
import datetime, io, re, zipfile
import xml.etree.ElementTree as ET
from subsets_utils import get

MONTHS = ["january","february","march","april","may","june","july","august",
          "september","october","november","december"]
TMPL = "https://www.cpb.nl/system/files/cpbmedia/cpb-world-trade-monitor-{m}-{y}.xlsx"
M = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"
R = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"

def fetch():
    today = datetime.date.today(); y, m = today.year, today.month
    for _ in range(10):
        url = TMPL.format(m=MONTHS[m-1], y=y)
        try:
            r = get(url, timeout=(10.0,120.0))
            if r.status_code == 200 and r.content[:2] == b"PK":
                print("HIT", url, len(r.content)); return r.content
        except Exception as e:
            print("miss", url, type(e).__name__)
        m -= 1
        if m == 0: m, y = 12, y-1
    raise RuntimeError("not found")

def shared(zf):
    root = ET.fromstring(zf.read("xl/sharedStrings.xml"))
    return ["".join(t.text or "" for t in si.iter(f"{{{M}}}t")) for si in root.findall(f"{{{M}}}si")]

def rows(zf, path, ss):
    root = ET.fromstring(zf.read(path)); out=[]
    for row in root.iterfind(f".//{{{M}}}sheetData/{{{M}}}row"):
        cells={}
        for c in row.findall(f"{{{M}}}c"):
            ref=c.get("r",""); col="".join(ch for ch in ref if ch.isalpha())
            t=c.get("t"); v=c.find(f"{{{M}}}v")
            if v is None or v.text is None: continue
            if t=="s": val=ss[int(v.text)]
            elif t=="str": val=v.text
            else:
                try: val=float(v.text)
                except ValueError: val=v.text
            cells[col]=val
        out.append(cells)
    return out

CODE=re.compile(r"^[a-z]{3}_[a-z0-9]{2}_[a-z]{4}_[a-z]{2}$")

data=fetch()
zf=zipfile.ZipFile(io.BytesIO(data)); ss=shared(zf)
wb=ET.fromstring(zf.read("xl/workbook.xml"))
rels=ET.fromstring(zf.read("xl/_rels/workbook.xml.rels"))
rid={r.get("Id"):r.get("Target") for r in rels}
sheets={}
for sh in wb.iterfind(f".//{{{M}}}sheets/{{{M}}}sheet"):
    tgt=rid[sh.get(f"{{{R}}}id")]
    tgt = tgt.lstrip("/") if tgt.startswith("/") else "xl/"+tgt.lstrip("/")
    sheets[sh.get("name")]=tgt
print("SHEETS", sheets)

total_series=0; total_vals=0
for name,path in sheets.items():
    rr=rows(zf,path,ss)
    # period header row
    pcols={}
    for row in rr:
        cand={c:v for c,v in row.items() if isinstance(v,str) and re.match(r"^\d{4}m\d{2}$",v)}
        if len(cand)>len(pcols): pcols=cand
    print(name,"periods",len(pcols), sorted(pcols.values())[:2], sorted(pcols.values())[-2:])
    for row in rr:
        code=row.get("C")
        if not isinstance(code,str) or not CODE.match(code): continue
        total_series+=1
        for col,per in pcols.items():
            if col in row and isinstance(row[col],float):
                total_vals+=1
    # show one sample series values
print("TOTAL series", total_series, "TOTAL value cells", total_vals)
