from subsets_utils import get
import csv, io, time
SPARQL = "https://statistics.gov.scot/sparql.csv"
def q(query, t=240):
    r = get(SPARQL, params={"query": query}, headers={"Accept":"text/csv"}, timeout=(10,t))
    return r.status_code, r.text
QB='PREFIX qb: <http://purl.org/linked-data/cube#>'

def keyset_page(ds, last, lim=50000):
    flt = f'FILTER(STR(?obs) > "{last}")' if last else ''
    qy=f'''{QB} SELECT ?obs WHERE {{ ?obs qb:dataSet <{ds}> . {flt} }} ORDER BY ?obs LIMIT {lim}'''
    return q(qy)

# keyset over births: page 1, page 2 deep-ish, measure
B='http://statistics.gov.scot/data/births'
last=None
total=0
t0=time.time()
for i in range(4):
    t=time.time(); st,txt=keyset_page(B,last)
    rows=[r["obs"] for r in csv.DictReader(io.StringIO(txt))]
    if not rows: break
    last=rows[-1]; total+=len(rows)
    print(f"page {i}: status={st} n={len(rows)} {time.time()-t:.1f}s last=...{last[-40:]}")
print("4 pages total", total, f"{time.time()-t0:.1f}s")

# keyset on the huge historical dataset - just time 2 pages
H='http://statistics.gov.scot/data/population-estimates-historical-geographic-boundaries'
t=time.time(); st,txt=keyset_page(H,None)
rows=[r["obs"] for r in csv.DictReader(io.StringIO(txt))]
print("hist page0:",st,len(rows),f"{time.time()-t:.1f}s")
mid=rows[-1]
t=time.time(); st,txt=keyset_page(H,mid)
print("hist page1:",st,txt.count(chr(10)),f"{time.time()-t:.1f}s")
