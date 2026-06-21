import sys; sys.path.insert(0,"src")
from nodes.ons import _plan_columns, _to_float, _resolve_csv_url, get_client
import csv, pyarrow as pa

for did in ["TS001","retail-sales-index","ST001","mid-year-pop-est"]:
    url=_resolve_csv_url(did)
    client=get_client()
    with client.stream("GET", url, timeout=(10,120)) as r:
        r.raise_for_status()
        reader=csv.reader(r.iter_lines())
        header=next(reader)
        out,vi=_plan_columns(header)
        # read first 3 data rows
        sample=[next(reader) for _ in range(3)]
    print(f"\n{did}: value_idx={vi}")
    print("  header:", header[:6], "..." if len(header)>6 else "")
    print("  out_names:", out)
    print("  row0 value:", _to_float(sample[0][vi]), "| dims:", [sample[0][i] for i in range(len(out)) if i!=vi][:4])
