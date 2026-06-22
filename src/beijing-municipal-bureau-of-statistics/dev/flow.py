import subsets_utils as su, json
H="https://hgk.tjj.beijing.gov.cn"
NS=H+"/query/queryres/queryreport/QueryReportAction!"
report="60Y-1-03-N"; subject="0100"; sortType="01"; freqType="C_YY"

# 1. seed session
v=H+f"/query/queryReport/queryReportAction?method=queryHtmlStyle&queryCondition.reportNumber={report}&queryCondition.objectType=04&queryCondition.objectCode={subject}&yhid=guest&netType=2"
r=su.get(v, timeout=(10,60)); print("viewer", r.status_code, "cookies", dict(su.get_client().cookies))

# 2. freq mask
d={"reportDataKeyDTO.reportNumber":report,"reportDataKeyDTO.reportVersion":"",
   "reportDataKeyDTO.queryType":"","reportDataKeyDTO.usageType":"01",
   "reportDataKeyDTO.dataSortTypeCode":sortType}
r=su.post(NS+"queryRptTimeFreqMask", data=d, timeout=(10,60))
print("freqMask", r.status_code, r.text[:200])
mask_info=json.loads(r.text)
dept=mask_info[0]["departmentCode"]; years=mask_info[0]["list"]
print("dept",dept,"years",years)

# 3. queryReportData for first year
yr=years[0]
for maskval in [yr, yr+"01"]:
    d2={"reportDataKeyDTO.reportNumber":report,"reportDataKeyDTO.departmentCode":dept,
        "reportDataKeyDTO.collectFrequenceMask":maskval,"reportDataKeyDTO.collectFrequenceTypeCode":freqType,
        "reportDataKeyDTO.usageType":"01","reportDataKeyDTO.objectType":"04",
        "reportDataKeyDTO.objectCode":subject,"reportDataKeyDTO.reportVersion":"",
        "reportDataKeyDTO.queryType":""}
    r=su.post(NS+"queryReportData", data=d2, timeout=(10,60))
    print(f"reportData mask={maskval}", r.status_code, "len", len(r.text), "head", r.text[:120])
