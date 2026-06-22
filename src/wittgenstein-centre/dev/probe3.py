import sys, duckdb
sys.path.insert(0, "src")
from nodes import wittgenstein_centre as W

REC = W._RECORD
def url(f): return f"{REC}/files/{f.replace(' ','%20')}/content"

con = duckdb.connect()
con.execute("INSTALL httpfs; LOAD httpfs;")

# register dep views under the exact download-id names the SQL references
con.execute(f"""CREATE VIEW "wittgenstein-centre-recode-dictionary" AS
  SELECT * FROM read_csv_auto('{url("Recode dictionary.csv")}')""")
con.execute(f"""CREATE VIEW "wittgenstein-centre-mean-years-schooling" AS
  SELECT * FROM read_csv_auto('{url("MYS_AG_SSPs_V14.csv")}')""")
con.execute(f"""CREATE VIEW "wittgenstein-centre-asfr" AS
  SELECT * FROM read_csv_auto('{url("ASFR_AE_SSPs_V14.csv")}')""")
con.execute(f"""CREATE VIEW "wittgenstein-centre-sex-ratio-at-birth" AS
  SELECT * FROM read_csv_auto('{url("SRB_SSPs_V14.csv")}')""")

def run(name, sql):
    print(f"\n=== {name} ===")
    df = con.execute(sql).fetch_df()
    print("rows:", len(df))
    print(df.head(4).to_string())
    print("cols:", list(df.columns))

run("recode", W._RECODE_SQL)
run("mys", W._indicator_sql("wittgenstein-centre-mean-years-schooling", "mean_years_schooling", has_edu=False))
run("asfr", W._indicator_sql("wittgenstein-centre-asfr", "asfr_births_per_1000_women", has_edu=True))
run("srb", W._SRB_SQL)
