import sys
sys.path.insert(0,"src"); sys.path.insert(0,"src/nodes")
import beijing_municipal_bureau_of_statistics as M

sid="beijing-municipal-bureau-of-statistics-01-ls-2-01"
ent=M._BY_SPEC[sid]; report,subject,sort=ent["report"],ent["subject"],ent["sort"]
v=M._parse_viewer(M._get_viewer(report,subject,sort))
print("viewer",v)
# try freqmask with different usageType
for ut in ("01","02","03","04"):
    m,d=M._freq_masks(report,sort,ut)
    print(f"freqmask ut={ut}: masks={m[:8]} dept={d}")

# brute data: vary mask year, usageType, collectDataVersion
def datakey(mask,ut,ver,cdv):
    return {
      "reportDataKeyDTO.reportNumber":report,
      "reportDataKeyDTO.departmentCode":"null",
      "reportDataKeyDTO.collectFrequenceMask":mask,
      "reportDataKeyDTO.collectDataVersion":cdv,
      "reportDataKeyDTO.collectFrequenceTypeCode":v["freqType"] or "",
      "reportDataKeyDTO.usageType":ut,
      "reportDataKeyDTO.objectType":"04",
      "reportDataKeyDTO.objectCode":subject,
      "reportDataKeyDTO.reportVersion":ver,
    }
import itertools
hits=[]
for mask in ["2013","2012","2011","2010","2005","2015","2020","2023","2008","2009","2014"]:
    for ut in ["02","01"]:
        for ver in [v["reportVersion"] or "", "201101",""]:
            r=M._post("queryReportData",datakey(mask,ut,ver,"1"))
            if len(r.text)>3:
                hits.append((mask,ut,ver,len(r.text)))
                print("HIT mask=%s ut=%s ver=%s len=%d"%(mask,ut,ver,len(r.text)))
if not hits: print("NO HITS for ls-2-01 across brute grid")
