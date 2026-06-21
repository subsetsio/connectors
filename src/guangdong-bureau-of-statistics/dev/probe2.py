import re
from subsets_utils import get
import xlrd

def load(url):
    r=get(url,timeout=(10,120)); return xlrd.open_workbook(file_contents=r.content).sheet_by_index(0)

def cell(sh,r,c):
    if r<0 or c<0 or r>=sh.nrows or c>=sh.ncols: return ""
    v=sh.cell_value(r,c)
    return v

def is_num(v): return isinstance(v,(int,float)) and not isinstance(v,bool)

def detect_header(sh):
    for r in range(min(sh.nrows,15)):
        nz=sum(1 for c in range(2,sh.ncols) if str(cell(sh,r,c)).strip()!="")
        if nz>=2: return r
    return None

def parse(url):
    sh=load(url)
    hr=detect_header(sh)
    hdr=[str(cell(sh,hr,c)).strip() for c in range(sh.ncols)] if hr is not None else []
    # normalize year-like floats
    def normh(x):
        try:
            f=float(x); 
            if f==int(f): return str(int(f))
        except: pass
        return x
    hdr=[normh(h) for h in hdr]
    rows=0; cells=0
    for r in range((hr or 0)+1, sh.nrows):
        rl=str(cell(sh,r,0)).strip()
        has_val=any(is_num(cell(sh,r,c)) for c in range(2,sh.ncols))
        if not (rl or has_val): continue
        if has_val: rows+=1
        for c in range(2,sh.ncols):
            v=cell(sh,r,c)
            if is_num(v): cells+=1
    print(f"{url.split('/')[-1]:16} dims {sh.nrows}x{sh.ncols} hdr_row={hr} headers={hdr[:8]} datarows~{rows} numcells~{cells}")

base="http://tjnj.gdstats.gov.cn:8080/tjnj/2025/directory"
for u in ["02/excel/02-15-0.xls","02/excel/02-15-1.xls","06/excel/06-08.xls","09/excel/09-01.xls","24/excel/24-A-01.xls","24/excel/24-D-02.xls","12/excel/12-26.xls"]:
    try: parse(f"{base}/{u}")
    except Exception as e: print(u,"ERR",type(e).__name__,e)
