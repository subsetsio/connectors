import sys, os, json, time, random, collections
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from subsets_utils import get, post

BASE = "https://openstat.psa.gov.ph/PXWeb/api/v1/en/DB/"
ents = list(json.load(open("/Users/nathansnellaert/Documents/hardened/data/sources/philippine-statistics-authority/assets/collect/entities/current.json")).keys())
random.seed(7)
sample = random.sample(ents, 70)

import collections
calls = collections.deque()
def throttle():
    now=time.time()
    while calls and now-calls[0]>10: calls.popleft()
    if len(calls)>=8: time.sleep(max(10-(now-calls[0])+0.3,0))
    calls.append(time.time())

cellcounts=[]
reqs_total=0
for p in sample:
    throttle()
    try:
        meta = get(BASE+p, timeout=(10,60)).json()
    except Exception as e:
        print("ERR", p, e); continue
    cells=1
    for v in meta.get("variables",[]): cells*=len(v.get("values") or v.get("valueTexts") or [1])
    cellcounts.append((cells,p))
    reqs_total += -(-cells//1000)  # ceil chunks

cellcounts.sort()
import statistics
cs=[c for c,_ in cellcounts]
print("n sampled:", len(cs))
print("min/median/mean/max cells:", min(cs), statistics.median(cs), int(statistics.mean(cs)), max(cs))
print("biggest 5:", cellcounts[-5:])
print("sum chunks(reqs) for sample:", reqs_total)
print("=> est chunks per table mean:", reqs_total/len(cs))
print("=> EXTRAPOLATED total data-POSTs for 3049 tables:", int(reqs_total/len(cs)*3049))
# buckets
b=collections.Counter()
for c in cs:
    if c<=1000: b["<=1k (1 req)"]+=1
    elif c<=10000: b["1k-10k"]+=1
    elif c<=100000: b["10k-100k"]+=1
    elif c<=1000000: b["100k-1M"]+=1
    else: b[">1M"]+=1
print("buckets:", dict(b))
