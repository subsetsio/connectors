import sys; sys.path.insert(0,"src")
import subsets_utils as su, json
import nodes.beijing_municipal_bureau_of_statistics as M
# entity 01-LS-1-07: report LS-1-07, subject 3700, sort 01
report,subject,sort="LS-1-07","3700","01"
vh=M._get_viewer(report,subject,sort)
info=M._parse_viewer(vh); print("viewer info", info)
masks,dept=M._freq_masks(report,sort); print("masks",masks,"dept",dept)
if masks:
    tpl=M._post("updateReportHtml",M._data_key(report,info['dept'] or dept,masks[0],info['freqType'],subject,info['reportVersion'])).text
    labels,dc,mr,mc=M._parse_template(tpl); print("n labels",len(labels),"n datacells",len(dc))
    rd=M._post("queryReportData",M._data_key(report,info['dept'] or dept,masks[0],info['freqType'],subject,info['reportVersion'])).json()
    print("data blocks", len(rd))
    if rd:
        print("block0 DSID", rd[0].get('DSID'), "n data rows", len(rd[0].get('data',[])))
        if rd[0].get('data'):
            r0=rd[0]['data'][0]
            print("metaData len", len(r0.get('metaData',[])), "value len", len(r0.get('value',[])))
            print("sample values", r0.get('value',[])[:10])
