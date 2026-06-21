from subsets_utils import get
def cnt(table, col):
    q=f"select count(*) as total, count({col}) as nonnull from {table}"
    r=get("https://exoplanetarchive.ipac.caltech.edu/TAP/sync",
          params={"query":q,"format":"json"}, timeout=(15,120))
    print(table, col, "->", r.json()[0])
cnt("ps","sy_kepmagerr1")
cnt("ps","sy_kepmag")     # sanity: the value column should be populated
cnt("toi","sectors")
cnt("toi","pl_insolerr1")
cnt("toi","toi")          # sanity: primary id populated
