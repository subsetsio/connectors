import sys, os, json, time
sys.path.insert(0, "src"); sys.path.insert(0, "src/nodes")
os.environ.setdefault("CI","")
import beijing_municipal_bureau_of_statistics as M

def first_rows(spec_id):
    """Return row count, short-circuiting at the first non-empty mask."""
    ent = M._BY_SPEC[spec_id]
    report, subject, sort = ent["report"], ent["subject"], ent["sort"]
    viewer = M._parse_viewer(M._get_viewer(report, subject, sort))
    if viewer is None:
        return 0
    rv, ft, ut = viewer["reportVersion"], viewer["freqType"], viewer["usageType"]
    masks, mask_dept = M._freq_masks(report, sort, ut)
    dept = viewer["dept"] or mask_dept
    if not masks:
        return 0
    dk = lambda mask: M._data_key(report, dept, mask, ft, subject, rv, ut)
    tpl = M._post("updateReportHtml", dk(masks[0])).text
    labels, datacells, min_row, min_col = M._parse_template(tpl)
    if not datacells:
        return 0
    tpl_ids = {cid for _,_,cid in datacells}
    total = 0
    for mask in masks:
        blocks = M._post("queryReportData", dk(mask)).json()
        for block in blocks or []:
            for dr in block.get("data", []):
                vmap = dict(zip(dr.get("metaData", []), dr.get("value", [])))
                for cid in tpl_ids:
                    v = vmap.get(cid)
                    if v is not None and str(v).strip() != "":
                        total += 1
        if total > 0:
            return total  # short-circuit: non-empty
    return total

ids = list(M._BY_SPEC.keys())
N = int(os.environ.get("SCAN_N", "10")); START = int(os.environ.get("SCAN_START", "0"))
ids = ids[START:START+N]
out_path = os.environ["SCAN_OUT"]
results = json.load(open(out_path)) if os.path.exists(out_path) else {}
t0=time.time()
for i, sid in enumerate(ids):
    if sid in results: continue
    try:
        results[sid] = first_rows(sid)
    except Exception as e:
        results[sid] = f"ERR:{type(e).__name__}:{str(e)[:80]}"
    if (i+1) % 5 == 0:
        json.dump(results, open(out_path,"w"), ensure_ascii=False)
        print(f"  {i+1}/{len(ids)} {time.time()-t0:.0f}s", flush=True)
json.dump(results, open(out_path,"w"), ensure_ascii=False)
print(f"DONE {len(ids)} in {time.time()-t0:.0f}s")
