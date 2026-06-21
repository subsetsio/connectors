import sys
sys.path.insert(0,"src/nodes")
import guangdong_bureau_of_statistics as m
import pyarrow as pa

# exercise the real fetch+parse on a few representative tables WITHOUT save_raw
for nid in ["guangdong-bureau-of-statistics-02-01",
            "guangdong-bureau-of-statistics-02-15",   # split table
            "guangdong-bureau-of-statistics-24-a-01",  # appendix complex
            "guangdong-bureau-of-statistics-09-01"]:   # complex header
    tid,parts=m._BY_NODE[nid]
    rows=[]
    for p in parts:
        c=m._fetch_xls(f"{m.BASE}/{p[:2]}/excel/{p}.xls")
        rows+=m._parse_sheet(c,tid,p)
    t=pa.Table.from_pylist(rows,schema=m.SCHEMA)
    nn_num=sum(1 for v in t.column("value_num").to_pylist() if v is not None)
    print(f"{nid:42} parts={len(parts)} rows={len(t)} numcells={nn_num} cols_distinct={len(set(t.column('column_header').to_pylist()))}")
    # show a couple sample rows
    for i in (0, len(rows)//2):
        r={k:rows[i][k] for k in ('row_label_cn','row_label_en','column_header','value_num','value_str')}
        print("    ",r)
print("specs:",len(m.DOWNLOAD_SPECS),"transforms:",len(m.TRANSFORM_SPECS))
