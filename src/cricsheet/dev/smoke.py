import io, zipfile, csv, collections, duckdb, pyarrow as pa
from subsets_utils import get
import sys; sys.path.insert(0, "src")
from nodes.cricsheet import BALL_COLUMNS, _INFO_SINGLE

content = get("https://cricsheet.org/downloads/mlc_csv2.zip", timeout=(10,120)).content
z = zipfile.ZipFile(io.BytesIO(content))

# deliveries
ball = [n for n in z.namelist() if n.endswith(".csv") and not n.endswith("_info.csv")]
rows=[]
for n in ball:
    rdr=csv.reader(io.TextIOWrapper(z.open(n),encoding="utf-8"))
    h=next(rdr); assert h==BALL_COLUMNS
    for r in rdr:
        if not r: continue
        r=(r+[""]*27)[:27]
        rows.append(r)
cols=list(zip(*rows))
deliv=pa.table({c:pa.array(v,type=pa.string()) for c,v in zip(BALL_COLUMNS,cols)})
print("deliveries raw rows:", deliv.num_rows)

# matches
info=[n for n in z.namelist() if n.endswith("_info.csv")]
mrows=[]
for n in info:
    vals=collections.defaultdict(list)
    for r in csv.reader(io.TextIOWrapper(z.open(n),encoding="utf-8")):
        if len(r)>=3 and r[0]=="info": vals[r[1]].append(r[2:])
    def first(k):
        v=vals.get(k); return v[0][0] if v and v[0] else None
    teams=[t[0] for t in vals.get("team",[]) if t]
    dates=sorted(d[0] for d in vals.get("date",[]) if d)
    row={k:first(k) for k in _INFO_SINGLE}
    row["match_id"]=first("match_id"); row["start_date"]=dates[0] if dates else None
    row["end_date"]=dates[-1] if dates else None
    row["team1"]=teams[0] if teams else None; row["team2"]=teams[1] if len(teams)>1 else None
    mrows.append(row)
matches=pa.Table.from_pylist(mrows)
print("matches raw rows:", matches.num_rows)

con=duckdb.connect()
con.register("cricsheet-deliveries", deliv)
con.register("cricsheet-matches", matches)

# load the actual SQL from the module specs
from nodes.cricsheet import TRANSFORM_SPECS
for spec in TRANSFORM_SPECS:
    if spec.id=="cricsheet-people-transform": continue
    out=con.execute(spec.sql).fetch_arrow_table()
    print("\n==",spec.id,"-> rows", out.num_rows)
    print(out.schema)
    print(out.slice(0,2).to_pylist()[:1])
