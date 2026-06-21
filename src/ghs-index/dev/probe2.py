import csv, io, re
from subsets_utils import get
URL = "https://www.ghsindex.org/wp-content/uploads/2022/04/2021-GHS-Index-April-2022.csv"
text = get(URL, timeout=(10.0,120.0)).content.decode("utf-8-sig")
header = next(csv.reader(io.StringIO(text)))
def parse_code(h):
    if h.strip().upper()=="OVERALL SCORE": return "OVERALL","Overall score"
    if ")" in h:
        c,l=h.split(")",1); return c.strip(), l.strip()
    return h.strip(),h.strip()
codes=[parse_code(h)[0] for h in header[2:]]
from collections import Counter
print("n score cols:", len(codes), "unique:", len(set(codes)))
print("dupes:", {k:v for k,v in Counter(codes).items() if v>1})
def level(code):
    if code=="OVERALL": return "overall"
    if re.fullmatch(r"\d+", code): return "category"
    if re.fullmatch(r"\d+\.\d+", code): return "indicator"
    if re.fullmatch(r"\d+\.\d+\.\d+", code): return "subindicator"
    if re.fullmatch(r"\d+\.\d+\.\d+[a-z]+", code): return "question"
    return "other"
print("levels:", Counter(level(c) for c in codes))
print("other:", [c for c in codes if level(c)=="other"][:10])
