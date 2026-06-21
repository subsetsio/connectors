import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src", "nodes"))
import pyarrow as pa
import philippine_statistics_authority as M

BASE = M.BASE
def run(path, label):
    url = BASE + path
    meta = M._get_json(url)
    variables = M._variables(meta)
    used=set(); c2c={code:M._colname(code,used) for code,_,_ in variables}
    schema = pa.schema([(c2c[code],pa.string()) for code,_,_ in variables]+[("value",pa.float64())])
    chunks = list(M._chunks(variables))
    fullcells=1
    for _,codes,_ in variables: fullcells*=len(codes)
    total_rows=0; maxchunk=0
    for sel in chunks:
        q={"query":[{"code":variables[i][0],"selection":{"filter":"item","values":sel[i]}} for i in range(len(variables)) if len(sel[i])>0],"response":{"format":"json-stat2"}}
        js=M._post_json(url,q)
        rows=M._decode(js,c2c)
        t=pa.Table.from_pylist(rows,schema=schema)  # validates schema conformance
        total_rows+=len(t); maxchunk=max(maxchunk,len(t))
    print(f"\n[{label}] {path}")
    print(" dims:", [(code,len(codes)) for code,codes,_ in variables])
    print(" full_cells:", fullcells, " n_chunks:", len(chunks), " max_chunk_rows:", maxchunk)
    print(" total_rows_built:", total_rows, " (== full_cells:", total_rows==fullcells, ")")
    print(" columns:", schema.names)
    # show a couple sample rows from last chunk
    print(" sample:", t.slice(0,2).to_pylist())

run("2I/0082I5DFCF2.px", "tiny-72")
run("2M/PI/CPI/2012/0012M4ACPI1.px", "huge-1.9M")
