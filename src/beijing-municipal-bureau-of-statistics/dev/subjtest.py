import sys
sys.path.insert(0,"src"); sys.path.insert(0,"src/nodes")
import beijing_municipal_bureau_of_statistics as M
report="LS-2-01"; sort="01"
# discover all subject codes from constants
import json
subs=sorted({e["subject"] for e in M.ENTITIES})
print("subjects to try:", subs)
for subject in subs:
    v=M._parse_viewer(M._get_viewer(report,subject,sort))
    if not v: 
        continue
    masks,md=M._freq_masks(report,sort,v["usageType"])
    if not masks: continue
    dk=lambda mask: M._data_key(report, v["dept"] or md, mask, v["freqType"], subject, v["reportVersion"], v["usageType"])
    r=M._post("queryReportData",dk(masks[0]))
    print(f"subj={subject} masks={masks[:3]} datalen={len(r.text)}")
