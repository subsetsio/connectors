"""Local dry-run: build each transform's dep view from ONE cycle of real data
and execute the transform SQL. Catches column/cast errors before the cloud run.
Does NOT call save_raw_* (no production writes)."""
import io, os, csv, zipfile, tempfile
import duckdb, pyarrow as pa
from nodes import fec

CY = "2026"

def temp(b):
    fd,p=tempfile.mkstemp(suffix=".txt")
    os.write(fd,b); os.close(fd); return p

def view_from_pipe(name, prefix, cols, extra_sql_select=None):
    b = fec._zip_member_bytes(CY, prefix)
    p = temp(b)
    clause = fec._csv_clause(p, cols)
    duckdb.sql(f'CREATE OR REPLACE TEMP VIEW "{name}" AS SELECT \'{CY}\' AS cycle, * FROM {clause}')
    return p

def run_transform(spec, label):
    rel = duckdb.sql(spec.sql)
    t = rel.to_arrow_table()
    print(f"  [{label}] {t.num_rows:,} rows, cols={t.column_names[:6]}...")
    assert t.num_rows > 0, f"{label}: 0 rows"

specs = {s.id: s for s in fec.TRANSFORM_SPECS}

# candidates: join weball+cn into the view
wb = fec._zip_member_bytes(CY,"weball"); cn = fec._zip_member_bytes(CY,"cn")
wbp=temp(wb); cnp=temp(cn)
cn_sub=f"(SELECT CAND_ID, ANY_VALUE(CAND_OFFICE) AS CAND_OFFICE, ANY_VALUE(CAND_PCC) AS CAND_PCC FROM {fec._csv_clause(cnp,fec.CN_COLS)} GROUP BY CAND_ID)"
duckdb.sql(f'CREATE OR REPLACE TEMP VIEW "fec-candidates" AS SELECT \'{CY}\' AS cycle, w.*, c.CAND_OFFICE AS CN_OFFICE, c.CAND_PCC AS CN_PCC FROM {fec._csv_clause(wbp,fec.WEBALL_COLS)} w LEFT JOIN {cn_sub} c ON w.CAND_ID=c.CAND_ID')
run_transform(specs["fec-candidates-transform"], "candidates")

# committees: webk+cm
wk=fec._zip_member_bytes(CY,"webk"); cm=fec._zip_member_bytes(CY,"cm")
wkp=temp(wk); cmp=temp(cm)
cm_sub=f"(SELECT CMTE_ID, ANY_VALUE(CMTE_PTY_AFFILIATION) AS CMTE_PTY_AFFILIATION, ANY_VALUE(CMTE_ST) AS CMTE_ST, ANY_VALUE(ORG_TP) AS ORG_TP, ANY_VALUE(CONNECTED_ORG_NM) AS CONNECTED_ORG_NM, ANY_VALUE(CAND_ID) AS CAND_ID FROM {fec._csv_clause(cmp,fec.CM_COLS)} GROUP BY CMTE_ID)"
duckdb.sql(f'CREATE OR REPLACE TEMP VIEW "fec-committees" AS SELECT \'{CY}\' AS cycle, k.*, m.CMTE_PTY_AFFILIATION AS CM_PTY, m.CMTE_ST AS CM_ST, m.ORG_TP AS CM_ORG_TP, m.CONNECTED_ORG_NM AS CM_CONNECTED_ORG, m.CAND_ID AS CM_CAND_ID FROM {fec._csv_clause(wkp,fec.WEBK_COLS)} k LEFT JOIN {cm_sub} m ON k.CMTE_ID=m.CMTE_ID')
run_transform(specs["fec-committees-transform"], "committees")

# linkages, house-senate (single pipe files)
view_from_pipe("fec-candidate-committee-linkages","ccl",fec.CCL_COLS)
run_transform(specs["fec-candidate-committee-linkages-transform"], "linkages")
view_from_pipe("fec-house-senate-current-campaigns","webl",fec.WEBL_COLS)
run_transform(specs["fec-house-senate-current-campaigns-transform"], "house-senate")

# IE (header CSV)
ie = fec._ie_get(f"{fec.BULK}/{CY}/independent_expenditure_{CY}.csv")
iep=temp(ie)
duckdb.sql(f'CREATE OR REPLACE TEMP VIEW "fec-independent-expenditures" AS SELECT \'{CY}\' AS cycle, * FROM read_csv(\'{iep}\', header=true, all_varchar=true, ignore_errors=true)')
run_transform(specs["fec-independent-expenditures-transform"], "independent-expenditures")

# streamed txn files: parse a sample of the member into a view
def sample_view(name, prefix, cols, limit=20000):
    url=f"{fec.BULK}/{CY}/{prefix}{CY[2:]}.zip"
    zp=fec._stream_zip_to_tempfile(url)
    zf=zipfile.ZipFile(zp); m=[n for n in zf.namelist() if not n.startswith('__MACOSX')][0]
    rows=[]
    with zf.open(m) as raw:
        rdr=csv.reader(io.TextIOWrapper(raw,encoding='latin-1',newline=''),delimiter='|',quoting=csv.QUOTE_NONE)
        for f in rdr:
            if len(f)<len(cols): continue
            rows.append(f[:len(cols)])
            if len(rows)>=limit: break
    os.unlink(zp)
    colsT=list(zip(*rows))
    arrays=[pa.array([CY]*len(rows),pa.string())]+[pa.array([v if v!='' else None for v in colsT[i]],pa.string()) for i in range(len(cols))]
    t=pa.table(arrays,names=["cycle"]+cols)
    duckdb.sql(f'CREATE OR REPLACE TEMP TABLE "{name}" AS SELECT * FROM t')

for name,prefix,cols in [
    ("fec-pac-contributions","pas2",fec.PAS2_COLS),
    ("fec-operating-expenditures","oppexp",fec.OPPEXP_COLS),
    ("fec-inter-committee-transactions","oth",fec.OTH_COLS),
    ("fec-individual-contributions","indiv",fec.INDIV_COLS),
]:
    sample_view(name,prefix,cols)
    run_transform(specs[name+"-transform"], name)

print("ALL TRANSFORMS OK")
