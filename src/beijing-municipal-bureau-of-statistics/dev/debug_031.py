import sys; sys.path.insert(0,"src")
import nodes.beijing_municipal_bureau_of_statistics as M
report,subject,sort="LS-031-001","3700","01"
vh=M._get_viewer(report,subject,sort)
info=M._parse_viewer(vh); print("viewer info", info, "viewer len", len(vh))
if info:
    masks,dept=M._freq_masks(report,sort,info['usageType']); print("masks",masks,"dept",dept)
    if masks:
        dk=M._data_key(report, info['dept'] or dept, masks[0], info['freqType'], subject, info['reportVersion'], info['usageType'])
        tpl=M._post("updateReportHtml",dk).text
        labels,dc,mr,mc=M._parse_template(tpl); print("labels",len(labels),"datacells",len(dc))
        rd=M._post("queryReportData",dk).json()
        print("blocks",len(rd))
        if rd and rd[0].get('data'):
            r0=rd[0]['data'][0]; print("nonnull values", len([v for v in r0.get('value',[]) if v not in (None,'')]))
