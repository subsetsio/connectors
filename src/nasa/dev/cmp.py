from subsets_utils import get
def q(sql):
    r=get("https://exoplanetarchive.ipac.caltech.edu/TAP/sync",params={"query":sql,"format":"json"},timeout=(15,120))
    return r.json()
print("cumulative disposition dist:", q("select koi_disposition, count(*) n from cumulative group by koi_disposition order by n desc"))
print("sup_koi disposition dist:", q("select koi_disposition, count(*) n from Q1_Q17_DR25_SUP_KOI group by koi_disposition order by n desc"))
# do they cover same kepoi_name set and same dispositions? join on kepoi_name
print("rows where disposition differs between the two:",
   q("select count(*) n from cumulative c join Q1_Q17_DR25_SUP_KOI s using(kepoi_name) where c.koi_disposition is distinct from s.koi_disposition"))
print("overlap count:", q("select count(*) n from cumulative c join Q1_Q17_DR25_SUP_KOI s using(kepoi_name)"))
print("a populated science col in sup_koi (koi_period) nonnull:", q("select count(koi_period) nn, count(*) tot from Q1_Q17_DR25_SUP_KOI"))
