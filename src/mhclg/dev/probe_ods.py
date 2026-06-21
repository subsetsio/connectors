import sys, os, io, zipfile, time, resource
sys.path.insert(0, os.path.abspath("src"))
from subsets_utils import get
from lxml import etree

NS_T="urn:oasis:names:tc:opendocument:xmlns:table:1.0"
NS_O="urn:oasis:names:tc:opendocument:xmlns:office:1.0"
NS_TX="urn:oasis:names:tc:opendocument:xmlns:text:1.0"
def q(ns,t): return "{%s}%s"%(ns,t)

def stream_ods(raw, max_rows_probe=None):
    zf=zipfile.ZipFile(io.BytesIO(raw))
    with zf.open("content.xml") as f:
        ctx=etree.iterparse(f, events=("end",), tag=q(NS_T,"table"))
        for _,table in ctx:
            name=table.get(q(NS_T,"name"))
            nrows=0
            for row in table.iterfind(q(NS_T,"table-row")):
                rep=int(row.get(q(NS_T,"number-rows-repeated") or "1") or "1")
                # build cell list
                cells=[]
                for cell in row.iterfind(q(NS_T,"table-cell")):
                    crep=int(cell.get(q(NS_T,"number-columns-repeated") or "1") or "1")
                    val=cell.get(q(NS_O,"value"))
                    if val is None:
                        ps=cell.findall(q(NS_TX,"p"))
                        txt="".join("".join(p.itertext()) for p in ps) if ps else ""
                    else:
                        txt=val
                    cells.extend([txt]*crep)
                # trim trailing empties
                while cells and cells[-1]=="" : cells.pop()
                for _ in range(rep):
                    nrows+=1
                    if cells:
                        yield (name,nrows,cells)
                row.clear()
            table.clear()
            print(f"   table {name!r}: rows~{nrows}")

bp="government/statistical-data-sets/fire-statistics-data-tables"
r=get(f"https://www.gov.uk/api/content/{bp}", timeout=(10,120)); r.raise_for_status()
att=next(a for a in r.json()["details"]["attachments"] if a.get("filename")=="dwelling-fires-dataset.ods")
print("downloading", att["filename"], att.get("file_size"),"bytes")
raw=get(att["url"], timeout=(10,300)).content
print("got", len(raw), "bytes")
t0=time.time(); total=0; sample=None
for name,ri,cells in stream_ods(raw):
    total+=1
    if sample is None: sample=(name,ri,cells[:8])
print("rows yielded:", total, "in %.1fs"%(time.time()-t0))
print("sample:", sample)
print("peak RSS MB:", resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1e6)
