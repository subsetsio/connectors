import subsets_utils as su, json
H="https://hgk.tjj.beijing.gov.cn"
NS=H+"/query/queryres/queryreport/QueryReportAction!"
report="60Y-1-03-N"; subject="0100"; sortType="01"; freqType="C_YY"; dept="071"
v=H+f"/query/queryReport/queryReportAction?method=queryHtmlStyle&queryCondition.reportNumber={report}&queryCondition.objectType=04&queryCondition.objectCode={subject}&yhid=guest&netType=2"
su.get(v, timeout=(10,60))
def key(mask):
    return {"reportDataKeyDTO.reportNumber":report,"reportDataKeyDTO.departmentCode":dept,
     "reportDataKeyDTO.collectFrequenceMask":mask,"reportDataKeyDTO.collectFrequenceTypeCode":freqType,
     "reportDataKeyDTO.usageType":"01","reportDataKeyDTO.objectType":"04",
     "reportDataKeyDTO.objectCode":subject,"reportDataKeyDTO.reportVersion":"","reportDataKeyDTO.queryType":""}
for mask in ["201301","2013"]:
    rd=su.post(NS+"queryReportData", data=key(mask), timeout=(10,120))
    print(f"mask={mask}", rd.status_code, "len", len(rd.text), "head", rd.text[:90])
