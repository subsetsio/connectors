import tempfile, duckdb
from deltalake import write_deltalake
import nodes.stack_overflow_annual_developer_survey as m

# Monkeypatch save_raw_parquet to capture the table instead of writing prod raw
captured={}
import subsets_utils
def fake_save(table, asset): captured[asset]=table; return "ok"
m.save_raw_parquet=fake_save

# results for messy 2011 + codebook
m.fetch_results("stack-overflow-annual-developer-survey-results-2011")
# shrink codebook test to 2 years for speed
m.RESULTS_YEARS=["2015","2016","2025"]
m.fetch_codebook("stack-overflow-annual-developer-survey-schema-codebook")

for asset,t in captured.items():
    # apply the transform SQL via duckdb view, then delta write
    view=asset
    duckdb.sql(f'CREATE OR REPLACE VIEW "{view}" AS SELECT * FROM t') if False else None
    con=duckdb.connect()
    con.register(view, t)
    if "schema-codebook" in asset:
        sql=m._CODEBOOK_SQL
    else:
        sql=m._results_sql(asset)
    res=con.sql(sql).fetch_arrow_table()
    d=tempfile.mkdtemp(); write_deltalake(d,res,mode="overwrite")
    print(asset,"-> rows",res.num_rows,"cols",res.num_columns)
    if "schema-codebook" in asset:
        print("  codebook cols:",res.column_names,"years:",sorted(set(res.column('survey_year').to_pylist())))
