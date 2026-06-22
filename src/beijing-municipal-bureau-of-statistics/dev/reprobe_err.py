import sys, json
sys.path.insert(0,"src"); sys.path.insert(0,"src/nodes")
import beijing_municipal_bureau_of_statistics as M
m=json.load(open("dev/scan_merged.json"))
errs=[k for k,v in m.items() if isinstance(v,str)]
print("re-probing", len(errs), "errored ids")
def rows(sid):
    ent=M._BY_SPEC[sid]; report,subject,sort=ent["report"],ent["subject"],ent["sort"]
    v=M._parse_viewer(M._get_viewer(report,subject,sort))
    if not v: return 0
    masks,md=M._freq_masks(report,sort,v["usageType"])
    dept=v["dept"] or md
    if not masks: return 0
    dk=lambda mask: M._data_key(report,dept,mask,v["freqType"],subject,v["reportVersion"],v["usageType"])
    tpl=M._post("updateReportHtml",dk(masks[0])).text
    labels,datacells,mr,mc=M._parse_template(tpl)
    if not datacells: return 0
    ids={c for _,_,c in datacells}
    tot=0
    for mask in masks:
        for b in (M._post("queryReportData",dk(mask)).json() or []):
            for dr in b.get("data",[]):
                vmap=dict(zip(dr.get("metaData",[]),dr.get("value",[])))
                tot+=sum(1 for c in ids if vmap.get(c) not in (None,"") and str(vmap.get(c)).strip()!="")
        if tot>0: return tot
    return tot
for sid in errs:
    try:
        r=rows(sid); print(f"  {sid.split('statistics-')[1]}: {r}")
        m[sid]=r
    except Exception as e:
        print(f"  {sid.split('statistics-')[1]}: ERR2 {type(e).__name__}: {str(e)[:80]}")
        m[sid]=f"ERR:{e}"[:100]
json.dump(m, open("dev/scan_merged.json","w"), ensure_ascii=False)
