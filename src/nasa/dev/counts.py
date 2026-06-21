from subsets_utils import get
tables=["CUMULATIVE","K2TARGETS","KEPLERSTELLAR","Q1_Q17_DR25_KOI","Q1_Q17_DR25_KS",
"Q1_Q17_DR25_SUP_KOI","Q1_Q17_DR25_SUP_KS","Q1_Q17_DR25_TCE","TD","k2pandc","ml","ps","pscomppars","stellarhosts","toi"]
for t in tables:
    r=get("https://exoplanetarchive.ipac.caltech.edu/TAP/sync",
          params={"query":f"select count(*) as n from {t}","format":"json"}, timeout=(15,180))
    try:
        n=r.json()[0]["n"]
    except Exception as e:
        n="ERR "+r.text[:80]
    print(f"{t:24s} {n}")
