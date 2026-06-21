import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src', 'nodes'))
# import internals from the production module
import importlib.util
spec = importlib.util.spec_from_file_location("ahrq_node", os.path.join(os.path.dirname(__file__),'..','src','nodes','ahrq.py'))
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
puf = "HC-254H"  # small 2024 Home Health event file
url = m._resolve_xlsx_url(puf)
print("resolved:", url)
blob = m._download_zip(url)
print("zip bytes:", len(blob))
import io, zipfile, tempfile, os as _os
with zipfile.ZipFile(io.BytesIO(blob)) as zf:
    name=[n for n in zf.namelist() if n.lower().endswith('.xlsx')][0]
    xb=zf.read(name)
tmp=tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False); tmp.write(xb); tmp.flush(); tmp.close()
con=m._duckdb_excel()
t=con.execute(f"SELECT * FROM read_xlsx('{tmp.name}', all_varchar=true)").fetch_arrow_table()
_os.unlink(tmp.name)
print("rows", t.num_rows, "cols", t.num_columns)
print("sample cols", t.column_names[:8])
