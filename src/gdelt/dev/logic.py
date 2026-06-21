import io, zipfile, duckdb, pyarrow as pa
from subsets_utils import get
from nodes.gdelt import _index_export_urls_by_date, _aggregate_day, _BATCH_SCHEMA, TRANSFORM_SPECS
ml = get("http://data.gdeltproject.org/gdeltv2/masterfilelist.txt", timeout=(10,300)).text
by_date = _index_export_urls_by_date(ml)
# pick a recent complete date with files; take 2nd-to-last date key
dates = sorted(by_date)
d = dates[-2]
print("testing file-date:", d, "files:", len(by_date[d]))
# limit to first 6 files for a fast smoke test of logic
agg = _aggregate_day(by_date[d][:6])
print("agg groups:", len(agg))
rows = {k:[] for k in ["date","action_geo_country_iso2","event_root_code","quad_class","num_events","sum_mentions","sum_articles","sum_goldstein","sum_tone"]}
for (dt,iso,root,quad),(n,m,a,g,t) in agg.items():
    rows["date"].append(dt); rows["action_geo_country_iso2"].append(iso); rows["event_root_code"].append(root)
    rows["quad_class"].append(quad); rows["num_events"].append(n); rows["sum_mentions"].append(m)
    rows["sum_articles"].append(a); rows["sum_goldstein"].append(g); rows["sum_tone"].append(t)
tbl = pa.table(rows, schema=_BATCH_SCHEMA)
con = duckdb.connect()
con.register("gdelt-events", tbl)
sql = TRANSFORM_SPECS[0].sql
out = con.execute(sql).fetch_arrow_table()
print("transform out rows:", out.num_rows)
print("cols:", out.column_names)
import pandas as pd
print(out.slice(0,5).to_pandas().to_string())
# sanity ranges
df = out.to_pandas()
print("avg_goldstein range:", df.avg_goldstein.min(), df.avg_goldstein.max())
print("avg_tone range:", df.avg_tone.min(), df.avg_tone.max())
print("event_root_label nulls:", df.event_root_label.isna().sum())
print("distinct dates:", sorted(df.date.unique())[:5])
