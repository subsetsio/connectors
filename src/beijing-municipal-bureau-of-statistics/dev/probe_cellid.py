import sys
sys.path.insert(0, "src"); sys.path.insert(0, "src/nodes")
import beijing_municipal_bureau_of_statistics as M

def probe(spec_id):
    ent = M._BY_SPEC[spec_id]
    report, subject, sort = ent["report"], ent["subject"], ent["sort"]
    viewer = M._parse_viewer(M._get_viewer(report, subject, sort))
    masks, mask_dept = M._freq_masks(report, sort, viewer["usageType"])
    dept = viewer["dept"] or mask_dept
    dk = lambda mask: M._data_key(report, dept, mask, viewer["freqType"], subject, viewer["reportVersion"], viewer["usageType"])
    tpl = M._post("updateReportHtml", dk(masks[0])).text
    labels, datacells, mr, mc = M._parse_template(tpl)
    tpl_ids = [cid for _,_,cid in datacells]
    blocks = M._post("queryReportData", dk(masks[0])).json()
    data_ids = []
    for b in blocks or []:
        for dr in b.get("data",[]):
            data_ids += dr.get("metaData",[])
    print(f"\n=== {spec_id}")
    print("  template cell_ids sample:", tpl_ids[:6])
    print("  data metaData sample:    ", data_ids[:6])
    print("  overlap:", len(set(tpl_ids) & set(data_ids)), "of", len(set(tpl_ids)), "tpl /", len(set(data_ids)), "data")

for sid in ["beijing-municipal-bureau-of-statistics-01-ls-1-07",
            "beijing-municipal-bureau-of-statistics-01-ls-1-08"]:
    probe(sid)
