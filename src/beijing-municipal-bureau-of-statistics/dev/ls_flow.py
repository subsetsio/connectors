import subsets_utils as su, re, json, html
H="https://hgk.tjj.beijing.gov.cn"
NS=H+"/query/queryres/queryreport/QueryReportAction!"
report,subject,sort="LS-1-07","3700","01"
v=H+f"/query/queryReport/queryReportAction?method=queryHtmlStyle&queryCondition.reportNumber={report}&queryCondition.objectType=04&queryCondition.objectCode={subject}&yhid=guest&netType=2&queryCondition.dataSortTypeCode={sort}"
h=su.get(v,timeout=(10,60)).text
seg=re.search(r'id="showSinglereport"([^>]*)>',h).group(1)
def a(n): mm=re.search(n+r'\s*=\s*"?([^"\s>]*)"?',seg); return mm.group(1) if mm else None
rv,ut,ft,dept=a("reportVersion"),a("usageType"),a("collectFrequenceTypeCode"),a("sourceDepartmentCode")
print("rv",rv,"usageType",ut,"freqType",ft,"dept",repr(dept))
fm=su.post(NS+"queryRptTimeFreqMask",data={"reportDataKeyDTO.reportNumber":report,"reportDataKeyDTO.usageType":ut,"reportDataKeyDTO.dataSortTypeCode":sort},timeout=(10,60)).json()
print("freqMask blocks:", len(fm), "block0 sample keys:", list(fm[0].keys())[:6] if fm else None)
# extract masks both shapes
masks=[]
for blk in fm:
    if blk.get("list"): masks+=blk["list"]
    elif blk.get("collectFrequenceMask"): masks.append(blk["collectFrequenceMask"])
print("masks", masks)
deptv = dept or (fm[0].get("departmentCode") if fm else None)
def key(mask, cdv):
    return {"reportDataKeyDTO.reportNumber":report,"reportDataKeyDTO.departmentCode":deptv or "null",
     "reportDataKeyDTO.collectFrequenceMask":mask,"reportDataKeyDTO.collectDataVersion":cdv,
     "reportDataKeyDTO.collectFrequenceTypeCode":ft,"reportDataKeyDTO.usageType":ut,
     "reportDataKeyDTO.objectType":"04","reportDataKeyDTO.objectCode":subject,"reportDataKeyDTO.reportVersion":rv}
for cdv in ["1","null",""]:
    rd=su.post(NS+"queryReportData",data=key(masks[0],cdv),timeout=(10,120)).json()
    nrows = len(rd[0]['data']) if rd and rd[0].get('data') else 0
    nv = len([x for x in (rd[0]['data'][0].get('value',[]) if nrows else []) if x not in (None,'')])
    print(f"cdv={cdv!r}: blocks={len(rd)} datarows={nrows} nonnull_vals={nv}")
