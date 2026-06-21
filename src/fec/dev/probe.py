import io, zipfile, tempfile, os, duckdb
from subsets_utils import get

WEBALL_COLS = ["CAND_ID","CAND_NAME","CAND_ICI","PTY_CD","CAND_PTY_AFFILIATION","TTL_RECEIPTS","TRANS_FROM_AUTH","TTL_DISB","TRANS_TO_AUTH","COH_BOP","COH_COP","CAND_CONTRIB","CAND_LOANS","OTHER_LOANS","CAND_LOAN_REPAY","OTHER_LOAN_REPAY","DEBTS_OWED_BY","TTL_INDIV_CONTRIB","CAND_OFFICE_ST","CAND_OFFICE_DISTRICT","SPEC_ELECTION","PRIM_ELECTION","RUN_ELECTION","GEN_ELECTION","GEN_ELECTION_PRECENT","OTHER_POL_CMTE_CONTRIB","POL_PTY_CONTRIB","CVG_END_DT","INDIV_REFUNDS","CMTE_REFUNDS"]

def dl(cycle, prefix):
    s = cycle[2:]
    url = f"https://www.fec.gov/files/bulk-downloads/{cycle}/{prefix}{s}.zip"
    r = get(url, timeout=(10,120))
    r.raise_for_status()
    zf = zipfile.ZipFile(io.BytesIO(r.content))
    name = [n for n in zf.namelist() if not n.startswith("__MACOSX")][0]
    return zf.read(name)

raw = dl("2024","weball")
print("weball24 bytes", len(raw))
tmp = tempfile.NamedTemporaryFile(suffix=".txt", delete=False); tmp.write(raw); tmp.close()
names = "[" + ",".join(f"'{c}'" for c in WEBALL_COLS) + "]"
rel = duckdb.sql(f"SELECT * FROM read_csv('{tmp.path if hasattr(tmp,'path') else tmp.name}', delim='|', header=false, names={names}, all_varchar=true, ignore_errors=true)")
t = rel.fetch_arrow_table()
print("rows", t.num_rows, "cols", t.num_columns)
print(t.slice(0,2).to_pylist()[0])
os.unlink(tmp.name)
