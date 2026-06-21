import io, csv
from subsets_utils import get

BASE = "https://edge.boi.org.il/FusionEdgeServer/sdmx/v2/data/dataflow/BOI.STATISTICS"
ENTITY_IDS = ["ACC","ATM","BBS_99","BFR_99","BIR","BIR_MRTG_99","BKN","BMB_99","BOP","BR",
"BTS_7","CAP","CARDS","CCIR","CCP","CHEQUES","CONS","DEBT_AGG","DEM","DRV","ECON_IND","ENR",
"EXR","EXS","FTR","INSINV","INSINV2","LBM","MAG","MASAV","MF","MNF","NA","PRI","PS",
"REAL_ES_DF","REV","SECDWH","TLB","ZAHAV","ZCM"]

for flow in ENTITY_IDS:
    url = f"{BASE}/{flow}/1.0?format=csv"
    try:
        r = get(url, timeout=(10.0, 300.0))
    except Exception as e:
        print(f"{flow:14s} ERROR {type(e).__name__}: {e}")
        continue
    if r.status_code != 200:
        print(f"{flow:14s} status={r.status_code}  body={r.text[:120]!r}")
        continue
    rdr = csv.reader(io.StringIO(r.text))
    header = next(rdr, None)
    n = sum(1 for _ in rdr)
    ncols = len(header) if header else 0
    print(f"{flow:14s} status=200 bytes={len(r.content):>10} rows={n:>8} cols={ncols} hdr={header}")
