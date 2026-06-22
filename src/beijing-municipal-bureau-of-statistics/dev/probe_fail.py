import sys, json
sys.path.insert(0, "src")
sys.path.insert(0, "src/nodes")
import beijing_municipal_bureau_of_statistics as M

def probe(spec_id):
    ent = M._BY_SPEC[spec_id]
    report, subject, sort = ent["report"], ent["subject"], ent["sort"]
    viewer_html = M._get_viewer(report, subject, sort)
    viewer = M._parse_viewer(viewer_html)
    print(f"\n=== {spec_id}  report={report} subject={subject} sort={sort}")
    print("viewer_html len:", len(viewer_html), "| showSinglereport present:", 'showSinglereport' in viewer_html)
    if viewer is None:
        print("  viewer parse -> None (no report tag)")
        return
    print("  viewer:", viewer)
    masks, mask_dept = M._freq_masks(report, sort, viewer["usageType"])
    dept = viewer["dept"] or mask_dept
    print("  masks:", masks[:5], "... n=", len(masks), "| dept:", dept)
    if masks:
        tpl = M._post("updateReportHtml", M._data_key(report, dept, masks[0], viewer["freqType"], subject, viewer["reportVersion"], viewer["usageType"])).text
        labels, datacells, min_row, min_col = M._parse_template(tpl)
        print("  tpl len:", len(tpl), "| datacells:", len(datacells), "| labels:", len(labels))
        # try data for first mask
        blocks = M._post("queryReportData", M._data_key(report, dept, masks[0], viewer["freqType"], subject, viewer["reportVersion"], viewer["usageType"])).json()
        nrows = sum(len(b.get("data",[])) for b in (blocks or []))
        print("  data blocks:", len(blocks or []), "| data rows:", nrows)
        if blocks and blocks[0].get("data"):
            dr = blocks[0]["data"][0]
            print("  sample metaData:", dr.get("metaData",[])[:5], "| value:", dr.get("value",[])[:5])

for sid in ["beijing-municipal-bureau-of-statistics-01-ls-031-001",
            "beijing-municipal-bureau-of-statistics-01-ls-1-07",
            "beijing-municipal-bureau-of-statistics-01-ls-1-08"]:
    try:
        probe(sid)
    except Exception as e:
        print(f"  ERROR {sid}: {type(e).__name__}: {e}")
